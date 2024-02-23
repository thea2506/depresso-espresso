import React from 'react';
import styles from '../../Post.module.css';

interface PostProps {
  imageUrl?: string;
  content?: string;
}

const Post: React.FC<PostProps> = ({ imageUrl, content}) => {

  return (
    <div className={styles.post}>
      {imageUrl && <img src={imageUrl} alt="Post" className={styles.image} />}
      <p>{content}</p>
    </div>
  );
}


export default Post;