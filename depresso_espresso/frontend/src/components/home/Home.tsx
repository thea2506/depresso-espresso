//#region imports
import axios from "axios";
import { useContext, useEffect, useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { PostForm } from "../data/PostForm";
import { PostModel } from "../data/PostModel";
import PostList from "../profile/PostList";
import AuthContext from "../../contexts/AuthContext";
//#endregion

const Home = () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [refresh, setRefresh] = useState<boolean>(false);
  const { curUser } = useContext(AuthContext);
  const [posts, setPosts] = useState<PostModel[]>([]);
  //#endregion

  useEffect(() => {
    const getFeed = async () => {
      const res = await axios.get(
        `${import.meta.env.VITE_BACKEND_URL}/api/feed`
      );
      if (res.status !== 200) return;
      console.log(res.data.items);
      setPosts(res.data.items);
    };

    getFeed();
  }, [refresh]);

  if (!Object.entries(curUser).length) return <></>;

  return (
    <div className="flex flex-col w-full px-4 py-8 gap-y-4 sm:px-12 md:px-20 md:items-center md:justify-center">
      <ToastContainer />
      <PostForm
        author={curUser}
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
