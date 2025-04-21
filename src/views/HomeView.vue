<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Управление социальными сетями нового поколения</h1>
        <p class="hero-subtitle">
          Используйте мощные инструменты с ИИ для оптимизации вашего контента, 
          отслеживания аудитории и повышения вовлеченности на всех платформах.
        </p>
        <div class="hero-cta">
          <router-link to="/signup" class="btn btn-primary">Начать бесплатно</router-link>
          <router-link to="/login" class="btn btn-outline">Войти</router-link>
        </div>
      </div>
      <div class="hero-image">
        <img src="@/assets/dashboard-preview.svg" alt="Дашборд WEBPUB" class="dashboard-preview" />
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="stat-card">
        <h3>10M+</h3>
        <p>Постов создано</p>
      </div>
      <div class="stat-card">
        <h3>500K+</h3>
        <p>Активных пользователей</p>
      </div>
      <div class="stat-card">
        <h3>3X</h3>
        <p>Рост вовлеченности</p>
      </div>
      <div class="stat-card">
        <h3>98%</h3>
        <p>Удовлетворенность</p>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <h2 class="section-title">Функции, разработанные для роста</h2>
      <div class="features-grid">
        <div class="feature-card" @mousemove="handleMouseMove" ref="featureCard1">
          <div class="feature-icon">
            <i class="fas fa-chart-line"></i>
          </div>
          <h3>Аналитика на основе ИИ</h3>
          <p>
            Получите глубокое понимание вашей аудитории с аналитикой,
            управляемой искусственным интеллектом, которая раскрывает скрытые тенденции и возможности.
          </p>
        </div>
        <div class="feature-card" @mousemove="handleMouseMove" ref="featureCard2">
          <div class="feature-icon">
            <i class="fas fa-calendar-check"></i>
          </div>
          <h3>Умное планирование</h3>
          <p>
            Используйте алгоритм, который автоматически определяет оптимальное время для публикации,
            повышая охват и вовлеченность.
          </p>
        </div>
        <div class="feature-card" @mousemove="handleMouseMove" ref="featureCard3">
          <div class="feature-icon">
            <i class="fas fa-users"></i>
          </div>
          <h3>Отслеживание роста</h3>
          <p>
            Следите за своим ростом во времени с помощью подробных отчетов и статистики,
            которые помогают вам понять, что работает, а что нет.
          </p>
        </div>
        <div class="feature-card" @mousemove="handleMouseMove" ref="featureCard4">
          <div class="feature-icon">
            <i class="fas fa-magic"></i>
          </div>
          <h3>Автооптимизация</h3>
          <p>
            Позвольте нашим инструментам автоматически оптимизировать ваш контент
            для максимальной производительности на основе анализа исторических данных.
          </p>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works-section">
      <h2 class="section-title">Как это работает</h2>
      <div class="steps-container">
        <div class="step">
          <div class="step-number">1</div>
          <h3>Подключите свои аккаунты</h3>
          <p>
            Легко интегрируйтесь со всеми своими социальными платформами
            через нашу безопасную систему единого входа.
          </p>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <h3>Создавайте и планируйте</h3>
          <p>
            Создавайте увлекательный контент и планируйте его заранее
            с нашими инструментами на основе ИИ для повышения эффективности.
          </p>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <h3>Анализируйте и оптимизируйте</h3>
          <p>
            Отслеживайте производительность, выявляйте паттерны и
            постоянно улучшайте свою стратегию в социальных сетях.
          </p>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <h2>Преобразите свое присутствие в социальных сетях уже сегодня</h2>
      <p>
        Присоединяйтесь к тысячам создателей контента, которые уже пользуются
        преимуществами нашей платформы управления социальными сетями.
      </p>
      <router-link to="/signup" class="btn btn-primary">Начать бесплатный период</router-link>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Ссылки на элементы для эффекта парения
const featureCard1 = ref(null);
const featureCard2 = ref(null);
const featureCard3 = ref(null);
const featureCard4 = ref(null);

// Обработчик движения мыши для эффекта наклона карточек
const handleMouseMove = (event) => {
  const card = event.currentTarget;
  const rect = card.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  
  const centerX = rect.width / 2;
  const centerY = rect.height / 2;
  
  const deltaX = (x - centerX) / centerX;
  const deltaY = (y - centerY) / centerY;
  
  card.style.transform = `perspective(1000px) rotateX(${deltaY * 5}deg) rotateY(${-deltaX * 5}deg) scale3d(1.02, 1.02, 1.02)`;
};

// При выходе мыши возвращаем карточку в исходное положение
onMounted(() => {
  const cards = [featureCard1.value, featureCard2.value, featureCard3.value, featureCard4.value];
  
  cards.forEach(card => {
    if (card) {
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
      });
    }
  });
});
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
  overflow: hidden;
}

/* Hero Section */
.hero-section {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  padding: 4rem;
  position: relative;
}

.hero-section::before {
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

.hero-section::after {
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

.hero-title {
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

.hero-cta {
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

.hero-image {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-preview {
  width: 100%;
  max-width: 800px;
  position: relative;
  z-index: 1;
  animation: levitate 4s ease-in-out infinite;
}

.dashboard-preview img {
  width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.dashboard-preview::after {
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

.dashboard-preview:hover::after {
  opacity: 1;
}

/* Stats Section */
.stats-section {
  padding: 8rem 4rem;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
}

.stat-card {
  text-align: center;
  position: relative;
}

.stat-card h3 {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #60a5fa 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-card p {
  color: #94a3b8;
  font-size: 1rem;
}

/* Features Section */
.features-section {
  padding: 8rem 4rem;
  background: rgba(15, 23, 42, 0.8);
  position: relative;
}

.section-title {
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
.how-it-works-section {
  padding: 8rem 4rem;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
}

.steps-container {
  max-width: 1200px;
  margin: 0 auto;
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
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 2rem;
  }

  .hero-content {
    align-items: center;
  }

  .hero-title {
    font-size: 3rem;
  }

  .features-section,
  .how-it-works-section,
  .cta-section {
    padding: 4rem 2rem;
  }
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-cta {
    flex-direction: column;
    width: 100%;
  }

  .section-title {
    font-size: 2rem;
  }
}
</style> 