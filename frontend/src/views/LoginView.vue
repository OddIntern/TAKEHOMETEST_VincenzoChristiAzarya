<template>
  <div class="flex items-center justify-center min-h-screen bg-slate-900">
    <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-2xl shadow-2xl">
      <div class="text-center">
        <h1 class="text-3xl font-extrabold text-gray-900">Flow</h1>
        <p class="text-gray-500 mt-2">{{ isRegister ? 'Create an account' : 'A Simple Task Management App' }}</p>
      </div>
      
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Username</label>
          <input v-model="username" type="text" required class="w-full p-3 mt-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="Enter username" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">Password</label>
          <input v-model="password" type="password" required class="w-full p-3 mt-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="Enter password" />
        </div>
        
        <div v-if="error" class="p-3 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100 text-center font-medium">
            {{ error }}
        </div>

        <button type="submit" class="w-full py-3 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-lg">
          {{ isRegister ? 'Sign Up' : 'Login' }}
        </button>
      </form>

      <div class="text-center">
        <button @click="toggleMode" class="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors">
            {{ isRegister ? 'Already have an account? Login' : 'Need an account? Register' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useTaskStore } from '../stores/taskStore'
import { useRouter } from 'vue-router'
import axios from 'axios'

const username = ref('')
const password = ref('')
const isRegister = ref(false)
const error = ref('')
const store = useTaskStore()
const router = useRouter()

const toggleMode = () => {
    isRegister.value = !isRegister.value
    error.value = ''
    username.value = ''
    password.value = ''
}

const handleSubmit = async () => {
    error.value = ''
    if (isRegister.value) {
        // Handle Register
        try {
            await axios.post('http://127.0.0.1:5000/auth/register', {
                username: username.value,
                password: password.value
            })
            // Auto login after register
            await performLogin()
        } catch (e) {
            error.value = e.response?.data?.message || 'Registration failed'
        }
    } else {
        // Handle Login
        await performLogin()
    }
}

const performLogin = async () => {
    const success = await store.login(username.value, password.value)
    if (success) {
        router.push('/board')
    } else {
        error.value = 'Invalid username or password'
    }
}
</script>