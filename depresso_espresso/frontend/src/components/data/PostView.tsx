//#region imports
// import { useState } from "react";
import axios from "axios";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer } from "react-toastify";
import { GoComment, GoHeart, GoPencil, GoShare, GoTrash } from "react-icons/go";
import { AiOutlineClose } from "react-icons/ai";
import { useEffect, useState } from "react";
import { MdOutlinePublic } from "react-icons/md";
import { animated, useSpring } from "@react-spring/web";
import Popup from "reactjs-popup";
import Markdown from "react-markdown";

// components
import { UserDisplay } from "../UserDisplay";
import { PostModel } from "./PostModel";
import CommentList from "../profile/CommentList";
import { PostForm } from "./PostForm";
//#endregion

//#region interfaces
interface CreatePostViewProps {
  post: PostModel;
  refresh: boolean;
  setRefresh: (refresh: boolean) => void;
}
//#endregion

/**
 *
 * @param {string} username - The username of the user.
 * @param {string} user_img_url - The URL of the user's avatar
 * @returns
 */
const PostView = ({ post, refresh, setRefresh }: CreatePostViewProps) => {
  const [username, setUsername] = useState("");
  const [authorId, setAuthorId] = useState("");
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

  const handleShareClick = () => {
    console.log("Share clicked");
  };

  const handleLikeToggle = () => {
    setRefresh(!refresh);
    axios.post("/toggle_like", { postid: post.postid });
  };

  const handleDelete = async () => {
    try {
      const response = await axios.post("/delete_post", {
        postid: post.postid,
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
  }, []);
  //#endregion

  const interactSection = [
    {
      icon: <GoHeart />,
      count: post.likes,
      onClick: handleLikeToggle,
    },
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
            username={username}
            oldContent={post.content}
            oldImageUrl={post.image_url}
            oldImageFile={post.image_file}
            oldVisibility={post.visibility}
            oldIsMarkdownEnabled={post.contenttype}
            postId={post.postid}
            edit={true}
            refresh={refresh}
            setRefresh={setRefresh}
            closePopup={() => setOpen(false)}
          />
        </div>
      </Popup>

      <div
        className={
          "w-full p-3 md:p-8 bg-accent-3 rounded-[1.4rem] flex flex-col gap-y-8"
        }
      >
        <div className="flex items-center justify-between">
          <UserDisplay
            username={post.username}
            user_img_url={post.user_img_url}
            link={`/authors/${post.authorid}`}
          />

          <div className="items-center hidden md:flex md:justify-center gap-x-1 opacity-80">
            <MdOutlinePublic className="w-4 h-4" />
            <p className="text-sm">
              {formatDateString(post.publishdate.substring(0, 16))}
            </p>
          </div>
        </div>

        {/* Content */}
        {post.contenttype === "markdown" ? (
          <Markdown>{mdContent}</Markdown>
        ) : (
          <p className="text-start">{post.content}</p>
        )}

        {/* Image - need to display currently not saved I think*/}
        {post.image_url && (
          <img
            src={post.image_url}
            alt="post"
            className="w-full h-96 object-cover rounded-[1.4rem]"
          />
        )}

        {post.image_file && (
          <img
            src={post.image_file}
            alt="post"
            className="w-full h-96 object-cover rounded-[1.4rem]"
          />
        )}

        {/* Like, Comment, Share Section */}
        <div className="flex items-center justify-between w-full">
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

          {authorId === post.authorid && (
            <GoPencil
              className="text-xl cursor-pointer hover:text-secondary-light text-primary"
              onClick={() => setOpen(true)}
            />
          )}

          {authorId === post.authorid && (
            <GoTrash
              className="text-xl cursor-pointer hover:text-secondary-light text-primary"
              onClick={handleDelete}
            />
          )}
        </div>
      </div>
      {showComments && (
        <div className="w-full mb-4">
          <CommentList post={post} />
        </div>
      )}
    </animated.div>
  );
};

export { PostView };
