from aiogram import Bot, types
from aiogram.types import ChatMemberAdministrator
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    
    async def get_channel_info(self, channel_id: str) -> dict:
        try:
            chat = await self.bot.get_chat(channel_id)
            return {
                "id": str(chat.id),
                "title": chat.title,
                "username": chat.username,
                "description": chat.description,
                "photo": chat.photo.big_file_id if chat.photo else None
            }
        except Exception as e:
            logger.error(f"Error getting channel info: {e}")
            raise
    
    async def check_bot_admin(self, channel_id: str) -> bool:
        try:
            chat_member = await self.bot.get_chat_member(channel_id, self.bot.id)
            return isinstance(chat_member, ChatMemberAdministrator)
        except Exception as e:
            logger.error(f"Error checking bot admin status: {e}")
            return False
    
    async def send_message(
        self,
        channel_id: str,
        text: str,
        image_url: str = None,
        parse_mode: str = "HTML"
    ) -> str:
        try:
            if image_url:
                # Download and send image with caption
                message = await self.bot.send_photo(
                    chat_id=channel_id,
                    photo=image_url,
                    caption=text,
                    parse_mode=parse_mode
                )
            else:
                # Send text only
                message = await self.bot.send_message(
                    chat_id=channel_id,
                    text=text,
                    parse_mode=parse_mode
                )
            return str(message.message_id)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise
    
    async def get_channel_stats(self, channel_id: str, message_id: str) -> dict:
        try:
            message = await self.bot.get_message(channel_id, int(message_id))
            return {
                "views": message.views if hasattr(message, 'views') else 0,
                "forwards": message.forward_count if hasattr(message, 'forward_count') else 0,
                "replies": message.reply_count if hasattr(message, 'reply_count') else 0
            }
        except Exception as e:
            logger.error(f"Error getting message stats: {e}")
            return {
                "views": 0,
                "forwards": 0,
                "replies": 0
            }
    
    async def close(self):
        await self.bot.session.close()

telegram_service = TelegramService() 