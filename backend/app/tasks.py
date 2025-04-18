from celery import shared_task
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from .db.session import SessionLocal
from .models.post import Post
from .models.channel import TelegramChannel
from .models.metrics import PostMetrics, ChannelMetrics
from .services.telegram import telegram_service
from .services.gpt import generate_content, generate_image
from .services.s3 import upload_to_s3

logger = logging.getLogger(__name__)

@shared_task
def schedule_post(post_id: str):
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post or post.status != 'approved':
            return
        
        channel = db.query(TelegramChannel).filter(TelegramChannel.id == post.channel_id).first()
        if not channel or not channel.is_active:
            return
        
        # Generate content if needed
        if not post.content:
            post.content = generate_content()
        
        # Generate image if needed
        if not post.image_url:
            image_data = generate_image(post.content)
            post.image_url = upload_to_s3(image_data, f"posts/{post_id}.jpg")
        
        # Update post status
        post.status = 'scheduled'
        db.commit()
        
        # Schedule the actual publishing
        publish_post.apply_async(
            args=[str(post.id)],
            eta=post.scheduled_time
        )
    except Exception as e:
        logger.error(f"Error scheduling post: {e}")
    finally:
        db.close()

@shared_task
def publish_post(post_id: str):
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post or post.status != 'scheduled':
            return
        
        channel = db.query(TelegramChannel).filter(TelegramChannel.id == post.channel_id).first()
        if not channel or not channel.is_active:
            post.status = 'failed'
            db.commit()
            return
        
        # Send message to Telegram
        message_id = telegram_service.send_message(
            channel_id=channel.channel_id,
            text=post.content,
            image_url=post.image_url
        )
        
        # Update post status
        post.status = 'published'
        post.telegram_message_id = message_id
        db.commit()
        
        # Schedule metrics update
        update_post_metrics.apply_async(
            args=[str(post.id)],
            countdown=3600  # Update after 1 hour
        )
    except Exception as e:
        logger.error(f"Error publishing post: {e}")
        post.status = 'failed'
        db.commit()
    finally:
        db.close()

@shared_task
def update_post_metrics(post_id: str):
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post or not post.telegram_message_id:
            return
        
        channel = db.query(TelegramChannel).filter(TelegramChannel.id == post.channel_id).first()
        if not channel:
            return
        
        # Get message stats from Telegram
        stats = telegram_service.get_channel_stats(
            channel_id=channel.channel_id,
            message_id=post.telegram_message_id
        )
        
        # Update metrics
        metrics = db.query(PostMetrics).filter(PostMetrics.post_id == post.id).first()
        if not metrics:
            metrics = PostMetrics(post_id=post.id)
            db.add(metrics)
        
        metrics.views_count = stats['views']
        metrics.shares_count = stats['forwards']
        metrics.comments_count = stats['replies']
        db.commit()
        
        # Schedule next update
        update_post_metrics.apply_async(
            args=[str(post.id)],
            countdown=3600  # Update every hour
        )
    except Exception as e:
        logger.error(f"Error updating post metrics: {e}")
    finally:
        db.close()

@shared_task
def update_channel_metrics(channel_id: str):
    db = SessionLocal()
    try:
        channel = db.query(TelegramChannel).filter(TelegramChannel.id == channel_id).first()
        if not channel or not channel.is_active:
            return
        
        # Get channel info from Telegram
        channel_info = telegram_service.get_channel_info(channel.channel_id)
        
        # Update metrics
        metrics = db.query(ChannelMetrics).filter(ChannelMetrics.channel_id == channel.id).first()
        if not metrics:
            metrics = ChannelMetrics(channel_id=channel.id)
            db.add(metrics)
        
        metrics.subscribers_count = channel_info.get('members_count', 0)
        db.commit()
        
        # Schedule next update
        update_channel_metrics.apply_async(
            args=[str(channel.id)],
            countdown=3600  # Update every hour
        )
    except Exception as e:
        logger.error(f"Error updating channel metrics: {e}")
    finally:
        db.close()

@shared_task
def generate_content(prompt: str = None) -> str:
    try:
        return generate_content(prompt)
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return ""

@shared_task
def generate_image(prompt: str) -> str:
    try:
        image_data = generate_image(prompt)
        return upload_to_s3(image_data, f"generated/{datetime.now().isoformat()}.jpg")
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return "" 