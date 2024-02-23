import axios from "axios";

//#region imports
import React, { useState } from "react";

// components
import { Button } from "../Button";
import { Profile } from "./Profile";
import { GitHubActionsList } from "../data/GithubActionsList";
import { animated, useSpring } from "@react-spring/web";
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

  const [displayName, setDisplayName] = useState("");
  const [githubLink, setGithubLink] = useState("");
  const [profileImage, setProfileImage] = useState("");
  const [currentTopic, setCurrentTopic] = useState<string>(topics[0].context);
  const [loading, setLoading] = useState<boolean>(false);
  const springs = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 },
  });

  //#region functions
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    setCurrentTopic((e.target as HTMLButtonElement).innerText);
    console.log(githubLink, "githubLink");
  };

  const getData = async () => {
    try {
      const response = await axios.get("/user_data");
      const data = await response.data;
      setDisplayName(data["display_name"]);
      setGithubLink(data["github_link"]);
      setProfileImage(data["profile_image"]);
    } catch (error) {
      console.error("An error occurred", error);
    }
    // This could probably be combined into 1 request using render context
  };
  getData();
  //#endregion

  return (
    <animated.div
      className="flex flex-col px-4 gap-y-8 sm:px-12 md:px-20"
      style={springs}
    >
      <Profile
        display_name={displayName}
        imageURL={profileImage}
        github={githubLink}
        loading={loading}
        setLoading={setLoading}
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
      {currentTopic === "GitHub" && githubLink !== "" && (
        <GitHubActionsList
          github={githubLink}
          displayName={displayName}
        />
      )}
      {currentTopic === "GitHub" && githubLink === "" && (
        <div className="flex items-center justify-center text-lg opacity-80">
          Link your Github...
        </div>
      )}
    </animated.div>
  );
};

export default ProfilePage;
