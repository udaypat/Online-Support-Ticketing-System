<template>
  <div>
    <div id="heading">
      <h1>Smart Support</h1>

    </div>

    <main class="form-signin text-center">
      <form @submit.prevent="loginUser" method="post">
        <h1 class="h3 mb-3 fw-normal">Please sign in</h1>

        <div class="form-floating">
          <input type="username" name="user" class="form-control" id="floatingInput" placeholder="username"
            v-model="userdata.username" required />
          <label for="floatingInput">Username</label>
        </div>
        <div class="form-floating">
          <input type="password" name="passwd" class="form-control" id="floatingPassword" placeholder="Password" required
            v-model="userdata.password" />
          <label for="floatingPassword">Password</label>
        </div>
        <div>
          <button id="submitbtn" class="w-100 btn btn-lg btn-primary" type="submit">
            Sign in
          </button>
        </div>
        <br />
      </form>
      <div>
        <router-link class="w-100 btn btn-lg btn-secondary" to="/signup" type="button">Sign Up
        </router-link>
      </div>
      <br />
      <div v-if="this.errors.error" class="alert alert-danger" role="alert">
        Wrong {{ errors.type }}
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "SignIn",
  data() {
    return {
      userdata: {
        username: "",
        password: "",
      },
      errors: {
        error: false,
        type: "",
      },
      user_details: {},
    };
  },
  methods: {
    loginUser() {
      console.log("clicked submit");
      const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.userdata),
      };

      fetch("http://127.0.0.1:5000/api/user/login", options)
        .then((response) => response.json())
        .then((response) => {
          let token = response.access_token;
          if (token) {
            localStorage.clear();
            localStorage.setItem("access_key", "Bearer " + token);


            this.store_user()


          } else if (response.msg == "Bad username") {
            this.errors.error = true;
            this.errors.type = "Username";
          } else {
            this.errors.error = true;
            this.errors.type = "Password";
          }
        })
        .catch((err) => console.error(err));
    },
    store_user() {


      const options = {
        method: 'GET',
        headers: {
          Authorization: localStorage.getItem("access_key")
        }
      };

      fetch(`http://127.0.0.1:5000/api/user`, options)
        .then(response => response.json())
        .then(response => {
          localStorage.setItem("user_details", JSON.stringify(response));
          this.user_details = response
          this.store_roles()

        })
        .catch(err => console.error(err));
    },
    store_roles() {

      this.user_details.roles.forEach((item) => {
        console.log(item.name);
        if (item.name === "Student") {
          localStorage.setItem("is_student", true)
        }
        if (item.name === "Admin") { localStorage.setItem("is_admin", true); }
        if (item.name === "Support") { localStorage.setItem("is_support", true) }
      })
      this.$router.push("/home");
    }

  },
  created() {
    localStorage.clear();

  },
};
</script>

<style scoped>
html,
body {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="username"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
