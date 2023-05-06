<template>
    <NavBar></NavBar>
    <div class="container mt-4">
        <div class="row">
            <div class="col">
                <div class="d-flex flex-column justify-content-right align-items-left">
                    <h2> Tickets</h2>



                    <table class="table table-borderless table-group-divider">
                        <thead>
                            <tr>
                                <th>User ID</th>
                                <th>Username</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Roles</th>

                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in user_list">

                                <td>{{ user.user_id }}</td>
                                <td>{{ user.username }}</td>
                                <td>{{ user.first_name }} {{ user.last_name }}</td>
                                <td>{{ user.email }}</td>

                                <!-- <td>
                                    <label class="role-label" v-for="role in roles" :key="role.role_id">
                                        <input type="checkbox"
                                            :checked="user.roles.some(userRole => userRole.role_id === role.role_id)"
                                            v-model="user.roles" :value="role">
                                        {{ role.name }}
                                    </label>
                                </td> -->
                                <td>
                                    <label class="role-label" v-for="role in roles" :key="role.role_id">
                                        <input type="checkbox"
                                            :checked="user.roles.some(userRole => userRole.role_id === role.role_id)"
                                            v-model="user.roles" :value="role"
                                            :disabled="!editing || selectedUser !== user" />
                                        {{ role.name }}
                                    </label>
                                    <button class="btn btn-primary" v-if="user ===
                                        selectedUser && editing" @click="update_roles">Save</button>

                                    <button v-else class="btn btn-primary float-right"
                                        @click="toggleEditing(user)">Edit</button>

                                    <button class="btn btn-warning m-1" data-bs-toggle="modal" data-bs-target="#tagsModal"
                                        @click="change_tags(user)">Assign Tags</button>

                                </td>


                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>





    <!-- Modal -->
    <div class="modal fade" id="tagsModal" tabindex="-1" aria-labelledby="tagsModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="tagsModalLabel">Tags</h5>
                    <button type="button" class="btn-close" id="close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-6">
                            <h6>Assigned Tags</h6>
                            <ul class="list-group">
                                <li v-if="selectedUser" v-for="tag in selectedUser.tags" class="list-group-item">{{ tag.name
                                }}
                                </li>
                            </ul>
                        </div>
                        <div class="col-6">
                            <h6>Available Tags</h6>
                            <ul class="list-group">
                                <li class="list-group-item" v-for="tag in avaliable_tags">
                                    <div class="form-check">
                                        <input v-model="seleted_tag" class="form-check-input" type="radio"
                                            name="available-tag" :id="tag.tag_id" :value="tag.tag_id">
                                        <label class="form-check-label" :for="tag.tag_id">
                                            {{ tag.name }}
                                        </label>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <hr>
                    <div class="row">
                        <div class="col-12">
                            <form id="add-tag-form" class="row g-2">
                                <div class="col-8">
                                    <input type="text" v-model="new_tag" class="form-control" placeholder="New Tag Name">
                                </div>
                                <div class="col-4">
                                    <button type="button" class="btn btn-primary" @click="add_tag">Add Tag</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" @click="update_tags">Save changes</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
    components: {
        NavBar,
    },
    data() {
        return {


            user_list: [],
            new_tag: "",
            roles: [
                {
                    "description": null,
                    "name": "Admin",
                    "role_id": 1
                },

                {
                    "description": null,
                    "name": "Support",
                    "role_id": 2
                },
                {
                    "description": null,
                    "name": "Student",
                    "role_id": 3
                },
            ],
            userRole: {},
            editing: false,
            selectedUser: null,
            user_object: {
                username: '',
                roles: []
            },
            tag_list: [],
            avaliable_tags: [],
            seleted_tag: ''


        }
    },
    methods: {

        toggleEditing(user) {
            if (this.selectedUser === user) {

                this.editing = !this.editing;
            } else {
                this.selectedUser = user;
                this.editing = true;
            }
        },

        change_tags(user) {
            this.selectedUser = user;

            this.avaliable_tags = this.tag_list.filter(a => !this.selectedUser.tags.map(b => b.tag_id).includes(a.tag_id))
        },

        update_tags() {

            const tag_obj = {
                "username": this.selectedUser.username,
                "tag_id": this.seleted_tag
            }

            console.log(tag_obj)
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: localStorage.getItem("access_key")

                },
                body: JSON.stringify(tag_obj)
            };

            fetch('http://127.0.0.1:5000/api/user/tags', options)
                .then(response => {
                    if (response.status == 200) {
                        document.getElementById('close').click();
                        this.get_users()
                        this.get_tags()
                        this.seleted_tag = ''
                        this.selectedUser = ''
                        // this.$router.go()
                    }
                })
                .then(response => { })
                .catch(err => console.error(err));
        },

        update_roles() {

            console.log('update user')
            // console.log(JSON.stringify(this.selectedUser))
            this.user_object.username = this.selectedUser.username
            this.user_object.roles = this.selectedUser.roles.map(role => role.name);
            console.log(JSON.stringify(this.user_object))
            const options = {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: localStorage.getItem("access_key")

                },
                body: JSON.stringify(this.user_object)
            };

            fetch('http://127.0.0.1:5000/api/user/roles', options)
                .then(response => {
                    if (response.status == 200) {

                        this.editing = false;
                        this.get_users()
                    }
                })
                .then(response => console.log(response))
                .catch(err => console.error(err));

        },
        get_users() {
            console.log('gettng users')
            const options = {
                method: 'GET',
                headers: {
                    Authorization: localStorage.getItem("access_key")

                }
            };

            fetch('http://127.0.0.1:5000/api/user/all', options)
                .then(response => response.json())
                .then(response => this.user_list = response)
                .catch(err => console.error(err));
        },
        get_tags() {
            //Get list of tags

            fetch(`http://127.0.0.1:5000/api/tags`, {
                headers: { Authorization: localStorage.getItem("access_key") },
            })
                .then((res) => res.json())
                .then((res) => {
                    this.tag_list = res

                });
        },
        add_tag() {
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: localStorage.getItem("access_key")


                },
                body: JSON.stringify({ "name": this.new_tag })
            };

            fetch('http://127.0.0.1:5000/api/tags', options)
                .then(response => {
                    if (response.status == 200) {
                        document.getElementById('close').click();
                        // this.$router.go()
                        this.get_users()
                        this.get_tags()
                        this.seleted_tag = ''
                        this.selectedUser = ''
                        this.new_tag = ''
                    }
                })
                .then(response => console.log(response))
                .catch(err => console.error(err));
        }
    },
    created() {
        this.get_users()
        this.get_tags()
    },

}
</script>

<style>
.role-label {
    display: inline-block;
    margin-right: 10px;
}

/* 
.btn {
    width: 70px;
    
} */
</style>