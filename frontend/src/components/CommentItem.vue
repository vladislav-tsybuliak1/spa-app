<script>
import DOMPurify from 'dompurify';

export default {
  props: {
    comment: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      imageModalVisible: false,
      imageModalSrc: ''
    };
  },
  methods: {
    showEmail() {
      this.$emit('showEmail', this.comment);
    },
    showHomePage() {
      this.$emit('showHomePage', this.comment);
    },
    sanitizeHTML(html) {
      return DOMPurify.sanitize(html);
    },
    showImageModal(imageSrc) {
      this.imageModalSrc = imageSrc;
      this.imageModalVisible = true;
    },
    getMediaUrl(path) {
      const baseUrl = `${import.meta.env.VITE_API_URL}`; // Set your backend base URL here
      return `${baseUrl}${path}`;
    }
  },
};
</script>

<template>
  <div class="comment-item">
    <div class="comment-header">
      <p class="comment-user">
        {{ comment.user.username }}
        <span class="comment-date">
              at {{ new Date(comment.created_at).toLocaleString() }}
            </span>
      </p>
    </div>

    <p class="comment-text" v-html="sanitizeHTML(comment.text)"></p>

    <!-- Attached Image -->
    <div v-if="comment.attached_image" class="attached-image" @click="showImageModal(getMediaUrl(comment.attached_image))">
      <img :src="getMediaUrl(comment.attached_image)" alt="Attached Image"/>
    </div>

    <!-- Attached File -->
    <div v-if="comment.attached_file" class="attached-file">
      <a :href="getMediaUrl(comment.attached_file)" target="_blank">
        Attached file
      </a>
    </div>

    <div class="footer-buttons">
      <button @click="showEmail(comment)">Email</button>
      <button @click="showHomePage(comment)">Home page</button>
    </div>


    <!-- Display Replies -->
    <div v-if="comment.replies" class="replies">
      <comment-item
          v-for="childReply in comment.replies"
          :key="childReply.id"
          :comment="childReply"
          @showEmail="showEmail"
          @showHomePage="showHomePage"
      />
    </div>

    <!-- Image Modal -->
    <div v-if="imageModalVisible" class="image-modal" @click="imageModalVisible = false">
      <div class="image-modal-content">
        <img :src="imageModalSrc" alt="Modal Image" />
      </div>
    </div>

  </div>
</template>

<style scoped>
.comment-item {
  background-color: rgba(234, 222, 222, 0.85);
  border: 1px solid #444;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.comment-header {
  display: flex;
  font-size: 1em;
  margin-bottom: 10px;
}

.comment-user {
  font-weight: bold;
  color: #7a4b00;
}

.comment-date {
  color: #3e3d3d;
  font-weight: lighter;
  margin-left: 10px;
}

.comment-text {
  color: #150d17;
  margin-bottom: 10px;
}

.attached-image img {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.attached-image img:hover {
  transform: scale(1.05);
}

.attached-file a {
  display: inline-block;
  margin-top: 10px;
  color: #3498db;
  text-decoration: underline;
  font-size: 0.9em;
}

.attached-file a:hover {
  color: #5dade2;
}

.footer-buttons {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.footer-buttons button {
  background-color: #6a0dad;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.3s ease;
}

.footer-buttons button:hover {
  background-color: #8b5ed4;
}

.replies {
  margin-left: 20px;
  margin-top: 10px;
  border-left: 2px solid #555;
  padding-left: 15px;
}

.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.image-modal-content {
  max-width: 90%;
  max-height: 90%;
}

.image-modal-content img {
  width: 100%;
  height: auto;
  border-radius: 10px;
}

</style>
