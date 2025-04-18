from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..db.session import get_db
from ..models.post import Post
from ..models.user import User
from ..schemas.post import (
    PostCreate,
    PostResponse,
    PostUpdate,
    PostStatus
)
from ..core.security import get_current_user
from ..services.s3 import upload_to_s3
from ..tasks import (
    schedule_post,
    generate_content,
    generate_image
)

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify channel ownership
    channel = db.query(TelegramChannel).filter(
        TelegramChannel.id == post.channel_id,
        TelegramChannel.owner_id == current_user.id
    ).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Create post in database
    db_post = Post(
        channel_id=post.channel_id,
        content=post.content,
        scheduled_time=post.scheduled_time,
        created_by=current_user.id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Schedule the post
    schedule_post.delay(str(db_post.id))
    
    return db_post

@router.post("/{post_id}/image")
async def upload_post_image(
    post_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.created_by == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Upload image to S3
    image_data = await file.read()
    image_url = upload_to_s3(image_data, f"posts/{post_id}/{file.filename}")
    
    if not image_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image"
        )
    
    # Update post with image URL
    post.image_url = image_url
    db.commit()
    
    return {"image_url": image_url}

@router.post("/{post_id}/generate-content")
async def generate_post_content(
    post_id: str,
    prompt: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.created_by == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Generate content
    content = generate_content.delay(prompt).get()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate content"
        )
    
    # Update post with generated content
    post.content = content
    db.commit()
    
    return {"content": content}

@router.post("/{post_id}/generate-image")
async def generate_post_image(
    post_id: str,
    prompt: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.created_by == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Generate image
    image_url = generate_image.delay(prompt or post.content).get()
    if not image_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate image"
        )
    
    # Update post with generated image
    post.image_url = image_url
    db.commit()
    
    return {"image_url": image_url}

@router.get("/", response_model=List[PostResponse])
async def list_posts(
    channel_id: str = None,
    status: PostStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Post).filter(Post.created_by == current_user.id)
    
    if channel_id:
        query = query.filter(Post.channel_id == channel_id)
    
    if status:
        query = query.filter(Post.status == status)
    
    return query.order_by(Post.scheduled_time).all()

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.created_by == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return post

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.created_by == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Update post fields
    for field, value in post_update.dict(exclude_unset=True).items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    
    # Reschedule if needed
    if post_update.scheduled_time:
        schedule_post.delay(str(post.id))
    
    return post

@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.created_by == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"} 