//#region imports
import React, { useContext } from "react";
import { PostModel } from "../data/PostModel";
import { PostView } from "../data/PostView";
import { twMerge } from "tailwind-merge";
import AuthContext from "../../contexts/AuthContext";
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
  const { curUser } = useContext(AuthContext);
  if (!Object.entries(curUser).length) return <></>;

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
