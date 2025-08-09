import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// Axios global config for session auth + CSRF
axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// Preload CSRF cookie (safe GET)
axios.get('/api/accounts/csrf/').catch(() => {})

// Redirect to login on auth errors
axios.interceptors.response.use(
	(res) => res,
	(err) => {
		const status = err?.response?.status
		const detail = err?.response?.data?.detail
		if (status === 401 || (status === 403 && detail === 'Authentication credentials were not provided.')) {
			// Optional: keep return path
			const current = window.location.pathname
			if (!current.startsWith('/login')) {
				router.push({ name: 'login', query: { next: current } })
			}
		}
		return Promise.reject(err)
	}
)
