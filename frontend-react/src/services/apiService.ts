import axios, { AxiosInstance, AxiosResponse } from 'axios';

const API_BASE_URL = 'http://localhost:8080/api';

export interface User {
  id: number;
  username: string;
}

export interface VaultEntry {
  id: number;
  service_name: string;
  username: string;
  password: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface LoginResponse {
  message: string;
  token: string;
  user: User;
}

export interface RegisterRequest {
  username: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface VaultEntryCreate {
  service_name: string;
  username: string;
  password: string;
  notes?: string;
}

export interface VaultEntryUpdate {
  password?: string;
  notes?: string;
}

class ApiService {
  private apiClient: AxiosInstance;

  constructor() {
    this.apiClient = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    this.apiClient.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    this.apiClient.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.clearAuthData();
          window.location.href = '/';
        }
        return Promise.reject(error);
      }
    );
  }

  private clearAuthData(): void {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }

  async register(userData: RegisterRequest): Promise<{ message: string }> {
    const response = await this.apiClient.post('/register', userData);
    return response.data;
  }

  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await this.apiClient.post('/login', credentials);
    const { token, user } = response.data;
    
    localStorage.setItem('authToken', token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return response.data;
  }

  async logout(): Promise<{ message: string }> {
    const response = await this.apiClient.post('/logout');
    this.clearAuthData();
    return response.data;
  }

  async checkUsername(username: string): Promise<{ available: boolean }> {
    const response = await this.apiClient.get(`/check-username/${username}`);
    return response.data;
  }

  async getVaultEntries(): Promise<VaultEntry[]> {
    const response = await this.apiClient.get('/vault/entries');
    return response.data;
  }

  async createVaultEntry(entry: VaultEntryCreate): Promise<{ message: string }> {
    const response = await this.apiClient.post('/vault/entries', entry);
    return response.data;
  }

  async updateVaultEntry(entryId: number, entry: VaultEntryUpdate): Promise<{ message: string }> {
    const response = await this.apiClient.put(`/vault/entries/${entryId}`, entry);
    return response.data;
  }

  async deleteVaultEntry(entryId: number): Promise<{ message: string }> {
    const response = await this.apiClient.delete(`/vault/entries/${entryId}`);
    return response.data;
  }

  async deleteAccount(password: string): Promise<{ message: string }> {
    const user = this.getCurrentUser();
    if (!user) throw new Error('No user logged in');
    
    const response = await this.apiClient.delete('/user/delete', {
      data: {
        username: user.username,
        password: password
      }
    });
    
    this.clearAuthData();
    return response.data;
  }

  getCurrentUser(): User | null {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  getAuthToken(): string | null {
    return localStorage.getItem('authToken');
  }

  isAuthenticated(): boolean {
    return !!this.getAuthToken();
  }
}

export const apiService = new ApiService();
export default apiService;
