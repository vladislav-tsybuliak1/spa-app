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
      errorMessage: null,
      successMessage: null,
    };
  },
  computed: {
    token () {
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

        >
          <p class="comment-user">{{ comment.user.username }}</p>
          <p class="comment-text" v-html="sanitizeHTML(comment.text)"></p>
          <p class="comment-date">{{ new Date(comment.created_at).toLocaleString() }}</p>
        </div>
      </div>
      <p v-else class="no-comments">No comments yet. Be the first to
        comment!</p>
    </div>
  </div>
</template>

<style scoped>
.comment-wrapper {
  width: 80vi;
  margin: 0 auto;
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

.comment-text{
  color: white;
}

</style>
