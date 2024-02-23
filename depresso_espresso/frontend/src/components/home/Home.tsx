//#region imports
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
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
      const response = await axios.get("/user");
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
    <div>
      <ToastContainer />
      <h3>{display_name} home page</h3>
      <p>This component shows a cat.</p>
      <p>You must be signed in to view</p>
    </div>
  );
};

export default Home;
