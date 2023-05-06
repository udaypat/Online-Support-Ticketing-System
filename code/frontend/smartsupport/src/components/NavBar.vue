<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <span class="navbar-brand">Smart Support</span>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <router-link :class="{ 'nav-link': true, active: $route.path === '/home' }" to="/home">
                        Home
                    </router-link>

                    <router-link v-if="is_student" :class="{ 'nav-link': true, active: $route.path === '/mytickets' }"
                        to="/mytickets">
                        My Tickets
                    </router-link>
                    <router-link v-if="is_admin || is_support"
                        :class="{ 'nav-link': true, active: $route.path === '/alltickets' }" to="/alltickets">
                        All Tickets
                    </router-link>
                    <router-link v-if="is_admin" :class="{ 'nav-link': true, active: $route.path === '/users' }"
                        to="/users">
                        All Users
                    </router-link>
                    <router-link :class="{ 'nav-link': true, active: $route.path === '/profile' }" to="/profile">
                        My Profile
                    </router-link>
                    <router-link :class="{ 'nav-link': true, active: $route.path === '/faqs' }" to="/faqs">
                        FAQs
                    </router-link>


                    <form class="d-flex" role="search">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
                            v-model="search_string_local" @keyup="search_tickets" />
                        <button class="btn btn-outline-success" type="submit">
                            Search
                        </button>
                    </form>

                    <router-link :class="{ 'nav-link': true }" to="/">
                        Logout
                    </router-link>
                </div>
            </div>
            <span class="navbar-text lead">
                Welcome, {{ user_details.first_name }} {{ user_details.last_name }}
            </span>
        </div>
    </nav>

    <div>
        <!-- <button @click="openOffcanvas">Open Offcanvas</button> -->
        <div class="offcanvas offcanvas-start" tabindex="-1" ref="offcanvas" :class="{ show: offcanvasState.show }"
            @hidden.bs.offcanvas="offcanvasState.show = false">
            <div class="offcanvas-header">
                <h3 class="offcanvas-title" id="offcanvasExampleLabel">Existing Tickets</h3>
                <button @click="closeOffcanvas" type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas"
                    aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
                <!-- offcanvas content -->
                <div class="media justify-content-end" v-for="(s_ticket, index) in searched_ticket_list" :key="index">
                    <router-link :to="'/ticket/' + s_ticket.ticket_id" class="text-decoration-none text-dark">
                        <div class="media-body text-right">
                            <h5 class="mt-0 text-dark">{{ s_ticket.title }}
                            </h5>
                            <p>
                                {{ s_ticket.body.substring(0, 100) + "..." }}
                            </p>
                            <div class="col align-self-end text-end">
                                <!-- <router-link :to="'/ticket/' + s_ticket.ticket_id">Read more... </router-link> -->
                            </div>
                        </div>
                    </router-link>
                    <hr>
                </div>
                <div v-if="show_search_spinner" class="d-flex text-primary justify-content-center">
                    <div class="spinner-border" role="status">
                        <span class="sr-only"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>




<script>
import { ref, reactive, watch } from 'vue';
import * as search from '../utilities/search.js'
import * as auth from '../utilities/auth.js';
import config from "@/config.js";


export default {
    name: "Navbar",
    setup() {
        const offcanvasRef = ref(null);
        const offcanvasState = reactive({
            show: false
        });

        const openOffcanvas = () => {
            offcanvasState.show = true;
            document.body.classList.add('offcanvas-open');
        }

        const closeOffcanvas = () => {
            offcanvasState.show = false;
            document.body.classList.remove('offcanvas-open');
        }

        return {
            offcanvasRef,
            offcanvasState,
            openOffcanvas,
            closeOffcanvas,
        }
    },
    data() {
        return {
            ticket_data: {
                title: "",
            },
            search_string_local: "",
            searched_ticket_list: [],
            show_search_spinner: true,
            user_details: {},
            is_admin: false,
            is_support: false,
            is_student: false,
        };
    },
    props: {
        search_string: String,
    },
    methods: {
        updateLocalSearchString(event) {
            this.search_string_local = event.target.value;
            this.$emit('update:propValue', this.search_string_local);
        },

        search_tickets() {
            search.search_tickets(this.search_string_local, this)
        },
    },

    created() {
        this.is_admin = localStorage.getItem("is_admin");
        this.is_support = localStorage.getItem("is_support");
        this.is_student = localStorage.getItem("is_student");
        this.user_details = JSON.parse(localStorage.getItem("user_details"));
    },


};
</script>