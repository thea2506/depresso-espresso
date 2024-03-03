import { useState } from "react";
import axios from "axios";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import { PostModel } from "../data/PostModel";
import { FaPaperPlane } from "react-icons/fa6";
import { useEffect } from "react";
import { CommentModel } from "../data/CommentModel";

import { Button } from "../Button";

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

const CommentList = ({ post }: { post: PostModel }) => {
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState<CommentModel[]>([]);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await axios.post("/get_post_comments", {
          postId: post.postid,
        });
        console.log("comments resp", response.data);
        if (response.status === 200) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          const commentModels = response.data.map((rawcomment: any) => {
            return {
              authorid: rawcomment.fields.authorid,
              authorname: rawcomment.fields.authorname,
              comment: rawcomment.fields.comment,
              commentlikecount: rawcomment.fields.commentlikecount,
              contenttype: rawcomment.fields.contenttype,
              editdate: rawcomment.fields.editdate,
              liked_by: rawcomment.fields.liked_by,
              postid: rawcomment.fields.postid,
              publishdate: rawcomment.fields.publishdate,
            };
          });
          console.log("commentmodels", commentModels);
          setComments(commentModels);
        } else {
          console.error("Failed to fetch comments");
        }
      } catch (error) {
        console.error("An error occurred");
      }
    };

    fetchComments();
  }, [post.postid]);

  const handleCommentSubmit = async () => {
    try {
      const formField = new FormData();
      formField.append("comment", comment);
      formField.append("postid", post.postid);

      const response = await axios.post("/make_comment", formField);

      if (response.data.success) {
        console.log("Comment creation successful");
      } else {
        toast.error("Failed to create comment", myToast);
      }
    } catch (error) {
      toast.error("An error occurred", myToast);
    }
  };

  return (
    <div>
      <ToastContainer />
      <div className="flex items-center bg-accent-3">
        <input
          className="w-full p-4 bg-white rounded-2xl focus:outline-none"
          type="text"
          placeholder="Say Something"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        />
        <Button
          buttonType="icon"
          onClick={handleCommentSubmit}
          icon={<FaPaperPlane />}
        />
      </div>

      <div>
        {comments.map((comment: CommentModel, index: number) => (
          <div
            className="w-full p-4 bg-white rounded-2xl focus:outline-none"
            style={{ marginTop: "10px" }}
            key={index}
          >
            <h2>{comment.authorname} </h2>
            <h3>{comment.publishdate.substring(0, 16)} </h3>
            <p>{comment.comment}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommentList;
