//#region imports
import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

// components
import { Button } from "../Button";
import { Profile } from "./Profile";
import { GitHubActionsList } from "../data/GithubActionsList";
import { animated, useSpring } from "@react-spring/web";
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

  const { authorId } = useParams<{ authorId: string }>();
  const [displayName, setDisplayName] = useState("");
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
  };

  useEffect(() => {
    const getData = async () => {
      try {
        const response = await axios.get(`/api/authors/${authorId}`);
        const data = response.data;
        setDisplayName(data.displayName);
        setGithubLink(data.github);
        setProfileImage(data.profileImage);
      } catch (error) {
        console.error("An error occurred", error);
      }
    };
    getData();

    const retrievePosts = async () => {
      try {
        const response = await axios.get("/get_author_posts", {
          params: {
            authorid: authorId,
          },
        });
        const postData = response.data;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const postModels = postData.map((rawpost: any) => {
          return {
            authorid: rawpost.fields.authorid,
            content: rawpost.fields.content,
            postid: rawpost.pk,
            likes: rawpost.fields.liked_by.length,
            commentcount: rawpost.fields.commentcount,
            sharecount: rawpost.fields.shared_by.length,
            username: rawpost.fields.authorname,
            publishdate: rawpost.fields.publishdate,
            visibility: rawpost.fields.visibility,
            image_url: rawpost.fields.image_url,
            image_file: rawpost.fields.image_file,
            contenttype: rawpost.fields.contenttype,
          };
        });
        setPosts(postModels);
      } catch (error) {
        console.error(error);
      }
    };
    retrievePosts();
  }, [authorId, loading, displayName, githubLink, profileImage]);

  //#endregion
  console.log("posts", posts);
  return (
    <animated.div
      className="flex flex-col w-full px-4 gap-y-8 sm:px-12 md:px-20"
      style={springs}
    >
      <Profile
        id={authorId}
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
      {currentTopic === "GitHub" && githubLink != null && (
        <GitHubActionsList
          github={githubLink}
          displayName={displayName}
        />
      )}

      {currentTopic === "GitHub" && githubLink == null && (
        <div className="flex items-center justify-center text-lg opacity-80">
          Link your Github...
        </div>
      )}

      {/* Followers Topic */}

      {/* Posts Topic */}
      {currentTopic === "Posts" && posts.length > 0 && (
        <PostList
          posts={posts}
          refresh={loading}
          setRefresh={setLoading}
        />
      )}

      {currentTopic === "Posts" && posts.length == 0 && (
        <div className="flex items-center justify-center text-lg opacity-80">
          No posts yet...
        </div>
      )}
    </animated.div>
  );
};

export default ProfilePage;
