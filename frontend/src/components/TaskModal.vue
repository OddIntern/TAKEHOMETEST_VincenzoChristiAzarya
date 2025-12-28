<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black/50 flex justify-center items-center z-50 p-4 backdrop-blur-sm">
    <div class="bg-white rounded-lg shadow-2xl w-full max-w-lg p-6 border border-gray-100 max-h-[90vh] overflow-y-auto flex flex-col">
      
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">{{ isEdit ? 'Edit Task' : 'New Task' }}</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="flex-1 space-y-4">
        <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Title</label>
            <input v-model="form.title" class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none font-medium" placeholder="Task Title" required />
        </div>
        <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Description</label>
            <textarea v-model="form.description" class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none text-sm h-20 resize-none"></textarea>
        </div>

        <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Assign People</label>
            <div class="flex gap-2 flex-wrap items-center">
                <button type="button" v-for="user in store.teamMembers" :key="user.id" 
                    @click="toggleUser(user.id)"
                    :class="form.assignedUserIds.includes(user.id) ? 'bg-blue-50 border-blue-500 text-blue-700 ring-1 ring-blue-500' : 'bg-white border-gray-300 text-gray-600 hover:bg-gray-50'"
                    class="flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-semibold transition-all">
                    <div :class="user.color" class="w-5 h-5 rounded-full text-white flex items-center justify-center text-[9px]">{{ user.initials }}</div>
                    {{ user.name }}
                </button>
                
                <button type="button" @click="addNewPerson" class="flex items-center gap-1 px-3 py-1.5 rounded-full border border-dashed border-gray-300 text-gray-500 hover:text-blue-600 hover:border-blue-400 hover:bg-blue-50 transition-all text-xs font-bold">
                    <span>+</span> Add People
                </button>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Status</label>
                <select v-model="form.status" class="w-full border border-gray-300 rounded-md px-2 py-2 text-sm bg-white">
                    <option value="To Do">To Do</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Done">Done</option>
                </select>
            </div>
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Due Date</label>
                <input type="date" v-model="form.dueDate" class="w-full border border-gray-300 rounded-md px-2 py-2 text-sm" />
            </div>
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Tag</label>
                <select v-model="form.tag" class="w-full border border-gray-300 rounded-md px-2 py-2 text-sm bg-white">
                    <option>Feature</option><option>Bug</option><option>Design</option><option>Planned</option>
                </select>
            </div>
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Urgency</label>
                <select v-model="form.urgency" class="w-full border border-gray-300 rounded-md px-2 py-2 text-sm bg-white">
                    <option value="High">High (Red)</option>
                    <option value="Medium">Medium (Yellow)</option>
                    <option value="Low">Low (Gray)</option>
                </select>
            </div>
        </div>

        <div v-if="isEdit" class="border-t border-gray-100 pt-4 mt-2">
            <h3 class="text-xs font-bold text-gray-500 uppercase mb-2">Activity Log</h3>
            <div class="bg-gray-50 rounded-lg p-3 h-32 overflow-y-auto text-xs space-y-2 border border-gray-200">
                <div v-for="(log, i) in reversedHistory" :key="i" class="flex gap-2">
                    <span class="text-gray-400 min-w-[100px]">{{ new Date(log.date).toLocaleString() }}</span>
                    <span class="text-gray-700 font-medium">{{ log.action }}</span>
                </div>
                <div v-if="!form.history?.length" class="text-gray-400 italic">No history available</div>
            </div>
        </div>

        <div class="flex justify-end gap-3 pt-4 border-t border-gray-100">
            <button type="button" @click="$emit('close')" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-md text-sm">Cancel</button>
            <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 shadow-md text-sm font-medium">
                {{ isEdit ? 'Save Changes' : 'Create Task' }}
            </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, computed } from 'vue'
import { useTaskStore } from '../stores/taskStore'

const props = defineProps(['isOpen', 'task', 'defaultStatus', 'defaultDate'])
const emit = defineEmits(['close', 'save'])
const store = useTaskStore()

const form = reactive({
    id: null, title: '', description: '', status: 'To Do', 
    tag: 'Feature', urgency: 'Low', dueDate: '', assignedUserIds: [], history: []
})

const isEdit = computed(() => !!props.task)
const reversedHistory = computed(() => [...(form.history || [])].reverse())

watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        if (props.task) {
            Object.assign(form, JSON.parse(JSON.stringify(props.task))) 
        } else {
            Object.assign(form, {
                id: null, title: '', description: '', status: props.defaultStatus || 'To Do',
                tag: 'Feature', urgency: 'Low', dueDate: props.defaultDate || '', assignedUserIds: [], history: []
            })
        }
    }
})

const toggleUser = (uid) => {
    const idx = form.assignedUserIds.indexOf(uid)
    if (idx === -1) form.assignedUserIds.push(uid)
    else form.assignedUserIds.splice(idx, 1)
}

const addNewPerson = () => {
    const name = prompt("Enter new team member name:")
    if (name) {
        store.addTeamMember(name)
    }
}

const handleSubmit = () => emit('save', { ...form })
</script>