const Profile = () => {
  return (
    <div className="flex flex-col items-center justify-first-line:center gap-y-4">
      <div className="w-48 h-48 rounded-full md:w-64 md:h-64 bg-accent-3"></div>

      <div className="flex flex-col">
        <p className="text-lg font-semibold md:text-xl opacity-95">
          Thea Nguyen
        </p>
        <p className="text-sm md:text-base text-secondary-dark">
          https://github.com/thea2506
        </p>
      </div>
    </div>
  );
};

const ProfilePage = () => {
  const topics = [
    { context: "Posts" },
    { context: "GitHub" },
    { context: "Followers" },
  ];

  const handleClick = () => {
    console.log("Move to new section");
  };

  return (
    <div className="flex flex-col mx-0 md:mx-8 gap-y-12">
      <Profile />
      <ul className="flex items-center justify-between gap-x-4">
        {topics.map((topic, index) => (
          <button
            key={index}
            onClick={handleClick}
            className="w-1/2 py-3 text-base text-white rounded-lg md:text-lg md:py-4 bg-primary"
          >
            {topic.context}
          </button>
        ))}
      </ul>
    </div>
  );
};

export default ProfilePage;
