//#region imports
import { PostModel } from "../data/PostModel";
import { PostView } from "../data/PostView";
import { twMerge } from "tailwind-merge";
//#endregion

//#region interfaces
interface PostListProps {
  posts: PostModel[];
  className?: string;
}
//#endregion

const PostList = ({ posts, className }: PostListProps) => {
  return (
    <ul
      className={twMerge(
        "flex flex-col items-center justify-center w-full gap-y-4",
        className
      )}
    >
      {posts.map((post: PostModel) => (
        <li className="flex flex-col items-center justify-center w-full gap-y-4">
          <PostView post={post} />
        </li>
      ))}
    </ul>
  );
};

export default PostList;
