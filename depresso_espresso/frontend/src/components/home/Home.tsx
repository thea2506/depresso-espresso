//#region imports
import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { PostForm } from "../data/PostForm";
import { PostModel } from "../data/PostModel";
import PostList from "../profile/PostList";
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
  const [posts, setPosts] = useState<PostModel[]>([]);

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

  /**
   * Retrieves the posts from the backend
   */
  const retrievePosts = async () => {
    try {
      const response = await axios.get("/get_all_posts");
      const postData = response.data;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const postModels = postData.map((rawpost: any) => {
        return {
          authorid: rawpost.fields.authorid,
          content: rawpost.fields.content,
          postid: rawpost.pk,
          user_img_url: rawpost.fields.user_img_url,
          likes: rawpost.fields.liked_by.length,
          commentcount: rawpost.fields.commentcount,
          username: rawpost.fields.authorname,
          publishdate: rawpost.fields.publishdate,
        };
      });
      console.log("postmodels", postModels);
      setPosts(postModels);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    retrievePosts();
  }, []);

  retrieveData();
  //#endregion

  return (
    <div className="flex flex-col items-center justify-center w-full">
      <ToastContainer />
      <PostForm
        username={username}
        user_img_url={image_url}
      />

      <PostList
        posts={posts}
        className="w-full lg:w-1/2"
      />
    </div>
  );
};

export default Home;
