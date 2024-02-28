import axios from "axios";

//#region imports
import React, { useEffect, useState } from "react";

// components
import { Button } from "../Button";
import { Profile } from "./Profile";
import { GitHubActionsList } from "../data/GithubActionsList";
import { animated, useSpring } from "@react-spring/web";
import FollowList from "./FollowList";
import PostList from "./PostList";
import { PostModel } from "../data/PostModel";
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
  const [followers, setFollowers] = useState("");
  const [githubLink, setGithubLink] = useState("");
  const [profileImage, setProfileImage] = useState("");
  const [currentTopic, setCurrentTopic] = useState<string>(topics[0].context);
  const [loading, setLoading] = useState<boolean>(false);
  const [posts, setPosts] = useState<PostModel[]>([]);
  const springs = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 },
  });

  //#region functions
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    setCurrentTopic((e.target as HTMLButtonElement).innerText);
    console.log(followers);
  };

  const getData = async () => {
    try {
      const response = await axios.get("/user_data");
      const data = await response.data;
      setDisplayName(data["display_name"]);
      setGithubLink(data["github_link"]);
      setProfileImage(data["profile_image"]);
      setFollowers(data["followers"]);
    } catch (error) {
      console.error("An error occurred", error);
    }
    // This could probably be combined into 1 request using render context
  };

  const retrievePosts = async () => {
    try {
      const response = await axios.get("/get_author_posts");
      const postData = response.data;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const postModels = postData.map((rawpost: any) => {
        return {
          authorid: rawpost.fields.authorid,
          content: rawpost.fields.content,
          postid: rawpost.pk,
          user_img_url: rawpost.fields.user_img_url,
          likes: rawpost.fields.liked_by.length,
          commentcount: rawpost.fields.commentcount,
          username: rawpost.fields.authorname,
          publishdate: rawpost.fields.publishdate,
        };
      });
      console.log("postmodels", postModels);
      setPosts(postModels);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    retrievePosts();
  }, []);

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

      {/* Github Topic */}
      {currentTopic === "GitHub" &&
        (githubLink === "" || githubLink !== null) && (
          <GitHubActionsList
            github={githubLink}
            displayName={displayName}
          />
        )}
      {currentTopic === "GitHub" &&
        (githubLink === "" || githubLink === null) && (
          <div className="flex items-center justify-center text-lg opacity-80">
            Link your Github...
          </div>
        )}

      {/* Followers Topic */}
      {currentTopic === "Followers" &&
        followers != null &&
        followers != undefined && <FollowList followers={followers} />}

      {currentTopic === "Followers" &&
        (followers === null || followers === undefined) && (
          <div className="flex items-center justify-center text-lg opacity-80">
            Make more friends ... Is this a clone account?
          </div>
        )}

      {/* Posts Topic */}
      {currentTopic === "Posts" && posts.length > 0 && (
        <PostList posts={posts} />
      )}

      {currentTopic === "Posts" && posts.length === 0 && (
        <div className="flex items-center justify-center text-lg opacity-80">
          No posts yet...
        </div>
      )}
    </animated.div>
  );
};

export default ProfilePage;
