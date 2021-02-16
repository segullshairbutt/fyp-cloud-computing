import axios from 'axios';

const baseURL = 'http://localhost:8000';

let axiosInstance = axios.create({
  baseURL
});

export default axiosInstance;
