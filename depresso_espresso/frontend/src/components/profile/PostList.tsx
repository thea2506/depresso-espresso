//#region imports
import { PostModel } from "../data/PostModel";
import { PostView } from "../data/PostView";
import { twMerge } from "tailwind-merge";
//#endregion

//#region interfaces
interface PostListProps {
  posts: PostModel[];
  className?: string;
  refresh: boolean;
  setRefresh: (refresh: boolean) => void;
}
//#endregion

const PostList = ({ posts, refresh, setRefresh, className }: PostListProps) => {
  return (
    <ul
      className={twMerge(
        "flex flex-col items-center justify-center gap-y-8 w-full",
        className
      )}
    >
      {posts.map((post: PostModel) => (
        <PostView
          post={post}
          refresh={refresh}
          setRefresh={setRefresh}
        />
      ))}
    </ul>
  );
};

export default PostList;
