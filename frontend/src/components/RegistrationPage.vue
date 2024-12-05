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
        this.errorMessage = "Passwords do not match!";
        return;
      }

      try {
        await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/users/register/`, {
          username: this.username,
          email: this.email,
          password: this.password
        });
        this.successMessage = "Registration successful! You can now log in."
      } catch (error) {
        if (error.response && error.response.data) {
        const errors = error.response.data;

        if (errors.username) {
            this.errorMessage += "Username: " + errors.username.join(', ') + ' ';
        }
        if (errors.email) {
            this.errorMessage += "Email: " + errors.email.join(', ') + ' ';
        }
        if (errors.password) {
            this.errorMessage += "Password: " + errors.password.join(', ');
        }
    } else {
        this.errorMessage = "An error occurred! Please try again later.";
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
  </div>
</template>

<style scoped>

.wrapper {
  width: 400px;
  margin: auto;
  padding: 20px;
  border-radius: 10px;
  background-color: #1f0f24;
  color: wheat;
  text-align: center;
}

.wrapper h1 {
  margin-bottom: 20px;
}

.form-group {
  margin: 15px 0;
}

input {
  width: 90%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
}

input:focus {
  outline: none;
  border-color: #007bff;
}

.btn:disabled {
  cursor: not-allowed;
}

.btn {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 500ms ease;
}

.btn:hover {
  background-color: #0056b3;
  transform: scale(1.1) translateY(-5px);
}

.error {
  color: #ff4d4d;
  margin-bottom: 10px;
}

.success {
  color: #4caf50;
  margin-bottom: 10px;
}

</style>
