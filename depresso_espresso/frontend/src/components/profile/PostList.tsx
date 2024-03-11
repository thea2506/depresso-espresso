//#region imports
import React from "react";
import { useState } from "react";
import { PostModel } from "../data/PostModel";
import { PostView } from "../data/PostView";
import { twMerge } from "tailwind-merge";
import { useEffect } from "react";
import { AuthorModel } from "../data/AuthorModel";
import axios from "axios";
//#endregion

//#region interfaces
interface PostListProps {
  posts: PostModel[];
  className?: string;
  refresh: boolean;
  setRefresh: React.Dispatch<React.SetStateAction<boolean>>;
}
//#endregion

const PostList = ({ posts, refresh, setRefresh, className }: PostListProps) => {
  const [curUser, setCurUser] = useState({} as AuthorModel);

  useEffect(() => {
    const retrieveData = async () => {
      try {
        const response = await axios("/curUser");
        if (response.data.success) {
          setCurUser(response.data);
        }
      } catch (error) {
        console.error(error);
      }
    };
    retrieveData();
  }, []);

  return (
    <ul
      className={twMerge(
        "flex flex-col items-center justify-center gap-y-8 w-full",
        className
      )}
    >
      {posts.map((post: PostModel) => (
        <PostView
          curUser={curUser}
          post={post}
          refresh={refresh}
          setRefresh={setRefresh}
        />
      ))}
    </ul>
  );
};

export default PostList;
