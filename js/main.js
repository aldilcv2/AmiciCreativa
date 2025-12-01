// ========================================
// PORTFOLIO DATA LOADER
// ========================================

let portfolioData = null;

// Load portfolio data from JSON
async function loadPortfolioData() {
    try {
        const response = await fetch('data/portfolio-data.json');
        if (!response.ok) {
            throw new Error('Failed to load portfolio data');
        }
        portfolioData = await response.json();
        if (portfolioData.config) {
            applyTheme(portfolioData.config.theme);
            updateLogo(portfolioData.config.logo);
        }
        populateContent();
        initializeAnimations();
    } catch (error) {
        console.error('Error loading portfolio data:', error);
        // Fallback to default content if JSON fails to load
        portfolioData = getDefaultData();
        populateContent();
        initializeAnimations();
    }
}

// Apply Theme Settings
function applyTheme(theme) {
    if (!theme) return;
    const root = document.documentElement;
    if (theme.primaryColor) root.style.setProperty('--color-dark-blue', theme.primaryColor);
    if (theme.secondaryColor) root.style.setProperty('--color-light-gray', theme.secondaryColor);
    if (theme.backgroundColor) root.style.setProperty('--color-white', theme.backgroundColor);
    if (theme.textColor) root.style.setProperty('--color-dark', theme.textColor);

    if (theme.fontHeading) root.style.setProperty('--font-heading', `'${theme.fontHeading}', sans-serif`);
    if (theme.fontBody) root.style.setProperty('--font-body', `'${theme.fontBody}', sans-serif`);
}

// Update Logo
function updateLogo(logo) {
    if (!logo) return;
    const logoEl = document.getElementById('nav-logo');
    if (logo.type === 'image' && logo.content) {
        logoEl.innerHTML = `<img src="${logo.content}" alt="Logo" style="height: 40px;">`;
    } else {
        logoEl.textContent = logo.content || portfolioData.personal.name.split(' ')[0];
    }
}

// Default data fallback
function getDefaultData() {
    return {
        personal: {
            name: "Motion Graphics Artist",
            title: "Creative Designer & Animator",
            tagline: "Bringing ideas to life",
            heroDescription: "Crafting captivating visual stories"
        },
        about: {
            bio: "A passionate motion graphics artist.",
            description: "Creating engaging animations.",
            expertise: []
        },
        skills: [],
        projects: [],
        contact: {
            email: "contact@example.com",
            location: "Your City",
            availability: "Available for freelance",
            social: []
        }
    };
}

// ========================================
// POPULATE CONTENT
// ========================================

function populateContent() {
    // Hero Section
    document.getElementById('hero-name').textContent = portfolioData.personal.name;
    document.getElementById('hero-title').textContent = portfolioData.personal.title;
    document.getElementById('hero-description').textContent = portfolioData.personal.heroDescription;
    // Logo is handled by updateLogo()

    // About Section
    document.getElementById('about-bio').textContent = portfolioData.about.bio;
    document.getElementById('about-description').textContent = portfolioData.about.description;

    // Expertise Grid
    const expertiseGrid = document.getElementById('expertise-grid');
    expertiseGrid.innerHTML = '';
    portfolioData.about.expertise.forEach((item, index) => {
        const card = document.createElement('div');
        card.className = 'expertise-card fade-in-up';
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `<h3>${item}</h3>`;
        expertiseGrid.appendChild(card);
    });

    // Skills Section
    const skillsGrid = document.getElementById('skills-grid');
    skillsGrid.innerHTML = '';
    portfolioData.skills.forEach((skill, index) => {
        const card = document.createElement('div');
        card.className = 'skill-card fade-in-up';
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `
            <div class="skill-header">
                <div class="skill-icon">${skill.icon}</div>
                <div class="skill-info">
                    <h3>${skill.name}</h3>
                    <p class="skill-category">${skill.category}</p>
                </div>
            </div>
            <div class="skill-progress">
                <div class="progress-label">
                    <span>Proficiency</span>
                    <span>${skill.proficiency}%</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar" data-progress="${skill.proficiency}"></div>
                </div>
            </div>
        `;
        skillsGrid.appendChild(card);
    });

    // Projects Section
    const projectsGrid = document.getElementById('projects-grid');
    projectsGrid.innerHTML = '';
    portfolioData.projects.forEach((project, index) => {
        const card = document.createElement('div');
        card.className = 'project-card fade-in-up';
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `
            <div class="project-thumbnail">
                ${project.videoUrl && (project.videoUrl.endsWith('.mp4') || project.videoUrl.endsWith('.webm')) ?
                `<video src="${project.videoUrl}" muted loop playsinline onmouseover="this.play()" onmouseout="this.pause();this.currentTime=0;" style="width:100%;height:100%;object-fit:cover;"></video>` :
                `<img src="${project.thumbnail}" alt="${project.title}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'400\\' height=\\'300\\'%3E%3Crect fill=\\'%23E5E7EB\\' width=\\'400\\' height=\\'300\\'/%3E%3Ctext fill=\\'%236B7280\\' font-family=\\'Arial\\' font-size=\\'20\\' x=\\'50%25\\' y=\\'50%25\\' text-anchor=\\'middle\\' dy=\\'.3em\\'%3E${project.title}%3C/text%3E%3C/svg%3E'">`
            }
                <div class="project-overlay">
                    <div class="play-icon">▶</div>
                </div>
            </div>
            <div class="project-info">
                <div class="project-header">
                    <h3>${project.title}</h3>
                    <span class="project-year">${project.year}</span>
                </div>
                <p class="project-description">${project.description}</p>
                <div class="project-tags">
                    ${project.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
        `;

        // Add click handler for video link
        if (project.videoUrl) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', () => {
                // If it's an external link, open in new tab
                if (project.videoUrl.startsWith('http')) {
                    window.open(project.videoUrl, '_blank');
                } else {
                    // If it's a local video, maybe open a modal or just play it full screen?
                    // For now, let's open it in a new tab to be safe/simple
                    window.open(project.videoUrl, '_blank');
                }
            });
        }

        projectsGrid.appendChild(card);
    });

    // Contact Section
    document.getElementById('contact-email').textContent = portfolioData.contact.email;
    document.getElementById('contact-email').href = `mailto:${portfolioData.contact.email}`;
    document.getElementById('contact-location').textContent = portfolioData.contact.location;
    document.getElementById('contact-availability').textContent = portfolioData.contact.availability;

    // Social Links
    const socialLinks = document.getElementById('social-links');
    socialLinks.innerHTML = '';
    portfolioData.contact.social.forEach((social, index) => {
        const link = document.createElement('a');
        link.href = social.url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.className = 'social-link fade-in-up';
        link.style.animationDelay = `${index * 0.1}s`;
        link.title = social.platform;
        link.innerHTML = social.icon;
        socialLinks.appendChild(link);
    });

    // Footer
    document.getElementById('footer-name').textContent = portfolioData.personal.name;
    document.getElementById('current-year').textContent = new Date().getFullYear();
}

// ========================================
// NAVIGATION
// ========================================

function initializeNavigation() {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');

        // Animate hamburger icon
        const spans = navToggle.querySelectorAll('span');
        if (navMenu.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });

    // Close mobile menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            const spans = navToggle.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    });

    // Smooth scroll for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ========================================
// ANIMATIONS
// ========================================

function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');

                // Animate progress bars when skills section is visible
                if (entry.target.classList.contains('skill-card')) {
                    const progressBar = entry.target.querySelector('.progress-bar');
                    if (progressBar) {
                        const progress = progressBar.getAttribute('data-progress');
                        setTimeout(() => {
                            progressBar.style.width = `${progress}%`;
                        }, 200);
                    }
                }
            }
        });
    }, observerOptions);

    // Observe all fade-in-up elements
    const fadeElements = document.querySelectorAll('.fade-in-up');
    fadeElements.forEach(el => observer.observe(el));
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

// Debounce function for performance
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

// ========================================
// INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // Load portfolio data and initialize
    loadPortfolioData();

    // Initialize navigation
    initializeNavigation();

    // Add resize listener with debounce
    window.addEventListener('resize', debounce(() => {
        // Handle any responsive adjustments here
    }, 250));
});

// ========================================
// SMOOTH SCROLL POLYFILL FOR OLDER BROWSERS
// ========================================

// Check if smooth scroll is supported
if (!('scrollBehavior' in document.documentElement.style)) {
    // Load polyfill for older browsers
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/smoothscroll-polyfill@0.4.4/dist/smoothscroll.min.js';
    document.head.appendChild(script);
}
