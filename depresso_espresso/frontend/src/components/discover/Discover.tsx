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

const Discover = () => {
  // const { setAuthorID } = useContext(AuthContext);

  //#endregion
  return (
    <div className="flex flex-col items-center justify-center w-full">
      <AuthorSearch></AuthorSearch>
    </div>
  );
};

export default Discover;
