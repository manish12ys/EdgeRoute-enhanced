// Enhanced Completion Animations

// Main class to handle all completion animations
class CompletionAnimations {
    constructor() {
        this.confettiColors = [
            '#ff4545', '#00ff99', '#006aff', '#ff0095', '#ffbe0b',
            '#38b000', '#4361ee', '#ff5c8d', '#7209b7', '#3a0ca3'
        ];
        this.confettiCount = 200;
        this.fireworkCount = 8;
        this.particleCount = 40;
        this.milestones = [25, 50, 75, 100]; // Percentage milestones
        this.lastMilestone = 0;
        this.confettiContainer = null;
        this.setupConfettiContainer();
        this.setupKeyframes();
    }

    // Set up the confetti container
    setupConfettiContainer() {
        // Create container if it doesn't exist
        if (!document.querySelector('.confetti-container')) {
            this.confettiContainer = document.createElement('div');
            this.confettiContainer.className = 'confetti-container';
            document.body.appendChild(this.confettiContainer);
        } else {
            this.confettiContainer = document.querySelector('.confetti-container');
        }
    }

    // Set up all animation keyframes
    setupKeyframes() {
        if (!document.getElementById('animation-keyframes')) {
            const style = document.createElement('style');
            style.id = 'animation-keyframes';
            style.textContent = `
                @keyframes fall {
                    0% {
                        top: -20px;
                        transform: rotate(0deg) translateX(0);
                    }
                    25% {
                        transform: rotate(45deg) translateX(30px);
                    }
                    50% {
                        transform: rotate(90deg) translateX(-30px);
                    }
                    75% {
                        transform: rotate(135deg) translateX(30px);
                    }
                    100% {
                        top: 100vh;
                        transform: rotate(180deg) translateX(0);
                        opacity: 0;
                    }
                }

                @keyframes sway {
                    0% {
                        transform: translateX(-15px) rotateZ(-10deg);
                    }
                    50% {
                        transform: translateX(15px) rotateZ(10deg);
                    }
                    100% {
                        transform: translateX(-15px) rotateZ(-10deg);
                    }
                }

                @keyframes particle-explosion {
                    0% {
                        opacity: 1;
                        transform: translate(0, 0) scale(0);
                    }
                    50% {
                        opacity: 1;
                    }
                    100% {
                        opacity: 0;
                        transform: translate(var(--end-x), var(--end-y)) scale(1);
                    }
                }

                @keyframes particle-fade {
                    0% {
                        opacity: 1;
                        transform: translate(0, 0) scale(1);
                    }
                    100% {
                        opacity: 0;
                        transform: translate(var(--end-x), var(--end-y)) scale(0);
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // Create and animate confetti
    createConfetti() {
        // Clear any existing confetti
        this.confettiContainer.innerHTML = '';

        for (let i = 0; i < this.confettiCount; i++) {
            const confetti = document.createElement('div');

            // Random shape
            const shapeRandom = Math.random();
            if (shapeRandom < 0.33) {
                confetti.className = 'confetti star';
            } else if (shapeRandom < 0.66) {
                confetti.className = 'confetti circle';
            } else {
                confetti.className = 'confetti square';
            }

            // Random properties
            const size = Math.random() * 15 + 8;
            const color = this.confettiColors[Math.floor(Math.random() * this.confettiColors.length)];
            const left = Math.random() * 100;
            const animationDuration = Math.random() * 4 + 3;
            const delay = Math.random() * 2;
            const swayDuration = Math.random() * 3 + 2;
            const opacity = Math.random() * 0.4 + 0.6;

            // Apply styles
            confetti.style.width = `${size}px`;
            confetti.style.height = `${size}px`;
            confetti.style.backgroundColor = color;
            confetti.style.left = `${left}%`;
            confetti.style.top = '-20px';
            confetti.style.opacity = opacity.toString();
            confetti.style.transform = `rotate(${Math.random() * 360}deg)`;

            // Animation
            confetti.style.animation = `
                fall ${animationDuration}s cubic-bezier(0.25, 0.46, 0.45, 0.94) ${delay}s forwards,
                sway ${swayDuration}s ease-in-out ${delay}s infinite
            `;

            // Add to container
            this.confettiContainer.appendChild(confetti);
        }

        // Clean up after animation completes
        setTimeout(() => {
            this.confettiContainer.innerHTML = '';
        }, 8000);
    }

    // Create particle explosion effect
    createParticleExplosion(node) {
        const rect = node.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const particleContainer = document.createElement('div');
        particleContainer.style.position = 'fixed';
        particleContainer.style.left = '0';
        particleContainer.style.top = '0';
        particleContainer.style.width = '100%';
        particleContainer.style.height = '100%';
        particleContainer.style.pointerEvents = 'none';
        particleContainer.style.zIndex = '9998';
        document.body.appendChild(particleContainer);

        // Create particles
        for (let i = 0; i < this.particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'completion-particle';

            // Random properties
            const size = Math.random() * 8 + 4;
            const color = this.confettiColors[Math.floor(Math.random() * this.confettiColors.length)];
            const angle = Math.random() * Math.PI * 2; // Random angle in radians
            const distance = Math.random() * 150 + 50;
            const duration = Math.random() * 1 + 0.5;
            const delay = Math.random() * 0.3;

            // Calculate end position
            const endX = distance * Math.cos(angle);
            const endY = distance * Math.sin(angle);

            // Apply styles
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.backgroundColor = color;
            particle.style.boxShadow = `0 0 ${size * 2}px ${color}`;
            particle.style.left = `${centerX}px`;
            particle.style.top = `${centerY}px`;
            particle.style.opacity = '1';
            particle.style.setProperty('--end-x', `${endX}px`);
            particle.style.setProperty('--end-y', `${endY}px`);
            particle.style.animation = `particle-explosion ${duration}s cubic-bezier(0.165, 0.84, 0.44, 1) ${delay}s forwards`;

            particleContainer.appendChild(particle);
        }

        // Remove container after animation
        setTimeout(() => {
            document.body.removeChild(particleContainer);
        }, 2000);
    }

    // Create enhanced firework effect
    createFireworks(node) {
        const rect = node.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < this.fireworkCount; i++) {
            setTimeout(() => {
                this.createFirework(centerX, centerY);
            }, i * 200);
        }
    }

    // Create a single enhanced firework
    createFirework(x, y) {
        const fireworkContainer = document.createElement('div');
        fireworkContainer.style.position = 'fixed';
        fireworkContainer.style.left = '0';
        fireworkContainer.style.top = '0';
        fireworkContainer.style.width = '100%';
        fireworkContainer.style.height = '100%';
        fireworkContainer.style.pointerEvents = 'none';
        fireworkContainer.style.zIndex = '9998';
        document.body.appendChild(fireworkContainer);

        const particleCount = 40;
        const colors = this.confettiColors;

        // Create the main firework dot
        const mainDot = document.createElement('div');
        mainDot.style.position = 'absolute';
        mainDot.style.width = '8px';
        mainDot.style.height = '8px';
        mainDot.style.borderRadius = '50%';
        mainDot.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        mainDot.style.boxShadow = `0 0 20px 10px ${mainDot.style.backgroundColor}`;
        mainDot.style.left = `${x}px`;
        mainDot.style.top = `${y}px`;
        mainDot.style.opacity = '1';
        mainDot.style.transition = 'all 0.3s ease-out';
        fireworkContainer.appendChild(mainDot);

        // Animate main dot explosion
        setTimeout(() => {
            mainDot.style.opacity = '0';
            mainDot.style.transform = 'scale(3)';

            // Create particles
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'firework';

                const angle = (i / particleCount) * 360;
                const color = colors[Math.floor(Math.random() * colors.length)];
                const size = Math.random() * 4 + 3;
                const distance = 80 + Math.random() * 80;
                const duration = Math.random() * 0.8 + 0.6;

                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${x}px`;
                particle.style.top = `${y}px`;
                particle.style.backgroundColor = color;
                particle.style.boxShadow = `0 0 ${size * 2}px ${color}`;

                // Calculate end position
                const endX = distance * Math.cos(angle * Math.PI / 180);
                const endY = distance * Math.sin(angle * Math.PI / 180);

                particle.style.setProperty('--end-x', `${endX}px`);
                particle.style.setProperty('--end-y', `${endY}px`);
                particle.style.animation = `particle-explosion ${duration}s cubic-bezier(0.165, 0.84, 0.44, 1) forwards`;

                fireworkContainer.appendChild(particle);
            }
        }, 50);

        // Remove container after animation
        setTimeout(() => {
            document.body.removeChild(fireworkContainer);
        }, 1500);
    }

    // Show enhanced celebration modal
    showCelebrationModal(title, message) {
        // Create modal if it doesn't exist
        let modal = document.querySelector('.celebration-modal');

        if (!modal) {
            modal = document.createElement('div');
            modal.className = 'celebration-modal';
            modal.innerHTML = `
                <div class="icon"><i class="fas fa-trophy"></i></div>
                <h2></h2>
                <p></p>
                <button class="btn-continue">Continue Learning</button>
            `;
            document.body.appendChild(modal);

            // Add event listener to close button
            modal.querySelector('.btn-continue').addEventListener('click', () => {
                modal.classList.remove('show');
            });
        }

        // Update content
        modal.querySelector('h2').textContent = title;
        modal.querySelector('p').textContent = message;

        // Show modal
        modal.classList.add('show');

        // Auto-hide after 8 seconds
        setTimeout(() => {
            if (modal.classList.contains('show')) {
                modal.classList.remove('show');
            }
        }, 8000);
    }

    // Show enhanced milestone toast notification
    showMilestoneToast(percentage) {
        // Find the milestone that was reached
        const milestone = this.milestones.find(m =>
            percentage >= m && this.lastMilestone < m
        );

        if (!milestone) return;

        // Note: lastMilestone is now updated in checkAndCelebrateMilestone

        // Create toast if it doesn't exist
        let toast = document.querySelector('.milestone-toast');

        if (!toast) {
            toast = document.createElement('div');
            toast.className = 'milestone-toast';
            toast.innerHTML = `
                <div class="d-flex align-items-center">
                    <div class="milestone-icon"><i class="fas fa-medal"></i></div>
                    <div>
                        <div class="milestone-title"></div>
                        <div class="milestone-message"></div>
                    </div>
                </div>
            `;
            document.body.appendChild(toast);
        }

        // Update content and icon based on milestone
        let icon = 'medal';
        let message = 'You\'re making great progress on this roadmap!';

        if (milestone === 25) {
            icon = 'star';
            message = 'You\'ve completed 25% of this roadmap. Keep going!';
        } else if (milestone === 50) {
            icon = 'award';
            message = 'Halfway there! You\'ve completed 50% of this roadmap.';
        } else if (milestone === 75) {
            icon = 'crown';
            message = 'Almost there! Just 25% more to complete this roadmap.';
        } else if (milestone === 100) {
            icon = 'trophy';
            message = 'Congratulations! You\'ve completed the entire roadmap!';
        }

        toast.querySelector('.milestone-icon i').className = `fas fa-${icon}`;
        toast.querySelector('.milestone-title').textContent = `${milestone}% Milestone Reached!`;
        toast.querySelector('.milestone-message').textContent = message;

        // Show toast
        toast.classList.add('show');

        // Auto-hide after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 5000);
    }

    // Celebrate node completion with enhanced effects
    celebrateNodeCompletion(node) {
        // Create particle explosion
        this.createParticleExplosion(node);

        // Create fireworks with slight delay
        setTimeout(() => {
            this.createFireworks(node);
        }, 300);

        // Add glow effect (CSS animation is applied via the node-completed class)
    }

    // Celebrate roadmap completion with enhanced effects
    celebrateRoadmapCompletion() {
        // Show confetti
        this.createConfetti();

        // Show celebration modal with slight delay
        setTimeout(() => {
            this.showCelebrationModal(
                'Roadmap Completed!',
                'Congratulations! You\'ve mastered all topics in this roadmap. Your dedication to learning is impressive!'
            );
        }, 500);
    }

    // Check for milestone and celebrate if needed
    checkAndCelebrateMilestone(percentage) {
        // Find the highest milestone that was reached
        const milestone = this.milestones.find(m =>
            percentage >= m && this.lastMilestone < m
        );

        if (milestone) {
            console.log(`Milestone reached: ${milestone}%`);
            this.showMilestoneToast(percentage);
            this.lastMilestone = milestone;

            // If 100% completed, celebrate roadmap completion
            if (milestone === 100) {
                this.celebrateRoadmapCompletion();
            }
        }
    }
}

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Create global instance
    if (!window.completionAnimations) {
        console.log('Initializing CompletionAnimations');
        window.completionAnimations = new CompletionAnimations();
    } else {
        console.log('CompletionAnimations already initialized');
    }
});

// Fallback initialization in case DOMContentLoaded already fired
if (document.readyState === 'complete' && !window.completionAnimations) {
    console.log('Fallback initialization of CompletionAnimations');
    window.completionAnimations = new CompletionAnimations();
}
