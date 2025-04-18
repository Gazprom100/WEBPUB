<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="glitch-text">Next Generation<br/>Social Media Management</h1>
        <p class="hero-subtitle">Streamline your content, amplify your reach, and grow your audience with AI-powered tools</p>
        <div class="cta-buttons">
          <router-link to="/signup" class="btn btn-primary">Get Started Free</router-link>
          <a href="#features" class="btn btn-outline">See How It Works</a>
        </div>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-number">10K+</span>
            <span class="stat-label">Active Users</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">5M+</span>
            <span class="stat-label">Posts Published</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">98%</span>
            <span class="stat-label">Satisfaction Rate</span>
          </div>
        </div>
      </div>
      <div class="hero-visual">
        <div class="floating-elements">
          <div class="element element-1"></div>
          <div class="element element-2"></div>
          <div class="element element-3"></div>
        </div>
        <div class="hero-image">
          <img src="@/assets/dashboard-preview.png" alt="Dashboard Preview" />
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features">
      <h2>Powerful Features for Modern Content Creators</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-robot"></i>
          </div>
          <h3>AI-Powered Analytics</h3>
          <p>Get deep insights into your content performance with advanced AI analytics</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-calendar-alt"></i>
          </div>
          <h3>Smart Scheduling</h3>
          <p>Schedule your content at optimal times for maximum engagement</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-chart-line"></i>
          </div>
          <h3>Growth Tracking</h3>
          <p>Monitor your audience growth and engagement metrics in real-time</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-magic"></i>
          </div>
          <h3>Auto-Optimization</h3>
          <p>Automatically optimize your content for better performance</p>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works">
      <div class="section-content">
        <h2>How It Works</h2>
        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>Connect Your Accounts</h3>
            <p>Easily connect all your social media accounts in one place</p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>Create & Schedule</h3>
            <p>Create engaging content and schedule it for optimal times</p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>Analyze & Optimize</h3>
            <p>Get insights and optimize your content strategy</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>Ready to Transform Your Social Media Presence?</h2>
        <p>Join thousands of content creators who are already growing their audience</p>
        <router-link to="/signup" class="btn btn-primary">Start Your Free Trial</router-link>
      </div>
      <div class="cta-background"></div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

const handleMouseMove = (e) => {
  const cards = document.querySelectorAll('.feature-card')
  cards.forEach(card => {
    const rect = card.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width) * 100
    const y = ((e.clientY - rect.top) / rect.height) * 100
    card.style.setProperty('--mouse-x', `${x}%`)
    card.style.setProperty('--mouse-y', `${y}%`)
  })
}

onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
})
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
  overflow: hidden;
}

/* Hero Section */
.hero {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  padding: 4rem;
  position: relative;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(56, 189, 248, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.hero::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    linear-gradient(90deg, rgba(99, 102, 241, 0.05) 1px, transparent 1px),
    linear-gradient(0deg, rgba(99, 102, 241, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
  mask-image: radial-gradient(circle at center, transparent 30%, black 70%);
  pointer-events: none;
}

.hero-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 2rem;
  z-index: 1;
}

.glitch-text {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.1;
  background: linear-gradient(135deg, #60a5fa 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  animation: glitch 5s infinite;
  text-shadow: 
    2px 2px 10px rgba(96, 165, 250, 0.2),
    -2px -2px 10px rgba(99, 102, 241, 0.2);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #94a3b8;
  max-width: 600px;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.125rem;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  color: white;
  border: none;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
}

.btn-outline {
  border: 2px solid rgba(99, 102, 241, 0.5);
  color: white;
  background: transparent;
}

.btn-outline:hover {
  background: rgba(99, 102, 241, 0.1);
  border-color: #6366f1;
}

.hero-stats {
  display: flex;
  gap: 3rem;
  margin-top: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #60a5fa 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
}

.stat-number::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, currentColor, transparent);
  opacity: 0.3;
}

.stat-label {
  color: #94a3b8;
  font-size: 1rem;
}

.hero-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.element {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
}

.element-1 {
  width: 300px;
  height: 300px;
  background: rgba(59, 130, 246, 0.2);
  top: 10%;
  left: 20%;
  animation: float 8s infinite;
}

.element-2 {
  width: 200px;
  height: 200px;
  background: rgba(99, 102, 241, 0.2);
  bottom: 20%;
  right: 10%;
  animation: float 6s infinite reverse;
}

.element-3 {
  width: 150px;
  height: 150px;
  background: rgba(56, 189, 248, 0.2);
  top: 50%;
  left: 50%;
  animation: float 10s infinite;
}

.hero-image {
  width: 100%;
  max-width: 800px;
  position: relative;
  z-index: 1;
  animation: levitate 4s ease-in-out infinite;
}

.hero-image img {
  width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.hero-image::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(99, 102, 241, 0.1) 0%,
    rgba(96, 165, 250, 0.1) 100%
  );
  border-radius: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.hero-image:hover::after {
  opacity: 1;
}

/* Features Section */
.features {
  padding: 8rem 4rem;
  background: rgba(15, 23, 42, 0.8);
  position: relative;
}

.features h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 4rem;
  background: linear-gradient(135deg, #60a5fa 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.feature-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  padding: 2rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
    rgba(99, 102, 241, 0.1) 0%,
    transparent 50%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-icon {
  position: relative;
}

.feature-icon::after {
  content: '';
  position: absolute;
  width: 30px;
  height: 30px;
  background: radial-gradient(circle, rgba(96, 165, 250, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(2);
    opacity: 0;
  }
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: white;
}

.feature-card p {
  color: #94a3b8;
  line-height: 1.6;
}

/* How It Works Section */
.how-it-works {
  padding: 8rem 4rem;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
}

.section-content {
  max-width: 1200px;
  margin: 0 auto;
}

.how-it-works h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 4rem;
  background: linear-gradient(135deg, #60a5fa 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
}

.step {
  text-align: center;
  position: relative;
}

.step-number {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 auto 1.5rem;
}

.step-number::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: inherit;
  border-radius: 50%;
  filter: blur(10px);
  opacity: 0.5;
  z-index: -1;
}

.step h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: white;
}

.step p {
  color: #94a3b8;
  line-height: 1.6;
}

/* CTA Section */
.cta-section {
  padding: 6rem 4rem;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 1;
}

.cta-content h2 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #60a5fa 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.cta-content p {
  color: #94a3b8;
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

.cta-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(56, 189, 248, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(99, 102, 241, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.cta-section::before {
  content: '';
  position: absolute;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.2) 0%, transparent 70%);
  top: 0;
  right: 0;
  transform: translate(30%, -30%);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes levitate {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes glitch {
  0%, 100% {
    transform: none;
    opacity: 1;
  }
  7% {
    transform: skew(-0.5deg, -0.9deg);
    opacity: 0.75;
  }
  10% {
    transform: none;
    opacity: 1;
  }
  27% {
    transform: none;
    opacity: 1;
  }
  30% {
    transform: skew(0.8deg, -0.1deg);
    opacity: 0.75;
  }
  35% {
    transform: none;
    opacity: 1;
  }
}

@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 2rem;
  }

  .hero-content {
    align-items: center;
  }

  .hero-stats {
    justify-content: center;
  }

  .glitch-text {
    font-size: 3rem;
  }

  .features,
  .how-it-works,
  .cta-section {
    padding: 4rem 2rem;
  }
}

@media (max-width: 640px) {
  .glitch-text {
    font-size: 2.5rem;
  }

  .cta-buttons {
    flex-direction: column;
    width: 100%;
  }

  .hero-stats {
    flex-direction: column;
    gap: 2rem;
  }

  .features h2,
  .how-it-works h2,
  .cta-content h2 {
    font-size: 2rem;
  }
}
</style> 