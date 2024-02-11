//#region imports
import React, { useState } from "react";
//#endregion

// components
import { Button } from "../Button";

const Profile = () => {
  return (
    <div className="flex flex-col items-center justify-first-line:center gap-y-4">
      <div className="relative">
        <div className="w-48 h-48 rounded-full md:w-60 md:h-60 bg-accent-3"></div>
        <Button
          className="absolute right-4 top-4"
          buttonType="icon"
          icon="src/assets/icons/edit.svg"
        ></Button>
      </div>

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

  const [currentTopic, setCurrentTopic] = useState(topics[0].context);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    setCurrentTopic((e.target as HTMLButtonElement).innerText);
  };

  return (
    <div className="flex flex-col gap-y-8">
      <Profile />
      <ul className="flex items-center justify-between gap-x-4">
        {topics.map((topic, index) => (
          <button
            key={index}
            onClick={handleClick}
            // buttonType="text"
            className={`w-1/2 py-3 text-base text-white rounded-lg md:text-lg md:py-4 bg-primary hover:bg-secondary-light ${
              currentTopic === topic.context ? "bg-secondary-light" : ""
            }`}
          >
            {topic.context}
          </button>
        ))}
      </ul>
    </div>
  );
};

export default ProfilePage;
