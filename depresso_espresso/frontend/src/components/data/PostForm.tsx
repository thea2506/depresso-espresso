//#region imports
import { useState } from "react";
import axios from "axios";
import defaultProfileImage from "../../assets/images/default_profile.jpg";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import { FaLock } from "react-icons/fa6";
import { animated, useSpring } from "@react-spring/web";

// components
import { Button } from "../Button";
//#endregion

//#region interfaces
interface CreatePostProps {
  username: string;
  user_img_url?: string;
  edit: boolean;

  // edits
  oldContent?: string;
  oldVisibility?: string;
  oldImageUrl?: string;
  oldImageUploadUrl?: File;
  oldIsMarkdownEnabled?: string;
  postId?: string;
}
//#endregion

const myToast: ToastOptions = {
  position: "top-center",
  autoClose: 1000,
  hideProgressBar: true,
  closeOnClick: true,
  closeButton: false,
  pauseOnHover: false,
  draggable: false,
  progress: undefined,
};

/**
 *
 * @param {string} username - The username of the user.
 * @param {string} user_img_url - The URL of the user's avatar
 * @returns
 */
const PostForm = ({
  username,
  user_img_url,
  edit = false,
  oldContent,
  oldVisibility,
  oldImageUrl,
  oldIsMarkdownEnabled,
  postId,
}: CreatePostProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [springs, api] = useSpring(() => ({
    from: { opacity: 0, y: -100 },
  }));

  const [content, setContent] = useState(oldContent || "");
  const [imageUrl, setImageUrl] = useState(oldImageUrl || "");
  const [imageUploadUrl, setImageUploadUrl] = useState<File | null>();
  const [isMarkdownEnabled, setMarkdownEnabled] = useState(
    oldIsMarkdownEnabled || "false"
  );
  const [visibility, setVisibility] = useState(oldVisibility || "public");

  //#region functions
  const openPost = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      api.start({
        from: {
          opacity: 0,
          y: -100,
        },
        to: {
          opacity: 1,
          y: 0,
        },
      });
    } else {
      api.start({
        from: {
          opacity: 1,
          y: 0,
        },
        to: {
          opacity: 0,
          y: -100,
        },
      });
    }
  };

  const handlePostSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      const formField = new FormData();
      formField.append("content", content);
      if (isMarkdownEnabled) {
        formField.append("contenttype", "markdown");
      } else {
        formField.append("contenttype", "plaintext");
      }
      // formField.append("image_post_id", imagePostId?.toString() || "");
      if (imageUrl != "") formField.append("attached_img_post", imageUrl);
      formField.append("visibility", visibility);
      formField.append("username", username);
      if (edit && postId) formField.append("postid", postId);

      const response = edit
        ? await axios.post("/edit_post", formField)
        : await axios.patch("/make_post", formField);

      if (response.data.success) {
        console.log("PostForm Created Successfully");

        toast.success("PostForm Created Successfully", myToast);
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      } else {
        console.log("Failed to create post");
        toast.error("Failed to create post", myToast);
      }
    } catch (error) {
      console.error("An error occurred", error);
      toast.error("An error occurred", myToast);
    }
  };
  //#endregion

  return (
    <div className="flex flex-col items-center justify-center w-full px-6 md:px-8 lg:px-0 gap-y-4">
      <ToastContainer />
      {/* Short version*/}
      {edit === false && (
        <div
          className="flex w-full px-4 py-6 bg-white cursor-pointer lg:w-1/2 text-primary border-[2rem] rounded-[1.4rem] border-accent-3"
          onClick={openPost}
        >
          <p>What's on your mind?</p>
        </div>
      )}
      {/* Long version */}
      <animated.form
        onSubmit={handlePostSubmit}
        style={edit === false ? { ...springs } : {}}
        className={`w-full rounded-[1.4rem] flex flex-col gap-y-6 bg-accent-3 ${
          edit || isOpen
            ? `block  ${isOpen && "p-8 lg:w-1/2"} ${
                edit && "px-2 py-4 sm:p-4 lg:p-8"
              }`
            : "hidden"
        }`}
      >
        <div className="flex items-center justify-between">
          {/* User info  */}
          <div className="flex items-center justify-center gap-x-4">
            <img
              className="object-cover w-12 h-12 rounded-full md:w-13 md:h-13 lg:w-14 lg:h-14"
              src={user_img_url != null ? user_img_url : defaultProfileImage}
              alt="Profile picture"
            />
            <p className="text-primary">{username}</p>
          </div>
          <Button
            buttonType="text"
            className="px-12 lg:px-20 rounded-2xl"
            type="submit"
          >
            Post
          </Button>
        </div>
        {/* Input Box */}
        <textarea
          name="post-content"
          id="post-content"
          cols={30}
          rows={10}
          maxLength={850}
          placeholder={"Say something..."}
          defaultValue={oldContent || ""}
          className="resize-none focus:outline-none w-full p-4 bg-white rounded-[1.4rem] overflow-none"
          onChange={(e) => setContent(e.target.value)}
        ></textarea>

        {/* Options */}
        <div className="flex items-center justify-between gap-x-4">
          <div className="flex gap-x-4">
            <FaLock className="w-6 h-7 text-primary" />
            <select
              name="privacy"
              id="privacy"
              className="px-4 py-1 bg-white rounded-xl"
            >
              {["Public", "Private"].map((option, index) => (
                <option
                  key={index}
                  value={option.toLowerCase()}
                  onClick={() => setVisibility(option.toLowerCase())}
                >
                  {option}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-center align-baseline gap-x-4 text-primary">
            <p className="text-sm leading-8 md:text-base">Markdown</p>
            <input
              onChange={(e) => {
                setMarkdownEnabled(e.target.checked.toString());
              }}
              type="checkbox"
              name="markdown"
              id="markdown"
              className={`w-6 h-6 transition ease-out duration-150 bg-white rounded-md appearance-none cursor-pointer checked:bg-primary ${
                isOpen || edit ? "opacity-100" : "opacity-0"
              }`}
            />
          </div>
          <div className="flex text-sm gap-x-2 text-primary md:text-base">
            <p>{!imageUploadUrl && "No image"}</p>
            <p>{imageUploadUrl && imageUploadUrl?.name}</p>
          </div>
        </div>
        <input
          className="w-full p-4 bg-white rounded-2xl focus:outline-none"
          placeholder="Image URL"
          type="text"
          onChange={(e) => setImageUrl(e.target.value)}
        />
        <form onSubmit={(e) => console.log(e)}>
          <label className="flex items-center justify-center py-4 text-white cursor-pointer bg-primary rounded-2xl">
            <input
              type="file"
              id="file"
              name="file"
              onChange={(e) => {
                const file = e.target.files?.[0] || null;
                setImageUploadUrl(file);
              }}
            />
            Upload Image
          </label>
        </form>
      </animated.form>
    </div>
  );
};

export { PostForm };
