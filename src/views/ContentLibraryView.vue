<template>
  <div class="content-library">
    <header class="library-header">
      <h1>Content Library</h1>
      <div class="actions">
        <button class="btn-upload" @click="showUploadDialog = true">
          <span class="icon">+</span> Upload Media
        </button>
        <div class="search">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search media files..." 
            @input="searchMedia"
          />
        </div>
        <div class="filters">
          <select v-model="typeFilter">
            <option value="">All Types</option>
            <option value="image">Images</option>
            <option value="video">Videos</option>
            <option value="audio">Audio</option>
            <option value="document">Documents</option>
          </select>
          <select v-model="sortBy">
            <option value="date">Date Added</option>
            <option value="name">File Name</option>
            <option value="size">File Size</option>
            <option value="type">File Type</option>
          </select>
        </div>
      </div>
    </header>

    <div class="library-content">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading your media files...</p>
      </div>
      
      <div v-else-if="!filteredMedia.length" class="empty-state">
        <div class="empty-icon">📁</div>
        <h3>No media files found</h3>
        <p v-if="searchQuery || typeFilter">Try adjusting your search or filters</p>
        <p v-else>Upload media files to get started</p>
        <button class="btn-primary" @click="showUploadDialog = true">Upload Media</button>
      </div>
      
      <div v-else class="media-grid">
        <div 
          v-for="item in filteredMedia" 
          :key="item.id" 
          class="media-item"
          :class="{'selected': selectedItems.includes(item.id)}"
          @click="toggleSelect(item.id)"
        >
          <div class="media-preview">
            <img v-if="item.type === 'image'" :src="item.url" :alt="item.name">
            <div v-else-if="item.type === 'video'" class="video-thumbnail">
              <span class="play-icon">▶</span>
              <img :src="item.thumbnail" :alt="item.name">
            </div>
            <div v-else class="file-icon">
              {{ getFileIcon(item.type) }}
            </div>
          </div>
          <div class="media-info">
            <h4 class="media-title">{{ item.name }}</h4>
            <div class="media-meta">
              <span>{{ formatFileSize(item.size) }}</span>
              <span>{{ formatDate(item.dateAdded) }}</span>
            </div>
            <div class="media-actions">
              <button @click.stop="copyUrl(item)" title="Copy URL">📋</button>
              <button @click.stop="downloadFile(item)" title="Download">⬇️</button>
              <button @click.stop="deleteFile(item.id)" title="Delete">🗑️</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedItems.length" class="batch-actions">
      <span>{{ selectedItems.length }} items selected</span>
      <button @click="deselectAll">Cancel</button>
      <button @click="downloadSelected">Download</button>
      <button @click="deleteSelected">Delete</button>
    </div>

    <div v-if="showUploadDialog" class="upload-dialog">
      <div class="dialog-content">
        <header>
          <h2>Upload Media</h2>
          <button @click="showUploadDialog = false" class="close-btn">×</button>
        </header>
        <div class="upload-area" @drop.prevent="handleFileDrop" @dragover.prevent>
          <input 
            type="file" 
            ref="fileInput" 
            multiple 
            @change="handleFileSelect" 
            style="display: none;"
          >
          <div class="drop-zone">
            <div class="upload-icon">📤</div>
            <p>Drag files here or <span @click="$refs.fileInput.click()" class="browse-link">browse</span></p>
            <p class="supported-formats">Supported formats: JPG, PNG, GIF, MP4, MP3, PDF</p>
          </div>
        </div>
        <div v-if="filesToUpload.length" class="upload-preview">
          <h3>Ready to upload ({{ filesToUpload.length }})</h3>
          <ul class="file-list">
            <li v-for="(file, index) in filesToUpload" :key="index">
              <span>{{ file.name }}</span>
              <span>{{ formatFileSize(file.size) }}</span>
              <button @click="removeFileFromUpload(index)">×</button>
            </li>
          </ul>
        </div>
        <div class="dialog-actions">
          <button @click="showUploadDialog = false" class="btn-cancel">Cancel</button>
          <button 
            @click="uploadFiles" 
            class="btn-upload" 
            :disabled="!filesToUpload.length || uploading"
          >
            <span v-if="uploading">Uploading...</span>
            <span v-else>Upload Files</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContentLibraryView',
  data() {
    return {
      loading: true,
      mediaItems: [],
      searchQuery: '',
      typeFilter: '',
      sortBy: 'date',
      selectedItems: [],
      showUploadDialog: false,
      filesToUpload: [],
      uploading: false,
      // Sample data for demo
      sampleMedia: [
        {
          id: 1,
          name: 'Product Photo.jpg',
          type: 'image',
          url: 'https://picsum.photos/id/1/300/200',
          size: 1240000,
          dateAdded: '2023-07-15T10:30:00',
        },
        {
          id: 2,
          name: 'Promo Video.mp4',
          type: 'video',
          url: '#',
          thumbnail: 'https://picsum.photos/id/25/300/200',
          size: 8500000,
          dateAdded: '2023-07-10T15:45:00',
        },
        {
          id: 3,
          name: 'Brand Guidelines.pdf',
          type: 'document',
          url: '#',
          size: 3200000,
          dateAdded: '2023-07-05T09:15:00',
        },
        {
          id: 4,
          name: 'Background Music.mp3',
          type: 'audio',
          url: '#',
          size: 4800000,
          dateAdded: '2023-07-01T14:20:00',
        },
        {
          id: 5,
          name: 'Team Photo.jpg',
          type: 'image',
          url: 'https://picsum.photos/id/91/300/200',
          size: 2100000,
          dateAdded: '2023-06-28T11:10:00',
        }
      ]
    }
  },
  computed: {
    filteredMedia() {
      let result = [...this.mediaItems];
      
      // Apply type filter
      if (this.typeFilter) {
        result = result.filter(item => item.type === this.typeFilter);
      }
      
      // Apply search
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(item => 
          item.name.toLowerCase().includes(query)
        );
      }
      
      // Apply sorting
      result.sort((a, b) => {
        switch(this.sortBy) {
          case 'name':
            return a.name.localeCompare(b.name);
          case 'size':
            return b.size - a.size;
          case 'type':
            return a.type.localeCompare(b.type);
          case 'date':
          default:
            return new Date(b.dateAdded) - new Date(a.dateAdded);
        }
      });
      
      return result;
    }
  },
  mounted() {
    // Simulate API loading
    setTimeout(() => {
      this.mediaItems = this.sampleMedia;
      this.loading = false;
    }, 1000);
  },
  methods: {
    searchMedia() {
      // This would normally debounce and call an API
      console.log('Searching for:', this.searchQuery);
    },
    
    toggleSelect(id) {
      const index = this.selectedItems.indexOf(id);
      if (index >= 0) {
        this.selectedItems.splice(index, 1);
      } else {
        this.selectedItems.push(id);
      }
    },
    
    deselectAll() {
      this.selectedItems = [];
    },
    
    downloadSelected() {
      // Implementation would call API to get download links
      console.log('Downloading selected items:', this.selectedItems);
      alert('Download started for ' + this.selectedItems.length + ' items');
      this.deselectAll();
    },
    
    deleteSelected() {
      if (confirm(`Are you sure you want to delete ${this.selectedItems.length} items?`)) {
        // Implementation would call API to delete items
        console.log('Deleting selected items:', this.selectedItems);
        this.mediaItems = this.mediaItems.filter(item => !this.selectedItems.includes(item.id));
        this.deselectAll();
      }
    },
    
    copyUrl(item) {
      // Implementation would copy URL to clipboard
      console.log('Copying URL for:', item.name);
      alert(`URL for ${item.name} copied to clipboard`);
    },
    
    downloadFile(item) {
      // Implementation would trigger download
      console.log('Downloading file:', item.name);
      alert(`Download started for ${item.name}`);
    },
    
    deleteFile(id) {
      if (confirm('Are you sure you want to delete this file?')) {
        // Implementation would call API to delete
        console.log('Deleting file with ID:', id);
        this.mediaItems = this.mediaItems.filter(item => item.id !== id);
      }
    },
    
    handleFileSelect(event) {
      const files = Array.from(event.target.files);
      this.addFilesToUpload(files);
    },
    
    handleFileDrop(event) {
      const files = Array.from(event.dataTransfer.files);
      this.addFilesToUpload(files);
    },
    
    addFilesToUpload(files) {
      this.filesToUpload.push(...files);
    },
    
    removeFileFromUpload(index) {
      this.filesToUpload.splice(index, 1);
    },
    
    uploadFiles() {
      this.uploading = true;
      
      // Simulate upload
      setTimeout(() => {
        // Implementation would call API to upload files
        console.log('Uploading files:', this.filesToUpload);
        
        // Add new files to the library
        const newFiles = this.filesToUpload.map((file, index) => {
          const id = this.mediaItems.length + index + 1;
          let type = 'document';
          if (file.type.startsWith('image/')) type = 'image';
          if (file.type.startsWith('video/')) type = 'video';
          if (file.type.startsWith('audio/')) type = 'audio';
          
          return {
            id,
            name: file.name,
            type,
            url: type === 'image' ? URL.createObjectURL(file) : '#',
            thumbnail: type === 'video' ? 'https://picsum.photos/300/200?random=' + id : null,
            size: file.size,
            dateAdded: new Date().toISOString()
          };
        });
        
        this.mediaItems.unshift(...newFiles);
        this.filesToUpload = [];
        this.uploading = false;
        this.showUploadDialog = false;
        
        alert('Upload complete!');
      }, 2000);
    },
    
    getFileIcon(type) {
      switch(type) {
        case 'document': return '📄';
        case 'audio': return '🎵';
        case 'video': return '🎬';
        default: return '📁';
      }
    },
    
    formatFileSize(bytes) {
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + ' KB';
      return Math.round(bytes / (1024 * 1024) * 10) / 10 + ' MB';
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    }
  }
}
</script>

<style scoped>
.content-library {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.library-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  gap: 15px;
}

.library-header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
}

.actions {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.btn-upload {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn-upload:hover {
  background-color: #3a80d2;
}

.search input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

.filters {
  display: flex;
  gap: 10px;
}

.filters select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.library-content {
  flex: 1;
  overflow-y: auto;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #ccc;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #4a90e2;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.media-item {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  cursor: pointer;
}

.media-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.media-item.selected {
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.3);
}

.media-preview {
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  position: relative;
}

.media-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-icon {
  font-size: 3rem;
  color: #aaa;
}

.video-thumbnail {
  position: relative;
  width: 100%;
  height: 100%;
}

.video-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.media-info {
  padding: 12px;
}

.media-title {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.media-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 8px;
}

.media-actions {
  display: flex;
  justify-content: flex-end;
  gap: 5px;
}

.media-actions button {
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.media-actions button:hover {
  opacity: 1;
}

.batch-actions {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  background-color: #f5f5f5;
  border-top: 1px solid #eee;
  gap: 10px;
  margin-top: 20px;
}

.batch-actions span {
  margin-right: auto;
  font-weight: 500;
}

.batch-actions button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.batch-actions button:first-of-type {
  background-color: #f0f0f0;
}

.batch-actions button:nth-of-type(2) {
  background-color: #4a90e2;
  color: white;
}

.batch-actions button:last-of-type {
  background-color: #e25c5c;
  color: white;
}

.upload-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.dialog-content header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.dialog-content h2 {
  margin: 0;
  font-size: 1.4rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #888;
}

.upload-area {
  padding: 20px;
}

.drop-zone {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  transition: all 0.2s;
}

.drop-zone:hover {
  border-color: #4a90e2;
  background-color: rgba(74, 144, 226, 0.05);
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 10px;
  color: #ccc;
}

.browse-link {
  color: #4a90e2;
  cursor: pointer;
  text-decoration: underline;
}

.supported-formats {
  font-size: 0.8rem;
  color: #888;
  margin-top: 10px;
}

.upload-preview {
  padding: 0 20px 20px;
}

.upload-preview h3 {
  font-size: 1rem;
  margin: 0 0 10px 0;
}

.file-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 4px;
}

.file-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #eee;
}

.file-list li:last-child {
  border-bottom: none;
}

.file-list button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #e25c5c;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  padding: 15px 20px;
  border-top: 1px solid #eee;
  gap: 10px;
}

.btn-cancel {
  background-color: #f0f0f0;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .library-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .actions {
    width: 100%;
  }
  
  .search input {
    width: 100%;
  }
  
  .media-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }
}
</style> 