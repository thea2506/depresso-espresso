//#region imports
import React, { useContext, useEffect, useState } from "react";
import axios from "axios";
import { useLocation, useParams } from "react-router-dom";

// components
import { Button } from "../Button";
import { Profile } from "./Profile";
import { GitHubActionsList } from "../data/GithubActionsList";
import PostList from "./PostList";
import FollowerList from "./FollowerList";
import { PostModel } from "../data/PostModel";
import { AuthorModel } from "../data/AuthorModel";
import AuthContext from "../../contexts/AuthContext";
// import defaultPic from "../../assets/images/default_profile.jpg";
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
  const { state } = useLocation();

  const { authorId, "*": splat } = useParams();
  const { curUser } = useContext(AuthContext);
  const [currentTopic, setCurrentTopic] = useState<string>(topics[0].context);
  const [refresh, setRefresh] = useState<boolean>(false);
  const [posts, setPosts] = useState<PostModel[]>([]);
  const [followers, setFollowers] = useState<AuthorModel[]>([]);
  const [thisProfileUser, setThisProfileUser] = useState<AuthorModel | null>(
    curUser && authorId && curUser.id === authorId ? curUser : null
  );

  //#region functions
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    setCurrentTopic((e.target as HTMLButtonElement).innerText);
  };

  useEffect(() => {
    const getData = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/api/authors/${
            authorId ? authorId + "/" : splat
          }`
        );
        const data = response.data;
        const authorUrl = data.url;
        setThisProfileUser(data);

        // followers
        try {
          const response = await axios.get(`${authorUrl}/followers`, {
            auth: {
              username: import.meta.env.VITE_USERNAME,
              password: import.meta.env.VITE_PASSWORD,
            },
          });
          const data = response.data;
          const followerModels = (data?.items as AuthorModel[]) || [];
          if (followerModels) setFollowers(followerModels);
        } catch (error) {
          /* empty */
        }

        // posts
        try {
          const response = await axios.get(`${authorUrl}/posts/`, {
            auth: {
              username: import.meta.env.VITE_USERNAME,
              password: import.meta.env.VITE_PASSWORD,
            },
            params: curUser,
          });
          const posts = response.data;
          const postModels = (posts.items as PostModel[]) || [];
          setPosts(postModels);
        } catch (error) {
          // empty
        }

        if (state && state.reload) state.reload = false;
      } catch (error) {
        console.error("An error occurred", error);
      }
    };

    if (!thisProfileUser || state?.reload) {
      getData();
    }
  }, [thisProfileUser, authorId, refresh, splat, state, curUser]);

  //#endregion

  return (
    <div className="flex flex-col w-full px-4 py-8 gap-y-8 sm:px-12 md:px-20">
      {thisProfileUser && (
        <Profile
          user={thisProfileUser}
          setUser={setThisProfileUser}
          refresh={refresh}
          setRefresh={setRefresh}
        />
      )}
      {thisProfileUser && (
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
      )}

      {/* Github Topic */}
      {currentTopic === "GitHub" && thisProfileUser?.github ? (
        <GitHubActionsList
          github={thisProfileUser?.github}
          displayName={thisProfileUser?.displayName}
        />
      ) : null}

      {currentTopic === "GitHub" && !thisProfileUser?.github ? (
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
          refresh={refresh}
          setRefresh={setRefresh}
        />
      )}

      {currentTopic === "Posts" && posts.length == 0 && (
        <div className="flex items-center justify-center text-lg opacity-80">
          No posts yet... or maybe it is refresh!
        </div>
      )}
    </div>
  );
};

export default ProfilePage;
