// src/axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // Replace with the resturan api url
  timeout: 1000,
  headers: { 'Content-Type': 'application/json' }
});

export default instance;
