import { Dispatch, useState, SetStateAction, useContext } from "react";
import axios from "axios";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import { PostModel } from "../data/PostModel";
import { FaPaperPlane } from "react-icons/fa6";
import { useEffect } from "react";
import { CommentModel } from "../data/CommentModel";

import { Button } from "../Button";
import { UserDisplay } from "../UserDisplay";

import AuthContext from "../../contexts/AuthContext";

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
  const { curUser } = useContext(AuthContext);

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
    const fetchComments = async () => {
      try {
        const response = await axios.get(`${post.id}/comments`);
        if (response.status === 200) {
          const comment_list = (response.data.items as CommentModel[]) || [];

          comment_list.forEach(async (comment: CommentModel) => {
            const response = await axios.get(`${comment.id}/likes`);
            if (response.status === 200) {
              comment.likecount = response.data.items.length;
            } else {
              console.error("Failed to fetch likes");
            }
          });

          setComments(comment_list);
        } else {
          console.error("Failed to fetch comments");
        }
      } catch (error) {
        console.error("An error occurred", error);
      }
    };

    fetchComments();
  }, [post.author.id, post.id, refresh]);

  const handleCommentSubmit = async () => {
    try {
      const response = await axios.post(`${post.id}/comments`, {
        type: "comment",
        author: {
          type: "author",
          id: curUser!.id,
          url: curUser!.url,
          host: curUser!.host,
          displayName: curUser!.displayName,
          github: curUser!.github,
          profileImage: curUser!.profileImage,
        },
        comment: comment,
        contentType: "text/plain",
      });

      if (response.status === 200 || response.status === 201) {
        setRefresh(!refresh);
        setComment("");
      } else {
        toast.error("Failed to create comment", myToast);
      }
      // if (checkSameOrigin(post.id)) {

      // } else {
      //   const response = await axios.post(`${post.author.url}/inbox`, {
      //     type: "comment",
      //     author: curUser,
      //     comment: comment,
      //     contentType: "text/plain",
      //   });
      //   if (response.status === 200 || response.status === 201) {
      //     toast.success("Commented", myToast);
      //     setComment("");
      //     setRefresh(!refresh);
      //   }
      // }
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
                displayName={comment.author.displayName}
                user_img_url={comment.author.profileImage}
                link={comment.author.url}
              />
              <p className="text-sm opacity-70">
                {formatDateString(comment.published.substring(0, 16))}
              </p>
            </div>

            <div className="flex justify-between w-full gap-2">
              <p className="flex-1 p-4 bg-white text-start rounded-xl">
                {comment.comment}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommentList;
