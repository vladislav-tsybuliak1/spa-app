import {createRouter, createWebHistory} from 'vue-router';
import RegistrationPage from './components/RegistrationPage.vue';
import LogInPage from "./components/LogInPage.vue";
import CommentsPage from "./components/CommentsPage.vue";

const routes = [
    {path: '/register/', component: RegistrationPage},
    {path: '/', redirect: '/register/'},
    {path: '/login/', component: LogInPage},
    {path: '/comments/', component: CommentsPage}
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
