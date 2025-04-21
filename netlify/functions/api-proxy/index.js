const axios = require('axios');

exports.handler = async function(event, context) {
  // Разрешаем все CORS заголовки
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

  try {
    // Извлекаем путь и параметры из запроса
    const path = event.path.replace('/.netlify/functions/api-proxy', '');
    const targetUrl = `https://webpub-backend.netlify.app/.netlify/functions/api${path}`;
    
    console.log(`Proxy request to: ${targetUrl}`);
    console.log(`Method: ${event.httpMethod}`);
    console.log(`Body: ${event.body || 'no body'}`);
    
    // Настраиваем запрос к API
    const requestConfig = {
      method: event.httpMethod,
      url: targetUrl,
      headers: {
        'Content-Type': 'application/json'
      }
    };
    
    // Добавляем тело запроса, если есть
    if (event.body) {
      requestConfig.data = JSON.parse(event.body);
    }
    
    // Добавляем заголовок авторизации, если есть
    if (event.headers.authorization) {
      requestConfig.headers.Authorization = event.headers.authorization;
    }
    
    // Отправляем запрос к API бекенда
    const response = await axios(requestConfig);
    
    // Возвращаем ответ
    return {
      statusCode: response.status,
      headers,
      body: JSON.stringify(response.data)
    };
  } catch (error) {
    console.error('Proxy error:', error);
    
    // Правильно обрабатываем ошибки от API
    if (error.response) {
      return {
        statusCode: error.response.status,
        headers,
        body: JSON.stringify(error.response.data)
      };
    }
    
    // Общая ошибка
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Proxy Error', 
        message: error.message 
      })
    };
  }
}; 