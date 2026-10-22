import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0 }),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true },
    },
    { path: '/', name: 'dashboard', component: () => import('@/views/DashboardView.vue') },
    { path: '/diary', name: 'diary', component: () => import('@/views/TagebuchView.vue') },
    {
      path: '/knowledge',
      name: 'knowledge',
      component: () => import('@/views/KnowledgeView.vue'),
    },
    {
      path: '/knowledge/subjects/:id',
      name: 'knowledge-subject',
      component: () => import('@/views/SubjectView.vue'),
    },
    {
      path: '/knowledge/new',
      name: 'knowledge-new',
      component: () => import('@/views/KnowledgeEditorView.vue'),
    },
    {
      path: '/knowledge/entries/:id',
      name: 'knowledge-entry',
      component: () => import('@/views/KnowledgeEntryView.vue'),
    },
    {
      path: '/knowledge/entries/:id/edit',
      name: 'knowledge-edit',
      component: () => import('@/views/KnowledgeEditorView.vue'),
    },
    {
      path: '/pinboard',
      name: 'pinboard',
      component: () => import('@/views/PinboardView.vue'),
    },
    { path: '/events', name: 'events', component: () => import('@/views/EventsView.vue') },
    {
      path: '/events/:id',
      name: 'event-detail',
      component: () => import('@/views/EventDetailView.vue'),
    },
    { path: '/people', name: 'people', component: () => import('@/views/PeopleView.vue') },
    { path: '/calendar', name: 'calendar', component: () => import('@/views/CalendarView.vue') },
    { path: '/tasks', name: 'tasks', component: () => import('@/views/TasksView.vue') },
    { path: '/:pathMatch(.*)*', redirect: { name: 'dashboard' } },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.ready) await auth.fetchMe()

  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.name === 'login' && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }
  return true
})

export default router
