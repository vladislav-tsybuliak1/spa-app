<script>
import axios from 'axios';
import CommentItem from './CommentItem.vue';

export default {
  components: {CommentItem},
  data() {
    return {
      commentText: '',
      commentHomePage: '',
      commentAttachedImage: null,
      commentAttachedFile: null,
      comments: [],
      chosenComment: null,
      isEmailShown: false,
      isHomePageShown: false,
      isCommentFormVisible: false,
      errorMessage: null,
      successMessage: null,
      attachedFilePreview: '',
      captcha: {
        key: '',
        imageUrl: '',
      },
      captchaResponse: '',
      isCaptchaVerified: false,
      currentPage: 1,
      totalPages: 0,
      nextPageUrl: null,
      prevPageUrl: null,
      orderBy: 'created_at',
      orderDirection: 'asc',
    };
  },
  computed: {
    token() {
      return localStorage.getItem('access_token');
    }
  },
  methods: {
    async fetchComments(url = `${import.meta.env.VITE_API_URL}/api/v1/comments/`) {
      try {
        const ordering = `${this.orderDirection === 'desc' ? '-' : ''}${this.orderBy}`;
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
          params: {
            ordering,
          },
        });
        this.comments = response.data.results;
        this.totalPages = response.data.pages;
        this.nextPageUrl = response.data.next;
        this.prevPageUrl = response.data.previous;
        this.currentPage = new URL(url).searchParams.get('page') || 1;
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

      await this.validateCaptcha();
      if (!this.isCaptchaVerified) {
        return;
      }

      try {
        const formData = new FormData();
        formData.append('text', this.commentText);
        if (this.commentHomePage) {
          formData.append('home_page', this.commentHomePage);
        }
        if (this.commentAttachedImage) {
          formData.append('attached_image', this.commentAttachedImage);
        }
        if (this.commentAttachedFile) {
          formData.append('attached_file', this.commentAttachedFile);
        }
        if (this.chosenComment) {
          formData.append('parent', this.chosenComment.id);
        }
        const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/api/v1/comments/`,
            formData,
            {
              headers: {
                Authorization: `Bearer ${this.token}`,
                'Content-Type': 'multipart/form-data'
              },
            }
        );

        await this.fetchComments();
        await this.refreshCaptcha();
        this.resetCommentAttr();
        this.errorMessage = '';
        this.successMessage = 'Comment posted successfully!';
      } catch (error) {
        if (error.response && error.response.data) {
          const errors = error.response.data;
          if (errors.text) {
            this.errorMessage += 'Text: ' + errors.text.join(', ') + ' ';
          }
          if (errors.home_page) {
            this.errorMessage += 'Home page: ' + errors.home_page.join(', ') + ' ';
          }
          if (errors.attached_image) {
            this.errorMessage += 'Image: ' + errors.attached_image.join(', ') + ' ';
          }
          if (errors.attached_file) {
            this.errorMessage += 'File: ' + errors.attached_file.join(', ') + ' ';
          }
          if (errors.parent) {
            this.errorMessage += 'Comment: ' + errors.parent.join(', ') + ' ';
          }
        }
      }
    },
    async fetchCaptcha() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/get-captcha/`);
        this.captcha.key = response.data.key;
        this.captcha.imageUrl = response.data.image_url;
      } catch (error) {
        console.error('Error fetching CAPTCHA:', error);
      }
    },
    async refreshCaptcha() {
      await this.fetchCaptcha();
      this.captchaResponse = '';
      this.isCaptchaVerified = false;
    },
    async validateCaptcha() {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/validate-captcha/`,
            {
              captcha_0: this.captcha.key,
              captcha_1: this.captchaResponse,
            },
            {
              headers: {
                'Authorization': `Bearer ${this.token}`,
              }
            }
        );
        this.isCaptchaVerified = true;
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.captcha
        } else {
          this.errorMessage = 'An error occurred! Please try again later.';
        }
      }
    },
    getCaptchaImageUrl() {
      return `${import.meta.env.VITE_API_URL}` + this.captcha.imageUrl
    },
    showEmail(comment) {
      this.isEmailShown = true;
      this.chosenComment = comment;
    },
    showHomePage(comment) {
      this.isHomePageShown = true;
      this.chosenComment = comment;
    },
    replyToComment(comment) {
      this.chosenComment = comment;
      this.toggleCommentForm()
    },
    resetCommentAttr() {
      this.commentText = '';
      this.commentHomePage = '';
      this.commentAttachedImage = null;
      this.commentAttachedFile = null;
      this.chosenComment = null;
    },
    closeWindow() {
      this.resetCommentAttr();
      this.isEmailShown = false;
      this.isHomePageShown = false;
      this.isCommentFormVisible = false;
    },
    clearSuccess() {
      this.successMessage = '';
      this.isCommentFormVisible = false;
    },
    clearError() {
      this.errorMessage = '';
    },
    toggleCommentForm() {
      this.isCommentFormVisible = true;
    },
    onImageChange(event) {
      const image = event.target.files[0];
      if (image) {
        this.commentAttachedImage = image;
        console.log("Image" + this.commentAttachedImage)
        console.log("File" + this.commentAttachedFile)
        this.attachedFilePreview = URL.createObjectURL(image);
      }
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.commentAttachedFile = file;
        console.log(this.commentAttachedFile)
        console.log(this.commentAttachedImage)
      }
    },
    clearAttachedFile() {
      this.commentAttachedImage = null;
      this.commentAttachedFile = null;
      this.attachedFilePreview = '';
    },
    logOut() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      this.$router.push('/login');
    }
  },
  mounted() {
    if (this.token) {
      this.fetchComments();
    }
    this.refreshCaptcha();
  },
};
</script>

<template>
  <div v-if="!token" class="auth-warning">
    <p>You must <a href="/login/"> login</a> to view or post comments.</p>
  </div>

  <div v-else class="comment-wrapper">
    <div class="comment-header">
      <div>
        <h2>Comments</h2>
        <button @click="toggleCommentForm">Write a comment</button>
      </div>
      <button @click="logOut">Logout</button>
    </div>

    <div class="ordering-pagination">

      <div class="pagination-controls">
        <button
            :disabled="!prevPageUrl"
            @click="fetchComments(prevPageUrl)">
          Previous
        </button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button
            :disabled="!nextPageUrl"
            @click="fetchComments(nextPageUrl)">
          Next
        </button>
      </div>

      <div class="ordering-controls">
        <label for="orderBy">Order By:</label>
        <select id="orderBy" v-model="orderBy" @change="fetchComments()">
          <option value="user__username">Username</option>
          <option value="user__email">Email</option>
          <option value="created_at">Date Created</option>
        </select>

        <label for="orderDirection">Direction:</label>
        <select id="orderDirection" v-model="orderDirection"
                @change="fetchComments()">
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
      </div>

    </div>


    <!-- List of Comments -->
    <div v-if="comments" class="comment-list">
      <comment-item
          v-for="comment in comments"
          :key="comment.id"
          :comment="comment"
          @showEmail="showEmail"
          @showHomePage="showHomePage"
          @replyToComment="replyToComment"
      />
    </div>
    <p v-else class="no-comments">No comments yet. Be the first to
      comment!
    </p>
  </div>

  <div v-if="isCommentFormVisible" class="show-window">
    <div class="show-window-content">
      <div class="show-window-header">
        <p v-if="chosenComment">
          Replying to <strong>{{ chosenComment.user.username }}</strong>
        </p>
        <p v-else>Create a new comment</p>
      </div>

      <textarea v-model="commentText" placeholder="Enter your text here..."
                rows="8" cols="45"></textarea>
      <input type="url" v-model="commentHomePage"
             placeholder="Enter your home page (optional)"/>

      <p class="file-label">Choose image file (optional):</p>
      <input type="file" @change="onImageChange" accept="image/*"/>
      <div v-if="commentAttachedImage">
        <img :src="attachedFilePreview" alt="Attached file"
             class="attached-file-preview"/>
      </div>

      <p class="file-label">Choose .txt file (optional):</p>
      <input type="file" @change="onFileChange" accept="text/plain"/>
      <div v-if="commentAttachedFile">
        <p class="attached-file-preview">{{ commentAttachedFile.name }}</p>
      </div>

      <div class="captcha">
        <img :src="getCaptchaImageUrl()" alt="Captcha"/>
        <button class="captcha-refresh-btn" @click="refreshCaptcha">Refresh
          CAPTCHA
        </button>
      </div>
      <input
          v-model="captchaResponse"
          type="text"
          placeholder="Enter CAPTCHA text"
          required
      />

      <div class="show-window-footer">
        <button type="button" @click="clearAttachedFile" class="clear-btn">
          Clear Attached File(s)
        </button>

        <button @click="addComment" class="add-comment-btn">Post Comment
        </button>
      </div>

      <button @click="closeWindow" class="close-btn">X</button>
    </div>
  </div>

  <div v-if="successMessage" class="show-window">
    <div class="show-window-content">
      <p class="success">{{ successMessage }}</p>
      <button @click="clearSuccess()" class="close-btn">X</button>
    </div>
  </div>

  <div v-if="errorMessage" class="show-window">
    <div class="show-window-content">
      <p class="error">{{ errorMessage }}</p>
      <button @click="clearError()" class="close-btn">X</button>
    </div>
  </div>

  <div v-if="isEmailShown" class="show-window">
    <div class="show-window-content">
      <h3>{{ chosenComment.user.username }} email:</h3>
      <p>{{ chosenComment.user.email }}</p>
      <button @click="closeWindow()" class="close-btn">X</button>
    </div>
  </div>

  <div v-if="isHomePageShown" class="show-window">
    <div class="show-window-content">
      <h3>{{ chosenComment.user.username }} home page:</h3>
      <p v-if="chosenComment.home_page">{{ chosenComment.home_page }}</p>
      <p v-else>the user didn't provide a home page url</p>
      <button @click="closeWindow()" class="close-btn">X</button>
    </div>
  </div>


</template>

<style scoped>

.comment-wrapper {
  width: 80vi;
  margin: 20px auto;
  color: #151513;
  padding: 20px;
  border-radius: 10px;
}

.comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #f39c12;
  padding: 10px 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-header h2 {
  margin: 0;
  color: #2d2d2d;
  font-size: 24px;
  font-weight: bold;
}

.comment-header button {
  background-color: #ffffff;
  color: #2d2d2d;
  margin-left: 15px;
  border: 1px solid #2d2d2d;
  border-radius: 5px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.comment-header button:hover {
  background-color: #2d2d2d;
  color: #ffffff;
}

.comment-header div {
  display: flex;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination-controls button {
  margin: 0 10px;
  padding: 5px 15px;
  font-size: 18px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.pagination-controls button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination-controls span {
  font-size: 18px;
}

.ordering-controls {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  gap: 15px;
}

.ordering-controls select {
  padding: 5px 10px;
  font-size: 14px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.ordering-controls label {
  font-size: 18px;
  padding: 5px 10px;
}

.ordering-pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
}

textarea {
  width: 90%;
  margin-bottom: 10px;
}

input[type="url"],
input[type="file"],
input[type="text"] {
  width: 85%;
  margin-bottom: 10px;
}

.attached-file-preview {
  max-width: 100%;
  max-height: 100px;
  display: block;
  margin-left: 20px;
  margin-bottom: 10px;
  text-align: left;
}

.auth-warning {
  text-align: center;
  padding: 30px;
  color: orangered;
}

.auth-warning a {
  color: white;
}

.file-label {
  text-align: left;
  margin-left: 25px;
}

.no-comments {
  margin-top: 20px;
}

.comment-list {
  margin-top: 20px;
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
  padding: 30px 50px 20px 20px;
  border-radius: 10px;
  width: 400px;
  text-align: center;
  position: relative;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}

.show-window-header {
  margin-bottom: 20px;
  font-size: 25px;
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

.show-window-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 20px;
}

.captcha {
  display: flex;
  margin: 20px;
}

.captcha-refresh-btn,
.show-window-footer button {
  border: 1px solid #2d2d2d;
  border-radius: 5px;
  padding: 8px 12px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.captcha-refresh-btn {
  background-color: #005e7a;
  color: white;
  margin-left: 10px;
}

.captcha-refresh-btn:hover {
  background-color: #138baf;
}

.clear-btn {
  background-color: #553703;
  color: #ffffff;
}

.clear-btn:hover {
  background-color: #976309;
}

.add-comment-btn {
  background-color: #205e04;
  color: #ffffff;
}

.add-comment-btn:hover {
  background-color: #3cc106;
}

</style>
