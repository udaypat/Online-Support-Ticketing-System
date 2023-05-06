<template>
    <NavBar></NavBar>

    <div class="container mt-4">
        <div class="row">
            <div class="col" style="min-width: 50%; max-width: 51%; ">
                <div class="d-flex flex-column justify-content-left align-items-left">
                    <!-- First flexbox content goes here -->
                    <h1>{{ ticket.title }}
                    </h1>
                    <div class="d-flex">
                        <span v-for="tag in ticket.tags" class="badge bg-success rounded-pill me-1">{{ tag.name }}</span>
                        <!-- <span class="badge bg-info rounded-pill me-2">Badge 1</span> -->
                    </div>

                    <div class="row">
                        <button @click="upvote" type="button" class="btn btn-sm btn-primary mt-3" style="width: 20%;">
                            Votes <span class="badge text-bg-secondary">{{ ticket.votes_count }}</span>
                        </button> &nbsp;

                        <button v-if="ticket.student.user_id === currentUser_id" type="button"
                            class="btn btn-sm btn-danger mt-3" @click="deleteticket" style="width: 20%;">Delete
                            Ticket</button>

                        <button v-if="(is_admin || is_support) && ticket.status == 'Open'" type="button"
                            class="btn btn-sm btn-warning mt-3" @click="close_ticket" style="width: 20%;">Close
                            Ticket</button>
                    </div>

                    <p class="mt-4  fs-5 fw-normal text-body">{{ ticket.body }}</p>
                    <!-- Solution box below title -->
                    <div class="card mb-3" v-if="sol.body">
                        <div class="card-body">
                            <h5 class="card-title">Solution</h5>
                            <div class="media justify-content-end">
                                <div class="media-body text-right bg-success-bck">


                                    <h5 class="mt-0">{{ sol.commentor.first_name }} {{
                                        sol.commentor.last_name }}
                                    </h5>
                                    <p v-if="sol.body">{{ sol.body }}</p>
                                </div>

                            </div>
                        </div>
                    </div>


                    <div id="postcomment" class="justify-content-center">

                        <h2>Post comments</h2>
                        <form class=" ">
                            <div class="form-group form-floating mb-3" style="width: 100%;">
                                <textarea v-model="new_comment" class="form-control w-100" placeholder=""
                                    id="floatingTextarea"></textarea>
                                <label for="floatingTextarea">Leave a comment here</label>

                            </div>
                            <button @click.prevent="post_comment" type="submit" class="btn btn-primary btn-sm col-12">Post
                                comment</button>
                        </form>

                    </div>
                </div>

            </div>

            <div class="col">
                <div class="d-flex flex-column justify-content-center align-items-center">
                    <!-- Second flexbox content goes here -->
                    <h1>Comments</h1>
                    <div class="container">
                        <div class="d-flex flex-column">
                            <div class="card mb-3">
                                <div class="card-body">
                                    <h5 class="card-title">Comments</h5>

                                    <div class="media justify-content-end" v-for="(comment, index) in comments"
                                        :key="index">
                                        <hr>
                                        <div class="media-body text-right" :class="{ 'bg-success-bck': comment.solution }">

                                            <h5 class="mt-0">{{ comment.commentor.first_name }} {{
                                                comment.commentor.last_name }}
                                            </h5>

                                            <!-- <p>{{ comment.body }}<span v-if="comment.solution"
                                                    class="badge rounded-pill text-bg-success m-1 ">Solution</span>
                                            </p> -->
                                            <p>{{ comment.body }}<span v-if="is_solution(comment)"
                                                    class="badge rounded-pill text-bg-success m-1 ">Solution</span>
                                            </p>

                                            <button class="btn btn-success m-1"
                                                v-if="ticket.student.user_id === currentUser_id && ticket.status == 'Open'"
                                                @click="mark_solution(comment.comment_id)">
                                                Mark as solution
                                            </button>

                                            <button class="btn btn-danger"
                                                v-if="comment.commentor.user_id === currentUser_id"
                                                @click="deleteComment(comment)">
                                                Delete
                                            </button>
                                        </div>

                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <!-- <div class="row">
            <div class="col">
                <div class="d-flex flex-column justify-content-left align-items-left">
                    Third flexbox content goes here
                    <h1>Post comments</h1>
                    <form>
                        <div class="form-group form-floating " style="width: 50%;">
                            <textarea v-model="new_comment" class="form-control" placeholder=""
                                id="floatingTextarea"></textarea>
                            <label for="floatingTextarea">Leave a comment here</label>

                        </div>
                        <button @click.prevent="post_comment" type="submit" class="btn btn-primary">Post comment</button>
                    </form>

                </div>
            </div>
        </div> -->
    </div>
</template>


<script>
import NavBar from '@/components/NavBar.vue';
import swal from 'sweetalert';
export default {
    components: {
        NavBar,
    },
    name: "Ticket",
    data() {
        return {
            ticket_id: '',
            ticket: {},
            comments: [],
            new_comment: '',
            currentUser_id: JSON.parse(localStorage.getItem("user_details")).user_id,
            sol: '',
            is_admin: localStorage.getItem("is_admin"),
            is_support: localStorage.getItem("is_support")

        }
    },
    methods: {

        is_solution(comment) {

            if (comment.solution) {
                this.sol = comment
                return true
            }
            return false
        },

        mark_solution(comment_id) {
            console.log("marked sol")
            const options = {
                method: 'PUT',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch(`http://127.0.0.1:5000/api/comments/${comment_id}/solution`, options)
                .then(response => response.json())
                .then(response => { this.get_comments(); this.get_ticket(); })
                .catch(err => console.error(err));
        },

        deleteComment(comment) {
            if (comment.solution) {
                this.sol.body = false
            }
            const options = {
                method: 'DELETE',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch(`http://127.0.0.1:5000/api/comments/${comment.comment_id}`, options)
                .then(response => response.json())
                .then(response => { this.get_comments() })
                .catch(err => console.error(err));
        },

        upvote() {
            console.log('clicked on upvote')
            const options = {
                method: 'POST',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}/upvote`, options)
                .then(response => {
                    if (response.status === 200) {
                        this.ticket.votes_count++;
                    } else if (response.status === 400) {
                        swal({
                            title: 'Already voted. Revoke vote ?',
                            buttons: true,
                        }).then((revoke) => {
                            if (revoke) {
                                this.revoke_vote()

                            }
                        });
                    }
                    return response.json();
                })
                .then(response => console.log(response))
                .catch(err => console.error(err));
        },

        revoke_vote() {
            const options = {
                method: 'DELETE',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}/revoke-vote`, options)
                .then(response => {
                    if (response.status === 200) {
                        this.ticket.votes_count--;
                    }
                })
                .then(response => console.log(response))
                .catch(err => console.error(err));
        },

        deleteticket() {

            swal({
                title: "Are you sure?",
                text: "Once deleted, you will not be able to recover this ticket!",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
                .then((willDelete) => {
                    if (willDelete) {
                        const options = {
                            method: 'DELETE',
                            headers: {
                                Authorization: localStorage.getItem("access_key")

                            }
                        };

                        fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}`, options)
                            .then(response => {
                                response.json();
                            })
                            .then(response => {
                                this.$router.push('/home')
                            })
                            .catch(err => console.error(err));

                    } else {
                        swal("Your ticket is safe!");
                    }
                });

        },

        close_ticket() {
            swal({
                title: "Are you sure?",
                text: "Once Closed, you will not be able to recover this ticket!",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
                .then((willclose) => {
                    if (willclose) {
                        const options = {
                            method: 'PUT',
                            headers: {
                                Authorization: localStorage.getItem("access_key")

                            }
                        };

                        fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}/close`, options)
                            .then(response => {
                                if (response.status === 200) {
                                    this.$router.push('/home')
                                }
                            })
                            .then(response => {

                            })
                            .catch(err => console.error(err));

                    } else {
                        swal("Your ticket is safe!");
                    }
                });

        },



        get_comments() {
            console.log("getting comments")
            const options = {
                method: 'GET',
                headers: {
                    Authorization: localStorage.getItem("access_key")
                }
            };

            fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}/comments`, options)
                .then(response => response.json())
                .then(response => { this.comments = response; })
                .catch(err => console.error(err));
        },

        post_comment() {
            console.log("clicked post comment")
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: localStorage.getItem("access_key")

                },
                body: `{"body":"${this.new_comment}"}`
            };

            fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}/comments`, options)
                .then(response => response.json())
                .then(response => {
                    this.get_comments();
                    this.new_comment = ''

                })
                .catch(err => console.error(err));
        },

        get_ticket() {
            console.log('Ticket', this.ticket_id)
            const options = {
                method: 'GET',
                headers: {
                    Authorization: localStorage.getItem("access_key")
                }
            };

            fetch(`http://127.0.0.1:5000/api/tickets/${this.ticket_id}`, options)
                .then(response => response.json())
                .then(response => { this.ticket = response })
                .catch(err => console.error(err));
        }

    },
    created() {

        console.log("created tocket page")
        this.ticket_id = this.$route.params.tid;

        //Get comments
        this.get_comments();

        // Get ticket details
        this.get_ticket()
    },



};

</script>


<style>
.bg-success-bck {
    --bs-bg-opacity: .6;
    background-color: rgba(var(--bs-success-rgb), var(--bs-bg-opacity)) !important;
}
</style>