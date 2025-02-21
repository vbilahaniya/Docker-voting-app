const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');

const app = express();
const redisClient = redis.createClient({ url: 'redis://redis:6379' });
redisClient.connect();

const pool = new Pool({
  host: 'postgres',
  user: 'postgres',
  password: 'postgres',
  database: 'postgres'
});

app.get('/results', async (req, res) => {
  const result = await redisClient.keys('*');
  const votes = {};
  for (let key of result) {
    votes[key] = await redisClient.get(key);
  }
  res.json(votes);
});

app.listen(4000, () => console.log('Result app running on port 4000'));
