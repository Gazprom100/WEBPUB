// Простая функция для эмуляции API на Netlify
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

// Секрет для JWT
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-here';

// Эмуляция базы данных
const users = [];

// Хеширование пароля
function hashPassword(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

// Генерация токенов
function generateTokens(userId) {
  const accessToken = jwt.sign({ sub: userId }, JWT_SECRET, { expiresIn: '1h' });
  const refreshToken = jwt.sign({ sub: userId, type: 'refresh' }, JWT_SECRET, { expiresIn: '7d' });
  return { accessToken, refreshToken };
}

exports.handler = async function(event, context) {
  // CORS заголовки
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Для preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers
    };
  }

  const path = event.path.replace('/.netlify/functions/api', '');
  
  try {
    // Регистрация
    if (path === '/auth/signup' && event.httpMethod === 'POST') {
      const { email, password, full_name } = JSON.parse(event.body);
      
      // Проверяем, существует ли уже пользователь
      const existingUser = users.find(u => u.email === email);
      if (existingUser) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ detail: 'Email already registered' })
        };
      }
      
      // Создаем нового пользователя
      const userId = crypto.randomUUID();
      const hashedPassword = hashPassword(password);
      
      users.push({
        id: userId,
        email,
        hashed_password: hashedPassword,
        full_name,
        is_active: true
      });
      
      // Возвращаем информацию о пользователе (без пароля)
      return {
        statusCode: 201,
        headers,
        body: JSON.stringify({
          id: userId,
          email,
          full_name,
          is_active: true
        })
      };
    }
    
    // Логин
    if (path === '/auth/login' && event.httpMethod === 'POST') {
      const { username, password } = JSON.parse(event.body);
      
      // Находим пользователя
      const user = users.find(u => u.email === username);
      if (!user || user.hashed_password !== hashPassword(password)) {
        return {
          statusCode: 401,
          headers,
          body: JSON.stringify({ 
            detail: 'Incorrect email or password' 
          })
        };
      }
      
      // Генерируем токены
      const { accessToken, refreshToken } = generateTokens(user.id);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          access_token: accessToken,
          refresh_token: refreshToken,
          token_type: 'bearer'
        })
      };
    }
    
    // Сброс пароля
    if (path === '/auth/forgot-password' && event.httpMethod === 'POST') {
      const { email } = JSON.parse(event.body);
      
      // В реальном сценарии здесь должна быть отправка email
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ 
          message: 'If your email is registered, you will receive a password reset link' 
        })
      };
    }
    
    // Эмуляция получения информации о пользователе
    if (path === '/auth/me' && event.httpMethod === 'GET') {
      // Проверка авторизации
      const authHeader = event.headers.authorization;
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return {
          statusCode: 401,
          headers,
          body: JSON.stringify({ detail: 'Not authenticated' })
        };
      }
      
      // Получаем токен
      const token = authHeader.replace('Bearer ', '');
      
      try {
        // Верифицируем токен
        const decoded = jwt.verify(token, JWT_SECRET);
        const userId = decoded.sub;
        
        // Находим пользователя
        const user = users.find(u => u.id === userId);
        if (!user) {
          return {
            statusCode: 404,
            headers,
            body: JSON.stringify({ detail: 'User not found' })
          };
        }
        
        // Возвращаем информацию о пользователе
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            id: user.id,
            email: user.email,
            full_name: user.full_name,
            is_active: user.is_active
          })
        };
      } catch (error) {
        return {
          statusCode: 401,
          headers,
          body: JSON.stringify({ detail: 'Invalid token' })
        };
      }
    }

    // Обработка не найденных маршрутов
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ detail: 'Not Found' })
    };
    
  } catch (error) {
    console.error('API Error:', error);
    
    // Возвращаем ошибку
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ detail: 'Internal Server Error' })
    };
  }
}; 