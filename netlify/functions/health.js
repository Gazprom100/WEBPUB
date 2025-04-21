exports.handler = async function(event, context) {
  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type'
    },
    body: JSON.stringify({
      status: 'ok',
      timestamp: new Date().toISOString(),
      env: process.env.NODE_ENV,
      message: 'WEBPUB API функция работает нормально!'
    })
  };
}; 