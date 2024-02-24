import React, { useState } from 'react';
import styles from '../../Post.module.css';

const publicIconUrl = "https://cdn-icons-png.flaticon.com/512/2889/2889676.png";
const imageiconUrl = "data:image/png;base64,..."; // Your base64 image
const usericonUrl = "https://cdn-icons-png.flaticon.com/512/149/149071.png";

interface CreatePostProps {
  username?: string; // Assuming username is passed as a prop to this component
}

const Post: React.FC<CreatePostProps> = ({ username }) => {
  const [content, setContent] = useState('');
  const [visibility, setVisibility] = useState('public');
  const [isMarkdownEnabled, setMarkdownEnabled] = useState(false);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [imageUploadUrl, setImageUploadUrl] = useState('');

  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(e.target.value);
  };

  const handleVisibilityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setVisibility(e.target.value);
  };

  const handleMarkdownToggle = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMarkdownEnabled(e.target.checked);
  };

  const handlePostSubmit = () => {
    // Here you would handle the submission of the post
    console.log('Post submitted with content:', content);
  };

  const handleImageUpload = () => {
    // Here you would handle the uploading of the image using the provided URL
    setImageUrl(imageUploadUrl);
  };

  return (
    <div className={styles.createPostContainer}>
      <div className={styles.userInput}>
        <img src={usericonUrl} alt="User" className={styles.userIcon} />
        <span>{username}</span>
        <textarea
          className={styles.textarea}
          placeholder="What's on your mind?"
          value={content}
          onChange={handleContentChange}
        />
        {isMarkdownEnabled && (
          <div>
            <input
              type="text"
              placeholder="Enter image URL..."
              value={imageUploadUrl}
              onChange={(e) => setImageUploadUrl(e.target.value)}
              className={styles.textInput}
            />
            <button onClick={handleImageUpload} className={styles.uploadButton}>
              Upload Image
            </button>
          </div>
        )}
      </div>
      <div className={styles.options}>
        <img src={publicIconUrl} alt="Public" className={styles.icon} />
        <select
          className={styles.visibilitySelect}
          value={visibility}
          onChange={handleVisibilityChange}
        >
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
        <label className={styles.markdownToggle}>
          Enable Markdown
          <input
            type="checkbox"
            checked={isMarkdownEnabled}
            onChange={handleMarkdownToggle}
          />
        </label>
        <img src={imageiconUrl} className={styles.icon} />
        {imageUrl && <img src={imageUrl} alt="Preview" className={styles.imagePreview} />}
        <button onClick={handlePostSubmit} className={styles.postButton}>
          Post
        </button>
      </div>
    </div>
  );
};

export default Post;
