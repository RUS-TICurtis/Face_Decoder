// Centralized API configuration supporting environmental overrides
export const API_HOST = import.meta.env.VITE_API_BASE_URL || (window.location.port === '5173' ? '' : 'http://127.0.0.1:8001');
export const API_BASE = `${API_HOST}/api/v1`;
export const FACES_URL = `${API_HOST}/static/faces`;
export const RAW_URL = `${API_HOST}/static/raw`;
