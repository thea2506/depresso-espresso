import { useState } from "react";
import axios from "axios";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import { PostModel } from "../data/PostModel";
import { FaPaperPlane } from "react-icons/fa6";

const CommentList = ({ post}: { post: PostModel}) => {
  const [comment, setComment] = useState("");

  const myToast: ToastOptions = {
    position: "top-center",
    autoClose: 1000,
    hideProgressBar: true,
    closeOnClick: true,
    pauseOnHover: false,
    draggable: false,
    progress: undefined,
    closeButton: false,
  };

  const handleCommentSubmit = async () => {
    try {
      toast.success("Here now", myToast);
      const formField = new FormData();
      formField.append("comment", comment);
      formField.append("postid", post.postid);

      const response = await axios.post("/make_comment", formField);

      if (response.data.success) {
        toast.success("Comment Created Successfully", myToast);
        console.log("Comment creation successful");
      } else {
        console.log("Failed to create comment");
        toast.error("Failed to create comment", myToast);
      }
    } catch (error) {
      console.error("An error occurred", error);
      toast.error("An error occurred", myToast);
    }
  };

      return (
        <div style={{ display: "flex", alignItems: "center" }}>
          <input className="w-full p-4 bg-white rounded-2xl focus:outline-none" type="text" placeholder="Say Something" value={comment} onChange={(e) => setComment(e.target.value)} />
          <button onClick={handleCommentSubmit}>
            <FaPaperPlane />
          </button>
        </div>
  );
};

export default CommentList;
