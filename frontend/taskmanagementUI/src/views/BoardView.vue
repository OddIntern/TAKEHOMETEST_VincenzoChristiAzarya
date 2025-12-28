<template>
  <div class="min-h-screen bg-gray-100 font-sans flex flex-col">
    
<header class="bg-slate-900 border-b border-slate-800 shadow-sm z-10">
        <div class="px-8 py-5 flex justify-between items-center max-w-[1920px] mx-auto w-full">
            
            <div class="flex items-center gap-4">
                <div v-if="!isEditingTitle" class="flex items-center gap-3 group">
                    <h1 class="text-3xl font-extrabold text-white tracking-tight cursor-default">
                        {{ boardTitle }}
                    </h1>
                    <button @click="startEditingTitle" class="text-slate-500 hover:text-white transition-all opacity-0 group-hover:opacity-100 p-1.5 rounded-full hover:bg-slate-800" title="Rename Board">
                        <PencilIcon class="w-5 h-5" />
                    </button>
                </div>
                <div v-else class="flex items-center gap-2 animate-fade-in">
                    <input ref="titleInputRef" v-model="tempTitle" @keyup.enter="saveTitle" @keyup.esc="cancelEditTitle" type="text" class="text-2xl font-bold text-white bg-slate-800 border border-blue-500 rounded px-3 py-1 outline-none w-80 placeholder-slate-500" />
                    <div class="flex gap-1">
                        <button @click="saveTitle" class="p-1.5 bg-green-600 hover:bg-green-500 text-white rounded-md"><CheckIcon class="w-5 h-5" /></button>
                        <button @click="cancelEditTitle" class="p-1.5 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-md"><XMarkIcon class="w-5 h-5" /></button>
                    </div>
                </div>
            </div>

            <div class="flex items-center gap-4">
                
                <div class="bg-white p-1 rounded-lg border border-gray-200 flex shadow-sm h-10">
                    <button @click="viewMode = 'board'" :class="viewMode === 'board' ? 'bg-blue-50 text-blue-700 shadow-sm' : 'text-gray-500 hover:bg-gray-50'" class="flex items-center gap-2 px-4 rounded-md text-sm font-bold transition-all"><BoardIcon class="w-4 h-4" /> Board</button>
                    <button @click="viewMode = 'calendar'" :class="viewMode === 'calendar' ? 'bg-blue-50 text-blue-700 shadow-sm' : 'text-gray-500 hover:bg-gray-50'" class="flex items-center gap-2 px-4 rounded-md text-sm font-bold transition-all"><CalendarIcon class="w-4 h-4" /> Calendar</button>
                </div>

                <div class="relative">                   
                    <button 
                        id="user-menu-btn"
                        @click="toggleUserMenu"
                        class="flex items-center gap-3 pl-3 pr-2 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-full border border-slate-700 transition-all focus:ring-2 focus:ring-blue-500/50">
                        <span class="text-slate-200 text-sm font-semibold select-none">{{ store.user?.username || 'User' }}</span>
                        <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-xs">
                            {{ (store.user?.username || 'U').substring(0,2).toUpperCase() }}
                        </div>
                    </button>
                    
                    <div 
                        id="user-menu-dropdown"
                        v-if="isUserMenuOpen"
                        class="absolute right-0 top-full mt-2 w-48 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden animate-fade-in z-50">
                        
                        <div class="px-4 py-3 bg-gray-50 border-b border-gray-100">
                            <p class="text-xs text-gray-500 uppercase font-bold">Signed in as</p>
                            <p class="text-sm font-bold text-gray-800 truncate">{{ store.user?.username }}</p>
                        </div>
                        
                        <button 
                            @click="store.logout()" 
                            class="w-full text-left px-4 py-3 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2 font-medium transition-colors">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                            Logout
                        </button>
                    </div>

                </div>

            </div>
        </div>
    </header>

    <main class="flex-1 p-8 overflow-y-auto">
        <div class="max-w-[1920px] mx-auto h-full">

            <div v-if="viewMode === 'board'" class="grid grid-cols-1 md:grid-cols-3 gap-6 h-full">
                <div v-for="colName in ['To Do', 'In Progress', 'Done']" :key="colName" class="flex flex-col h-full">
                    
                    <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-200 border-t-4 mb-4"
                        :class="{'border-t-red-500': colName==='To Do', 'border-t-yellow-500': colName==='In Progress', 'border-t-green-500': colName==='Done'}">
                        <div class="flex justify-between items-center mb-3">
                            <div class="flex items-center gap-2">
                                <h3 class="font-bold text-gray-800 text-lg">{{ colName }}</h3>
                                <span class="bg-gray-100 text-gray-600 text-xs font-bold px-2.5 py-1 rounded-full border border-gray-200">
                                    {{ store.columns[colName].length }}
                                </span>
                            </div>
                            <button @click="openAddModal(colName)" class="text-gray-400 hover:text-blue-600 hover:bg-blue-50 w-8 h-8 rounded-full flex items-center justify-center transition-colors font-bold text-xl leading-none pb-1">+</button>
                        </div>
                        <div>
                            <select v-model="filters[colName]" class="w-auto text-xs font-medium border border-gray-200 rounded-md px-2 py-1.5 bg-gray-50 text-gray-600 outline-none cursor-pointer hover:border-gray-300 transition-colors focus:ring-2 focus:ring-blue-100">
                                <option value="All">Filter: All</option>
                                <option v-for="tag in ['Feature', 'Bug', 'Design', 'Planned']" :key="tag" :value="tag">{{ tag }}</option>
                            </select>
                        </div>
                    </div>

                    <draggable 
                        v-model="store.columns[colName]" 
                        group="tasks" 
                        @change="(e) => handleChange(e, colName)"
                        item-key="id"
                        class="flex-1 space-y-3 min-h-[150px]"
                        ghost-class="opacity-50"
                    >
                        <template #item="{element}">
                            <div v-if="filters[colName] === 'All' || element.tag === filters[colName]" 
                                class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all group relative cursor-grab"
                                :class="getUrgencyStyles(element.priority).border"
                                @click="openEditModal(element)">
                                
                                <div class="flex justify-between items-start mb-3">
                                    <span :class="tagStyles[element.tag] || tagStyles['Planned']" class="text-[10px] font-bold px-2.5 py-1 rounded-md uppercase tracking-wide border shadow-sm">
                                        {{ element.tag || 'Planned' }}
                                    </span>
                                    <div :class="getUrgencyStyles(element.priority).color" class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider bg-gray-50 px-2 py-1 rounded-md">
                                        <FlagIcon class="w-3.5 h-3.5" /> {{ element.priority || 'Low' }}
                                    </div>
                                </div>

                                <h4 class="text-gray-800 font-bold text-sm mb-1.5 leading-snug">{{ element.title }}</h4>
                                <p v-if="element.description" class="text-xs text-gray-500 line-clamp-2 mb-3 leading-relaxed">
                                    {{ element.description }}
                                </p>
                                
                                <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-50">
                                    <div class="text-[10px] text-gray-400 font-medium flex items-center gap-1.5">
                                        <span v-if="element.due_date" class="flex items-center gap-1.5 bg-gray-50 px-2 py-1 rounded text-gray-600 border border-gray-100">
                                            <CalendarIcon class="w-3.5 h-3.5 text-gray-400" /> 
                                            {{ element.due_date }}
                                        </span>
                                    </div>
                                    <div class="flex -space-x-2 pl-2 overflow-hidden">
                                        <div v-for="uid in (element.assigned_user_ids || [])" :key="uid" 
                                            class="w-6 h-6 rounded-full border-2 border-white text-[9px] flex items-center justify-center text-white font-bold shadow-sm ring-1 ring-gray-100"
                                            :class="getTeamMember(uid).color"
                                            :title="getTeamMember(uid).name">
                                            {{ getTeamMember(uid).initials }}
                                        </div>
                                    </div>
                                </div>

                                <div class="absolute top-3 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity bg-white/95 pl-1 shadow-sm rounded-md border border-gray-100 backdrop-blur-sm z-10">
                                    <button @click.stop="duplicateTask(element)" class="p-1.5 hover:bg-teal-50 text-gray-400 hover:text-teal-600 rounded" title="Duplicate">
                                        <CopyIcon class="w-3.5 h-3.5" />
                                    </button>
                                    <button @click.stop="deleteTask(element.id)" class="p-1.5 hover:bg-red-50 text-gray-400 hover:text-red-600 rounded" title="Delete">
                                        <TrashIcon class="w-3.5 h-3.5" />
                                    </button>
                                </div>
                            </div>
                        </template>

                        <template #footer>
                            <div v-if="store.columns[colName].length === 0" 
                                class="h-32 border-2 border-dashed border-gray-200 rounded-xl flex flex-col gap-2 items-center justify-center text-gray-400 text-sm italic bg-gray-50/50">
                                <span>Drop task here</span>
                            </div>
                        </template>
                    </draggable>
                </div>
            </div>

            <div v-else class="flex gap-6 h-[80vh]">
                <div class="flex-1 bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col">
                    <div class="p-4 flex justify-between items-center border-b border-gray-100">
                        <h2 class="text-2xl font-bold text-gray-800 flex items-baseline gap-2">
                            {{ currentMonthName }} <span class="text-xl font-normal text-gray-400">{{ currentYear }}</span>
                        </h2>
                        <div class="flex gap-1 bg-gray-100 p-1 rounded-lg">
                            <button @click="changeMonth(-1)" class="p-1.5 hover:bg-white hover:shadow-sm rounded-md text-gray-500 hover:text-blue-600 transition-all">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
                            </button>
                            <button @click="changeMonth(1)" class="p-1.5 hover:bg-white hover:shadow-sm rounded-md text-gray-500 hover:text-blue-600 transition-all">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </button>
                        </div>
                    </div>
                    <div class="grid grid-cols-7 border-b border-gray-100 bg-gray-50/80">
                        <div v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="day" class="py-3 text-center text-[11px] font-bold text-gray-400 uppercase tracking-wider">{{ day }}</div>
                    </div>
                    <div class="grid grid-cols-7 flex-1 auto-rows-fr overflow-y-auto bg-gray-100 gap-px border-b border-gray-200">
                        <div v-for="blank in blankDays" :key="'blank-'+blank" class="bg-gray-50/30"></div>
                        <div v-for="day in calendarDays" :key="day.date" class="bg-white p-2 min-h-[100px] hover:bg-gray-50 transition-colors flex flex-col group relative">
                            <span class="text-xs font-bold mb-2 block w-7 h-7 flex items-center justify-center rounded-full" :class="isToday(day.date) ? 'bg-blue-600 text-white shadow-md' : 'text-gray-400'">{{ day.dayNum }}</span>
                            <div class="space-y-1 overflow-y-auto flex-1 custom-scrollbar">
                                <div v-for="task in day.tasks" :key="task.id" @click="openEditModal(task)" class="text-[10px] bg-white border border-gray-200 p-1.5 rounded-md shadow-sm cursor-pointer truncate border-l-[3px] hover:shadow-md transition-all hover:border-gray-300" :class="getUrgencyStyles(task.priority).border">{{ task.title }}</div>
                            </div>
                            <button @click="openAddModalForDate(day.date)" class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 text-gray-300 hover:text-blue-600 hover:bg-blue-50 w-6 h-6 rounded flex items-center justify-center transition-all">+</button>
                        </div>
                    </div>
                </div>
                <div class="w-80 bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col">
                    <div class="p-4 border-b border-gray-100 bg-gray-50/50 rounded-t-xl">
                        <h3 class="font-bold text-gray-700 text-sm flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-orange-400 shadow-sm"></span> Unscheduled Tasks</h3>
                    </div>
                    <div class="p-3 overflow-y-auto flex-1 space-y-2.5 bg-gray-50/30">
                        <div v-if="unscheduledTasks.length === 0" class="flex flex-col items-center justify-center h-40 text-gray-400 gap-2">
                            <CalendarIcon class="w-8 h-8 opacity-20" />
                            <span class="text-xs italic">All tasks scheduled</span>
                        </div>
                        <div v-for="task in unscheduledTasks" :key="task.id" @click="openEditModal(task)" class="p-3 bg-white border border-gray-200 rounded-lg shadow-sm cursor-pointer border-l-4 hover:border-blue-400 hover:shadow-md transition-all group" :class="getUrgencyStyles(task.priority).border">
                            <div class="text-xs font-semibold text-gray-800 line-clamp-2 mb-2 group-hover:text-blue-600 transition-colors">{{ task.title }}</div>
                            <div class="flex justify-between items-center">
                                <span class="text-[9px] font-bold px-2 py-0.5 rounded border uppercase tracking-wide" :class="tagStyles[task.tag] || tagStyles['Planned']">{{ task.tag || 'Planned' }}</span>
                                <div class="flex -space-x-1">
                                    <div v-for="uid in (task.assigned_user_ids || []).slice(0,2)" :key="uid" class="w-5 h-5 rounded-full text-[9px] flex items-center justify-center text-white font-bold border border-white" :class="getTeamMember(uid).color">{{ getTeamMember(uid).initials }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

           <TaskModal 
                :isOpen="isModalOpen" 
                :task="editingTask" 
                :defaultStatus="activeCol" 
                :defaultDate="activeDate"  @close="isModalOpen = false" 
                @save="handleSave" 
            />
        </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, reactive, nextTick } from 'vue'
import draggable from 'vuedraggable'
import { useTaskStore } from '../stores/taskStore'
import TaskModal from '../components/TaskModal.vue'
import { 
    CalendarIcon, FlagIcon, DocumentDuplicateIcon as CopyIcon, 
    TrashIcon, ViewColumnsIcon as BoardIcon, PencilIcon, 
    CheckIcon, XMarkIcon 
} from '@heroicons/vue/24/outline'

const store = useTaskStore()
const viewMode = ref('board')
const isModalOpen = ref(false)
const editingTask = ref(null)
const activeCol = ref('To Do')
const filters = reactive({ 'To Do': 'All', 'In Progress': 'All', 'Done': 'All' })
const calendarViewDate = ref(new Date())
const activeDate = ref('') 
const isUserMenuOpen = ref(false) 

const toggleUserMenu = () => {
    isUserMenuOpen.value = !isUserMenuOpen.value
}

// Logic to close menu when clicking outside
const handleClickOutside = (event) => {
    const dropdown = document.getElementById('user-menu-dropdown')
    const button = document.getElementById('user-menu-btn')
    
    // If click is NOT on the button AND NOT inside the dropdown, close it
    if (isUserMenuOpen.value && dropdown && button && !dropdown.contains(event.target) && !button.contains(event.target)) {
        isUserMenuOpen.value = false
    }
}

// Add/Remove Global Listener
onMounted(() => {
    store.fetchTasks()
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})

// --- RENAME BOARD LOGIC ---
const boardTitle = computed(() => store.user?.board_title || 'Project Board')
const isEditingTitle = ref(false)
const tempTitle = ref('')
const titleInputRef = ref(null)

const startEditingTitle = async () => {
    tempTitle.value = boardTitle.value
    isEditingTitle.value = true
    await nextTick()
    titleInputRef.value.focus()
}

const saveTitle = async () => {
    if (tempTitle.value.trim()) {
        await store.updateBoardTitle(tempTitle.value.trim())
    }
    isEditingTitle.value = false
}

const cancelEditTitle = () => {
    isEditingTitle.value = false
}

// --- CONFIG ---
const tagStyles = {
    'Feature': 'bg-blue-50 text-blue-700 border-blue-200',
    'Bug': 'bg-red-50 text-red-700 border-red-200',
    'Design': 'bg-purple-50 text-purple-700 border-purple-200',
    'Planned': 'bg-gray-50 text-gray-600 border-gray-200'
}

const getUrgencyStyles = (priority) => {
    const val = priority || 'Low'
    const config = {
        'High': { color: 'text-red-600 bg-red-50', border: 'border-l-red-500' },
        'Medium': { color: 'text-yellow-600 bg-yellow-50', border: 'border-l-yellow-500' },
        'Low': { color: 'text-gray-500 bg-gray-100', border: 'border-l-gray-300' }
    }
    return config[val] || config['Low']
}

const teamMembers = [
    { id: 'u1', name: 'Alex', initials: 'AL', color: 'bg-indigo-500' },
    { id: 'u2', name: 'Sam', initials: 'SA', color: 'bg-emerald-500' },
    { id: 'u3', name: 'Jordan', initials: 'JO', color: 'bg-amber-500' },
    { id: 'u4', name: 'Taylor', initials: 'TA', color: 'bg-rose-500' },
]


const getTeamMember = (id) => {
    return store.teamMembers.find(m => m.id === id) || { initials: '?', color: 'bg-gray-400' }
}
onMounted(() => store.fetchTasks())

const openAddModal = (col) => { 
    editingTask.value = null; 
    activeCol.value = col; 
    activeDate.value = '';
    isModalOpen.value = true; 
}
const openEditModal = (task) => { editingTask.value = task; isModalOpen.value = true; }
const duplicateTask = async (task) => { await store.duplicateTask(task.id); }
const deleteTask = async (id) => { if(confirm('Delete?')) await store.deleteTask(id); }

const handleSave = async (taskData) => {
    if (taskData.id) await store.updateTask(taskData)
    else await store.createTask(taskData)
    isModalOpen.value = false
    store.fetchTasks()
}

const handleChange = (evt, colName) => {
    if (evt.added) {
        store.moveTask(evt.added.element.id, colName, evt.added.newIndex, store.columns[colName].map(t=>t.id))
    }
}

// --- CALENDAR LOGIC ---
const currentMonthName = computed(() => calendarViewDate.value.toLocaleString('default', { month: 'long' }))
const currentYear = computed(() => calendarViewDate.value.getFullYear())

const changeMonth = (step) => {
    const newDate = new Date(calendarViewDate.value)
    newDate.setMonth(newDate.getMonth() + step)
    calendarViewDate.value = newDate
}

const openAddModalForDate = (dateStr) => {
    editingTask.value = null
    activeDate.value = dateStr 
    isModalOpen.value = true
}

const unscheduledTasks = computed(() => store.tasks.filter(t => !t.due_date))

const calendarDays = computed(() => {
    const year = calendarViewDate.value.getFullYear()
    const month = calendarViewDate.value.getMonth()
    const daysInMonth = new Date(year, month + 1, 0).getDate()
    
    const days = []
    for(let i=1; i<=daysInMonth; i++) {
        const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(i).padStart(2,'0')}`
        days.push({
            date: dateStr, dayNum: i,
            tasks: store.tasks.filter(t => t.due_date === dateStr)
        })
    }
    return days
})

const blankDays = computed(() => {
    const year = calendarViewDate.value.getFullYear()
    const month = calendarViewDate.value.getMonth()
    return new Date(year, month, 1).getDay()
})

const isToday = (dateStr) => {
    return new Date().toDateString() === new Date(dateStr).toDateString()
}
</script>