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
    if (path === '/login' && event.httpMethod === 'POST') {
      const data = JSON.parse(event.body);
      const { username, password } = data;
      
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
    if (path === '/me' && event.httpMethod === 'GET') {
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
    if (path === '/signup' && event.httpMethod === 'POST') {
      const data = JSON.parse(event.body);
      
      return {
        statusCode: 201,
        headers,
        body: JSON.stringify({
          id: 'new-user-123',
          email: data.email,
          full_name: data.full_name,
          is_active: true
        })
      };
    }
    
    // Обработка восстановления пароля
    if (path === '/forgot-password' && event.httpMethod === 'POST') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ 
          message: 'На ваш email отправлена инструкция по восстановлению пароля' 
        })
      };
    }
    
    // Неизвестный путь
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ detail: 'Route not found' })
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