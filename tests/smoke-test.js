const axios = require('axios');

const endpoint = 'https://crc-function-app.azurewebsites.net/api/VisitorCounter';

axios.get(endpoint)
  .then(res => {
    const count = res.data?.count;

    if (res.status === 200 && typeof count === 'number') {
      console.log(`✅ Smoke test passed. Visitor count: ${count}`);
      process.exit(0);
    } else {
      console.error('❌ Unexpected response:', res.data);
      process.exit(1);
    }
  })
  .catch(err => {
    console.error('❌ Smoke test failed:', err.message);
    process.exit(1);
  });
