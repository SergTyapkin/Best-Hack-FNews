import { createRouter, createWebHistory } from 'vue-router'

import SignIn from '../views/SignIn.vue'
import Exchange from '../views/Exchange.vue'
import News from '../views/News.vue'
import SetupNews from '../views/SetupNews.vue'
import Profile from '../views/Profile.vue'
import SignUp from '../views/SignUp.vue'
import Page404 from '../views/Page404.vue'

export const BASE_URL_PATH = '/fnews';

export default function createVueRouter(Store) {
    const routes = [
        {path: BASE_URL_PATH + '/', component: News, meta: {loginRequired: true}},
        {path: BASE_URL_PATH + '/setup', component: SetupNews, meta: {loginRequired: true}},
        {path: BASE_URL_PATH + '/exchange', component: Exchange, meta: {loginRequired: true}},
        {path: BASE_URL_PATH + '/signin', component: SignIn, meta: {noLoginRequired: true}},
        {path: BASE_URL_PATH + '/signup', component: SignUp, meta: {noLoginRequired: true}},
        {path: BASE_URL_PATH + '/profile', component: Profile, meta: {loginRequired: true}},
        {path: BASE_URL_PATH + '/:pathMatch(.*)*', component: Page404}
    ]

    const Router = createRouter({
        history: createWebHistory(),
        routes: routes,
    });

    let router_got_user = false
    Router.beforeEach(async (to, from, next) => {
        if (!router_got_user) {
            await Store.dispatch('GET_USER');
            router_got_user = true;
        }

        const baseBartRedirect = {
            path: BASE_URL_PATH + removeBasePartOnStart(to.fullPath),
        }
        const notLoginedRedirect = {
            path: BASE_URL_PATH + '/signin',
        }
        const loginedRedirect = {
            path: BASE_URL_PATH + '/profile',
        }

        function smartBasePartRedirect() {
            if (isStartsOnBasePart(to.fullPath))
                next();
            else
                next(baseBartRedirect);
        }

        if (to.matched.some(record => record.meta.loginRequired)) {
            if (Store.state.user.isLogined) {
                smartBasePartRedirect();
                return;
            }
            next(notLoginedRedirect);
            return;
        } else if (to.matched.some(record => record.meta.noLoginRequired)) {
            if (!Store.state.user.isLogined) {
                smartBasePartRedirect();
                return;
            }
            next(loginedRedirect);
            return;
        }
        smartBasePartRedirect();
    });

    return Router;
}

function isStartsOnBasePart(string) {
    return new RegExp(`^${BASE_URL_PATH}`, 'i').test(string);
}
function removeBasePartOnStart(string) {
    return string.replace(new RegExp(`^${BASE_URL_PATH}`, 'i'), '');
}
