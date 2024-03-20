//#region imports
// import axios from "axios";
// import { useContext, useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
// import { PostForm } from "../data/PostForm";
// import { PostModel } from "../data/PostModel";
// import PostList from "../profile/PostList";

import AuthorSearch from "../data/AuthorSearch";
import { useEffect, useState } from "react";
import axios from "axios";

const Discover = () => {
  const [allAuthors, setAllAuthors] = useState([]);
  useEffect(() => {
    async function fetchAuthors() {
      const response = await axios.get("/espresso-api/all-authors/");
      console.log(response.data);
    }
    fetchAuthors();
  }, []);
  //#endregion
  return (
    <div className="flex flex-col items-center justify-center w-full">
      {/* <AuthorSearch></AuthorSearch> */}
      <div></div>
    </div>
  );
};

export default Discover;
