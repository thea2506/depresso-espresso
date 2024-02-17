//#region imports
import React, { useState } from "react";

// components
import { Button } from "../Button";
import { Profile } from "./Profile";
import { GitHubActionsList } from "./GithubActionsList";
//#endregion

/**
 * Represents the profile page component.
 * @component
 */
const ProfilePage = () => {
  const topics = [
    { context: "Posts" },
    { context: "GitHub" },
    { context: "Followers" },
  ];

  const [currentTopic, setCurrentTopic] = useState<string>(topics[0].context);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    setCurrentTopic((e.target as HTMLButtonElement).innerText);
  };

  return (
    <div className="flex flex-col gap-y-8">
      {/* TODO: Pull profile picture, username and github (optional) from the db */}
      <Profile
        username="Taylor Adams"
        avatarURL="src/assets/images/profile.jpg"
        github="https://github.com/thea2506"
      />
      <ul className="flex items-center justify-between gap-x-2 sm:gap-x-4">
        {topics.map((topic, index) => (
          <Button
            key={index}
            onClick={handleClick}
            buttonType="text"
            className={
              currentTopic === topic.context
                ? "w-1/2 md:text-lg bg-secondary-light"
                : "w-1/2 md:text-lg"
            }
          >
            {topic.context}
          </Button>
        ))}
      </ul>
      {currentTopic === "GitHub" && (
        <GitHubActionsList
          username="thea2506"
          displayName="Thea Nguyen"
        />
      )}
    </div>
  );
};

export default ProfilePage;
