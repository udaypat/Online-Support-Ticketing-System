<template>
    <NavBar></NavBar>

    <div class="container mt-4">
        <ul class="nav nav-tabs mb-3" id="pills-tab" role="tablist">
            <li v-if="is_support"  class="nav-item" role="presentation">
                <button class="nav-link" :class="{'active': is_support}" id="supportTickets-tab" data-bs-toggle="pill" data-bs-target="#supportTickets" type="button" role="tab" aria-controls="supportTickets" aria-selected="false">
                    Support Tickets</button>
            </li>
            <li v-if="is_student" class="nav-item" role="presentation">
                <button class="nav-link" :class="{'active': !is_support && is_student}" id="studentTickets-tab" data-bs-toggle="pill" data-bs-target="#studentTickets" type="button" role="tab" aria-controls="studentTickets" aria-selected="false">
                    Student Tickets</button>
            </li>
        </ul>
        <div class="tab-content" id="nav-tabContent">
            <div v-if="is_support" id="supportTickets" class="row tab-pane " :class="{'active': is_support, 'show': is_support}" role="tabpanel" aria-labelledby="supportDashboard-tab" tabindex="0">
                <table id="mySupportTickets" class="table table-borderless table-group-divider">
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
                        <tr v-for="ticket in support_ticket_list" :key="ticket.ticket_id">
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
                                <div class="list-inline">
                                    <router-link :to="'/ticket/' + ticket.ticket_id" v-if="ticket.status === 'Open'"
                                        class="badge text-bg-success list-inline-item text-decoration-none">Respond</router-link>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="is_student" id="studentTickets" class="row tab-pane " :class="{'active': !is_support && is_student, 'show': !is_support  && is_student}" role="tabpanel" aria-labelledby="studentDashboard-tab" tabindex="0">
                <table id="myTickets" class="table table-borderless table-group-divider" v-if="student_ticket_list.length>0">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Votes</th>
                            <th>Date</th>
                            <th>Status</th>
                            <th>Tags</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="ticket in student_ticket_list" :key="ticket.ticket_id">
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
                                <span v-for="tag in ticket.tags">
                                    <span class="badge bg-secondary">{{tag.name}}</span>&nbsp;
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div v-if="student_ticket_list.length===0"> No Tickets to show</div>
            </div>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import config from "@/config.js";
// import $ from 'jquery'


export default {
    name: "MyTickets",
    components: {
        NavBar,
    },
    data(){
        return{
            support_ticket_list: [],
            student_ticket_list: [],
            is_support: false,
            is_student: false,
            is_admin: false,
        }
    },
    methods:{
        Get_support_tickets(){
            console.log('Getting support tickets')
            const options = {
                method: 'GET',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch(`${config.BASE_API_URL}/tickets/support/all`, options)
                .then(response => response.json())
                .then(response => this.support_ticket_list = response)
                .then(response => console.log(this.support_ticket_list))
                .catch(err => console.error(err));
        },
        Get_student_tickets() {
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
    },
    created(){
        this.is_admin = localStorage.getItem("is_admin");
        this.is_support = localStorage.getItem("is_support");
        this.is_student = localStorage.getItem("is_student");

        this.Get_support_tickets()
        this.Get_student_tickets()
    },
    mounted(){

    }
};

</script>


<style></style>