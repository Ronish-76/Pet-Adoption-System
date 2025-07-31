/**
 * Shelter Data Manager for Pet Adoption Platform
 * Handles all shelter-specific API interactions and database connections
 */

class ShelterDataManager {
  constructor() {
    this.apiBase = "http://localhost:8000/api";
    this.currentShelter = null;
    this.isAuthenticated = false;
    this.init();
  }

  init() {
    // Check if shelter is already logged in
    this.checkAuthStatus();
    this.setupEventListeners();
  }

  // Authentication Methods
  async login(username, password) {
    try {
      console.log("Attempting login with:", { username, password: "***" });

      const response = await fetch(`${this.apiBase}/accounts/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ username, password }),
      });

      console.log("Login response status:", response.status);
      const data = await response.json();
      console.log("Login response data:", data);

      if (response.ok) {
        // Check if user is a shelter
        if (data.user.profile && data.user.profile.is_shelter) {
          // Store tokens
          localStorage.setItem("shelter_access_token", data.access);
          localStorage.setItem("shelter_refresh_token", data.refresh);
          localStorage.setItem("shelter_user", JSON.stringify(data.user));

          this.currentShelter = data.user;
          this.isAuthenticated = true;

          this.updateUIForAuthenticatedShelter();
          return { success: true, data };
        } else {
          return {
            success: false,
            error: "This account is not a shelter account",
          };
        }
      } else {
        console.error("Login failed with status:", response.status);
        return { success: false, error: data.error || "Login failed" };
      }
    } catch (error) {
      console.error("Login network error:", error);
      return { success: false, error: "Network error" };
    }
  }

  async register(shelterData) {
    try {
      // Add shelter flag to registration data
      const registrationData = {
        ...shelterData,
        password2: shelterData.password, // Add password confirmation
        profile: {
          ...shelterData.profile,
          is_shelter: true,
        },
      };

      const response = await fetch(`${this.apiBase}/accounts/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(registrationData),
      });

      const data = await response.json();

      if (response.ok) {
        // Store tokens
        localStorage.setItem("shelter_access_token", data.access);
        localStorage.setItem("shelter_refresh_token", data.refresh);
        localStorage.setItem("shelter_user", JSON.stringify(data.user));

        this.currentShelter = data.user;
        this.isAuthenticated = true;

        this.updateUIForAuthenticatedShelter();
        return { success: true, data };
      } else {
        // Get detailed error message
        let errorMessage = "Registration failed";
        if (data.error) {
          errorMessage = data.error;
        } else if (data.detail) {
          errorMessage = data.detail;
        } else if (data.non_field_errors) {
          errorMessage = data.non_field_errors.join(", ");
        } else if (typeof data === "object") {
          // Handle field-specific errors
          const fieldErrors = [];
          for (const [field, errors] of Object.entries(data)) {
            if (Array.isArray(errors)) {
              fieldErrors.push(`${field}: ${errors.join(", ")}`);
            }
          }
          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join("; ");
          }
        }
        return { success: false, error: errorMessage };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  async logout() {
    try {
      const refreshToken = localStorage.getItem("shelter_refresh_token");
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
    localStorage.removeItem("shelter_access_token");
    localStorage.removeItem("shelter_refresh_token");
    localStorage.removeItem("shelter_user");

    this.currentShelter = null;
    this.isAuthenticated = false;

    this.updateUIForUnauthenticatedShelter();
    window.location.href = "/frontend/shelter_login.html";
  }

  checkAuthStatus() {
    const user = localStorage.getItem("shelter_user");
    const token = localStorage.getItem("shelter_access_token");

    if (user && token) {
      const userData = JSON.parse(user);
      if (userData.profile && userData.profile.is_shelter) {
        this.currentShelter = userData;
        this.isAuthenticated = true;
        this.updateUIForAuthenticatedShelter();
      } else {
        this.logout(); // Not a shelter user
      }
    } else {
      this.updateUIForUnauthenticatedShelter();
    }
  }

  // Pet Management Methods
  async getShelterPets() {
    try {
      const response = await fetch(`${this.apiBase}/pets/shelter/`, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      if (response.ok) {
        return { success: true, data };
      } else {
        return { success: false, error: data.error || "Failed to fetch shelter pets" };
      }
    } catch (error) {
      return { success: false, error: "Failed to fetch shelter pets" };
    }
  }

  async createPet(petData) {
    try {
      const response = await fetch(`${this.apiBase}/pets/create/`, {
        method: "POST",
        headers: this.getAuthHeaders(),
        credentials: "include",
        body: JSON.stringify(petData),
      });

      const data = await response.json();

      if (response.ok) {
        return { success: true, data };
      } else {
        return { success: false, error: data.error || "Failed to create pet" };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  async updatePet(petId, petData) {
    try {
      const response = await fetch(`${this.apiBase}/pets/${petId}/`, {
        method: "PUT",
        headers: this.getAuthHeaders(),
        credentials: "include",
        body: JSON.stringify(petData),
      });

      const data = await response.json();

      if (response.ok) {
        return { success: true, data };
      } else {
        return { success: false, error: data.error || "Failed to update pet" };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  async deletePet(petId) {
    try {
      const response = await fetch(`${this.apiBase}/pets/${petId}/`, {
        method: "DELETE",
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      if (response.ok) {
        return { success: true };
      } else {
        const data = await response.json();
        return { success: false, error: data.error || "Failed to delete pet" };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  // Adoption Management Methods
  async getShelterAdoptionRequests() {
    try {
      const response = await fetch(`${this.apiBase}/pets/shelter/adoptions/`, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      if (response.ok) {
        return { success: true, data };
      } else {
        return { success: false, error: data.error || "Failed to fetch adoption requests" };
      }
    } catch (error) {
      return { success: false, error: "Failed to fetch adoption requests" };
    }
  }

  async approveAdoptionRequest(requestId) {
    try {
      const response = await fetch(
        `${this.apiBase}/adoptions/${requestId}/update/`,
        {
          method: "PATCH",
          headers: this.getAuthHeaders(),
          credentials: "include",
          body: JSON.stringify({ status: "approved" }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        return { success: true, data };
      } else {
        return {
          success: false,
          error: data.error || "Failed to approve adoption request",
        };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  async rejectAdoptionRequest(requestId, reason) {
    try {
      const response = await fetch(
        `${this.apiBase}/adoptions/${requestId}/update/`,
        {
          method: "PATCH",
          headers: this.getAuthHeaders(),
          credentials: "include",
          body: JSON.stringify({ status: "rejected" }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        return { success: true, data };
      } else {
        return {
          success: false,
          error: data.error || "Failed to reject adoption request",
        };
      }
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  // Shelter Profile Methods
  async getShelterProfile() {
    try {
      const response = await fetch(`${this.apiBase}/accounts/profile/`, {
        headers: this.getAuthHeaders(),
        credentials: "include",
      });

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, error: "Failed to fetch shelter profile" };
    }
  }

  async updateShelterProfile(profileData) {
    try {
      const response = await fetch(`${this.apiBase}/accounts/profile/`, {
        method: "PUT",
        headers: this.getAuthHeaders(),
        credentials: "include",
        body: JSON.stringify(profileData),
      });

      const data = await response.json();

      if (response.ok) {
        // Update local shelter data
        this.currentShelter = data;
        localStorage.setItem("shelter_user", JSON.stringify(data));
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

  // Utility Methods
  getAuthHeaders() {
    const token = localStorage.getItem("shelter_access_token");
    return {
      "Content-Type": "application/json",
      Authorization: token ? `Bearer ${token}` : "",
    };
  }

  updateUIForAuthenticatedShelter() {
    // Update navigation
    const authElements = document.querySelectorAll(".shelter-auth-required");
    const unauthElements = document.querySelectorAll(".shelter-unauth-only");

    authElements.forEach((el) => (el.style.display = "block"));
    unauthElements.forEach((el) => (el.style.display = "none"));

    // Update shelter info
    const shelterInfoElements = document.querySelectorAll(".shelter-info");
    shelterInfoElements.forEach((el) => {
      if (this.currentShelter && this.currentShelter.profile) {
        el.textContent =
          this.currentShelter.profile.shelter_name ||
          this.currentShelter.username;
      }
    });

    // Update navigation links
    const loginLinks = document.querySelectorAll(".shelter-login-link");
    const logoutLinks = document.querySelectorAll(".shelter-logout-link");
    const dashboardLinks = document.querySelectorAll(".shelter-dashboard-link");

    loginLinks.forEach((link) => (link.style.display = "none"));
    logoutLinks.forEach((link) => (link.style.display = "inline"));
    dashboardLinks.forEach((link) => (link.style.display = "inline"));
  }

  updateUIForUnauthenticatedShelter() {
    // Update navigation
    const authElements = document.querySelectorAll(".shelter-auth-required");
    const unauthElements = document.querySelectorAll(".shelter-unauth-only");

    authElements.forEach((el) => (el.style.display = "none"));
    unauthElements.forEach((el) => (el.style.display = "block"));

    // Update navigation links
    const loginLinks = document.querySelectorAll(".shelter-login-link");
    const logoutLinks = document.querySelectorAll(".shelter-logout-link");
    const dashboardLinks = document.querySelectorAll(".shelter-dashboard-link");

    loginLinks.forEach((link) => (link.style.display = "inline"));
    logoutLinks.forEach((link) => (link.style.display = "none"));
    dashboardLinks.forEach((link) => (link.style.display = "none"));
  }

  setupEventListeners() {
    // Logout button listeners
    document.addEventListener("click", (e) => {
      if (
        e.target.classList.contains("shelter-logout-btn") ||
        e.target.classList.contains("shelter-logout-link")
      ) {
        e.preventDefault();
        this.logout();
      }
    });

    // Dashboard button listeners
    document.addEventListener("click", (e) => {
      if (
        e.target.classList.contains("shelter-dashboard-btn") ||
        e.target.classList.contains("shelter-dashboard-link")
      ) {
        e.preventDefault();
        window.location.href = "/frontend/shelter_dashboard.html";
      }
    });
  }

  // Error handling
  handleError(error) {
    console.error("ShelterDataManager Error:", error);
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

// Initialize ShelterDataManager globally
window.shelterDataManager = new ShelterDataManager();
