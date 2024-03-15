//#region imports

import { useState } from "react";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import axios from "axios";
import { Button } from "../Button";
//#endregion

/**
 * Renders a post creation.
 * @returns The rendered signup page.
 */

const MakePost = () => {
  const inputs: string[] = ["Post Body", "Add Image"];

  const [content, setContent] = useState<string>("");
  const [image_url, setImage] = useState<string>("");
  // const [isvalid, setValid] = useState<boolean>(true)

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

  const handleInputs = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === "Post Body") {
      setContent(value);
    } else if (name === "Add Image") {
      setImage(value);
    }
  };

  /** 
    const checkImageURL = (imageURL: string) => {
      const img = new Image();
      img.src = imageURL;
      if (img.complete) {
        return true;
      } else {
        img.onload = () => {
          return true;
        };
        img.onerror = () => {
          return false;
        };
      }
    };
    */

  /**
   * Posts the inputs to the backend.
   */
  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      const formField = new FormData();
      formField.append("content", content);
      formField.append("image_url", image_url);
      const response = await axios.post("/make_post", formField);

      if (response.data.success) {
        toast.success("Post Created Successfully", myToast);
      } else {
        toast.error("Failed to create post", myToast);
      }
    } catch (error) {
      console.error("An error occurred", error);
      toast.error("An error occurred", myToast);
    }
  };
  //#endregion

  return (
    <form
      className="z-10 flex flex-col w-3/4 lg:w-1/2 gap-y-4"
      onSubmit={handleSubmit}
    >
      <ToastContainer />
      {inputs.map((input, index) => {
        return (
          <div
            key={index}
            className="flex flex-col gap-y-1 text-start"
          >
            <label
              htmlFor={input}
              className="font-bold"
            >
              {input}
            </label>
            {input.toLowerCase() !== "post body" ? (
              <input
                type="text"
                id={input}
                name={input}
                className="w-full h-12 max-w-3xl px-4 py-2 bg-white border-2 rounded-xl border-primary"
                onChange={handleInputs}
              />
            ) : (
              <div className="relative max-w-3xl">
                <input
                  type="text"
                  id={input}
                  name={input}
                  className="w-full h-12 px-4 py-2 bg-white border-2 rounded-xl border-primary"
                  onChange={handleInputs}
                />
              </div>
            )}
          </div>
        );
      })}
      <Button
        buttonType="text"
        className="max-w-3xl mt-4 rounded-full hover:bg-primary md:hover:bg-secondary-light hover:text-white"
        type="submit"
      >
        Create Post
      </Button>
    </form>
  );
};

export default MakePost;