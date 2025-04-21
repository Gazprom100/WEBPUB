// Локальная аутентификация без бэкенда
exports.handler = async function(event, context) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Отвечаем на preflight запросы
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers
    };
  }

  // Разбираем путь
  const path = event.path.replace('/.netlify/functions/local-auth', '');
  
  console.log(`Local auth request: ${path}, method: ${event.httpMethod}`);
  
  try {
    // Обработка логина
    if ((path === '/login' || path === '/auth/login') && event.httpMethod === 'POST') {
      const data = JSON.parse(event.body);
      const { username, password } = data;
      
      console.log(`Попытка входа: ${username}`);
      
      // Демо-пользователь для тестов
      if (username === 'test@example.com' && password === 'password123') {
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            access_token: 'demo-token-123456',
            refresh_token: 'demo-refresh-123456',
            token_type: 'bearer'
          })
        };
      } else {
        return {
          statusCode: 401,
          headers,
          body: JSON.stringify({ detail: 'Неверный email или пароль' })
        };
      }
    }
    
    // Обработка запроса данных пользователя
    if ((path === '/me' || path === '/auth/me') && event.httpMethod === 'GET') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          id: '12345',
          email: 'test@example.com',
          full_name: 'Test User',
          is_active: true
        })
      };
    }
    
    // Обработка регистрации
    if ((path === '/signup' || path === '/auth/signup') && event.httpMethod === 'POST') {
      const data = JSON.parse(event.body);
      
      console.log(`Попытка регистрации: ${data.email}`);
      
      return {
        statusCode: 201,
        headers,
        body: JSON.stringify({
          id: 'new-user-123',
          email: data.email,
          full_name: data.full_name || 'New User',
          is_active: true
        })
      };
    }
    
    // Обработка восстановления пароля
    if ((path === '/forgot-password' || path === '/auth/forgot-password') && event.httpMethod === 'POST') {
      const data = JSON.parse(event.body);
      console.log(`Запрос сброса пароля для: ${data.email}`);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ 
          message: 'На ваш email отправлена инструкция по восстановлению пароля' 
        })
      };
    }
    
    // Тестовый эндпоинт
    if (path === '/test') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ 
          message: 'Локальная аутентификация работает!',
          timestamp: new Date().toISOString()
        })
      };
    }
    
    // Неизвестный путь
    console.log(`Неизвестный путь: ${path}`);
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ 
        detail: 'Route not found',
        path: path 
      })
    };
    
  } catch (error) {
    console.error('Local auth error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Server Error', 
        message: error.message 
      })
    };
  }
}; 