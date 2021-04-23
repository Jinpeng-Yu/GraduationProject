import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Home from '@/components/Home'
import Login from '../components/Login'
import Welcome from "../components/Welcome";
import Users from "../components/user/Users";
import Video from "../components/report/Video";
import Report from "../components/report/Report";
import Trends from "../components/report/Trends";

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', redirect:'/login' },
    { path: '/login', component:Login},
    {
      path: '/home',
      component:Home,
      redirect: '/welcome',
      children: [
        { path: '/welcome', component: Welcome},
        { path: '/users', component: Users},
        { path: '/videos', component: Video},
        { path: '/trends', component: Trends},
        { path: '/report', component: Report},
      ]
    },
  ]
})
