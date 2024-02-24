import React, { useState } from 'react';
import styles from '../../Post.module.css';
import axios from "axios";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
//import { useNavigate } from "react-router-dom";

const publicIconUrl = "https://cdn-icons-png.flaticon.com/512/2889/2889676.png";
const imageiconUrl = "data:image/png;base64,..."; // Your base64 image
//const usericonUrl = "https://cdn-icons-png.flaticon.com/512/149/149071.png";

interface CreatePostProps {
  username?: string; // Assuming username is passed as a prop to this component
  display_name?: string;
  user_img_url?: string;
}

const myToast: ToastOptions = {
  position: "top-center",
  autoClose: 1000,
  hideProgressBar: true,
  closeOnClick: true,
  closeButton: false,
  pauseOnHover: false,
  draggable: false,
  progress: undefined,
};

const Post: React.FC<CreatePostProps> = ({ username, user_img_url }) => {
  const [content, setContent] = useState('');
  const [visibility, setVisibility] = useState('public');
  const [isMarkdownEnabled, setMarkdownEnabled] = useState(false);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [imageUploadUrl, setImageUploadUrl] = useState('');
  const [imagePostId, setImagePostId] = useState('');
  //const nav = useNavigate();

  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(e.target.value);
  };

  const handleVisibilityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setVisibility(e.target.value);
  };

  const handleMarkdownToggle = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMarkdownEnabled(e.target.checked);
  };

  const handlePostSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {     

      const formField = new FormData();
      formField.append("content", content);
      formField.append("attached_img_post", imagePostId) // if an image was added link to it in the 
      formField.append("visibility", visibility)
      
      const response = await axios.post("/make_post", formField);

      if (response.data.success) {
        
        console.log("Post Created Successfully");
        
        toast.success("Post Created Successfully", myToast);
        setTimeout(() => { // Reference: https://stackoverflow.com/questions/75920012/react-toast-when-navigate by inkredusk 2024-02-24
          window. location. reload();
        }, 1000); 

      } else {
        console.log("Failed to create post");
        toast.error("Failed to create post", myToast);
      }

      } catch (error) {
        console.error("An error occurred", error);
        toast.error("An error occurred", myToast);
      }
    };

  const handleImageUpload = async () => {
    try {
    // Here you would handle the uploading of the image using the provided URL
    const formField = new FormData();
    formField.append("image_url", imageUploadUrl);
    const response = await axios.post("/make_post", formField);
    if (response.data.success) {
      setImagePostId(response.data["post_id"])
      toast.success("Image uploaded Successfully", myToast);
      console.log("Image uploaded Successfully");

    } else {
      console.log("Failed to upload Image");
      toast.error("Failed to upload Image", myToast);
    }

    } catch (error) {
      console.error("An error occurred", error);
      toast.error("An error occurred", myToast);
    }
    setImageUrl(imageUploadUrl);
  }

  return (
    
    <div className={styles.createPostContainer}>
      <ToastContainer />
      <div className={styles.userInput}>
        <img src={user_img_url} alt="https://cdn-icons-png.flaticon.com/512/149/149071.png" className={styles.userIcon} />
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
