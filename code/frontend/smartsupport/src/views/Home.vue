<template>
    <NavBar></NavBar>

    <div class="offcanvas">
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

    <!-- Modal -->
    <div class="modal fade" id="ticketAssignmentModel" tabindex="-1" aria-labelledby="ticketAssignmentModelLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="ticketAssignmentModelLabel">Assign to...</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <strong>Support</strong>
                    <ul class="list-group list-group-flush">
                        <span v-for="user in admin_and_support_user_list" :key="user.id">
                            <li class="list-group-item" v-if="user.roles.some((role) => role.name === 'Support')">
                                <span type="button" @click="assign_ticket_to_user(user.username)"
                                    class="badge text-bg-warning list-inline-item">Assign to</span>
                                {{ user.username }}
                            </li>
                        </span>
                    </ul>
                    <strong>Admin</strong>
                    <ul class="list-group list-group-flush">
                        <span v-for="user in admin_and_support_user_list" :key="user.id">
                            <li class="list-group-item" v-if="user.roles.some((role) => role.name === 'Admin')">
                                <span type="button" @click="assign_ticket_to_user(user.username)"
                                    class="badge text-bg-danger list-inline-item">Assign to</span>
                                {{ user.username }}
                            </li>
                        </span>
                    </ul>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <!-- <button type="button" class="btn btn-primary">Save changes</button> -->
                </div>
            </div>
        </div>
    </div>



    <div class="container mt-4">
        <ul class="nav nav-tabs mb-3" id="pills-tab" role="tablist">
            <li v-if="is_admin" class="nav-item" role="presentation">
                <button class="nav-link" :class="is_admin ? 'active' : ''" id="adminDashboard-tab" data-bs-toggle="pill"
                    data-bs-target="#adminDashboard" type="button" role="tab" aria-controls="adminDashboard"
                    aria-selected="true">
                    Admin Dashboard</button>
            </li>
            <li v-if="is_support" class="nav-item" role="presentation">
                <button class="nav-link" :class="{ 'active': !is_admin && is_support }" id="supportDashboard-tab"
                    data-bs-toggle="pill" data-bs-target="#supportDashboard" type="button" role="tab"
                    aria-controls="supportDashboard" aria-selected="false">
                    Support Dashboard</button>
            </li>
            <li v-if="is_student" class="nav-item" role="presentation">
                <button class="nav-link" :class="{ 'active': !is_admin && !is_support && is_student }"
                    id="studentDashboard-tab" data-bs-toggle="pill" data-bs-target="#studentDashboard" type="button"
                    role="tab" aria-controls="studentDashboard" aria-selected="false">
                    Student Dashboard</button>
            </li>
        </ul>

        <div class="tab-content" id="tab-tabContent">
            <div v-if="is_admin" id="adminDashboard" class="row tab-pane " :class="{ 'active': is_admin, 'show': is_admin }"
                role="tabpanel" aria-labelledby="adminDashboard-tab" tabindex="0">
                <!-- <h1 class="text-secondary">Admin Dashboard</h1> -->

                <div class="row">
                    <div class="col-lg-6">
                        <div class="d-flex flex-column justify-content-left align-items-left">
                            <div><h2 class="d-inline"><span class="text-danger">Open</span> Tickets</h2> (Top 10)</div>
                            <table class="table table-borderless table-group-divider">
                                <thead>
                                    <tr>
                                        <th>Title</th>
                                        <th>Votes</th>
                                        <th>Date</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="ticket in admin_open_ticket_list" :key="ticket.ticket_id">
                                        <td class="" :title="ticket.title">
                                            <router-link
                                                v-bind:class="{ 'text-danger': ticket.status === 'Open', 'text-success': ticket.status === 'Resolved', 'text-warning': ticket.status === 'Closed' }"
                                                :to="'/ticket/' + ticket.ticket_id" class="text-decoration-none">{{
                                                    ticket.title.substring(0, 25) }}...</router-link>
                                        </td>
                                        <td><small>{{ ticket.votes_count }}</small></td>
                                        <td><small>{{ ticket.created_at.substring(0, 10) }}</small></td>
                                        <td>
                                            <div class="list-inline">
                                                <!-- <router-link :to="'/ticket/' + ticket.ticket_id" class=""><button class="badge btn btn-sm btn-success">Respond</button></router-link>
                                            <router-link :to="'/ticket/' + ticket.ticket_id" class=""><button class="badge btn btn-sm btn-secondary">Assign</button></router-link> -->
                                                <router-link :to="'/ticket/' + ticket.ticket_id"
                                                    class="badge text-bg-success list-inline-item text-decoration-none">Respond</router-link>
                                                <!-- &nbsp; -->
                                                <!-- <span type="button" class="badge text-bg-warning list-inline-item">Assign</span> -->
                                                <span type="button" @click="get_admin_and_support_user(ticket.ticket_id)"
                                                    class="badge text-bg-warning list-inline-item" data-bs-toggle="modal"
                                                    data-bs-target="#ticketAssignmentModel">
                                                    Assign
                                                </span>
                                                <!-- / Assign -->
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="d-flex flex-column justify-content-right align-items-left">
                            <div><h2 class="d-inline"><span class="text-success">Resolved</span> / <span class="text-warning">Closed</span> Tickets</h2> (Top 10)</div>
                            <!-- <h2><span class="text-success">Resolved</span> / <span class="text-warning">Closed</span>
                                Tickets</h2> -->
                            <table class="table table-borderless table-group-divider">
                                <thead>
                                    <tr>
                                        <th>Title</th>
                                        <th>Votes</th>
                                        <th>Date</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="ticket in admin_resolved_closed_ticket_list" :key="ticket.ticket_id">
                                        <td class="" :title="ticket.title">

                                            <router-link
                                                v-bind:class="{ 'text-danger': ticket.status === 'Open', 'text-success': ticket.status === 'Resolved', 'text-warning': ticket.status === 'Closed' }"
                                                :to="'/ticket/' + ticket.ticket_id" class="text-decoration-none">{{
                                                    ticket.title.substring(0, 30) }}...</router-link>
                                        </td>
                                        <td><small>{{ ticket.votes_count }}</small></td>
                                        <td><small>{{ ticket.created_at.substring(0, 10) }}</small></td>
                                        <td>
                                            <small v-if="ticket.status === 'Resolved'">
                                                <button @click="Convert_to_faq(ticket.ticket_id)" title="Add to FAQs"
                                                    class="btn badge btn-sm btn-primary mt-0"
                                                    style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">+
                                                    FAQs</button>
                                            </small>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="is_support" id="supportDashboard" class="row tab-pane "
                :class="{ 'active': !is_admin && is_support, 'show': !is_admin && is_support }" role="tabpanel"
                aria-labelledby="supportDashboard-tab" tabindex="0">
                <!-- <h1 class="text-secondary">Support Dashboard</h1> -->

                <div class="row">
                    <div class="col">
                        <div class="d-flex flex-column justify-content-left align-items-left">
                            <div><h2 class="d-inline"><span class="text-danger">Open</span> Tickets</h2> (Top 10)</div>
                            <table class="table table-borderless table-group-divider">
                                <thead>
                                    <tr>
                                        <th>Title</th>
                                        <th>Votes</th>
                                        <th>Date</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="ticket in support_open_ticket_list" :key="ticket.ticket_id">
                                        <td class="" :title="ticket.title">
                                            <router-link
                                                v-bind:class="{ 'text-danger': ticket.status === 'Open', 'text-success': ticket.status === 'Resolved', 'text-warning': ticket.status === 'Closed' }"
                                                :to="'/ticket/' + ticket.ticket_id" class="text-decoration-none">{{
                                                    ticket.title.substring(0, 30) }}...</router-link>
                                        </td>
                                        <td><small>{{ ticket.votes_count }}</small></td>
                                        <td><small>{{ ticket.created_at.substring(0, 10) }}</small></td>
                                        <td>
                                            <div class="list-inline">
                                                <router-link :to="'/ticket/' + ticket.ticket_id"
                                                    class="badge text-bg-success list-inline-item text-decoration-none">Respond</router-link>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="col">
                        <div class="d-flex flex-column justify-content-right align-items-left">
                            <div><h2 class="d-inline"><span class="text-success">Resolved</span> / <span class="text-warning">Closed</span> Tickets</h2> (Top 10)</div>
                            <!-- <h2><span class="text-success">Resolved</span> / <span class="text-warning">Closed</span>
                                Tickets</h2> -->
                            <table class="table table-borderless table-group-divider">
                                <thead>
                                    <tr>
                                        <th>Title</th>
                                        <th>Votes</th>
                                        <th>Date</th>
                                        <th>Resolved on</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="ticket in support_resolved_closed_ticket_list" :key="ticket.ticket_id">
                                        <td class="" :title="ticket.title">
                                            <router-link
                                                v-bind:class="{ 'text-danger': ticket.status === 'Open', 'text-success': ticket.status === 'Resolved', 'text-warning': ticket.status === 'Closed' }"
                                                :to="'/ticket/' + ticket.ticket_id" class="text-decoration-none">{{
                                                    ticket.title.substring(0, 30) }}...</router-link>
                                        </td>
                                        <td><small>{{ ticket.votes_count }}</small></td>
                                        <td><small>{{ ticket.created_at.substring(0, 10) }}</small></td>
                                        <td>
                                            <small v-if="ticket.status === 'Resolved'">
                                                {{ ticket.updated_at.substring(0, 10) }}
                                            </small>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>


            </div>

            <div v-if="is_student" id="studentDashboard" class="row tab-pane "
                :class="{ 'active': !is_admin && !is_support && is_student, 'show': !is_admin && !is_support && is_student }"
                role="tabpanel" aria-labelledby="studentDashboard-tab" tabindex="0">
                <!-- <h1 class="text-secondary">Student Dashboard</h1> -->

                <div class="row">
                    <div class="col">
                        <div class="d-flex flex-column justify-content-left align-items-left">
                            <!-- First flexbox content goes here -->
                            <div><h2 class="d-inline">My Tickets</h2> (Top 10)</div>

                            <!-- <li v-for="ticket in student_ticket_list">{{ ticket.title }}</li> -->
                            <table v-if="student_ticket_list.length>0" class="table table-borderless table-group-divider">
                                <thead>
                                    <tr>
                                        <th>Title</th>
                                        <th>Votes</th>
                                        <th>Date</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="ticket in student_ticket_list" :key="ticket.ticket_id">
                                        <td><router-link :to="'/ticket/' + ticket.ticket_id" class="">{{
                                            ticket.title.substring(0,
                                                30) }}...</router-link></td>
                                        <td>{{ ticket.votes_count }}</td>
                                        <td><small>{{ ticket.created_at.substring(0, 10) }}</small></td>
                                        <td
                                            v-bind:class="{ 'text-danger': ticket.status === 'Open', 'text-success': ticket.status === 'Resolved', 'text-warning': ticket.status === 'Closed' }">
                                            <strong>{{ ticket.status }}</strong>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <div v-if="student_ticket_list.length === 0">
                                No tickets to show
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="d-flex flex-column justify-content-center ">
                            <!-- Second flexbox content goes here -->
                            <h2>Raise a new Ticket</h2>
                            <div class="card border-light">
                                <div class="card-body">
                                    <form @submit.prevent="Createticket">
                                        <div class="form-group mb-3">
                                            <label for="title" class="form-label">Title</label>
                                            <input type="text" class="form-control" id="title" v-model="ticket_data.title"
                                                @keyup="search_tickets" required>
                                        </div>
                                        <div class="form-group mb-3">

                                            <label for="tags">Select Tag(s)</label>
                                            <select class="form-control" id="tags" required v-model="ticket_data.tags"
                                                multiple>
                                                <!-- <option value="Tags" disabled selected> </option> -->
                                                <option v-for="tag in tag_list">{{ tag.name }}</option>

                                            </select>
                                        </div>

                                        <div class="form-group mb-3">
                                            <label for="body">Body</label>
                                            <textarea type="text" class="form-control" id="body" v-model="ticket_data.body"
                                                required></textarea>
                                        </div>
                                        <button type="submit" class="btn btn-sm btn-primary">Submit</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>



    </div>
</template>

<script>
import { ref, reactive, watch } from 'vue';
import * as search from '../utilities/search.js';
import * as assign from '../utilities/assign.js';
import * as auth from '../utilities/auth.js';
import config from "@/config.js";
import NavBar from '@/components/NavBar.vue';
import swal from 'sweetalert';

export default {
    name: "Home",
    components: {
        NavBar,
    },
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
            admin_and_support_user_list: [],
            user_details: {},
            student_ticket_list: [],
            admin_open_ticket_list: [],
            admin_resolved_closed_ticket_list: [],
            support_open_ticket_list: [],
            support_resolved_closed_ticket_list: [],
            ticket_data: {
                title: "",
                tags: [],
                body: ""
            },
            tag_list: [],
            searched_ticket_list: [],
            show_search_spinner: true,
            is_admin: false,
            is_support: false,
            is_student: false,
            ticket_id_to_assign: "",
        };
    },


    methods: {
        Createticket() {
            console.log("clicked on create ticket")
            console.log(JSON.stringify(this.ticket_data))


            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: localStorage.getItem("access_key"),
                },
                body: JSON.stringify(this.ticket_data)
            };

            fetch(`${config.BASE_API_URL}/tickets`, options)
                .then(response => response.json())
                .then(response => this.Get_Student_Ticket_list())
                .catch(err => console.error(err));
        },
        Get_Student_Ticket_list() {
            // Get list of tickets
            fetch(`${config.BASE_API_URL}/tickets/user`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.student_ticket_list = res
                    console.log("got ticket list")
                });
        },
        Get_Admin_Open_Ticket_list() {
            // Get list of tickets
            fetch(`${config.BASE_API_URL}/tickets/open?page=0&per_page=10`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.admin_open_ticket_list = res
                    console.log("got amin open ticket list")
                });
        },
        Get_Admin_Resolved_Closed_Ticket_list() {
            // Get list of tickets
            fetch(`${config.BASE_API_URL}/tickets/resolved-or-closed?page=0&per_page=10`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.admin_resolved_closed_ticket_list = res
                    console.log("got amin resolved or closed ticket list")
                });
        },
        Get_Support_Open_Ticket_list() {
            // Get list of tickets
            fetch(`${config.BASE_API_URL}/tickets/support/open?page=0&per_page=10`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.support_open_ticket_list = res
                    console.log("got Support open ticket list")
                });
        },
        Get_Support_Resolved_Closed_Ticket_list() {
            // Get list of tickets
            fetch(`${config.BASE_API_URL}/tickets/support/resolved-or-closed?page=0&per_page=10`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.support_resolved_closed_ticket_list = res
                    console.log("got Support resolved or closed ticket list")
                });
        },
        Convert_to_faq(ticket_id) {
            swal({
                title: "Convert Ticket to FAQ",
                text: "Do you want to go ahead with this option?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
                .then((toFAQ) => {
                    if (toFAQ) {
                        const options = {
                            method: 'POST',
                            headers: {
                                Authorization: localStorage.getItem("access_key")

                            }
                        };

                        fetch(`${config.BASE_API_URL}/tickets/${ticket_id}/faqs`, options)
                            .then(response => {
                                if (!response.ok) {
                                    if (response.status === 400) {
                                        throw new Error('Bad Request');
                                    }
                                }
                                return response.json();
                            }).then(
                                swal({
                                    title: "Success",
                                    text: "Ticket converted to a FAQ successfully",
                                    icon: "success",
                                    button: "Okay"
                                })
                            )
                            .catch(err => console.error(err));

                    } else {
                        swal("Ticket not converted to a FAQ");
                    }
                });
        },
        assign_ticket_to_user(username){
            assign.assign_ticket_to_user(username, this)
        },
        get_admin_and_support_user(ticket_id){
            assign.get_admin_and_support_user(ticket_id, this)
        },
        search_tickets() {
            search.search_tickets(this.ticket_data.title, this)
        },
    },

    created() {
        // this.Get_Student_Ticket_list()
        // this.Get_Admin_Open_Ticket_list()
        // this.Get_Admin_Resolved_Closed_Ticket_list()
        //Get list of tags

        fetch(`${config.BASE_API_URL}/tags`, {
            headers: { Authorization: localStorage.getItem("access_key") },
        })
            .then((res) => res.json())
            .then((res) => {
                this.tag_list = res
            });


        //Store user details in localstorage
        // const options = {
        //     method: 'GET',
        //     headers: {
        //         Authorization: localStorage.getItem("access_key")
        //     }
        // };

        // fetch(`${config.BASE_API_URL}/user`, options)
        //     .then(response => response.json())
        //     .then(response => { localStorage.setItem("user_details", JSON.stringify(response)) })
        //     .then(this.user_details = JSON.parse(localStorage.getItem("user_details")))
        //     .then(auth.user_roles(this))
        //     .catch(err => console.error(err));

        this.user_details = localStorage.getItem("user_details");
        this.is_admin = localStorage.getItem("is_admin");
        this.is_support = localStorage.getItem("is_support");
        this.is_student = localStorage.getItem("is_student");

    },
    mounted() {
        // auth.user_roles(this)

        this.Get_Student_Ticket_list()
        this.Get_Admin_Open_Ticket_list()
        this.Get_Admin_Resolved_Closed_Ticket_list()
        this.Get_Support_Open_Ticket_list()
        this.Get_Support_Resolved_Closed_Ticket_list()
    },

};
</script>

<style>h3 {
    float: right;
}</style>


<style></style>