//#region imports
import axios from "axios";
import { useEffect, useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { PostForm } from "../data/PostForm";
import { PostModel } from "../data/PostModel";
import PostList from "../profile/PostList";
import { AuthorModel } from "../data/AuthorModel";
//#endregion

const Home = () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [user, setUser] = useState<any>({});
  const [posts, setPosts] = useState<PostModel[]>([]);
  const [refresh, setRefresh] = useState(false);
  const [author, setAuthor] = useState<AuthorModel>({} as AuthorModel);

  useEffect(() => {
    //#region funtions
    /**
     * Retrieves the user data from the backend
     */

    const retrieveCurrentUser = async () => {
      try {
        const response = await axios.get("/curUser");
        if (response.data.success == true) {
          const userData = response.data;
          setUser(userData);
        }
      } catch (error) {
        console.error(error);
      }
    };

    //#endregion

    retrieveCurrentUser();
  }, []);

  useEffect(() => {
    /**
     * Retrieves the author Object from the backend
     */

    const retrieveAuthor = async () => {
      try {
        const response = await axios.get(`/espresso-api/authors/${user.id}`);
        const authorData = response.data;
        setAuthor(authorData);
      } catch (error) {
        console.error(error);
      }
    };
    if (user.id) retrieveAuthor();
  }, [user]);

  useEffect(() => {
    /**
     * Retrieves the posts from the backend
     */
    const retrievePosts = async () => {
      try {
        const response = await axios.get(`${author.id}/posts/`);
        const allData = response.data;
        const posts = allData.items;

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const postModels = posts.map((rawpost: any) => {
          return {
            title: rawpost.title,
            id: rawpost.id,
            author: rawpost.author,
            description: rawpost.description,
            contentType: rawpost.contentType,
            content: rawpost.content,
            count: rawpost.count,
            origin: rawpost.origin,
            source: rawpost.source,
            published: rawpost.published,
            visibility: rawpost.visibility,
            likecount: rawpost.likecount,
            sharecount: rawpost.sharecount,
          };
        });
        setPosts(postModels);
      } catch (error) {
        console.error(error);
      }
    };

    if (author.id) retrievePosts();
  }, [author, refresh]);

  //#endregion
  return (
    <div className="flex flex-col w-full px-4 py-8 gap-y-4 sm:px-12 md:px-20 md:items-center md:justify-center">
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
