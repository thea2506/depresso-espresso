//#region imports
// import { useState } from "react";
import axios from "axios";
import defaultProfileImage from "../../assets/images/default_profile.jpg";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer } from "react-toastify";
import { GoComment, GoHeart, GoShare } from "react-icons/go";
import { animated } from "@react-spring/web";
import { useState } from "react";
import { MdOutlinePublic } from "react-icons/md";

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
const PostView = ({ post }: CreatePostViewProps) => {
  const [showComments, setShowComments] = useState(false);
  const [like, setLike] = useState<number | undefined>(post.likes || 0);
  const date = new Date(post.publishdate);
  const formattedDate = date
    .toLocaleString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      month: "long",
      day: "2-digit",
      year: "numeric",
    })
    .replace(",", "");

  //#region functions
  const handleLikeToggle = async () => {
    console.log(post.likes);
    axios.post("/toggle_like", { postid: post.postid }).then(() => {
      setLike(like == 0 ? 1 : 0);
    });
  };

  const handleCommentClick = () => {
    console.log("Comment clicked");
    setShowComments(!showComments);
  };

  const handleShareClick = () => {
    console.log("Share clicked");
  };
  //#endregion

  const interactSection = [
    { icon: <GoHeart />, count: like, onClick: handleLikeToggle },
    {
      icon: <GoComment />,
      count: post.commentcount,
      onClick: handleCommentClick,
    },
    { icon: <GoShare />, onClick: handleShareClick },
  ];

  return (
    <div className="flex flex-col items-center justify-center w-full px-6 md:px-8 lg:px-0 gap-y-4">
      <ToastContainer />
      <div
        className={
          "w-full p-8 bg-accent-3 rounded-[1.4rem] flex flex-col gap-y-6"
        }
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center justify-center gap-x-4">
            <img
              className="object-cover w-12 h-12 rounded-full md:w-13 md:h-13 lg:w-14 lg:h-14"
              src={
                post.user_img_url != null
                  ? post.user_img_url
                  : defaultProfileImage
              }
              alt="Profile picture"
            />
            <p className="text-primary">{post.username}</p>
          </div>

          <div className="flex items-center md:justify-center gap-x-1 opacity-80">
            <MdOutlinePublic className="w-4 h-4" />
            <p className="text-sm">{formattedDate}</p>
          </div>
        </div>
        <p>{post.content}</p>

        {/* Image - need to display currently not saved I think*/}

        {/* Like, Comment, Share Section */}
        <div className="flex items-center justify-between w-full">
          {interactSection.map((item, index) => (
            <div
              key={index}
              className="flex items-center justify-center text-lg lg:text-xl gap-x-4 text-primary"
            >
              <p
                className="text-xl cursor-pointer hover:text-secondary-light lg:text-2xl"
                onClick={item.onClick}
              >
                {item.icon}
              </p>
              <p>{item.count}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="w-full">
        {showComments && <CommentList post={post} />}
      </div>
    </div>
  );
};

export { PostView };
