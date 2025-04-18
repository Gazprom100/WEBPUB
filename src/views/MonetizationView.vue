<template>
  <div class="monetization-view">
    <div class="monetization-header">
      <h1>Monetization</h1>
      <div class="header-actions">
        <button class="btn btn-primary" @click="showWithdrawModal">
          Withdraw Funds
        </button>
      </div>
    </div>

    <!-- Balance Overview -->
    <div class="balance-cards">
      <div class="balance-card">
        <h3>Available Balance</h3>
        <div class="balance-amount">${{ formatNumber(balance.available) }}</div>
        <div class="balance-info">Available for withdrawal</div>
      </div>

      <div class="balance-card">
        <h3>Pending Balance</h3>
        <div class="balance-amount">${{ formatNumber(balance.pending) }}</div>
        <div class="balance-info">Will be available in 7 days</div>
      </div>

      <div class="balance-card">
        <h3>Total Earnings</h3>
        <div class="balance-amount">${{ formatNumber(balance.total) }}</div>
        <div class="balance-info">All time earnings</div>
      </div>
    </div>

    <!-- Revenue Sources -->
    <div class="content-card">
      <h2>Revenue Sources</h2>
      <div class="revenue-chart">
        <!-- Pie chart will go here -->
      </div>
      <div class="revenue-legend">
        <div v-for="source in revenueSources" :key="source.id" class="legend-item">
          <span class="legend-color" :style="{ background: source.color }"></span>
          <span class="legend-label">{{ source.label }}</span>
          <span class="legend-value">${{ formatNumber(source.amount) }}</span>
          <span class="legend-percent">{{ formatPercent(source.percentage) }}%</span>
        </div>
      </div>
    </div>

    <!-- Recent Transactions -->
    <div class="content-card">
      <div class="card-header">
        <h2>Recent Transactions</h2>
        <button class="btn btn-secondary" @click="showAllTransactions">
          View All
        </button>
      </div>

      <table class="transactions-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Channel</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in recentTransactions" :key="transaction.id">
            <td>{{ formatDate(transaction.date) }}</td>
            <td>
              <div class="transaction-description">
                <span class="transaction-type" :class="transaction.type">
                  {{ transaction.type }}
                </span>
                {{ transaction.description }}
              </div>
            </td>
            <td>{{ transaction.channel }}</td>
            <td :class="{ 'amount-positive': transaction.amount > 0 }">
              {{ transaction.amount > 0 ? '+' : '' }}${{ formatNumber(transaction.amount) }}
            </td>
            <td>
              <span class="status-badge" :class="transaction.status">
                {{ transaction.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Withdraw Modal -->
    <div v-if="showingWithdrawModal" class="modal">
      <div class="modal-content">
        <h2>Withdraw Funds</h2>
        
        <div class="form-group">
          <label class="form-label">Amount</label>
          <div class="input-group">
            <span class="input-prefix">$</span>
            <input 
              type="number" 
              v-model="withdrawAmount"
              class="form-input"
              :max="balance.available"
              min="0"
              step="0.01"
            >
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Payment Method</label>
          <select v-model="withdrawMethod" class="form-input">
            <option value="">Select payment method</option>
            <option v-for="method in paymentMethods" :key="method.id" :value="method.id">
              {{ method.name }}
            </option>
          </select>
        </div>

        <div class="modal-actions">
          <button class="btn btn-secondary" @click="showingWithdrawModal = false">
            Cancel
          </button>
          <button class="btn btn-primary" @click="processWithdrawal" :disabled="isProcessing">
            {{ isProcessing ? 'Processing...' : 'Withdraw' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Data
const balance = ref({
  available: 0,
  pending: 0,
  total: 0
})

const revenueSources = ref([
  { id: 1, label: 'Sponsored Posts', amount: 5000, percentage: 45, color: '#4CAF50' },
  { id: 2, label: 'Affiliate Links', amount: 3000, percentage: 27, color: '#2196F3' },
  { id: 3, label: 'Channel Memberships', amount: 2000, percentage: 18, color: '#FFC107' },
  { id: 4, label: 'Tips & Donations', amount: 1000, percentage: 10, color: '#9C27B0' }
])

const recentTransactions = ref([])
const paymentMethods = ref([
  { id: 'bank', name: 'Bank Transfer' },
  { id: 'paypal', name: 'PayPal' },
  { id: 'crypto', name: 'Cryptocurrency' }
])

// UI State
const showingWithdrawModal = ref(false)
const withdrawAmount = ref(0)
const withdrawMethod = ref('')
const isProcessing = ref(false)

// Methods
const formatNumber = (num) => {
  return num.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const formatPercent = (num) => {
  return num.toFixed(1)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const showWithdrawModal = () => {
  withdrawAmount.value = 0
  withdrawMethod.value = ''
  showingWithdrawModal.value = true
}

const showAllTransactions = () => {
  // Navigate to transactions history page
}

const processWithdrawal = async () => {
  if (!withdrawAmount.value || !withdrawMethod.value) return

  isProcessing.value = true
  try {
    await axios.post(`${import.meta.env.VITE_API_URL}/monetization/withdraw`, {
      amount: withdrawAmount.value,
      method: withdrawMethod.value
    })
    // Update balance and close modal
    await fetchBalance()
    showingWithdrawModal.value = false
  } catch (error) {
    console.error('Failed to process withdrawal:', error)
  } finally {
    isProcessing.value = false
  }
}

// Data fetching
const fetchBalance = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/monetization/balance`)
    balance.value = response.data
  } catch (error) {
    console.error('Failed to fetch balance:', error)
  }
}

const fetchTransactions = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/monetization/transactions`)
    recentTransactions.value = response.data
  } catch (error) {
    console.error('Failed to fetch transactions:', error)
  }
}

// Lifecycle
onMounted(() => {
  fetchBalance()
  fetchTransactions()
})
</script>

<style scoped>
.monetization-view {
  padding: 2rem;
}

.monetization-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.balance-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.balance-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.balance-amount {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
  margin: 0.5rem 0;
}

.balance-info {
  font-size: 0.9rem;
  color: var(--text-color);
  opacity: 0.8;
}

.content-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.revenue-chart {
  height: 300px;
  margin: 2rem 0;
  background: var(--background-color);
  border-radius: 4px;
}

.revenue-legend {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-value {
  font-weight: 500;
  margin-left: auto;
}

.legend-percent {
  color: var(--text-color);
  opacity: 0.8;
  width: 50px;
  text-align: right;
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
}

.transactions-table th,
.transactions-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.transaction-description {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.transaction-type {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  text-transform: uppercase;
}

.amount-positive {
  color: #28a745;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.status-badge.completed {
  background: #e8f5e9;
  color: #28a745;
}

.status-badge.pending {
  background: #fff3e0;
  color: #f57c00;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.input-group {
  display: flex;
  align-items: center;
}

.input-prefix {
  background: var(--background-color);
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-right: none;
  border-radius: 4px 0 0 4px;
}

.input-group .form-input {
  border-radius: 0 4px 4px 0;
}
</style> 