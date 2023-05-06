<template>
    <NavBar></NavBar>

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
        <h1>All Tickets</h1>
        <table id="allTickets" class="table table-borderless table-group-divider">
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Votes</th>
                    <th>Date</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="ticket in all_tickets" :key="ticket.ticket_id">
                    <td class="" :title="ticket.title">
                        <router-link
                            v-bind:class="{ 'text-danger': ticket.status === 'Open', 'text-success': ticket.status === 'Resolved', 'text-warning': ticket.status === 'Closed' }"
                            :to="'/ticket/' + ticket.ticket_id" class="text-decoration-none">{{
                                ticket.title }} </router-link>
                    </td>
                    <td><small>{{ ticket.votes_count }}</small></td>
                    <td><small>{{ ticket.created_at.substring(0, 10) }}</small></td>
                    <td><b><small v-bind:class="{ 'text-danger': ticket.status === 'Open', 'text-success': ticket.status === 'Resolved', 'text-warning': ticket.status === 'Closed' }">{{ ticket.status }}</small></b></td>
                    <td>
                        <div class="list-inline"  v-if="ticket.status === 'Open'">
                            <router-link :to="'/ticket/' + ticket.ticket_id"
                                class="badge text-bg-success list-inline-item text-decoration-none">Respond</router-link>
                            <span v-if="is_admin" type="button" @click="get_admin_and_support_user(ticket.ticket_id)"
                                class="badge text-bg-warning list-inline-item" data-bs-toggle="modal"
                                data-bs-target="#ticketAssignmentModel">
                                Assign
                            </span>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import * as assign from '../utilities/assign.js';
import config from "@/config.js";


export default {
    name: "AllTickets",
    components: {
        NavBar,
    },
    data(){
        return{
            all_tickets: [],
            admin_and_support_user_list: [],
            ticket_id_to_assign: "",
            is_admin: false,
            is_support: false,
        }
    },
    methods: {
        Get_all_tickets() {
            // Get list of tickets
            fetch(`${config.BASE_API_URL}/tickets?page=0&per_page=80000`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.all_tickets = res
                    console.log("got ticket list")
                    console.log(this.all_tickets)
                });
        },
        assign_ticket_to_user(username){
            assign.assign_ticket_to_user(username, this)
        },
        get_admin_and_support_user(ticket_id){
            assign.get_admin_and_support_user(ticket_id, this)
        }
    },
    created(){
        this.Get_all_tickets();

        this.is_admin = localStorage.getItem("is_admin");
        this.is_support = localStorage.getItem("is_support");
    }
};

</script>


<style></style>