/**
 * API Service for Pet Adoption Platform
 */

const API_BASE_URL = "http://localhost:8000/api";

class APIService {
  constructor() {
    // Using cookie-based authentication
  }

  // Helper method to get headers
  getHeaders(includeAuth = true) {
    const headers = {
      "Content-Type": "application/json",
    };
    // No need to manually add Authorization header - cookies handle this
    return headers;
  }

  // Helper method to handle API responses
  async handleResponse(response) {
    if (response.status === 401) {
      // Unauthorized - redirect to login if not already there
      if (window.location.pathname !== "/login.html") {
        window.location.href = "login.html";
      }
      return;
    }

    let data;
    try {
      data = await response.json();
    } catch (e) {
      throw new Error("Invalid server response");
    }

    if (!response.ok) {
      // Handle different error formats
      let errorMessage = "Request failed";

      if (data.detail) {
        errorMessage = data.detail;
      } else if (data.message) {
        errorMessage = data.message;
      } else if (data.error) {
        errorMessage = data.error;
      } else if (typeof data === "string") {
        errorMessage = data;
      } else if (data.username && Array.isArray(data.username)) {
        errorMessage = `Username: ${data.username[0]}`;
      } else if (data.email && Array.isArray(data.email)) {
        errorMessage = `Email: ${data.email[0]}`;
      } else if (data.password && Array.isArray(data.password)) {
        errorMessage = `Password: ${data.password[0]}`;
      }

      throw new Error(errorMessage);
    }

    return data;
  }

  // Helper method to make requests with timeout
  async makeRequest(url, options = {}, timeout = 10000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...options,
        credentials: "include", // Include cookies in requests
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === "AbortError") {
        throw new Error("Request timeout");
      }
      throw error;
    }
  }

  // Authentication APIs
  async login(username, password) {
    // Input validation
    if (!username || !password) {
      throw new Error("Username and password are required");
    }

    if (username.length > 150 || password.length > 128) {
      throw new Error("Invalid credentials");
    }

    const response = await this.makeRequest(`${API_BASE_URL}/accounts/login/`, {
      method: "POST",
      headers: this.getHeaders(false),
      body: JSON.stringify({
        username: username.trim(),
        password: password,
      }),
    });

    const data = await this.handleResponse(response);
    // Store tokens if available
    if (data && data.access) {
      localStorage.setItem("access_token", data.access);
    }
    if (data && data.refresh) {
      localStorage.setItem("refresh_token", data.refresh);
    }
    this.token = data.access;
    return data;
  }

  async register(userData) {
    // Input validation
    if (
      !userData.username ||
      !userData.email ||
      !userData.password ||
      !userData.password2
    ) {
      throw new Error("All fields are required");
    }

    if (userData.username.length < 3 || userData.username.length > 30) {
      throw new Error("Username must be between 3 and 30 characters");
    }

    if (userData.password !== userData.password2) {
      throw new Error("Passwords do not match");
    }

    if (userData.password.length < 8 || userData.password.length > 128) {
      throw new Error("Password must be between 8 and 128 characters");
    }

    // Sanitize input data
    const sanitizedData = {
      username: userData.username.trim(),
      email: userData.email.trim().toLowerCase(),
      password: userData.password,
      password2: userData.password2,
    };

    const response = await this.makeRequest(
      `${API_BASE_URL}/accounts/register/`,
      {
        method: "POST",
        headers: this.getHeaders(false),
        body: JSON.stringify(sanitizedData),
      },
      15000
    ); // Longer timeout for registration

    const data = await this.handleResponse(response);

    // Store tokens if available (some APIs return tokens on registration)
    if (data && data.access) {
      localStorage.setItem("access_token", data.access);
      if (data.refresh) {
        localStorage.setItem("refresh_token", data.refresh);
      }
      this.token = data.access;
    }

    return data;
  }

  async logout() {
    // Clear cookies by setting them to expire
    document.cookie =
      "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie =
      "refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  }

  // Token refresh method
  async refreshToken() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
      throw new Error("No refresh token available");
    }

    const response = await this.makeRequest(`${API_BASE_URL}/token/refresh/`, {
      method: "POST",
      headers: this.getHeaders(false),
      body: JSON.stringify({ refresh: refreshToken }),
    });

    const data = await this.handleResponse(response);

    if (data && data.access) {
      localStorage.setItem("access_token", data.access);
      this.token = data.access;
    }

    return data;
  }

  // User Profile APIs
  async getUserProfile() {
    const response = await this.makeRequest(
      `${API_BASE_URL}/accounts/profile/`,
      {
        headers: this.getHeaders(),
      }
    );

    return await this.handleResponse(response);
  }

  async updateUserProfile(profileData) {
    const response = await this.makeRequest(
      `${API_BASE_URL}/accounts/profile/`,
      {
        method: "PUT",
        headers: this.getHeaders(),
        body: JSON.stringify(profileData),
      }
    );
    return await this.handleResponse(response);
  }

  // Pet APIs
  async getPets(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = `${API_BASE_URL}/pets/${queryString ? "?" + queryString : ""}`;

    const response = await this.makeRequest(url, {
      headers: this.getHeaders(false),
    });

    return await this.handleResponse(response);
  }

  async getPetsPage(page = 1, filters = {}) {
    const params = { page, ...filters };
    return await this.getPets(params);
  }

  async getFeaturedPets() {
    const response = await this.makeRequest(`${API_BASE_URL}/pets/featured/`, {
      headers: this.getHeaders(false),
    });

    return await this.handleResponse(response);
  }

  async getPetDetail(petId) {
    if (!petId || isNaN(petId)) {
      throw new Error("Invalid pet ID");
    }

    const response = await this.makeRequest(`${API_BASE_URL}/pets/${petId}/`, {
      headers: this.getHeaders(false),
    });

    return await this.handleResponse(response);
  }

  async searchPets(query) {
    if (!query || query.trim().length === 0) {
      throw new Error("Search query is required");
    }

    const response = await this.makeRequest(
      `${API_BASE_URL}/pets/search/?q=${encodeURIComponent(query.trim())}`,
      {
        headers: this.getHeaders(false),
      }
    );

    return await this.handleResponse(response);
  }

  // Adoption APIs
  async createAdoptionRequest(petId, applicationData) {
    if (!petId || isNaN(petId)) {
      throw new Error("Invalid pet ID");
    }

    const response = await this.makeRequest(`${API_BASE_URL}/adoptions/`, {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({
        pet: petId,
        ...applicationData,
      }),
    });

    return await this.handleResponse(response);
  }

  async getAdoptionRequests() {
    const response = await this.makeRequest(`${API_BASE_URL}/adoptions/`, {
      headers: this.getHeaders(),
    });

    return await this.handleResponse(response);
  }

  async getAdoptionHistory() {
    const response = await this.makeRequest(
      `${API_BASE_URL}/adoptions/history/`,
      {
        headers: this.getHeaders(),
      }
    );

    return await this.handleResponse(response);
  }

  // Utility method to check if user is authenticated
  isAuthenticated() {
    return !!this.token && !!localStorage.getItem("access_token");
  }

  // Utility method to clear all auth data
  clearAuth() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("loginAttempts");
    this.token = null;
  }

  // Utility method to get current user from token
  getCurrentUser() {
    if (!this.token) return null;

    try {
      const payload = JSON.parse(atob(this.token.split(".")[1]));
      return {
        id: payload.user_id,
        username: payload.username,
        exp: payload.exp,
      };
    } catch (e) {
      return null;
    }
  }

  // Check if token is expired
  isTokenExpired() {
    const user = this.getCurrentUser();
    if (!user) return true;

    return Date.now() >= user.exp * 1000;
  }
}

// Create global API instance
const api = new APIService();
