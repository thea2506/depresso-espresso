




const FollowList = ({ followers }:{followers:any}) => {
  return (
    <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
      <ul>
        {followers.map((follower:any, index: any) => (
          <li key={index}>{follower}</li>
        ))}
      </ul>
    </div>
  );
};

export default FollowList;
