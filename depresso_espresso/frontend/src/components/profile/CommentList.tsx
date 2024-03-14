import { Dispatch, useState, SetStateAction } from "react";
import axios from "axios";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import { PostModel } from "../data/PostModel";
import { FaPaperPlane } from "react-icons/fa6";
import { useEffect } from "react";
import { CommentModel } from "../data/CommentModel";

import { Button } from "../Button";
import { UserDisplay } from "../UserDisplay";

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

const CommentList = ({
  post,
  refresh,
  setRefresh,
}: {
  refresh: boolean;
  setRefresh: Dispatch<SetStateAction<boolean>>;
  post: PostModel;
}) => {
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState<CommentModel[]>([]);
  const [, setAuthorImg] = useState("");

  //#region functions
  const formatDateString = (inputDateString: string) => {
    const date = new Date(inputDateString);
    const formattedDate = date.toLocaleString("en-US", {
      hour: "numeric",
      minute: "numeric",
      month: "short",
      day: "numeric",
      year: "numeric",
    });
    return formattedDate;
  };
  //#endregion

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get("/curUser");
        const data = response.data;

        if (data.success) {
          setAuthorImg(data.profileImage);
        }
      } catch (error) {
        console.error("An error occurred", error);
      }
    };

    const fetchComments = async () => {
      try {
        const response = await axios.post(
          `/authors/${post.author.pk}/posts/${post.id}/comments`
        );
        if (response.status === 200 && response.data.length > 0) {
          if (response.data.length > 0) {
            const commentModels = response.data.map(
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              (rawcomment: any) => {
                return {
                  type: "comment",
                  author: rawcomment.author,
                  comment: rawcomment.comment,
                  contenttype: rawcomment.contenttype,
                  published: rawcomment.published,
                  id: rawcomment.id,
                };
              }
            );
            setComments(commentModels);
          } else {
            console.log("No comments found");
            setComments([]);
          }
        } else {
          console.error("Failed to fetch comments");
        }
      } catch (error) {
        console.error("An error occurred", error);
      }
    };

    fetchProfile();
    fetchComments();
  }, [post.author.pk, post.id, refresh]);

  const handleCommentSubmit = async () => {
    try {
      const formField = new FormData();
      formField.append("comment", comment);
      formField.append("postid", post.id);

      const response = await axios.post("/make_comment", formField);

      if (response.data.success) {
        console.log("Comment creation successful");
        setRefresh(!refresh);
        setComment("");
      } else {
        toast.error("Failed to create comment", myToast);
      }
    } catch (error) {
      toast.error("An error occurred", myToast);
    }
  };

  return (
    <div className="flex flex-col gap-y-4 w-full rounded-[1.4rem] bg-accent-3 px-4 md:px-8">
      <ToastContainer />
      <div className="flex items-center mb-4 gap-x-4">
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

      <div className="flex flex-col gap-y-8">
        {comments.map((comment: CommentModel, index: number) => (
          <div
            key={index}
            className="flex flex-col mb-4 gap-y-4"
          >
            <div className="flex items-center justify-between">
              <UserDisplay
                username={comment.author.username}
                user_img_url={comment.author.profileImage}
                link={comment.author.url}
              />
              <p className="text-sm opacity-70">
                {formatDateString(comment.published.substring(0, 16))}
              </p>
            </div>
            <p className="text-start">{comment.comment}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommentList;
