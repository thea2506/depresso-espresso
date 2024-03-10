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

  // trigger home refresh everytime the post is changed/created
  refresh: boolean;
  setRefresh: (refresh: boolean) => void;

  // edits
  oldContent?: string;
  oldVisibility?: string;
  oldImageUrl?: string;
  oldImageFile?: string;
  oldIsMarkdownEnabled?: string;
  postId?: string;

  // close popup
  closePopup?: () => void;
}
//#endregion

const myToast: ToastOptions = {
  position: "top-center",
  autoClose: 900,
  hideProgressBar: false,
  closeOnClick: true,
  closeButton: false,
  pauseOnHover: false,
  draggable: false,
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
  refresh,
  setRefresh,
  oldContent,
  oldVisibility,
  oldImageUrl,
  oldImageFile,
  oldIsMarkdownEnabled,
  postId,
  closePopup,
}: CreatePostProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [springs, api] = useSpring(() => ({
    from: { opacity: 0, y: -100 },
  }));

  const [content, setContent] = useState(oldContent || "");
  const [imageUrl, setImageUrl] = useState(oldImageUrl || "");
  const [imageFile, setImageFile] = useState<File | null>(null);
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
      // content
      formField.append("content", content);

      // content type
      if (isMarkdownEnabled === "true" || isMarkdownEnabled === "markdown") {
        formField.append("contenttype", "markdown");
      } else {
        formField.append("contenttype", "plaintext");
      }

      // image url
      if (imageUrl != "") formField.append("image_url", imageUrl);

      // visibility
      formField.append("visibility", visibility);
      formField.append("username", username);
      //formField.append("authorprofile", user_img_url || "");

      if (edit && postId) formField.append("postid", postId);

      // image file
      console.log("imageFile", imageFile);
      if (imageFile != null) formField.append("image_file", imageFile);
      else if (imageFile == null && oldImageFile != null)
        formField.append("image_file", oldImageFile);

      const url = edit ? "/edit_post" : "/make_post";
      const response = await axios.post(url, formField);

      if (response.data.success) {
        setRefresh(!refresh);
        setTimeout(function () {
          closePopup && closePopup();
        }, 200);
      } else {
        toast.error("Failed to create/modify post", myToast);
      }
    } catch (error) {
      toast.error("An error occurred while posting", myToast);
    }
  };
  //#endregion

  return (
    <div className="flex flex-col items-center justify-center w-full gap-y-4">
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
            ? `block  ${isOpen && "p-8 lg:w-1/2"} ${edit && "p-4 lg:p-8"}`
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
            className="px-12 lg:px-20 rounded-2xl focus:outline-none"
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
              defaultChecked={
                oldIsMarkdownEnabled === "markdown" ? true : false
              }
              className={`w-6 h-6 transition ease-out duration-150 bg-white rounded-md appearance-none cursor-pointer checked:bg-primary ${
                isOpen || edit ? "opacity-100" : "opacity-0"
              }`}
            />
          </div>
          <div className="flex text-sm gap-x-2 text-primary md:text-base">
            <p>
              {oldImageFile && imageFile == null && oldImageFile.split("/")[1]}
            </p>
            <p>{imageFile && imageFile?.name}</p>
          </div>
        </div>
        <input
          className="w-full p-4 bg-white rounded-2xl focus:outline-none"
          placeholder="Image URL"
          defaultValue={oldImageUrl || ""}
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
                setImageFile(file);
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
