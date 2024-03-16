//#region imports
// import { useState } from "react";
import axios from "axios";
import "react-toastify/dist/ReactToastify.css";
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
      const response = await axios.post(
        `/authors/${post.author.pk}/posts/${post.id}/share_post`
      );
      if (response.data.success) {
        console.log("Post shared");
        setRefresh(!refresh);
      } else if (
        response.data.success === false &&
        response.data.message === "Already shared"
      ) {
        console.log("Post already shared");
        setRefresh(!refresh);
      } else if (
        response.data.success === false &&
        response.data.message === "Sharing own post"
      ) {
        console.log("You are trying to share your own post");
        setRefresh(!refresh);
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };

  const handleLikeToggle = async () => {
    console.log("Like clicked");
    const response = await axios.post(
      `authors/${post.author.pk}/posts/${post.id}/toggle_like`
    );
    if (response.data.already_liked == false) {
      await axios.post("/create_notification", {
        type: "like",
        sender_id: curUser.id,
        receiver_id: post.author.pk,
        post_id: post.id,
      });
    }

    setRefresh(!refresh);
  };

  const handleDelete = async () => {
    try {
      const response = await axios.post("/delete_post", {
        postid: post.id,
      });
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
    {
      icon: <GoShare />,
      count: post.sharecount,
      onClick: handleShareClick,
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
            author={post.author.fields}
            oldTitle={post.title}
            oldDescription={post.description}
            oldContent={post.content}
            oldImageFile={post.content}
            oldVisibility={post.visibility}
            oldContentType={post.contenttype}
            postId={post.id}
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
          <UserDisplay
            username={post.author.fields.displayName}
            user_img_url={post.author.fields.profileImage}
            link={`/authors/${post.author.pk}`}
          />

          <div className="items-center hidden md:flex md:justify-center gap-x-1 opacity-80">
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

        <div className="flex flex-col gap-y-2 text-start">
          <p className="font-semibold text-primary">Content</p>
          {post.contenttype === "text/markdown" && (
            <Markdown className="p-4 bg-white text-start rounded-xl">
              {mdContent}
            </Markdown>
          )}
          {post.contenttype === "text/plain" && (
            <p className="p-4 bg-white text-start rounded-xl">{post.content}</p>
          )}
          {post.contenttype?.includes("image") && (
            <img
              src={post.content}
              alt="post"
              className="w-full h-96 object-cover rounded-[1.4rem]"
            />
          )}
        </div>

        {/* Like, Comment, Share Section */}
        <div className="flex items-center justify-between w-full mt-2">
          {interactSection.map((item, index) => (
            <div
              key={index}
              className="flex items-center justify-center text-xl gap-x-4 text-primary"
            >
              <p
                className="cursor-pointer hover:text-secondary-light"
                onClick={item.onClick}
              >
                {item.icon}
              </p>
              <p>{item.count}</p>
            </div>
          ))}

          {curUser.id === post.author.pk && (
            <GoPencil
              className="text-xl cursor-pointer hover:text-secondary-light text-primary"
              onClick={() => setOpen(true)}
            />
          )}

          {curUser.id === post.author.pk && (
            <GoTrash
              className="text-xl cursor-pointer hover:text-secondary-light text-primary"
              onClick={handleDelete}
            />
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
