import PostView from "../data/PostView";


const PostList = ({ posts }:{posts:any}) => {
  return (
    <div style={{ overflowY: 'auto' }}>

      <ul>
        {posts.map((post:any) => (
          <li> 
           <PostView username={post.username} content={post.content} user_img_url={post.post} />
          </li>
        
        ))}
      </ul>
    </div>
  );
};

export default PostList;
