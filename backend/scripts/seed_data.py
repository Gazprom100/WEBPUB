#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для заполнения базы данных MongoDB тестовыми данными.
Запустите этот скрипт, чтобы создать тестовые данные для разработки.
"""

import asyncio
import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.mongodb import init_mongodb
from app.core.security import get_password_hash
from app.models.mongodb import User, Channel, Post, ChannelMetrics, PostStatus

async def create_test_data():
    """Создает тестовые данные в базе данных MongoDB."""
    print("Инициализация подключения к MongoDB...")
    await init_mongodb()
    
    print(f"Подключение к базе данных {settings.MONGODB_DB_NAME} установлено.")

    # Удаляем старые данные
    print("Удаление старых данных...")
    await User.delete_all()
    await Channel.delete_all()
    await Post.delete_all()
    await ChannelMetrics.delete_all()

    # Создаем тестовых пользователей
    print("Создание тестовых пользователей...")
    users = []
    
    test_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Тестовый Пользователь",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    await test_user.insert()
    users.append(test_user)
    
    admin_user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        full_name="Администратор",
        is_active=True,
        is_superuser=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    await admin_user.insert()
    users.append(admin_user)
    
    # Создаем тестовые каналы
    print("Создание тестовых каналов...")
    channels = []
    
    channel_categories = ["Новости", "Технологии", "Развлечения", "Образование", "Бизнес"]
    
    for i, user in enumerate(users):
        for j in range(2):  # У каждого пользователя по 2 канала
            category = channel_categories[(i + j) % len(channel_categories)]
            channel = Channel(
                username=f"channel_{i}_{j}",
                category=category,
                description=f"Тестовый канал #{j+1} пользователя {user.full_name}",
                is_monetized=j % 2 == 0,  # Чередуем монетизированные и немонетизированные каналы
                owner=user,
                created_at=datetime.utcnow() - timedelta(days=j*10),
                updated_at=datetime.utcnow()
            )
            await channel.insert()
            channels.append(channel)
    
    # Создаем тестовые публикации
    print("Создание тестовых публикаций...")
    for i, channel in enumerate(channels):
        for j in range(5):  # По 5 публикаций на канал
            # Создаем разные статусы для постов
            status = PostStatus.DRAFT
            scheduled_for = None
            published_at = None
            
            if j % 3 == 0:
                status = PostStatus.PUBLISHED
                published_at = datetime.utcnow() - timedelta(days=j)
            elif j % 3 == 1:
                status = PostStatus.SCHEDULED
                scheduled_for = datetime.utcnow() + timedelta(days=j)
            
            # Случайные метрики
            views = j * 100 + i * 50
            likes = int(views * 0.1)
            comments = int(views * 0.05)
            shares = int(views * 0.02)
            ctr = 0.05 + (j * 0.01)
            revenue = views * 0.001 if channel.is_monetized else 0.0
            
            post = Post(
                title=f"Тестовая публикация #{j+1} канала {channel.username}",
                description=f"Описание публикации #{j+1} для канала {channel.username}",
                content=f"<h1>Это тестовое содержимое публикации #{j+1}</h1><p>Здесь может быть любой HTML контент для публикации.</p>",
                status=status,
                author=channel.owner,
                channel=channel,
                media_urls=[f"https://example.com/images/{i}_{j}.jpg"] if j % 2 == 0 else [],
                
                # Метрики
                views_count=views,
                likes_count=likes,
                comments_count=comments,
                shares_count=shares,
                ctr=ctr,
                revenue=revenue,
                
                # Даты
                scheduled_for=scheduled_for,
                published_at=published_at,
                created_at=datetime.utcnow() - timedelta(days=j*2),
                updated_at=datetime.utcnow() - timedelta(days=j)
            )
            await post.insert()
    
    # Создаем метрики для каналов
    print("Создание метрик для каналов...")
    for channel in channels:
        for days_ago in range(30):
            date = datetime.utcnow() - timedelta(days=days_ago)
            
            # Генерируем какие-то значения с ростом или падением
            subscribers = 1000 + days_ago * 50
            views = 5000 + days_ago * 200
            engagement = 0.1 + (days_ago % 10) * 0.01
            revenue = views * 0.0005 if channel.is_monetized else 0.0
            
            metrics = ChannelMetrics(
                channel=channel,
                subscribers_count=subscribers,
                total_views=views,
                avg_engagement=engagement,
                total_revenue=revenue,
                metric_date=date
            )
            await metrics.insert()
    
    print("Тестовые данные успешно созданы!")
    print(f"Создано пользователей: {len(users)}")
    print(f"Создано каналов: {len(channels)}")
    print(f"Логин для тестового пользователя: test@example.com / password123")
    print(f"Логин для администратора: admin@example.com / admin123")

if __name__ == "__main__":
    asyncio.run(create_test_data()) 