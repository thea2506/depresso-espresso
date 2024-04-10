//#region imports
// import { useState } from "react";
// import axios from "axios";
import "react-toastify/dist/ReactToastify.css";
import axios from "axios";
import { ToastContainer } from "react-toastify";
import { GoComment, GoHeart, GoPencil, GoShare, GoTrash } from "react-icons/go";
import { AiOutlineClose } from "react-icons/ai";
import { Dispatch, useState } from "react";
import { MdOutlinePublic } from "react-icons/md";
import { animated, useSpring } from "@react-spring/web";
import Popup from "reactjs-popup";
import Markdown from "react-markdown";

// components
import { UserDisplay } from "../UserDisplay";
import { PostModel } from "./PostModel";
import CommentList from "../profile/CommentList";
import { PostForm } from "./PostForm";
import { AuthorModel } from "./AuthorModel";
//#endregion

//#region interfaces
interface CreatePostViewProps {
  curUser: AuthorModel;
  post: PostModel;
  refresh: boolean;
  setRefresh: Dispatch<React.SetStateAction<boolean>>;
}
//#endregion

/**
 *
 * @param {string} username - The username of the user.
 * @param {string} user_img_url - The URL of the user's avatar
 * @returns
 */
const PostView = ({
  curUser,
  post,
  refresh,
  setRefresh,
}: CreatePostViewProps) => {
  const [open, setOpen] = useState(false);
  const [sharable] = useState(post.visibility.toLowerCase() === "public");
  const [showComments, setShowComments] = useState(false);
  const springs = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 },
  });

  const mdContent = `
  ${post.content}
  `;

  //#region functions

  const handleCommentClick = () => {
    setShowComments(!showComments);
  };

  const handleShareClick = async () => {
    try {
      await axios.post(`${curUser.id}/posts/`, post);
      setRefresh(!refresh);
    } catch (error) {
      console.error("An error occurred", error);
    }
  };

  const handleLikeToggle = async () => {
    try {
      await axios.post(`${post.id}/like`, {
        summary: `${curUser.displayName} liked your post`,
        type: "Like",
        object: post.id,
        author: {
          type: "author",
          id: curUser.id,
          host: curUser.host,
          displayName: curUser.displayName,
          url: curUser.url,
          github: curUser.github,
          profileImage: curUser.profileImage,
        },
      });
      setRefresh(!refresh);
    } catch (error) {
      // console.error("An error occurred", error);
    }
  };

  const handleDelete = async () => {
    try {
      const response = await axios.delete(`${post.id}`);
      if (response.data.success) {
        setRefresh(!refresh);
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };

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

  const interactSection = [
    {
      icon: <GoHeart />,
      count: post.likecount,
      onClick: handleLikeToggle,
    },
    {
      icon: <GoComment />,
      count: post.count,
      onClick: handleCommentClick,
    },
  ];

  return (
    <animated.div
      style={springs}
      className="flex flex-col items-center justify-center gap-y-4
      bg-accent-3 rounded-[1.4rem] w-full px-4 md:px-0"
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
        <div className="flex flex-col w-full h-full p-4 rounded-xl bg-accent-3">
          <div className="relative flex items-center justify-center">
            <p className="text-xl md:text-2xl text-secondary-dark">Edit</p>
            <AiOutlineClose
              className="absolute top-0 text-3xl cursor-pointer text-primary right-2"
              onClick={() => setOpen(false)}
            />
          </div>
          <PostForm
            author={post.author}
            oldPost={post}
            edit={true}
            refresh={refresh}
            setRefresh={setRefresh}
            closePopup={() => setOpen(false)}
          />
        </div>
      </Popup>

      <div
        className={
          "w-full p-3 md:p-8 bg-accent-3 rounded-[1.4rem] flex flex-col gap-y-4"
        }
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-x-2">
            <UserDisplay
              displayName={post.author.displayName}
              user_img_url={post.author.profileImage}
              link={`authors/${post.author.url}`}
            />
            <p className="text-sm font-semibold capitalize text-secondary-dark opacity-80">
              ({post.visibility.toLowerCase()})
            </p>
          </div>

          <div className="items-center hidden md:flex md:justify-center gap-x-1 opacity-60">
            <MdOutlinePublic className="w-4 h-4" />
            <p className="text-sm">
              {formatDateString(post.published.substring(0, 16))}
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="flex flex-col gap-y-2 text-start">
          <p className="font-semibold text-primary">Title</p>
          <p className="p-4 bg-white text-secondary-dark rounded-xl">
            {post.title}
          </p>
        </div>
        <div className="flex flex-col gap-y-2 text-start">
          <p className="font-semibold text-primary">Description</p>
          <p className="p-4 bg-white text-secondary-dark rounded-xl">
            {post.description}
          </p>
        </div>

        <div className="flex flex-col w-full gap-y-2 text-start">
          <p className="font-semibold text-primary">Content</p>
          {post.contentType === "text/markdown" && (
            <Markdown className="flex w-full p-4 prose bg-white max-w-none text-start rounded-xl">
              {mdContent}
            </Markdown>
          )}
          {post.contentType === "text/plain" && (
            <p className="p-4 bg-white text-start rounded-xl">{post.content}</p>
          )}
          {post.contentType?.includes("image") && (
            <a href={`${post.id.replace(/\/+$/, "")}/image`}>
              <img
                src={
                  post.content.includes("data")
                    ? post.content
                    : `data:${post.contentType},` + post.content
                }
                alt="post"
                className="w-full h-96 object-cover rounded-[1.4rem]"
              />
            </a>
          )}
        </div>

        {/* Like, Comment, Share Section */}
        <div className="flex items-center justify-between w-full mt-2">
          {interactSection.map((item, index) => (
            <div
              key={index}
              className={`flex items-center justify-center text-xl gap-x-4 ${
                item.icon.type.displayName === "GoShare" &&
                (post.visibility === "friends" ||
                  post.visibility === "unlisted")
                  ? "text-gray-400 cursor-not-allowed"
                  : "text-primary"
              }`}
            >
              <p
                className={`cursor-pointer ${
                  item.icon.type.displayName === "GoShare" &&
                  (post.visibility === "friends" ||
                    post.visibility === "unlisted")
                    ? ""
                    : "hover:text-secondary-light"
                }`}
                onClick={
                  !(
                    item.icon.type.displayName === "GoShare" &&
                    (post.visibility === "friends" ||
                      post.visibility === "unlisted")
                  )
                    ? item.onClick
                    : undefined
                }
              >
                {item.icon}
              </p>
              <p>{item.count}</p>
            </div>
          ))}

          <div className="flex items-center justify-center text-xl gap-x-4 text-primary">
            <GoShare
              className={`text-xl cursor-pointer hover:text-secondary-light text-primary ${
                !sharable ? "opacity-50 pointer-events-none" : ""
              }`}
              onClick={handleShareClick}
            />
            <p>{post.sharecount}</p>
          </div>

          {curUser.id === post.author.id && (
            <>
              <GoPencil
                className="text-xl cursor-pointer hover:text-secondary-light text-primary"
                onClick={() => setOpen(true)}
              />
              <GoTrash
                className="text-xl cursor-pointer hover:text-secondary-light text-primary"
                onClick={handleDelete}
              />
            </>
          )}
        </div>
      </div>
      {showComments && (
        <div className="w-full mb-4">
          <CommentList
            post={post}
            refresh={refresh}
            setRefresh={setRefresh}
          />
        </div>
      )}
    </animated.div>
  );
};

export { PostView };
