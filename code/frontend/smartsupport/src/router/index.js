import { createRouter, createWebHistory } from 'vue-router'

import SignIn from '../views/SignIn.vue'
import SignUp from '../views/SignUp.vue'
import Home from '../views/Home.vue'
import Profile from '../views/Profile.vue'
import MyTickets from '../views/MyTickets.vue'
import AllTickets from '../views/AllTickets.vue'
import Ticket from '../views/Ticket.vue'
import Users from '../views/Users.vue'
import FAQs from '../views/FAQs.vue'




const routes = [
  {
    path: '/',
    component: SignIn
  },
  {
    path: "/signup",
    component: SignUp,
  },
  {
    path: "/home",
    component: Home,
  },
  {
    path: "/profile",
    component: Profile,
  },
  {
    path: "/mytickets",
    component: MyTickets,
  },
  {
    path: "/alltickets",
    component: AllTickets,
  },
  {
    path: "/faqs",
    component: FAQs,
  },
  {
    path: "/ticket/:tid",
    component: Ticket,
    meta: {
      watchParam: 'tid'
    }
  },
  {
    path: "/users",
    component: Users,
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
