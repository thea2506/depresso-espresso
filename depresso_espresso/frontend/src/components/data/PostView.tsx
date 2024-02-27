//#region imports
// import { useState } from "react";
import axios from "axios";
import defaultProfileImage from "../../assets/images/default_profile.jpg";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer} from "react-toastify";
import { FaHeart, FaComment, FaShare } from "react-icons/fa6";
import { animated } from "@react-spring/web";
import { useState } from 'react';


// components
import { PostModel } from "./PostModel";
import CommentList from "../profile/CommentList";
//#endregion

//#region interfaces
interface CreatePostViewProps {
  post: PostModel;
}
//#endregion


/**
 *
 * @param {string} username - The username of the user.
 * @param {string} user_img_url - The URL of the user's avatar
 * @returns
 */
const PostView = ({post}: CreatePostViewProps) => {
  const [showComments, setShowComments] = useState(false);

  const handleLikeToggle = () => {
    console.log("toggle_like");

    axios.post("/toggle_like", { postid: post.postid }).then((response) => {
      console.log('like response', response.data);
      window.location.reload(); // Refresh the page - TODO should be replaced with a more elegant solution in future
    });

  };

  const handleCommentClick = () => {
    console.log("Comment clicked");
    setShowComments(!showComments);
  };

  const handleShareClick = () => {
    console.log("Share clicked");
  };
  

  return (

    <div className="flex flex-col items-center justify-center w-full px-6 md:px-8 lg:px-0 gap-y-4">
      <ToastContainer />
  
      <animated.form
        className={'w-full p-8 lg:w-1/2 bg-accent-3 rounded-[1.4rem] flex flex-col gap-y-6 block' }    >
        <div className="flex items-center justify-between">
          <div className="flex items-center justify-center gap-x-4">
            <img
              className="object-cover w-12 h-12 rounded-full md:w-13 md:h-13 lg:w-14 lg:h-14"
              src={post.user_img_url != null ? post.user_img_url : defaultProfileImage}
              alt="Profile picture"
            />
            <p className="text-primary">{post.username}</p>
          </div>

          <span>
            {post.publishdate?.substring(0, 16)}
          </span>
       
        </div>
        <p>{post.content}</p>

        {/* Image - need to display currently not saved I think*/}

        

        {/* { Like, Comment, Share} */}
        <div className="flex items-center justify-between gap-x-4">
          <div className="flex gap-x-4">
            <div className="flex items-center justify-between gap-x-4">
              <div className="flex gap-x-4 w-full">
                <span className="flex items-center gap-x-1">
                  <FaHeart className="w-6 h-7 text-primary click-icon" onClick={handleLikeToggle} />
                  <span>{post.likes}</span>
                </span>
                <span>
                  <FaComment className="w-6 h-7 text-primary click-icon" onClick={handleCommentClick} />
                  <span>{post.commentcount}</span>
                </span>
                <span>
                  <FaShare className="w-6 h-7 text-primary click-icon" onClick={handleShareClick} />
                </span>
              </div>
            </div>    
          </div>
        </div>

        <div className="w-full">
            {showComments && <CommentList post={post} />} 
        </div>
       

        {/* Options */}
        {/* <div className="flex items-center justify-between gap-x-4">
          <div className="flex gap-x-4">
            <FaLock className="w-6 h-7 text-primary" />
            <select
              name="privacy"
              id="privacy"
              className="px-4 py-1 bg-white rounded-xl"
            >
              {["Public", "Private"].map((option, index) => (
                <option
                  key={index}
                  value={option.toLowerCase()}
                  onClick={() => setVisibility(option.toLowerCase())}
                >
                  {option}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-center align-baseline gap-x-4 text-primary">
            <p className="leading-8">Enable Markdown</p>
            <input
              onChange={(e) => {
                setMarkdownEnabled(e.target.checked);
              }}
              type="checkbox"
              name="markdown"
              id="markdown"
              className={`w-6 h-6 transition ease-out duration-150 bg-white rounded-md appearance-none cursor-pointer checked:bg-primary ${
                isOpen ? "opacity-100" : "opacity-0"
              }`}
            />
          </div>
          <div className="flex gap-x-2 text-primary">
            <p>{!imageUploadUrl && "No uploaded image"}</p>
            <p>{imageUploadUrl && imageUploadUrl?.name}</p>
          </div>
        </div>
        <input
          className="w-full p-4 bg-white rounded-2xl focus:outline-none"
          placeholder="Image URL"
          type="text"
          onChange={(e) => setImageUrl(e.target.value)}
        />
        <form onSubmit={(e) => console.log(e)}>
          <label className="flex items-center justify-center py-4 text-white cursor-pointer bg-primary rounded-2xl">
            <input
              type="file"
              id="file"
              name="file"
              onChange={(e) => {
                const file = e.target.files?.[0] || null;
                setImageUploadUrl(file);
              }}
            />
            Upload Image
          </label>
        </form> */}
      </animated.form>
    </div>
  );
};

export { PostView };
