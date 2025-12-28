import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000'

export const useTaskStore = defineStore('taskStore', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user')) || null, 
    tasks: [],
    teamMembers: JSON.parse(localStorage.getItem('teamMembers')) || [
        { id: 'u1', name: 'Alex', initials: 'AL', color: 'bg-indigo-500' },
        { id: 'u2', name: 'Sam', initials: 'SA', color: 'bg-emerald-500' },
        { id: 'u3', name: 'Jordan', initials: 'JO', color: 'bg-amber-500' },
        { id: 'u4', name: 'Taylor', initials: 'TA', color: 'bg-rose-500' },
    ]
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    columns: (state) => {
      const cols = { 'To Do': [], 'In Progress': [], 'Done': [] }
      const sorted = [...state.tasks].sort((a, b) => (a.position || 0) - (b.position || 0))
      
      sorted.forEach(task => {
        let status = task.status
        if (status === 'backlog') status = 'To Do'
        if (status === 'progress') status = 'In Progress'
        if (status === 'review') status = 'In Progress' 
        if (status === 'done') status = 'Done'

        if (cols[status]) {
            cols[status].push(task)
        } else {
            cols['To Do'].push(task)
        }
      })
      return cols
    }
  },

  actions: {
    getAuthHeader() {
        return { Authorization: `Bearer ${this.token}` }
    },

    async login(username, password) {
      try {
        const res = await axios.post(`${API_URL}/auth/login`, { username, password })
        this.token = res.data.token
        this.user = res.data.user
        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))
        return true
      } catch (e) {
        console.error("Login failed", e)
        return false
      }
    },

    logout() {
        this.token = ''
        this.user = null
        this.tasks = []
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login'
    },

    async fetchTasks() {
      if (!this.token) return
      try {
        const res = await axios.get(`${API_URL}/tasks`, { headers: this.getAuthHeader() })
        this.tasks = res.data
      } catch (e) {
        console.error("Fetch failed:", e)
        if (e.response && e.response.status === 401) {
            this.logout()
        }
      }
    },

    async createTask(taskData) {
      try {
        const res = await axios.post(`${API_URL}/tasks`, taskData, { headers: this.getAuthHeader() })
        this.tasks.push(res.data)
      } catch (e) { console.error("Create failed", e) }
    },

    async updateTask(taskData) {
        try {
          const res = await axios.put(`${API_URL}/tasks/${taskData.id}`, taskData, { headers: this.getAuthHeader() })
          const index = this.tasks.findIndex(t => t.id === taskData.id)
          if (index !== -1) this.tasks[index] = res.data
        } catch (e) { console.error("Update failed", e) }
    },
      
    async duplicateTask(taskId) {
        try {
          const res = await axios.post(`${API_URL}/tasks/${taskId}/duplicate`, {}, { headers: this.getAuthHeader() })
          this.tasks.push(res.data)
        } catch (e) { console.error("Duplicate failed", e) }
    },
      
    async deleteTask(taskId) {
        try {
          await axios.delete(`${API_URL}/tasks/${taskId}`, { headers: this.getAuthHeader() })
          this.tasks = this.tasks.filter(t => t.id !== taskId)
        } catch (e) { console.error("Delete failed", e) }
    },

    async moveTask(taskId, newStatus, newIndex, newOrderIds) {
        const task = this.tasks.find(t => t.id === taskId)
        if (task) task.status = newStatus
        
        try {
            await axios.patch(`${API_URL}/tasks/reorder`, {
                status: newStatus, task_ids: newOrderIds
            }, { headers: this.getAuthHeader() })
        } catch (e) { console.error("Reorder failed", e) }
    },

    addTeamMember(name) {
        const initials = name.substring(0, 2).toUpperCase()
        const colors = ['bg-pink-500', 'bg-cyan-500', 'bg-orange-500', 'bg-lime-500', 'bg-fuchsia-500']
        const color = colors[Math.floor(Math.random() * colors.length)]
        const newMember = { id: `u${Date.now()}`, name, initials, color }
        this.teamMembers.push(newMember)
        localStorage.setItem('teamMembers', JSON.stringify(this.teamMembers))
    },

    async updateBoardTitle(newTitle) {
        if (this.user) {
            this.user.board_title = newTitle
            localStorage.setItem('user', JSON.stringify(this.user))
        }

        try {
            const res = await axios.put(`${API_URL}/auth/board-title`, { title: newTitle }, { headers: this.getAuthHeader() })
            
            // sync with backend
            if (res.data.user) {
                this.user = res.data.user
                localStorage.setItem('user', JSON.stringify(this.user))
            }
            return true
        } catch (e) {
            console.error("Failed to update title", e)
            return false
        }
    }
  }
})