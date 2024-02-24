//#region imports
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Post from "../data/Post";
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
  const [display_name, setDisplayName] = useState<string>("");
  const navigate = useNavigate();

  //#region funtions
  /**
   * Retrieves the user data from the backend
   */
  const retrieveData = async () => {
    try {
      const response = await axios.get("/user_data");
      setDisplayName(response.data.display_name);
    } catch (error) {
      toast.error("Please Sign in to go further", myToast);
      navigate("/signin");
      console.error(error);
    }
  };

  retrieveData();
  //#endregion

  return (
    <div className="flex flex-col items-center justify-center">
      <ToastContainer />
      <p>Current user: {display_name}</p>
      <h1>
        POST COMPONENTS WILL APPEAR HERE AS A PUBLIC NEWSFEED (same as in
        design)
        <Post />
      </h1>
    </div>
  );
};

export default Home;
