import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

interface TokenResponse {
  access: string;
  refresh: string;
}

export const registerUser = async (username: string, password: string) => {
  const response = await axios.post(`${API_URL}/register/`, {
    username,
    password,
  });
  return response.data;
};

export const login = async (username: string, password: string): Promise<TokenResponse> => {
  const response = await axios.post(`${API_URL}/token/`, {
    username,
    password,
  });

  const tokens: TokenResponse = response.data;
  localStorage.setItem('access', tokens.access);
  localStorage.setItem('refresh', tokens.refresh);
  return tokens;
};

export const logout = () => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
};

export const isLoggedIn = () => {
  return !!localStorage.getItem('access');
};

export const getAccessToken = () => {
  return localStorage.getItem('access');
};

export const refreshToken = async (): Promise<string | null> => {
  const refresh = localStorage.getItem('refresh');
  if (!refresh) return null;

  try {
    const response = await axios.post(`${API_URL}/token/refresh/`, { refresh });
    const newAccess = response.data.access;
    localStorage.setItem('access', newAccess);
    return newAccess;
  } catch (error) {
    logout();
    return null;
  }
};

// Helper: Make an authenticated request
export const getCurrentUser = async () => {
  const access = getAccessToken();
  if (!access) throw new Error('Not authenticated');

  try {
    const response = await axios.get(`${API_URL}/me/`, {
      headers: {
        Authorization: `Bearer ${access}`,
      },
    });
    return response.data;
  } catch (err) {
    // Try refresh and retry once
    const newAccess = await refreshToken();
    if (!newAccess) throw new Error('Session expired');

    const response = await axios.get(`${API_URL}/me/`, {
      headers: {
        Authorization: `Bearer ${newAccess}`,
      },
    });
    return response.data;
  }
};
