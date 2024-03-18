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
import { AuthorModel } from "./AuthorModel";
//#endregion

//#region interfaces
interface CreatePostProps {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  author: AuthorModel;
  edit: boolean;

  // trigger home refresh everytime the post is changed/created
  refresh: boolean;
  setRefresh: (refresh: boolean) => void;

  // edits
  oldTitle?: string;
  oldDescription?: string;
  oldContentType?: string;
  oldContent?: string;
  oldVisibility?: string;
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
  author,
  edit = false,
  refresh,
  setRefresh,
  oldTitle,
  oldDescription,
  oldContentType,
  oldContent,
  oldVisibility,
  oldImageFile,
  postId,
  closePopup,
}: CreatePostProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [springs, api] = useSpring(() => ({
    from: { opacity: 0, y: -100 },
  }));

  const [contentType, setContentType] = useState(
    oldContentType || "text/plain"
  );
  const [title, setTitle] = useState(oldTitle || "");
  const [description, setDescription] = useState(oldDescription || "");
  const [visibility, setVisibility] = useState(oldVisibility || "PUBLIC");
  const [form, setForm] = useState("");
  const [imgDisabled, setImgDisabled] = useState(false);
  const [textDisabled, setTextDisabled] = useState(false);
  const [content, setContent] = useState(oldContent || "");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [base64Image, setBase64Image] = useState("");

  //#region functions
  const openPost = (newForm: string) => {
    if (
      newForm === "refresh" ||
      (newForm === "Image" && newForm == form) ||
      (newForm === "Text/Markdown" && newForm == form)
    ) {
      setImgDisabled(false);
      setTextDisabled(false);
      setForm("");
    } else if (newForm === "Image") {
      setImgDisabled(false);
      setTextDisabled(true);
      setForm("Image");
    } else if (newForm === "Text/Markdown") {
      setImgDisabled(true);
      setTextDisabled(false);
      setForm("Text/Markdown");
    }
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
      const formData = new FormData();
      formData.append("inbox", "No");
      formData.append("title", title);
      formData.append("description", description);

      formData.append("contentType", contentType);
      formData.append("visibility", visibility);
      formData.append("authorId", author.id);

      if (contentType.includes("image") && imageFile) {
        formData.append("content", base64Image);
      } else formData.append("content", content);

      if (edit && postId) formData.append("postid", postId);

      setForm("");

      const url = edit
        ? `/espresso-api/authors/${author.id}/posts/${postId}`
        : "/new_post/";

      let response;
      if (edit) {
        response = await axios.put(url, formData);
      } else {
        response = await axios.post(url, formData);
      }

      // create notification
      if (url == "/new_post/" && visibility.toLowerCase() != "private")
        await axios.post("/create_notification", {
          type: "post",
          sender_id: author.id,
          post_id: response.data.id,
        });

      openPost("refresh");
      closePopup && closePopup();
      setRefresh(!refresh);

      if (!response.data.success) {
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
        <div className="flex flex-col gap-y-12 w-full px-4 py-12 bg-accent-3 lg:w-1/2 text-primary rounded-[1.4rem]">
          <p className="font-semibold md:text-lg">What's on your mind today?</p>
          <div className="flex items-center mx-[4%] gap-x-8">
            {[
              { text: "Image", func: setImgDisabled, disabled: imgDisabled },
              {
                text: "Text/Markdown",
                func: setTextDisabled,
                disabled: textDisabled,
              },
            ].map((elem, index) => (
              <Button
                buttonType="text"
                key={index}
                className={`w-full ${elem.disabled && "opacity-70"}`}
                disabled={elem.disabled}
                onClick={() => openPost(elem.text)}
              >
                {elem.text}
              </Button>
            ))}
          </div>
        </div>
      )}
      {/* Long version */}
      <animated.form
        onSubmit={handlePostSubmit}
        style={edit === false ? { ...springs } : {}}
        className={`w-full rounded-[1.4rem] flex flex-col gap-y-8 bg-accent-3 ${
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
              src={
                author.profileImage ? author.profileImage : defaultProfileImage
              }
              alt="Profile picture"
            />
            <p className="text-primary">{author.displayName}</p>
          </div>
          <Button
            buttonType="text"
            className="px-12 lg:px-20 rounded-2xl focus:outline-none"
            type="submit"
          >
            Post
          </Button>
        </div>
        <input
          type="text"
          placeholder="Title"
          defaultValue={oldTitle || ""}
          className="w-full p-4 bg-white rounded-2xl focus:outline-none"
          maxLength={100}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          type="text"
          placeholder="Description"
          defaultValue={oldDescription || ""}
          className="w-full p-4 bg-white rounded-2xl focus:outline-none"
          maxLength={100}
          onChange={(e) => setDescription(e.target.value)}
        />
        {/* Text */}
        {form === "Text/Markdown" ||
        (oldContentType?.includes("text") && edit) ? (
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
          />
        ) : (
          <form onSubmit={(e) => console.log(e)}>
            <label className="flex items-center justify-center py-4 text-white cursor-pointer bg-primary rounded-2xl">
              <input
                type="file"
                id="file"
                name="file"
                onChange={(e) => {
                  const file = e.target.files?.[0] || null;
                  setImageFile(file);

                  if (file) {
                    const reader = new FileReader();
                    reader.onloadend = () => {
                      setBase64Image(reader.result as string);
                    };
                    reader.readAsDataURL(file);
                  }

                  file?.name.includes("png")
                    ? setContentType("image/png")
                    : setContentType("image/jpeg");
                }}
              />
              Upload Image
            </label>
          </form>
        )}

        {/* Options */}
        <div className="flex items-center justify-between w-full gap-x-4">
          {!edit ? (
            <div className="flex items-center gap-x-4">
              <FaLock className="w-6 h-7 text-primary" />
              <select
                id="privacy"
                className="p-2 bg-white rounded-md cursor-default focus:outline-none"
                onChange={(e) => setVisibility(e.target.value.toUpperCase())}
              >
                {["Public", "Friends", "Unlisted"].map((option, index) => (
                  <option
                    key={index}
                    value={option}
                  >
                    {option}
                  </option>
                ))}
              </select>
            </div>
          ) : null}
          {form == "Text/Markdown" ||
          (oldContentType?.includes("text") && edit) ? (
            <div className="flex items-center align-baseline gap-x-4 text-primary">
              <p className="text-sm leading-8 md:text-base">Markdown</p>
              <input
                onChange={(e) => {
                  e.target.checked
                    ? setContentType("text/markdown")
                    : setContentType("text/plain");
                }}
                type="checkbox"
                name="markdown"
                id="markdown"
                defaultChecked={contentType.includes("markdown") ? true : false}
                className={`w-6 h-6 transition ease-out duration-150 bg-white rounded-md appearance-none cursor-pointer checked:bg-primary ${
                  isOpen || edit ? "opacity-100" : "opacity-0"
                }`}
              />
            </div>
          ) : null}
          {form == "Image" || oldContentType?.includes("image") ? (
            <div className="flex text-sm gap-x-2 text-primary md:text-base">
              <p>
                {oldImageFile &&
                  imageFile == null &&
                  oldImageFile.split("/")[1]}
              </p>
              <p>{imageFile && imageFile?.name}</p>
            </div>
          ) : null}
        </div>
      </animated.form>
    </div>
  );
};

export { PostForm };
