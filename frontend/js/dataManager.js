/**
 * Data Manager for Pet Adoption Platform
 * Handles all API interactions and database connections
 */

class DataManager {
  constructor() {
    this.apiBase = "http://localhost:8000/api";
    this.currentUser = null;
    this.isAuthenticated = false;
    this.init();
  }

  init() {
    // Check if user is already logged in
    this.checkAuthStatus();
    this.setupEventListeners();
  }

  // Authentication Methods
  async login(username, password) {
    try {
      const response = await fetch(`${this.apiBase}/accounts/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store tokens
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        localStorage.setItem("user", JSON.stringify(data.user));

        this.currentUser = data.user;
        this.isAuthenticated = true;

        this.updateUIForAuthenticatedUser();
        return { success: true, data };
      } else {
        return { success: false, error: data.error || "Login failed" };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  async register(userData) {
    try {
      const response = await fetch(`${this.apiBase}/accounts/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (response.ok) {
        // Store tokens
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        localStorage.setItem("user", JSON.stringify(data.user));

        this.currentUser = data.user;
        this.isAuthenticated = true;

        this.updateUIForAuthenticatedUser();
        return { success: true, data };
      } else {
        return { success: false, error: data.error || "Registration failed" };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  async logout() {
    try {
      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        await fetch(`${this.apiBase}/accounts/logout/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({ refresh_token: refreshToken }),
        });
      }
    } catch (error) {
      console.error("Logout error:", error);
    }

    // Clear local storage
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");

    this.currentUser = null;
    this.isAuthenticated = false;

    this.updateUIForUnauthenticatedUser();
    window.location.href = "/frontend/landing.html";
  }

  checkAuthStatus() {
    const user = localStorage.getItem("user");
    const token = localStorage.getItem("access_token");

    if (user && token) {
      this.currentUser = JSON.parse(user);
      this.isAuthenticated = true;
      this.updateUIForAuthenticatedUser();
    } else {
      this.updateUIForUnauthenticatedUser();
    }
  }

  // Pet Data Methods
  async getPets(filters = {}) {
    try {
      const queryString = new URLSearchParams(filters).toString();
      const url = `${this.apiBase}/pets/${
        queryString ? "?" + queryString : ""
      }`;

      const response = await fetch(url, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, error: "Failed to fetch pets" };
    }
  }

  async getPetDetail(petId) {
    try {
      const response = await fetch(`${this.apiBase}/pets/${petId}/`, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, error: "Failed to fetch pet details" };
    }
  }

  async getFeaturedPets() {
    try {
      const response = await fetch(`${this.apiBase}/pets/featured/`, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, error: "Failed to fetch featured pets" };
    }
  }

  // Adoption Methods
  async createAdoptionRequest(petId, reason) {
    try {
      const response = await fetch(`${this.apiBase}/adoptions/`, {
        method: "POST",
        headers: this.getAuthHeaders(),
        credentials: "include",
        body: JSON.stringify({
          pet_id: petId,
          reason: reason,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        return { success: true, data };
      } else {
        return {
          success: false,
          error: data.error || "Failed to create adoption request",
        };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  async getAdoptionRequests() {
    try {
      const response = await fetch(`${this.apiBase}/adoptions/`, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, error: "Failed to fetch adoption requests" };
    }
  }

  async getAdoptionHistory() {
    try {
      const response = await fetch(`${this.apiBase}/adoptions/history/`, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, error: "Failed to fetch adoption history" };
    }
  }

  // User Profile Methods
  async getUserProfile() {
    try {
      const response = await fetch(`${this.apiBase}/accounts/profile/`, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, error: "Failed to fetch user profile" };
    }
  }

  async updateUserProfile(profileData) {
    try {
      const response = await fetch(`${this.apiBase}/accounts/profile/`, {
        method: "PUT",
        headers: this.getAuthHeaders(),
        credentials: "include",
        body: JSON.stringify(profileData),
      });

      const data = await response.json();

      if (response.ok) {
        // Update local user data
        this.currentUser = data;
        localStorage.setItem("user", JSON.stringify(data));
        return { success: true, data };
      } else {
        return {
          success: false,
          error: data.error || "Failed to update profile",
        };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  // Chat Methods
  async getConversations() {
    try {
      const response = await fetch(`${this.apiBase}/chat/conversations/`, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, error: "Failed to fetch conversations" };
    }
  }

  async getMessages(userId) {
    try {
      const response = await fetch(
        `${this.apiBase}/chat/messages/?user_id=${userId}`,
        {
          headers: this.getAuthHeaders(),
          credentials: "include",
        }
      );

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, error: "Failed to fetch messages" };
    }
  }

  async sendMessage(receiverId, content) {
    try {
      const response = await fetch(`${this.apiBase}/chat/messages/`, {
        method: "POST",
        headers: this.getAuthHeaders(),
        credentials: "include",
        body: JSON.stringify({
          receiver_id: receiverId,
          content: content,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        return { success: true, data };
      } else {
        return {
          success: false,
          error: data.error || "Failed to send message",
        };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  // Utility Methods
  getAuthHeaders() {
    const token = localStorage.getItem("access_token");
    return {
      "Content-Type": "application/json",
      Authorization: token ? `Bearer ${token}` : "",
    };
  }

  updateUIForAuthenticatedUser() {
    // Update navigation
    const authElements = document.querySelectorAll(".auth-required");
    const unauthElements = document.querySelectorAll(".unauth-only");

    authElements.forEach((el) => (el.style.display = "block"));
    unauthElements.forEach((el) => (el.style.display = "none"));

    // Update user info
    const userInfoElements = document.querySelectorAll(".user-info");
    userInfoElements.forEach((el) => {
      if (this.currentUser) {
        el.textContent =
          this.currentUser.username || this.currentUser.first_name || "User";
      }
    });

    // Update navigation links
    const loginLinks = document.querySelectorAll(".login-link");
    const logoutLinks = document.querySelectorAll(".logout-link");
    const profileLinks = document.querySelectorAll(".profile-link");

    loginLinks.forEach((link) => (link.style.display = "none"));
    logoutLinks.forEach((link) => (link.style.display = "inline"));
    profileLinks.forEach((link) => (link.style.display = "inline"));
  }

  updateUIForUnauthenticatedUser() {
    // Update navigation
    const authElements = document.querySelectorAll(".auth-required");
    const unauthElements = document.querySelectorAll(".unauth-only");

    authElements.forEach((el) => (el.style.display = "none"));
    unauthElements.forEach((el) => (el.style.display = "block"));

    // Update navigation links
    const loginLinks = document.querySelectorAll(".login-link");
    const logoutLinks = document.querySelectorAll(".logout-link");
    const profileLinks = document.querySelectorAll(".profile-link");

    loginLinks.forEach((link) => (link.style.display = "inline"));
    logoutLinks.forEach((link) => (link.style.display = "none"));
    profileLinks.forEach((link) => (link.style.display = "none"));
  }

  setupEventListeners() {
    // Logout button listeners
    document.addEventListener("click", (e) => {
      if (
        e.target.classList.contains("logout-btn") ||
        e.target.classList.contains("logout-link")
      ) {
        e.preventDefault();
        this.logout();
      }
    });

    // Profile button listeners
    document.addEventListener("click", (e) => {
      if (
        e.target.classList.contains("profile-btn") ||
        e.target.classList.contains("profile-link")
      ) {
        e.preventDefault();
        window.location.href = "/frontend/pages/profile.html";
      }
    });
  }

  // Error handling
  handleError(error) {
    console.error("DataManager Error:", error);
    this.showNotification(error, "error");
  }

  showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 5000);
  }
}

// Initialize DataManager globally
window.dataManager = new DataManager();
