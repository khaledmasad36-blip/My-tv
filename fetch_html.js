const axios = require('axios');
axios.get('http://ugeen.live/signup.html').then(res => console.log(res.data)).catch(err => console.error(err));
