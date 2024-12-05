<script>
import axios from "axios"

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      successMessage: '',
    }
  },
methods: {
    async logIn() {
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/api/v1/users/token/`,
          {
            username: this.username,
            password: this.password,
          }
        );


        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);

        this.successMessage = 'Login successful!';

        this.$router.push('/comments/');
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.detail || 'Login failed!';
        } else {
          this.errorMessage = 'An error occurred. Please try again.';
        }
      }
    },
  },
}
</script>

<template>
  <div class="wrapper">
    <h1>Sign in to SPA</h1>

    <!-- Error and Success Messages -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>

    <!-- Sign in Form -->
    <form @submit.prevent="register">
      <div class="form-group">
        <input
            type="text"
            v-model="username"
            placeholder="Username"
            required
        />
      </div>
      <div class="form-group">
        <input
            type="password"
            v-model="password"
            placeholder="Password"
            required
        />
      </div>
      <button class="btn"
              v-if="username && password"
              @click="logIn()">Login
      </button>
      <button class="btn" v-else disabled>Fill all the fields</button>
    </form>

    <div class="register-info">
      <p><a href="/register/">Register</a> if you are not registered yet</p>
    </div>

  </div>
</template>

<style scoped>

.register-info {
  padding: 20px;
}

.register-info a {
  color: white;
}

</style>