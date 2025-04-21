# Инструкция по запуску бэкенда WEBPUB с MongoDB

Эта инструкция поможет вам настроить и запустить бэкенд WEBPUB вместе с базой данных MongoDB.

## Предварительные требования

Для работы вам понадобится:
- Docker и Docker Compose
- Python 3.10 или выше (если запускаете локально)
- Node.js 18 или выше (для фронтенда)

## Запуск с использованием Docker

Самый простой способ запустить приложение - использовать Docker Compose:

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/WEBPUB.git
   cd WEBPUB
   ```

2. Создайте файл `.env` в корне проекта со следующими переменными окружения:
   ```
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   MONGODB_URL=mongodb://mongo:27017
   MONGODB_DB_NAME=webpub
   ```

3. Запустите все контейнеры с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. После запуска вы можете получить доступ к:
   - Фронтенду: http://localhost:3000
   - Бэкенду API: http://localhost:8000
   - MongoDB Express (веб-интерфейс для MongoDB): http://localhost:8081

## Локальный запуск бэкенда

Если вы хотите запустить бэкенд локально:

1. Установите MongoDB и запустите её:
   ```bash
   # Запуск MongoDB в контейнере Docker
   docker run -d -p 27017:27017 --name mongodb mongo:5.0
   ```

2. Перейдите в директорию бэкенда:
   ```bash
   cd backend
   ```

3. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

5. Создайте файл `.env` в директории `backend` со следующими переменными:
   ```
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   MONGODB_URL=mongodb://localhost:27017
   MONGODB_DB_NAME=webpub
   ```

6. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Бэкенд API будет доступен по адресу: http://localhost:8000

## Структура базы данных MongoDB

База данных MongoDB содержит следующие коллекции:
- `users` - информация о пользователях
- `channels` - каналы пользователей
- `posts` - публикации в каналах
- `channel_metrics` - метрики каналов

## Тестовые данные

Для быстрого начала работы вы можете загрузить тестовые данные в MongoDB:

```bash
# Выполните скрипт для заполнения базы тестовыми данными
python backend/scripts/seed_data.py
```

## Решение проблем

### Проблема с подключением к MongoDB
Если у вас возникает ошибка подключения к MongoDB, убедитесь, что:
1. MongoDB запущена и доступна по указанному адресу
2. В переменных окружения указан правильный URL
3. Порт 27017 не заблокирован файрволом

### Ошибка с импортом aiogram
Если при запуске появляется ошибка `ModuleNotFoundError: No module named 'aiogram'`, установите этот пакет:
```bash
pip install aiogram
```

## Дополнительная информация

- Документация API доступна по адресу: http://localhost:8000/docs
- Панель администратора MongoDB Express: http://localhost:8081
- Логи контейнеров можно посмотреть с помощью команды: `docker-compose logs -f` 