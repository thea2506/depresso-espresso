//#region imports
import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { PostForm } from "../data/PostForm";
import { PostModel } from "../data/PostModel";
import PostList from "../profile/PostList";
import { AuthorModel } from "../data/AuthorModel";
//#endregion

const Home = () => {
  const [author, setAuthor] = useState<AuthorModel>({} as AuthorModel);
  const [posts, setPosts] = useState<PostModel[]>([]);
  const [refresh, setRefresh] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    //#region funtions
    /**
     * Retrieves the user data from the backend
     */
    const retrieveData = async () => {
      try {
        const response = await axios.get("/curUser");
        if (response.data.success == true) {
          const userData = response.data;
          setAuthor(userData);
        }
      } catch (error) {
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
          console.log("rawpost", rawpost);
          return {
            username: rawpost.fields.author.displayName,
            // user_img_url: rawpost.fields.author_profile_image,

            // authorid: rawpost.fields.authorid,
            // content: rawpost.fields.content,
            // postid: rawpost.pk,
            // likes: rawpost.fields.liked_by.length,
            // commentcount: rawpost.fields.commentcount,
            // publishdate: rawpost.fields.publishdate,
            // visibility: rawpost.fields.visibility,
            // image_url: rawpost.fields.image_url,
            // contenttype: rawpost.fields.contenttype,
            // image_file: rawpost.fields.image_file,
          };
        });
        console.log("postmodels", postModels);
        setPosts(postModels);
      } catch (error) {
        console.error(error);
      }
    };
    retrieveData();
    retrievePosts();
  }, [navigate, refresh]);

  //#endregion
  return (
    <div className="flex flex-col w-full px-4 gap-y-4 sm:px-12 md:px-20 md:items-center md:justify-center">
      <ToastContainer />
      <PostForm
        author={author}
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
