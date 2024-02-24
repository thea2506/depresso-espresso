




const PostList = ({ posts }:{posts:any}) => {
  return (
    <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
      <ul>
        {posts.map((post:any, index: any) => (
          <li key={index}>{post}</li>
        ))}
      </ul>
    </div>
  );
};

export default PostList;
