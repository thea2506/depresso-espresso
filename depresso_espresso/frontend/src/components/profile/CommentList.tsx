import { useState } from "react";
import axios from "axios";
import { PostModel } from "../data/PostModel";
import { FaPaperPlane } from "react-icons/fa6";

const CommentList = ({ post }: { post: PostModel }) => {
  const [comment, setComment] = useState("");

  const handleCommentSubmit = async () => {
    try {
      await axios.post("/create_comment", { comment });
      // Handle success or any other logic here
    } catch (error) {
      // Handle error here
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
