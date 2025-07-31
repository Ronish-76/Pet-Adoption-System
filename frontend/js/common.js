/**
 * Common JavaScript functions for Pet Adoption Platform
 */

// Navbar scroll effect
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Add active class to current page in navigation
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        if (linkHref === currentPage) {
            link.classList.add('active');
        }
    });
});

/**
 * Form validation helpers
 */
function validateEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function validatePassword(password) {
    // At least 6 characters, with at least one number
    return password.length >= 6;
}

/**
 * UI Helpers
 */
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'loading';
        loadingIndicator.innerHTML = '<div class="spinner"></div>';
        
        element.style.opacity = '0.5';
        element.parentNode.insertBefore(loadingIndicator, element.nextSibling);
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.opacity = '1';
        const loadingIndicator = element.parentNode.querySelector('.loading');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }
}

/**
 * Modal helpers
 */
function showModal(title, content, onConfirm = null) {
    // Create modal container
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        backdrop-filter: blur(5px);
    `;
    
    // Create modal content
    const modalContent = document.createElement('div');
    modalContent.className = 'modal-content';
    modalContent.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 12px;
        max-width: 500px;
        width: 90%;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    `;
    
    // Add title and content
    modalContent.innerHTML = `
        <h2 style="margin-bottom: 1rem;">${title}</h2>
        <div style="margin-bottom: 1.5rem;">${content}</div>
        <div class="modal-buttons" style="display: flex; justify-content: center; gap: 1rem;">
            <button class="modal-cancel" style="padding: 0.5rem 1rem; border-radius: 8px; border: 1px solid #e2e8f0; background: white; cursor: pointer;">Cancel</button>
            <button class="modal-confirm" style="padding: 0.5rem 1rem; border-radius: 8px; background: #6366f1; color: white; border: none; cursor: pointer;">Confirm</button>
        </div>
    `;
    
    // Add to document
    document.body.appendChild(modal);
    modal.appendChild(modalContent);
    
    // Add event listeners
    const cancelButton = modalContent.querySelector('.modal-cancel');
    const confirmButton = modalContent.querySelector('.modal-confirm');
    
    cancelButton.addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    confirmButton.addEventListener('click', () => {
        if (onConfirm) onConfirm();
        document.body.removeChild(modal);
    });
    
    return modal;
}

function closeModal(modal) {
    if (modal && modal.parentNode) {
        modal.parentNode.removeChild(modal);
    }
}