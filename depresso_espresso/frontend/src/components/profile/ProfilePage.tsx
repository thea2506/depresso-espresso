//#region imports
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

// components
import { Button } from "../Button";
import { Profile } from "./Profile";
import { GitHubActionsList } from "../data/GithubActionsList";
import PostList from "./PostList";
import FollowerList from "./FollowerList";
import { PostModel } from "../data/PostModel";
import { AuthorModel } from "../data/AuthorModel";
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
  const [followers, setFollowers] = useState<AuthorModel[]>([]);

  //#region functions
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    setCurrentTopic((e.target as HTMLButtonElement).innerText);
  };

  useEffect(() => {
    const getData = async () => {
      try {
        const response = await axios.get(`/espresso-api/authors/${authorId}`);
        const data = response.data;
        setDisplayName(data.displayName);
        setGithubLink(data.github);
        setProfileImage(data.profileImage);
      } catch (error) {
        console.error("An error occurred", error);
      }
    };

    const fetchFollowers = async () => {
      try {
        console.log("authorId", authorId);
        const response = await axios.get(`/authors/${authorId}/followers/`);
        const data = response.data;

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const followerModels = data?.map((rawauthor: any) => ({
          type: rawauthor.type,
          id: rawauthor.id,
          url: rawauthor.url,
          host: rawauthor.host,
          displayName: rawauthor.displayName,
          username: rawauthor.username,
          github: rawauthor.github,
          profileImage: rawauthor.profileImage,
        }));
        setFollowers(followerModels);
      } catch (error) {
        console.error(error);
      }
    };
    fetchFollowers();

    const retrievePosts = async () => {
      try {
        const response = await axios.get(`/authors/${authorId}/posts`);
        const allData = response.data;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const postModels = allData.posts.map((rawpost: any) => {
          const author = allData.authors[0];
          author.fields.id = author.pk;
          return {
            // type: rawpost.fields.type,
            title: rawpost.fields.title,
            id: rawpost.pk,

            author: author,

            description: rawpost.fields.description,
            contenttype: rawpost.fields.contentType,
            content: rawpost.fields.content,

            count: rawpost.fields.count,

            published: rawpost.fields.published,
            visibility: rawpost.fields.visibility,

            likecount: rawpost.fields.likecount,
            sharecount: rawpost.fields.sharecount,
          };
        });
        setPosts(postModels);
      } catch (error) {
        console.error(error);
      }
    };
    getData();
    retrievePosts();
  }, [authorId, loading]);

  //#endregion
  return (
    <div className="flex flex-col w-full px-4 gap-y-8 sm:px-12 md:px-20">
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
      {currentTopic === "GitHub" && githubLink ? (
        <GitHubActionsList
          github={githubLink}
          displayName={displayName}
        />
      ) : null}

      {currentTopic === "GitHub" && !githubLink ? (
        <div className="flex items-center justify-center text-lg opacity-80">
          No Github link...
        </div>
      ) : null}

      {/* Followers Topic */}
      {currentTopic === "Followers" && followers.length > 0 && (
        <FollowerList followers={followers} />
      )}

      {currentTopic === "Followers" && followers.length == 0 && (
        <div className="flex items-center justify-center text-lg opacity-80">
          No followers yet...
        </div>
      )}

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
          No posts yet... or maybe it is loading!
        </div>
      )}
    </div>
  );
};

export default ProfilePage;
