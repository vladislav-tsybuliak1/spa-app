<script>
import axios from "axios"

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      errorMessage: '',
      successMessage: '',
    }
  },
  methods: {
    async signUp() {
      this.errorMessage = '';
      this.successMessage = '';

      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Passwords do not match!';
        return;
      }

      try {
        await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/users/register/`, {
          username: this.username,
          email: this.email,
          password: this.password
        });
        this.successMessage = 'Registration successful! You can now log in.';
        this.username = '';
        this.email = '';
        this.password = '';
        this.confirmPassword = '';
      } catch (error) {
        if (error.response && error.response.data) {
        const errors = error.response.data;

        if (errors.username) {
            this.errorMessage += 'Username: ' + errors.username.join(', ') + ' ';
        }
        if (errors.email) {
            this.errorMessage += 'Email: ' + errors.email.join(', ') + ' ';
        }
        if (errors.password) {
            this.errorMessage += 'Password: ' + errors.password.join(', ');
        }
    } else {
        this.errorMessage = 'An error occurred! Please try again later.';
    }
      }
    }
  }
}
</script>

<template>
  <div class="wrapper">
    <h1>Sign up to SPA</h1>

    <!-- Error and Success Messages -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>

    <!-- Registration Form -->
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
            type="email"
            v-model="email"
            placeholder="Email"
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
      <div class="form-group">
        <input
            type="password"
            v-model="confirmPassword"
            placeholder="Confirm Password"
            required
        />
      </div>
      <button class="btn"
              v-if="username && email && password && confirmPassword"
              @click="signUp()">Register
      </button>
      <button class="btn" v-else disabled>Fill all the fields</button>
    </form>

    <div class="login-info">
      <p><a href="/login/">Log in</a> if you are registered already</p>

    </div>

  </div>
</template>

<style scoped>

.login-info {
  padding: 20px;
}

.login-info a {
  color: white;
}

</style>
