//#region imports
import axios from "axios";
import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { PostForm } from "../data/PostForm";
import { PostModel } from "../data/PostModel";
import PostList from "../profile/PostList";
import { AuthContext } from "../../App";
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
  const { setAuthorID } = useContext(AuthContext);
  const [refresh, setRefresh] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
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
        localStorage.setItem("authorid", response.data.authorid);
        setAuthorID(response.data.authorid);
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
            visibility: rawpost.fields.visibility,
            image_url: rawpost.fields.image_url,
            contenttype: rawpost.fields.contenttype,
          };
        });
        console.log("postmodels", postModels);
        setPosts(postModels);
      } catch (error) {
        console.error(error);
      }
    };
    retrievePosts();
    retrieveData();
  }, [navigate, setAuthorID, refresh]);
  //#endregion
  return (
    <div className="flex flex-col w-full px-4 gap-y-4 sm:px-12 md:px-20 md:items-center md:justify-center">
      <ToastContainer />
      <PostForm
        username={username}
        user_img_url={image_url}
        edit={false}
        refresh={refresh}
        setRefresh={setRefresh}
      />

      <PostList
        posts={posts}
        className="w-full mt-8 lg:w-1/2"
        refresh={refresh}
        setRefresh={setRefresh}
      />
    </div>
  );
};

export default Home;
