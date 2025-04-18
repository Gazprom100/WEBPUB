from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.session import get_db
from ..models.channel import TelegramChannel
from ..models.user import User
from ..schemas.channel import (
    ChannelCreate,
    ChannelResponse,
    ChannelUpdate,
    ChannelStats
)
from ..core.security import get_current_user
from ..services.telegram import telegram_service
from ..tasks import update_channel_metrics

router = APIRouter()

@router.post("/", response_model=ChannelResponse)
async def create_channel(
    channel: ChannelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has reached channel limit
    user_channels = db.query(TelegramChannel).filter(
        TelegramChannel.owner_id == current_user.id
    ).count()
    
    if user_channels >= 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum channel limit reached"
        )
    
    # Verify bot is admin in the channel
    is_admin = await telegram_service.check_bot_admin(channel.channel_id)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bot must be an administrator in the channel"
        )
    
    # Get channel info from Telegram
    channel_info = await telegram_service.get_channel_info(channel.channel_id)
    
    # Create channel in database
    db_channel = TelegramChannel(
        channel_id=channel.channel_id,
        channel_name=channel_info['title'],
        channel_username=channel_info['username'],
        channel_description=channel_info['description'],
        channel_avatar_url=channel_info['photo'],
        bot_token=channel.bot_token,
        owner_id=current_user.id
    )
    
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    
    # Start metrics collection
    update_channel_metrics.delay(str(db_channel.id))
    
    return db_channel

@router.get("/", response_model=List[ChannelResponse])
async def list_channels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    channels = db.query(TelegramChannel).filter(
        TelegramChannel.owner_id == current_user.id
    ).all()
    return channels

@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == channel_id,
        TelegramChannel.owner_id == current_user.id
    ).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    return channel

@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: str,
    channel_update: ChannelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == channel_id,
        TelegramChannel.owner_id == current_user.id
    ).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    for field, value in channel_update.dict(exclude_unset=True).items():
        setattr(channel, field, value)
    
    db.commit()
    db.refresh(channel)
    return channel

@router.delete("/{channel_id}")
async def delete_channel(
    channel_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == channel_id,
        TelegramChannel.owner_id == current_user.id
    ).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    db.delete(channel)
    db.commit()
    return {"message": "Channel deleted successfully"}

@router.get("/{channel_id}/stats", response_model=ChannelStats)
async def get_channel_stats(
    channel_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == channel_id,
        TelegramChannel.owner_id == current_user.id
    ).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    metrics = db.query(ChannelMetrics).filter(
        ChannelMetrics.channel_id == channel.id
    ).first()
    
    if not metrics:
        return ChannelStats(
            subscribers_count=0,
            views_count=0,
            average_engagement=0
        )
    
    return metrics 