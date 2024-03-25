/* eslint-disable @typescript-eslint/no-explicit-any */
//#region imports
import { useContext, useState } from "react";
import axios from "axios";
import defaultProfileImage from "../../assets/images/default_profile.jpg";
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import { FaLock } from "react-icons/fa6";
import { animated, useSpring } from "@react-spring/web";

// components
import { Button } from "../Button";
import AuthContext from "../../contexts/AuthContext";
import { PostModel } from "./PostModel";
import { AuthorModel } from "./AuthorModel";
//#endregion

//#region interfaces
interface CreatePostProps {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  edit: boolean;

  author: AuthorModel;

  // trigger home refresh everytime the post is changed/created
  refresh: boolean;
  setRefresh: (refresh: boolean) => void;

  // edits
  oldPost?: PostModel;

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
  edit = false,
  refresh,
  setRefresh,
  oldPost,
  closePopup,
}: CreatePostProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [springs, api] = useSpring(() => ({
    from: { opacity: 0, y: -100 },
  }));

  const [contentType, setContentType] = useState(
    oldPost?.contentType || "text/plain"
  );
  const [title, setTitle] = useState(oldPost?.title || "");
  const [description, setDescription] = useState(oldPost?.description || "");
  const [visibility, setVisibility] = useState(oldPost?.visibility || "PUBLIC");
  const [form, setForm] = useState("");
  const [imgDisabled, setImgDisabled] = useState(false);
  const [textDisabled, setTextDisabled] = useState(false);
  const [content, setContent] = useState(oldPost?.content || "");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [base64Image, setBase64Image] = useState("");
  const { curUser } = useContext(AuthContext);

  //#region functions

  // check if authenticated
  if (!Object.entries(curUser).length) return <></>;

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
      const url = edit ? `${oldPost?.id}` : `${curUser.id}/posts`;

      const new_post = {
        title: title,
        description: description,
        contentType: contentType,
        visibility: visibility,
        author: { ...curUser },
        content: contentType.includes("image") ? base64Image : content,
      };

      let response;
      if (edit) {
        response = await axios.put(url, new_post);
      } else {
        response = await axios.post(url, new_post);
        const post_object = response.data.object;
        console.log(post_object);
      }

      if (response.status != 200 && response.status != 201) {
        toast.error("Failed to create/modify post", myToast);
        return;
      } else {
        openPost("refresh");
        closePopup && closePopup();
        setRefresh(!refresh);
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
                curUser.profileImage
                  ? curUser.profileImage
                  : defaultProfileImage
              }
              alt="Profile picture"
            />
            <p className="text-primary">{curUser.displayName}</p>
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
          defaultValue={oldPost?.title || ""}
          className="w-full p-4 bg-white rounded-2xl focus:outline-none"
          maxLength={100}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          type="text"
          placeholder="Description"
          defaultValue={oldPost?.description || ""}
          className="w-full p-4 bg-white rounded-2xl focus:outline-none"
          maxLength={100}
          onChange={(e) => setDescription(e.target.value)}
        />
        {/* Text */}
        {form === "Text/Markdown" ||
        (oldPost?.contentType?.includes("text") && edit) ? (
          <textarea
            name="post-content"
            id="post-content"
            cols={30}
            rows={10}
            maxLength={850}
            placeholder={"Say something..."}
            defaultValue={oldPost?.content || ""}
            className="resize-none focus:outline-none w-full p-4 bg-white rounded-[1.4rem] overflow-none"
            onChange={(e) => setContent(e.target.value)}
          />
        ) : form === "Image" ? (
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
                    ? setContentType("image/png;base64")
                    : setContentType("image/jpeg;base64");
                }}
              />
              Upload Image
            </label>
          </form>
        ) : (
          <></>
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
          (oldPost?.contentType?.includes("text") && edit) ? (
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
          {form == "Image" || oldPost?.contentType?.includes("image") ? (
            <div className="flex text-sm gap-x-2 text-primary md:text-base">
              <p>
                {oldPost?.imageFile &&
                  imageFile == null &&
                  oldPost?.imageFile.split("/")[1]}
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
