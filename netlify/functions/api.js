// Простая функция для эмуляции API на Netlify
const jwt = require('jsonwebtoken');
const { randomUUID, createHash } = require('crypto');

// Секрет для JWT
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-here';

// Эмуляция базы данных - добавляем тестового пользователя для отладки
const users = [
  {
    id: '12345',
    email: 'test@example.com',
    hashed_password: createHash('sha256').update('password123').digest('hex'),
    full_name: 'Test User',
    is_active: true
  }
];

// Хеширование пароля
function hashPassword(password) {
  return createHash('sha256').update(password).digest('hex');
}

// Генерация токенов
function generateTokens(userId) {
  const accessToken = jwt.sign({ sub: userId }, JWT_SECRET, { expiresIn: '1h' });
  const refreshToken = jwt.sign({ sub: userId, type: 'refresh' }, JWT_SECRET, { expiresIn: '7d' });
  return { accessToken, refreshToken };
}

exports.handler = async function(event, context) {
  // Для отладки, логируем запрос
  console.log('Request path:', event.path);
  console.log('Request method:', event.httpMethod);
  console.log('Request headers:', JSON.stringify(event.headers));
  
  // Разрешенные домены (добавить здесь все нужные домены)
  const allowedOrigins = [
    'https://webpub1.netlify.app',
    'https://www.webpub1.netlify.app',
    'http://localhost:3000',
    'http://localhost:8888',
    '*'
  ];
  
  // Получаем Origin из запроса
  const origin = event.headers.origin || event.headers.Origin || '*';
  
  // CORS заголовки
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Credentials': 'true',
    'Content-Type': 'application/json'
  };

  // Для preflight requests
  if (event.httpMethod === 'OPTIONS') {
    console.log('Обработка preflight запроса');
    return {
      statusCode: 204,
      headers
    };
  }

  const path = event.path.replace('/.netlify/functions/api', '');
  
  try {
    // Тестовый эндпоинт для проверки 
    if (path === '/test' && event.httpMethod === 'GET') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ 
          message: 'API работает!',
          timestamp: new Date().toISOString(),
          users_count: users.length
        })
      };
    }
    
    // Регистрация
    if (path === '/auth/signup' && event.httpMethod === 'POST') {
      console.log('Обработка запроса регистрации');
      
      let parsedBody;
      try {
        parsedBody = JSON.parse(event.body);
        console.log('Данные регистрации:', JSON.stringify(parsedBody));
      } catch (e) {
        console.error('Ошибка при разборе JSON', e);
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ detail: 'Invalid JSON body' })
        };
      }
      
      const { email, password, full_name } = parsedBody;
      
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
      const userId = randomUUID();
      const hashedPassword = hashPassword(password);
      
      users.push({
        id: userId,
        email,
        hashed_password: hashedPassword,
        full_name,
        is_active: true
      });
      
      console.log('Пользователь создан:', email);
      
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
      console.log('Обработка запроса логина');
      
      let parsedBody;
      try {
        parsedBody = JSON.parse(event.body);
        console.log('Данные логина:', JSON.stringify(parsedBody));
      } catch (e) {
        console.error('Ошибка при разборе JSON', e);
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ detail: 'Invalid JSON body' })
        };
      }
      
      const { username, password } = parsedBody;
      
      if (!username || !password) {
        console.log('Отсутствуют обязательные поля');
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ detail: 'Username and password required' })
        };
      }
      
      // Находим пользователя
      const user = users.find(u => u.email === username);
      console.log('Найден пользователь:', user ? user.email : 'not found');
      
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
      
      console.log('Успешный вход:', username);
      
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
      console.log('Обработка запроса сброса пароля');
      
      let parsedBody;
      try {
        parsedBody = JSON.parse(event.body);
      } catch (e) {
        console.error('Ошибка при разборе JSON', e);
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ detail: 'Invalid JSON body' })
        };
      }
      
      const { email } = parsedBody;
      
      // В реальном сценарии здесь должна быть отправка email
      console.log('Запрос сброса пароля для:', email);
      
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
      console.log('Обработка запроса GET /auth/me');
      
      // Проверка авторизации
      const authHeader = event.headers.authorization;
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        console.log('Отсутствует токен авторизации');
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
        
        console.log('Токен верифицирован для пользователя:', userId);
        
        // Находим пользователя
        const user = users.find(u => u.id === userId);
        if (!user) {
          console.log('Пользователь не найден:', userId);
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
        console.error('Ошибка верификации токена:', error);
        return {
          statusCode: 401,
          headers,
          body: JSON.stringify({ detail: 'Invalid token' })
        };
      }
    }

    // Обработка не найденных маршрутов
    console.log('Маршрут не найден:', path);
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ 
        detail: 'Not Found',
        path: path,
        method: event.httpMethod
      })
    };
    
  } catch (error) {
    console.error('API Error:', error);
    
    // Возвращаем ошибку
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        detail: 'Internal Server Error',
        message: error.message
      })
    };
  }
}; 