<script>
import axios from 'axios';
import DOMPurify from 'dompurify';

export default {
  data() {
    return {
      commentText: '',
      commentHomePage: '',
      commentAttachedImage: null,
      commentAttachedFile: null,
      commentParent: null,
      comments: [],
      chosenComment: null,
      isEmailShown: false,
      isHomePageShown: false,
      errorMessage: null,
      successMessage: null,
    };
  },
  computed: {
    token() {
      return localStorage.getItem('access_token');
    }
  },
  methods: {
    sanitizeHTML(html) {
      return DOMPurify.sanitize(html);
    },
    async fetchComments() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/comments/`, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });
        this.comments = response.data;
      } catch (error) {
        this.errorMessage = 'Failed to load comments.';
        console.error(error.response.data);
      }
    },
    async addComment() {
      if (!this.commentText.trim()) {
        this.errorMessage = 'Comment text cannot be empty!';
        return;
      }
      try {
        const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/api/v1/comments/`,
            {text: this.commentText},
            {
              headers: {
                Authorization: `Bearer ${this.token}`,
                'Content-Type': 'application/json'
              },
            }
        );

        await this.fetchComments();
        this.commentText = '';
        this.commentHomePage = '';
        this.commentAttachedImage = null;
        this.commentAttachedFile = null;
        this.errorMessage = '';
        this.successMessage = 'Comment posted successfully!';
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'Failed to post comment.';
      }
    },
    showEmail(comment) {
      this.isEmailShown = true;
      this.chosenComment = comment;
    },
    showHomePage(comment) {
      this.isHomePageShown = true;
      this.chosenComment = comment;
    },
    closeWindow() {
      this.isEmailShown = false;
      this.isHomePageShown = false;
      this.chosenComment = null;
    },
  },
  mounted() {
    if (this.token) {
      this.fetchComments();
    }
  },
};
</script>

<template>
  <div class="comment-wrapper">
    <h2>Comments</h2>

    <!-- Show a warning if the user is not authenticated -->
    <div v-if="!this.token" class="auth-warning">
      <p>You must <a href="/login/"> login</a> to view or post comments.</p>
    </div>

    <!-- Show the comment form and comments if authenticated -->
    <div v-else>

      <!-- Error Message -->
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <!-- Success Message -->
      <p v-if="successMessage" class="success">{{ successMessage }}</p>

      <!-- List of Comments -->
      <div v-if="this.comments" class="comment-list">
        <div
            v-for="comment in comments"
            :key="comment.id"
            class="comment-item"
            @showEmail="showEmail"
            @showHomePage="showHomePage"
        >
          <p class="comment-user">{{ comment.user.username }}</p>
          <p class="comment-text" v-html="sanitizeHTML(comment.text)"></p>
          <p class="comment-date">
            {{ new Date(comment.created_at).toLocaleString() }}</p>
          <div class="footer-buttons">
            <button @click="showEmail(comment)">Email</button>
            <button @click="showHomePage(comment)">Home page</button>
          </div>
        </div>
      </div>
      <p v-else class="no-comments">No comments yet. Be the first to
        comment!</p>
    </div>
  </div>

  <div v-if="isEmailShown" class="show-window">
    <div class="show-window-content">
      <h3>{{ chosenComment.user.username }} email:</h3>
      <p>{{ chosenComment.user.email }}</p>
      <button @click="closeWindow" class="close-btn">X</button>
    </div>
  </div>

  <div v-if="isHomePageShown" class="show-window">
    <div class="show-window-content">
      <h3>{{ chosenComment.user.username }} home page:</h3>
      <p v-if="chosenComment.home_page">{{ chosenComment.home_page }}</p>
      <p v-else>the user didn't provide a home page url</p>
      <button @click="closeWindow" class="close-btn">X</button>
    </div>
  </div>


</template>

<style scoped>
.comment-wrapper {
  width: 80vi;
  margin: 20px auto;
  background: #1f0f24;
  color: wheat;
  padding: 20px;
  border-radius: 10px;
}


.auth-warning {
  text-align: center;
}

.auth-warning a {
  color: white;
}

.no-comments {
  margin-top: 20px;
}

.comment-list {
  margin-top: 20px;
}

.comment-item {
  border-bottom: 1px solid #ccc;
  padding: 10px 0;
}

.comment-user {
  font-weight: bold;
}

.comment-date {
  font-size: 0.9em;
  color: #bbb;
}

.comment-text {
  color: white;
}

.footer-buttons {
  display: flex;
  margin-top: 10px;
}

.footer-buttons button {
  background-color: #6a0dad;
  color: #fff;
  border: none;
  margin-right: 5px;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.3s ease;
}

.footer-buttons button:hover {
  background-color: #8b5ed4;
}

.show-window {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.show-window-content {
  background-color: #2a2a2a;
  color: wheat;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  text-align: center;
  position: relative;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  color: wheat;
  border: 2px solid wheat;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  font-size: 1.2em;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.close-btn:hover {
  background-color: wheat;
  color: #2a2a2a;
}

</style>
