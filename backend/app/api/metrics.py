from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from ..db.session import get_db
from ..models.channel import TelegramChannel
from ..models.post import Post
from ..models.metrics import PostMetrics, ChannelMetrics
from ..schemas.metrics import (
    ChannelMetricsResponse,
    PostMetricsResponse,
    MetricsTimeRange
)
from ..core.security import get_current_user
from ..models.user import User
from ..models.channel import Channel

router = APIRouter()

@router.get("/channels/{channel_id}/metrics", response_model=ChannelMetricsResponse)
async def get_channel_metrics(
    channel_id: int,
    time_range: MetricsTimeRange = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if channel exists and user is the owner
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    if channel.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view metrics for this channel")

    # Calculate time range
    start_date = datetime.utcnow() - timedelta(days=time_range.days)

    # Get metrics for all posts in the channel within the time range
    posts_metrics = (
        db.query(PostMetrics)
        .join(Post)
        .filter(
            Post.channel_id == channel_id,
            Post.created_at >= start_date
        )
        .all()
    )

    # Calculate channel metrics
    total_views = sum(metrics.views_count for metrics in posts_metrics)
    total_shares = sum(metrics.shares_count for metrics in posts_metrics)
    total_comments = sum(metrics.comments_count for metrics in posts_metrics)
    total_ctr = sum(metrics.ctr for metrics in posts_metrics) if posts_metrics else 0

    num_posts = len(posts_metrics)
    average_views = total_views / num_posts if num_posts > 0 else 0
    average_shares = total_shares / num_posts if num_posts > 0 else 0
    average_comments = total_comments / num_posts if num_posts > 0 else 0
    average_ctr = total_ctr / num_posts if num_posts > 0 else 0

    # Calculate average engagement (likes + comments + shares) / views
    total_engagement = sum(
        metrics.likes_count + metrics.comments_count + metrics.shares_count
        for metrics in posts_metrics
    )
    average_engagement = total_engagement / total_views if total_views > 0 else 0

    return ChannelMetricsResponse(
        subscribers_count=channel.subscribers_count,
        views_count=total_views,
        average_engagement=average_engagement,
        average_views=average_views,
        average_shares=average_shares,
        average_comments=average_comments,
        average_ctr=average_ctr
    )

@router.get("/posts/{post_id}/metrics", response_model=PostMetricsResponse)
async def get_post_metrics(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if post exists and user is the creator
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.channel.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view metrics for this post")

    # Get post metrics
    metrics = db.query(PostMetrics).filter(PostMetrics.post_id == post_id).first()
    if not metrics:
        raise HTTPException(status_code=404, detail="Metrics not found for this post")

    return PostMetricsResponse(
        views_count=metrics.views_count,
        likes_count=metrics.likes_count,
        shares_count=metrics.shares_count,
        comments_count=metrics.comments_count,
        ctr=metrics.ctr,
        created_at=post.created_at,
        updated_at=post.updated_at
    )

@router.get("/channels/{channel_id}/top-posts", response_model=List[PostMetricsResponse])
async def get_top_posts(
    channel_id: int,
    limit: int = 10,
    time_range: MetricsTimeRange = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if channel exists and user is the owner
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    if channel.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view metrics for this channel")

    # Calculate time range
    start_date = datetime.utcnow() - timedelta(days=time_range.days)

    # Get top posts by engagement (likes + comments + shares)
    top_posts = (
        db.query(Post, PostMetrics)
        .join(PostMetrics)
        .filter(
            Post.channel_id == channel_id,
            Post.created_at >= start_date
        )
        .order_by(
            (PostMetrics.likes_count + PostMetrics.comments_count + PostMetrics.shares_count).desc()
        )
        .limit(limit)
        .all()
    )

    return [
        PostMetricsResponse(
            views_count=metrics.views_count,
            likes_count=metrics.likes_count,
            shares_count=metrics.shares_count,
            comments_count=metrics.comments_count,
            ctr=metrics.ctr,
            created_at=post.created_at,
            updated_at=post.updated_at
        )
        for post, metrics in top_posts
    ] 