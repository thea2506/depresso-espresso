//#region imports
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { PostForm } from "../data/PostForm";
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

const Home = () => {
  //   const [display_name, setDisplayName] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [image_url, setImage] = useState<string>("");

  const navigate = useNavigate();

  //#region funtions
  /**
   * Retrieves the user data from the backend
   */
  const retrieveData = async () => {
    try {
      const response = await axios.get("/user_data");
      // setDisplayName(response.data.display_name);
      setUsername(response.data.username);
      setImage(response.data.profile_image);
    } catch (error) {
      toast.error("Please Sign in to go further", myToast);
      navigate("/signin");
      console.error(error);
    }
  };

  const posts: PostModel[] = [{ username: "test4", content: "testtttttttttttttt" }, { username: "scott", content: "this is some text" }];

  retrieveData();
  //#endregion

  return (
    <div className="flex flex-col items-center justify-center w-full">
      <ToastContainer />
      <PostForm
        username={username}
        user_img_url={image_url}
      />
    </div>
  );
};

export default Home;
