import { PostModel } from "../data/PostModel";
import { PostView } from "../data/PostView";


const PostList = ({ posts }:{posts:PostModel[]}) => {
  return (
      <ul className="flex flex-col items-center justify-center w-full px-6 md:px-8 lg:px-0 gap-y-4">
        {posts.map((post:PostModel) => (
          <li className="flex flex-col items-center justify-center w-full px-6 md:px-8 lg:px-0 gap-y-4"  style={{margin: '10px 0px'}}> 
           <PostView post={post} />
          </li>
        ))}
      </ul>
  );
};

export default PostList;
