//#region imports
import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { PostForm } from "../data/PostForm";
import { PostModel } from "../data/PostModel";
import PostList from "../profile/PostList";
//#endregion

const Home = () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [author, setAuthor] = useState<any>({});
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
        const allData = response.data;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const postModels = allData.posts.map((rawpost: any, index: number) => {
          const author = allData.authors[index];
          author.fields.id = author.pk;
          return {
            author: author,

            id: rawpost.pk,
            title: rawpost.fields.title,
            description: rawpost.fields.description,
            contenttype: rawpost.fields.contentType,
            content: rawpost.fields.content,
            count: rawpost.fields.count,
            published: rawpost.fields.published,
            visibility: rawpost.fields.visibility,

            likes: rawpost.fields.liked_by.length,
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
