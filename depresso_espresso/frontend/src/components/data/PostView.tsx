import React, { useState } from 'react';
import styles from '../../Post.module.css';
// import axios from "axios";
import { ToastContainer  } from "react-toastify";
//import { useNavigate } from "react-router-dom";

const publicIconUrl = "https://cdn-icons-png.flaticon.com/512/2889/2889676.png";
const imageiconUrl = "data:image/png;base64,..."; // Your base64 image
//const usericonUrl = "https://cdn-icons-png.flaticon.com/512/149/149071.png";

interface CreatePostViewProps {
  username?: string; // Assuming username is passed as a prop to this component
  display_name?: string;
  user_img_url?: string;
  content?: string;
  imageUrl?: string;
}


const PostView: React.FC<CreatePostViewProps> = ({ username, content, user_img_url }) => {
  const [imageUrl] = useState<string | null>(null);

  //const nav = useNavigate();

  return (
    
    <div className={styles.createPostContainer}>
      <ToastContainer />
      <div className={styles.userInput}>
        <img src={user_img_url} alt="https://cdn-icons-png.flaticon.com/512/149/149071.png" className={styles.userIcon} />
        <span>{username}</span>
        <textarea  className={styles.textarea} readOnly>{content}</textarea>
      </div>
      <div className={styles.options}>
        <img src={publicIconUrl} alt="Public" className={styles.icon} />
        <img src={imageiconUrl} className={styles.icon} />
        {imageUrl && <img src={imageUrl} alt="Preview" className={styles.imagePreview} />}
     
      </div>
    </div>
  );
        
};

export default PostView;
