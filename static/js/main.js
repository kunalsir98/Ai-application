// AI Platform - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize navigation
    initializeNavigation();
    
    // Initialize file uploads
    initializeFileUploads();
    
    // Initialize copy functionality
    initializeCopyButtons();
    
    // Initialize theme management
    initializeTheme();
});

// Tooltip Initialization
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Animation Initialization
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    document.querySelectorAll('.feature-card, .tool-card, .provider-card').forEach(el => {
        observer.observe(el);
    });
}

// Form Enhancements
function initializeFormEnhancements() {
    // Auto-resize textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
    
    // Form validation feedback
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Show first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    showNotification('Please fill in all required fields', 'warning');
                }
            }
            form.classList.add('was-validated');
        });
    });
    
    // Real-time character counting
    document.querySelectorAll('textarea[data-max-length]').forEach(textarea => {
        const maxLength = parseInt(textarea.dataset.maxLength);
        const counter = document.createElement('small');
        counter.className = 'text-muted';
        textarea.parentNode.appendChild(counter);
        
        function updateCounter() {
            const remaining = maxLength - textarea.value.length;
            counter.textContent = `${remaining} characters remaining`;
            
            if (remaining < 50) {
                counter.className = 'text-warning';
            } else if (remaining < 0) {
                counter.className = 'text-danger';
            } else {
                counter.className = 'text-muted';
            }
        }
        
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });
}

// Navigation Enhancements
function initializeNavigation() {
    // Active page highlighting
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// File Upload Enhancements
function initializeFileUploads() {
    document.querySelectorAll('input[type="file"]').forEach(input => {
        const container = input.closest('.card-body') || input.parentNode;
        
        // Drag and drop functionality
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            container.addEventListener(eventName, preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            container.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            container.addEventListener(eventName, unhighlight, false);
        });
        
        container.addEventListener('drop', handleDrop, false);
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        function highlight() {
            container.classList.add('dragover');
        }
        
        function unhighlight() {
            container.classList.remove('dragover');
        }
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                input.files = files;
                
                // Trigger change event
                const event = new Event('change', { bubbles: true });
                input.dispatchEvent(event);
            }
        }
        
        // File selection feedback
        input.addEventListener('change', function() {
            if (this.files.length > 0) {
                const file = this.files[0];
                const fileName = file.name;
                const fileSize = formatFileSize(file.size);
                
                // Show file info
                let info = container.querySelector('.file-info');
                if (!info) {
                    info = document.createElement('div');
                    info.className = 'file-info mt-2';
                    container.appendChild(info);
                }
                
                info.innerHTML = `
                    <div class="alert alert-info">
                        <i class="fas fa-file me-2"></i>
                        <strong>${fileName}</strong> (${fileSize})
                    </div>
                `;
            }
        });
    });
}

// Copy Button Functionality
function initializeCopyButtons() {
    document.addEventListener('click', function(event) {
        if (event.target.matches('.copy-btn') || event.target.closest('.copy-btn')) {
            const button = event.target.closest('.copy-btn') || event.target;
            const targetSelector = button.dataset.target;
            const target = document.querySelector(targetSelector);
            
            if (target) {
                const text = target.textContent || target.value;
                copyToClipboard(text).then(() => {
                    const originalText = button.innerHTML;
                    button.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
                    
                    setTimeout(() => {
                        button.innerHTML = originalText;
                    }, 2000);
                });
            }
        }
    });
}

// Theme Management
function initializeTheme() {
    // Check for saved theme preference or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);
    
    // Theme toggle functionality
    document.addEventListener('click', function(event) {
        if (event.target.matches('.theme-toggle')) {
            const currentTheme = document.documentElement.dataset.theme || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        }
    });
}

function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    
    // Update theme toggle button if it exists
    const toggleBtn = document.querySelector('.theme-toggle');
    if (toggleBtn) {
        const icon = toggleBtn.querySelector('i');
        if (icon) {
            icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function copyToClipboard(text) {
    return navigator.clipboard.writeText(text).catch(err => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            document.body.removeChild(textArea);
            return successful ? Promise.resolve() : Promise.reject();
        } catch (err) {
            document.body.removeChild(textArea);
            return Promise.reject(err);
        }
    });
}

function showNotification(message, type = 'info', duration = 3000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
    
    return notification;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Loading State Management
function showLoadingState(element, text = 'Loading...') {
    element.classList.add('loading');
    const originalContent = element.innerHTML;
    element.dataset.originalContent = originalContent;
    
    element.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status"></span>
        ${text}
    `;
    
    return originalContent;
}

function hideLoadingState(element) {
    element.classList.remove('loading');
    const originalContent = element.dataset.originalContent;
    if (originalContent) {
        element.innerHTML = originalContent;
        delete element.dataset.originalContent;
    }
}

// Form Validation Helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateURL(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

// API Helper Functions
async function makeRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, config);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    }
}

// Local Storage Helpers
function saveToStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (error) {
        console.error('Failed to save to localStorage:', error);
        return false;
    }
}

function loadFromStorage(key, defaultValue = null) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : defaultValue;
    } catch (error) {
        console.error('Failed to load from localStorage:', error);
        return defaultValue;
    }
}

// Global Error Handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showNotification('An unexpected error occurred. Please try again.', 'danger');
});

// Global unhandled promise rejection handler
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('An error occurred while processing your request.', 'danger');
});

// Performance Monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        }, 0);
    });
}

// Export utility functions for use in other scripts
window.AIPlatform = {
    showNotification,
    showLoadingState,
    hideLoadingState,
    copyToClipboard,
    formatFileSize,
    makeRequest,
    saveToStorage,
    loadFromStorage,
    validateEmail,
    validateURL,
    debounce,
    throttle
};
