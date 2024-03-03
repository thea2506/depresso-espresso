//#region imports
// import { useState } from "react";
import axios from "axios";
import defaultProfileImage from "../../assets/images/default_profile.jpg";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer } from "react-toastify";
import { GoComment, GoHeart, GoPencil, GoShare } from "react-icons/go";
import { useEffect, useState } from "react";
import { MdOutlinePublic } from "react-icons/md";
import { animated, useSpring } from "@react-spring/web";
import Popup from "reactjs-popup";

// components
import { PostModel } from "./PostModel";
import CommentList from "../profile/CommentList";
import { PostForm } from "./PostForm";
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
  const [username, setUsername] = useState("");
  const [authorId, setAuthorId] = useState("");
  const [open, setOpen] = useState(false);
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
  const springs = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 },
  });

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

  useEffect(() => {
    const getData = async () => {
      try {
        const response = await axios.get("/user_data");
        setUsername(response.data.username);
        setAuthorId(response.data.authorid);
      } catch (error) {
        console.error(error);
      }
    };

    getData();
  });
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
    <animated.div
      style={springs}
      className="flex flex-col w-full px-6 md:px-8 lg:px-0 gap-y-4"
    >
      <ToastContainer />
      {/* Popup */}
      <Popup
        overlayStyle={{ background: "rgba(0, 0, 0, 0.5)" }}
        open={open}
        modal
        lockScroll={true}
        onClose={() => {
          setOpen(false);
        }}
        closeOnEscape={true}
      >
        <div className=" bg-accent-3 rounded-[1.4rem] w-[26rem] sm:w-[30rem] md:w-[48rem]">
          <PostForm
            username={username}
            oldContent={post.content}
            oldImageUrl={post.image_url}
            oldVisibility={post.visibility}
            oldIsMarkdownEnabled={post.contenttype}
            postId={post.postid}
            edit={true}
          />
        </div>
      </Popup>

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
        <p className="text-start">{post.content}</p>

        {/* Image - need to display currently not saved I think*/}
        {post.image_url && (
          <img
            src={post.image_url}
            alt="post"
            className="w-full h-96 object-cover rounded-[1.4rem]"
          />
        )}

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

          {authorId === post.authorid && (
            <GoPencil
              className="text-xl cursor-pointer hover:text-secondary-light text-primary lg:text-2xl"
              onClick={() => setOpen(!open)}
            />
          )}
        </div>
      </div>
      <div className="w-full">
        {showComments && <CommentList post={post} />}
      </div>
    </animated.div>
  );
};

export { PostView };
