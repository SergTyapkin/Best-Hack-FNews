import { createRouter, createWebHistory } from 'vue-router'

import SignIn from '../views/SignIn.vue'
import Profile from '../views/Profile.vue'
import SignUp from '../views/SignUp.vue'
import Page404 from '../views/Page404.vue'

export default function createVueRouter(Store) {
    const routes = [
        {path: '/signin', component: SignIn, meta: {noLoginRequired: true}},
        {path: '/signup', component: SignUp, meta: {noLoginRequired: true}},
        {path: '/profile', component: Profile, meta: {loginRequired: true}},
        {path: '/:pathMatch(.*)*', component: Page404}
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

        if (to.matched.some(record => record.meta.loginRequired)) {
            if (Store.state.user.isLogined) {
                next();
                return;
            }
            next({
                path: '/signin',
                params: {nextUrl: to.fullPath}
            });
        } else if (to.matched.some(record => record.meta.noLoginRequired)) {
            if (!Store.state.user.isLogined) {
                next();
                return;
            }
            next({
                path: '/profile',
                params: {nextUrl: to.fullPath}
            });
        }
        next();
    });

    return Router;
}
