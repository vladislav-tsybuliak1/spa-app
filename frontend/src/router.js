import {createRouter, createWebHistory} from 'vue-router';
import RegistrationPage from './components/RegistrationPage.vue'

const routes = [
    {path: '/register', component: RegistrationPage},
    {path: '/', redirect: '/register'}
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
