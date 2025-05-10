/**
 * Easter Eggs for EdgeRoute
 * 
 * This file contains various Easter eggs hidden throughout the application.
 * Enjoy discovering them!
 */

// Konami Code Easter Egg
class KonamiCode {
    constructor() {
        this.konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
        this.konamiIndex = 0;
        this.init();
    }

    init() {
        document.addEventListener('keydown', (e) => {
            // Check if the key matches the next key in the sequence
            if (e.key === this.konamiSequence[this.konamiIndex]) {
                this.konamiIndex++;
                
                // If the full sequence is entered, trigger the Easter egg
                if (this.konamiIndex === this.konamiSequence.length) {
                    this.activateKonamiCode();
                    this.konamiIndex = 0; // Reset for next time
                }
            } else {
                this.konamiIndex = 0; // Reset if wrong key
            }
        });
    }

    activateKonamiCode() {
        console.log('🎮 Konami Code activated!');
        
        // Create a container for the animation
        const container = document.createElement('div');
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100%';
        container.style.height = '100%';
        container.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        container.style.zIndex = '9999';
        container.style.display = 'flex';
        container.style.justifyContent = 'center';
        container.style.alignItems = 'center';
        container.style.flexDirection = 'column';
        container.style.color = '#fff';
        container.style.fontFamily = 'monospace';
        container.style.fontSize = '2rem';
        
        // Add content
        container.innerHTML = `
            <h1 style="color: #0f0; text-shadow: 0 0 10px #0f0; font-size: 3rem; margin-bottom: 20px;">KONAMI CODE ACTIVATED!</h1>
            <p>You've discovered a secret Easter egg!</p>
            <div id="game-container" style="margin-top: 20px; width: 400px; height: 300px; border: 2px solid #0f0; position: relative; overflow: hidden;">
                <div id="player" style="width: 20px; height: 20px; background-color: #0f0; position: absolute; top: 140px; left: 50px;"></div>
                <div id="goal" style="width: 20px; height: 20px; background-color: #f00; position: absolute; top: 140px; left: 330px;"></div>
            </div>
            <p style="margin-top: 20px;">Use arrow keys to move. Reach the red square!</p>
            <button id="close-game" style="margin-top: 20px; padding: 10px 20px; background-color: #333; color: #fff; border: none; cursor: pointer;">Close</button>
        `;
        
        document.body.appendChild(container);
        
        // Add event listener to close button
        document.getElementById('close-game').addEventListener('click', () => {
            document.body.removeChild(container);
        });
        
        // Simple game logic
        const player = document.getElementById('player');
        const goal = document.getElementById('goal');
        const gameContainer = document.getElementById('game-container');
        
        let playerX = 50;
        let playerY = 140;
        
        const movePlayer = (e) => {
            e.preventDefault(); // Prevent scrolling
            
            const step = 10;
            
            switch (e.key) {
                case 'ArrowUp':
                    playerY = Math.max(0, playerY - step);
                    break;
                case 'ArrowDown':
                    playerY = Math.min(gameContainer.offsetHeight - player.offsetHeight, playerY + step);
                    break;
                case 'ArrowLeft':
                    playerX = Math.max(0, playerX - step);
                    break;
                case 'ArrowRight':
                    playerX = Math.min(gameContainer.offsetWidth - player.offsetWidth, playerX + step);
                    break;
            }
            
            player.style.top = `${playerY}px`;
            player.style.left = `${playerX}px`;
            
            // Check if player reached the goal
            const goalRect = goal.getBoundingClientRect();
            const playerRect = player.getBoundingClientRect();
            
            if (
                playerRect.left < goalRect.right &&
                playerRect.right > goalRect.left &&
                playerRect.top < goalRect.bottom &&
                playerRect.bottom > goalRect.top
            ) {
                // Player reached the goal
                goal.style.backgroundColor = '#0f0';
                
                // Show victory message
                const victoryMessage = document.createElement('div');
                victoryMessage.style.position = 'absolute';
                victoryMessage.style.top = '50%';
                victoryMessage.style.left = '50%';
                victoryMessage.style.transform = 'translate(-50%, -50%)';
                victoryMessage.style.color = '#0f0';
                victoryMessage.style.fontSize = '2rem';
                victoryMessage.style.textShadow = '0 0 10px #0f0';
                victoryMessage.textContent = 'YOU WIN!';
                
                gameContainer.appendChild(victoryMessage);
                
                // Remove keyboard event listener
                document.removeEventListener('keydown', movePlayer);
            }
        };
        
        document.addEventListener('keydown', movePlayer);
    }
}

// Secret Theme Easter Egg
class SecretTheme {
    constructor() {
        this.clickSequence = ['logo', 'logo', 'profile', 'logo'];
        this.clickIndex = 0;
        this.clickTimeout = null;
        this.init();
    }

    init() {
        // Add click listeners to elements
        document.addEventListener('click', (e) => {
            // Check if clicked on logo
            if (e.target.closest('.navbar-brand')) {
                this.handleClick('logo');
            }
            // Check if clicked on profile
            else if (e.target.closest('.nav-link[href="/auth/profile"]')) {
                this.handleClick('profile');
            } else {
                this.resetSequence();
            }
        });
    }

    handleClick(elementType) {
        // Clear timeout if it exists
        if (this.clickTimeout) {
            clearTimeout(this.clickTimeout);
        }
        
        // Check if the click matches the next element in the sequence
        if (elementType === this.clickSequence[this.clickIndex]) {
            this.clickIndex++;
            
            // If the full sequence is clicked, trigger the Easter egg
            if (this.clickIndex === this.clickSequence.length) {
                this.activateSecretTheme();
                this.clickIndex = 0; // Reset for next time
            }
        } else {
            this.resetSequence();
        }
        
        // Set timeout to reset sequence after 2 seconds of inactivity
        this.clickTimeout = setTimeout(() => {
            this.resetSequence();
        }, 2000);
    }

    resetSequence() {
        this.clickIndex = 0;
        if (this.clickTimeout) {
            clearTimeout(this.clickTimeout);
            this.clickTimeout = null;
        }
    }

    activateSecretTheme() {
        console.log('🎨 Secret theme activated!');
        
        // Create a style element
        const style = document.createElement('style');
        style.id = 'secret-theme-style';
        
        // Add CSS for the secret theme
        style.textContent = `
            :root {
                --primary-color: #ff00ff !important;
                --secondary-color: #00ffff !important;
                --dark-color: #000080 !important;
                --light-color: #f0f8ff !important;
            }
            
            body {
                background: linear-gradient(135deg, #000080, #800080) !important;
                color: #f0f8ff !important;
            }
            
            .card {
                background-color: rgba(0, 0, 0, 0.7) !important;
                border: 2px solid #ff00ff !important;
                box-shadow: 0 0 15px #00ffff !important;
            }
            
            .btn-primary {
                background-color: #ff00ff !important;
                border-color: #ff00ff !important;
            }
            
            .btn-secondary {
                background-color: #00ffff !important;
                border-color: #00ffff !important;
                color: #000080 !important;
            }
            
            .navbar {
                background: linear-gradient(90deg, #000080, #800080) !important;
            }
            
            /* Add a notification */
            .secret-theme-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: rgba(0, 0, 0, 0.8);
                color: #ff00ff;
                padding: 15px;
                border-radius: 5px;
                z-index: 9999;
                animation: fadeInOut 5s forwards;
                border: 2px solid #00ffff;
            }
            
            @keyframes fadeInOut {
                0% { opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { opacity: 0; }
            }
        `;
        
        // Check if the secret theme is already active
        if (document.getElementById('secret-theme-style')) {
            // Remove the theme if it's already active
            document.head.removeChild(document.getElementById('secret-theme-style'));
            
            // Show notification
            this.showNotification('Retro Theme Deactivated!');
        } else {
            // Add the style to the head
            document.head.appendChild(style);
            
            // Show notification
            this.showNotification('Secret Retro Theme Activated!');
        }
    }

    showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'secret-theme-notification';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove notification after animation completes
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 5000);
    }
}

// Developer Console Message Easter Egg
class ConsoleMessage {
    constructor() {
        this.init();
    }

    init() {
        // Wait for page to load
        window.addEventListener('load', () => {
            this.showConsoleMessage();
        });
    }

    showConsoleMessage() {
        const styles = [
            'font-size: 20px',
            'font-family: monospace',
            'background: linear-gradient(to right, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8b00ff)',
            '-webkit-background-clip: text',
            'color: transparent',
            'padding: 10px',
        ].join(';');

        console.log('%c👋 Hello curious developer!', styles);
        console.log('%cYou found an Easter egg! Try typing "edgeroute.secretMessage()" below.', 'font-size: 14px; color: #00ff00;');
        
        // Add a secret function to the global scope
        window.edgeroute = {
            secretMessage: function() {
                console.log('%cCongratulations! You\'ve unlocked the secret console message!', 'font-size: 16px; color: #ff00ff;');
                console.log('%cHere\'s a hint for another Easter egg: Try the Konami code (↑↑↓↓←→←→BA) on any page.', 'font-size: 14px; color: #00ffff;');
                return '🎉 Achievement unlocked: Console Explorer!';
            }
        };
    }
}

// Hidden Achievement Easter Egg
class HiddenAchievement {
    constructor() {
        this.achievements = {
            'roadmap-explorer': {
                name: 'Roadmap Explorer',
                description: 'View 5 different roadmaps in a single session',
                count: 0,
                threshold: 5,
                unlocked: false
            },
            'night-owl': {
                name: 'Night Owl',
                description: 'Use the site between 12 AM and 4 AM',
                unlocked: false
            },
            'speed-clicker': {
                name: 'Speed Clicker',
                description: 'Click 50 times in 10 seconds',
                count: 0,
                threshold: 50,
                unlocked: false,
                timeout: null
            }
        };
        
        this.init();
    }

    init() {
        // Track roadmap views
        this.trackRoadmapViews();
        
        // Check if it's night time
        this.checkNightTime();
        
        // Track rapid clicks
        this.trackRapidClicks();
    }

    trackRoadmapViews() {
        // Check if we're on a roadmap page
        if (window.location.pathname.startsWith('/roadmap/') && !window.location.pathname.includes('/create')) {
            const roadmapId = window.location.pathname.split('/')[2];
            
            // Get viewed roadmaps from session storage
            const viewedRoadmaps = JSON.parse(sessionStorage.getItem('viewedRoadmaps') || '[]');
            
            // Add current roadmap if not already viewed
            if (!viewedRoadmaps.includes(roadmapId)) {
                viewedRoadmaps.push(roadmapId);
                sessionStorage.setItem('viewedRoadmaps', JSON.stringify(viewedRoadmaps));
                
                // Update achievement count
                this.achievements['roadmap-explorer'].count = viewedRoadmaps.length;
                
                // Check if achievement unlocked
                if (viewedRoadmaps.length >= this.achievements['roadmap-explorer'].threshold && !this.achievements['roadmap-explorer'].unlocked) {
                    this.achievements['roadmap-explorer'].unlocked = true;
                    this.unlockAchievement('roadmap-explorer');
                }
            }
        }
    }

    checkNightTime() {
        const currentHour = new Date().getHours();
        
        // Check if it's between 12 AM and 4 AM
        if (currentHour >= 0 && currentHour < 4 && !this.achievements['night-owl'].unlocked) {
            this.achievements['night-owl'].unlocked = true;
            this.unlockAchievement('night-owl');
        }
    }

    trackRapidClicks() {
        document.addEventListener('click', () => {
            // Increment click count
            this.achievements['speed-clicker'].count++;
            
            // Reset timeout if it exists
            if (this.achievements['speed-clicker'].timeout) {
                clearTimeout(this.achievements['speed-clicker'].timeout);
            }
            
            // Set timeout to reset click count after 10 seconds
            this.achievements['speed-clicker'].timeout = setTimeout(() => {
                this.achievements['speed-clicker'].count = 0;
            }, 10000);
            
            // Check if achievement unlocked
            if (this.achievements['speed-clicker'].count >= this.achievements['speed-clicker'].threshold && !this.achievements['speed-clicker'].unlocked) {
                this.achievements['speed-clicker'].unlocked = true;
                this.unlockAchievement('speed-clicker');
            }
        });
    }

    unlockAchievement(achievementId) {
        const achievement = this.achievements[achievementId];
        
        console.log(`🏆 Achievement unlocked: ${achievement.name}`);
        
        // Create achievement notification
        const notification = document.createElement('div');
        notification.style.position = 'fixed';
        notification.style.bottom = '20px';
        notification.style.right = '20px';
        notification.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        notification.style.color = '#ffd700';
        notification.style.padding = '15px';
        notification.style.borderRadius = '5px';
        notification.style.zIndex = '9999';
        notification.style.maxWidth = '300px';
        notification.style.boxShadow = '0 0 10px #ffd700';
        notification.style.border = '2px solid #ffd700';
        notification.style.animation = 'fadeInOut 5s forwards';
        
        // Add achievement content
        notification.innerHTML = `
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 10px;">🏆</div>
                <div>
                    <h3 style="margin: 0; color: #ffd700;">Achievement Unlocked!</h3>
                    <h4 style="margin: 5px 0; color: #fff;">${achievement.name}</h4>
                    <p style="margin: 0; font-size: 0.9rem; color: #ccc;">${achievement.description}</p>
                </div>
            </div>
        `;
        
        // Add animation style
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeInOut {
                0% { opacity: 0; transform: translateY(20px); }
                10% { opacity: 1; transform: translateY(0); }
                90% { opacity: 1; transform: translateY(0); }
                100% { opacity: 0; transform: translateY(20px); }
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(notification);
        
        // Remove notification after animation completes
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 5000);
        
        // Store unlocked achievements in local storage
        const unlockedAchievements = JSON.parse(localStorage.getItem('unlockedAchievements') || '[]');
        if (!unlockedAchievements.includes(achievementId)) {
            unlockedAchievements.push(achievementId);
            localStorage.setItem('unlockedAchievements', JSON.stringify(unlockedAchievements));
        }
    }
}

// Initialize all Easter eggs
document.addEventListener('DOMContentLoaded', () => {
    new KonamiCode();
    new SecretTheme();
    new ConsoleMessage();
    new HiddenAchievement();
    
    // Add secret admin panel Easter egg
    if (window.location.pathname === '/admin-panel-314159') {
        showSecretAdminPanel();
    }
});

// Secret Admin Panel Easter Egg
function showSecretAdminPanel() {
    // Replace the content of the page
    document.body.innerHTML = `
        <div style="padding: 20px; font-family: monospace; background-color: #000; color: #0f0; min-height: 100vh;">
            <h1 style="color: #0f0; text-align: center;">Secret Admin Panel</h1>
            <p style="text-align: center;">You've discovered the secret admin panel! This is just for fun.</p>
            
            <div style="margin: 20px 0; padding: 10px; border: 1px solid #0f0;">
                <h2>System Status</h2>
                <p>Server Status: <span style="color: #0f0;">ONLINE</span></p>
                <p>Database Status: <span style="color: #0f0;">CONNECTED</span></p>
                <p>Active Users: <span id="active-users">42</span></p>
                <p>Server Load: <span id="server-load">12%</span></p>
            </div>
            
            <div style="margin: 20px 0; padding: 10px; border: 1px solid #0f0;">
                <h2>Secret Controls</h2>
                <button onclick="alert('Just kidding! This button doesn\\'t actually do anything.')" style="background-color: #000; color: #0f0; border: 1px solid #0f0; padding: 5px 10px; margin: 5px; cursor: pointer;">Deploy Skynet</button>
                <button onclick="alert('This is just an Easter egg, not a real admin panel.')" style="background-color: #000; color: #0f0; border: 1px solid #0f0; padding: 5px 10px; margin: 5px; cursor: pointer;">Launch Missiles</button>
                <button onclick="window.location.href = '/';" style="background-color: #000; color: #0f0; border: 1px solid #0f0; padding: 5px 10px; margin: 5px; cursor: pointer;">Return to Site</button>
            </div>
            
            <div style="margin: 20px 0; padding: 10px; border: 1px solid #0f0;">
                <h2>Easter Egg Guide</h2>
                <p>Congratulations on finding this Easter egg! Here are all the Easter eggs in the site:</p>
                <ul>
                    <li>Konami Code: Press ↑↑↓↓←→←→BA on any page</li>
                    <li>Secret Theme: Click logo, logo, profile, logo in sequence</li>
                    <li>Console Message: Open browser console (F12)</li>
                    <li>Hidden Achievements: Various actions unlock achievements</li>
                    <li>Secret Admin Panel: Visit /admin-panel-314159</li>
                </ul>
            </div>
            
            <p style="text-align: center; margin-top: 40px;">This page is an Easter egg. <a href="/" style="color: #0f0;">Return to EdgeRoute</a></p>
        </div>
    `;
    
    // Add some fake activity
    setInterval(() => {
        document.getElementById('active-users').textContent = Math.floor(Math.random() * 100) + 1;
        document.getElementById('server-load').textContent = Math.floor(Math.random() * 30) + 5 + '%';
    }, 3000);
}
