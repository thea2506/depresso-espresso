//#region imports
import React, { useState } from "react";

// components
import { Button } from "../Button";
import { Profile } from "./Profile";
import { GitHubActionsList } from "../data/GithubActionsList";
//#endregion

/**
 * Renders a profile page component.
 * @returns The rendered profile page component.
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
        imageURL="https://images.unsplash.com/photo-1626808642875-0aa545482dfb?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
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
          github="https://github.com/thea2506"
          displayName="Taylor Adams"
        />
      )}
    </div>
  );
};

export default ProfilePage;
