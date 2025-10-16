// Authentication service for handling JWT tokens and user sessions
import axios from 'axios';

const AUTH_TOKEN_KEY = 'flowdoc_auth_token';

class AuthService {
    static async login(username, password) {
        try {
            const response = await axios.post('/api/auth/login', {
                username,
                password
            });
            const { token } = response.data;
            localStorage.setItem(AUTH_TOKEN_KEY, token);
            return true;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }

    static async logout() {
        localStorage.removeItem(AUTH_TOKEN_KEY);
    }

    static getToken() {
        return localStorage.getItem(AUTH_TOKEN_KEY);
    }

    static isAuthenticated() {
        return !!this.getToken();
    }
}