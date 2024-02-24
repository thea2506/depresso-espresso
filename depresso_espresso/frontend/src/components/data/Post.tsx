import React from 'react';
import styles from '../../Post.module.css';

const publicIconUrl= "https://cdn-icons-png.flaticon.com/512/2889/2889676.png"
const imageiconUrl = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAe1BMVEX///8BAQEAAABcXFydnZ2YmJjOzs7v7+8aGhrz8/Pn5+fR0dH4+Pjs7OzX19eioqLd3d02Nja/v7+KiopSUlJoaGizs7NZWVmoqKiRkZHHx8cWFha5ubk8PDxvb28lJSV8fHwMDAwsLCxGRkYdHR14eHhJSUkvLy+Li4u3DHLrAAAG+ElEQVR4nO2d6XqqOhRA2zgVxQkEZ4Vqte//hNehkB1IIMZM5357/TmnoDFLQrKzCfjxgSAIgiAIgiAIgiAIgiAIgiAIgiAIgiAIgiCIIkE07bplGgUG/TYd4gOLnSG/YHkr/dM9t1pchiYEZ7kXfndujn39gkNv/O4QMtNuOPdJ8KZ41C248kvwpjjVbHj2znCrV7BfnIWOB4o7RUX0djbrstxlzynrRam41mqYFMUmWotV4WCmKp2i2I3WYlXYFFXpaC22NDQw0r5IHw3VQEOLoKEiaGgRNFQEDS2ChoqgoUXQUBE0tAgaKoKGFkFDRdDQImioCBpaBA0VQUOLoKEiaGgRNFQEDS2ChoqgoUU8MAy1fnINt4ZRvN/m+XZ+SM0t5HVoOMzg2qzOSGsFKM4Mw5jAFah3RyMLeZ0Zzr6rK2xvjkbWYzsy3PBWEBPS01qJJ24MuYKGFJ0YjkVrwE00VCeGe7aLYf7S3t24MOxSp7tfDiU11+PDiWGwJaXfsTcbjmfphdBNusdFB4YrahMXEVtKFZdaK+LEsDgLCenSjSO64lxzAGffsOxIyQFuLo8iSbXWxIFhWh6sMbP9xBV/H/uGa4FJcRDJXmtNHBgmgtY4Kww136Fk33BR7KoMC4PC8EvvlNihYWVX0QOR879uWLbSys1kk/9NK+0KPrFXbD9prYkDw6gcLSZwc3gstmdaa+LAMCiHdmZYiMvNkbDUoB/d6L8W9DiI2pZlCAruJuvSqE1QZDCdF1mr/eqFzsiB4Y5G2ae/hjo+0G0Zt8Dwt7hd8vmv/D2vLuaH9CZoQpar/ig9EDB74k6BJ5XEFSEn2amyC8OInQEzs3wS84qLamkPIn3Xq5MsxoEwdYV/XHln2I6fmZO7e9NNru3IqfGz1rwHA0xEmTmppwi4MRxvuZXmH5ZA+H1sZcYNRxnhcS3l/Ti1uO1uSeBLmJNWZqLl7LrFgVQcRd3jGvSz5HJI9jAzJ3F/trtrT9GcORwk5w9xGyAYP76CWQdsar/J3uX1w92CXly7rvjn1BjYlPnwKW+jCLdXSMOomywunXUqHL733MPVBYoT0Vv/8OAqdxOZIBn+A2KGluDGb0OQKD6zrXhBFffNYbjXhkNxYwSDZEuW3GfD8EwFV9Wd4ClN5KepFJ8NE+rAyRL3SYM/8zpvDUGHOeedaiug2BCE+2s4apsz0sRHYxDurWEAqi/K3CT0NeIg3FtDMBxwJ8UPQLZAmIP01fAXJHPErxqAAy26ZOWpYQTa36DhdROgKFip4qfhUK6b/GASd4Ig3E9DcH61rSHqtQXhXhr+vLJuAcQFOa9B+2gIhvJvieQ26HV5kYGHhpMXJn93gqtgivXEP8Mwl4s3KTOY6Kjt9c+wQ4+I7KqMxiDcO0PQN8ovymgKwn0z3LTG21wagnDPDAcS8XbjB37WVjp4ZkhXnjbE21xAh3phdvhlmNFDuHjxE2FilclqeGW4k4y3ucAZM1j06Mgwmh46y6S3Y6etcFxTiBRS/jnswHCU0GT+Cc4HjrSGSo+m7nE7VOuGM/i0/dt/5+X4BUJoxUf+0mvLZFsu7bRtuKpfVMvKPcWmo+rKthNVLDMDlg1/K34PxUe3OZJKnLUQgIZeCNk1XNcF75VZsgv431gGzQnCrRpy11Q8GyqY5GXvfDCM+p7flE3DGV/w0VBpxa7vffK0OuRYNAy/CXBi1hzANVFjcalSxJXY3aJhAoU6cXy48rqd9x/iTtduPDple4ZwDvfzOFBhWlWUWXnQCmgr927amiHMvpQRS/XMfDne5gKzrZk1wwBc7QTHib3VkuR6FrHDsXU6sWQIZqhMCnQNDOVSazLAIDyzYwiDYnZCcQH9j1xqTYbfejdt1hAmw6pLDs6c8/N9QMf9acFwnDdYwJNG4+99XCrdtFlDEJJxUqArYQt+h3H114pMGsYt8yLQoi6c3YrURiJzhlEljKpzBT2fvjpUbvo3ZzisRfs14JxH4w35XXawNWYI5t2Z6OW71sOsRAYVTRlOQAq0YckBeJXOW9cWFgzB5dy8aV50auxuVQnBInhDhp+yg9345auGUsD1fYYM6VfYMi/aiMOedwDFGjZsLx+ErpqmGA9Sw3FpKXhsj1bA9EPLNPGP2IqhVMMLv2g71fgknpENQ8nOY2IkBjc8x/8rXHIASE0M/Cszhj/QkMyHwUCGAMTge7m3tNLPy6FZq2HKGG6PX1Kc4QC9lXtPC/QmOc3PTGF/7/jVX0V98U1SRWp/AlVSG/Ido/0XUf360WoDh7A6OXMNu3hBE5lHilpzB5R19YK2K4iZBzLe6J909YdvcjL1bNRbTBh/u7Yj37E5PwRBEARBEARBEARBEARBEARBEARBEARBzPIfahpitFVlvGAAAAAASUVORK5CYII="
const usericonUrl = "https://cdn-icons-png.flaticon.com/512/149/149071.png"

interface CreatePostProps {
  onContentChange?: (content: string) => void; // Function to handle content changes
  onVisibilityChange?: (visibility: string) => void; // Function to handle visibility changes
  onMarkdownToggle?: (isEnabled: boolean) => void; // Function to handle markdown toggle
  onImageUpload?: (image: File | null) => void; // Function to handle image upload
  onSubmitPost?: () => void; // Function to submit the post
  content?: string; // Content of the post
  visibility?: string; // Visibility setting of the post
  isMarkdownEnabled?: boolean; // Whether Markdown is enabled
  imageUrl?: string | null; // URL of the uploaded image (if any)
}

const Post: React.FC<CreatePostProps> = ({
  onContentChange,
  onVisibilityChange,
  onMarkdownToggle,
  onImageUpload,
  onSubmitPost,
  content='',
  visibility='public',
  isMarkdownEnabled=false,
  imageUrl
}) => {
  // Handlers for the input changes and submit action
  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (onContentChange)
    onContentChange(e.target.value);
  };

  const handleVisibilityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (onVisibilityChange)
    onVisibilityChange(e.target.value);
  };

  const handleMarkdownToggle = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (onMarkdownToggle)
    onMarkdownToggle(e.target.checked);
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      if (onImageUpload)
      onImageUpload(files[0]);
    }
  };

  const handlePostSubmit = () => {
    if (onSubmitPost)
    onSubmitPost();
  };

  return (
    <div className={styles.createPostContainer}>
      <div className={styles.userInput}>
        <textarea 
          className={styles.textarea}
          placeholder="What's on your mind?"
          value={content} 
          onChange={handleContentChange} 
        />
      </div>
      <div className={styles.userIcon}>
        <img src={usericonUrl} alt = "User" className={styles.icon} />
        {/* add username here of the user get it from the signin */}
        < p > Username </p>
        
        <textarea
          className={styles.textarea}
          placeholder="Say Something..."
          value={content} 
          onChange={handleContentChange}
        />
      </div>
      <div className={styles.options}>
        <img src={publicIconUrl} alt = "Public" className={styles.icon} />
        <select className={styles.visibilitySelect} value={visibility} onChange={handleVisibilityChange}>
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
        <label className={styles.markdownToggle}>
          <span className={styles.icon}>Enable Markdown</span>
          <input 
            type="checkbox" 
            checked={isMarkdownEnabled} 
            onChange={handleMarkdownToggle} 
          />
        </label>
        <div className={styles.fileInputContainer}>
          <img src={imageiconUrl} className={styles.icon} />
          <input 
            type="file" 
            className={styles.fileInput}
            onChange={handleImageUpload} 
          />
        </div>
        {imageUrl && <img src={imageUrl} alt="Preview" className={styles.imagePreview} />}
        <button onClick={handlePostSubmit} className={styles.postButton}>Post</button>
      </div>
    </div>
  );
}

export default Post;
