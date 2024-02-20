import axios from 'axios';

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

  const [display_name, setDisplayName] = useState("");
  const [github_link, setGithub] = useState("");
  const [profile_image, setProfImage] = useState("");
  const [currentTopic, setCurrentTopic] = useState<string>(topics[0].context);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    setCurrentTopic((e.target as HTMLButtonElement).innerText);
  };

  const getData = async () => {
    try{
        const response = await axios.get("user_data");
        setDisplayName(response.data['display_name'])
        setGithub(response.data['github_link'])
        setProfImage(response.data['profile_image'])
    } catch (error) {
      console.error("An error occurred", error);
    }
    // This could probably be combined into 1 request using render context

    try{ 
      await axios.get("profile");
    } catch (error) {
      console.error("An error occurred", error); 
    } 
  
  }
  getData(); // send request to profile endpoint to retrieve current user's info and render the component

  return (
    <div className="flex flex-col gap-y-8">
      {/* TODO: Pull profile picture, username and github (optional) from the db */}
      <Profile
        display_name= {display_name}
        imageURL= {profile_image}
        github={github_link}
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
          github={github_link}
          displayName={display_name}
        />
      )}
    </div>
  );
};


export default ProfilePage;
