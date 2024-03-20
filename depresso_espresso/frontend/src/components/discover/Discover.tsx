/* eslint-disable @typescript-eslint/no-explicit-any */
//#region imports
// import axios from "axios";
// import { useContext, useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
// import { PostForm } from "../data/PostForm";
// import { PostModel } from "../data/PostModel";
// import PostList from "../profile/PostList";

// import AuthorSearch from "../data/AuthorSearch";
import { useEffect, useState } from "react";
import axios, { AxiosError } from "axios";
import { AuthorModel } from "../data/AuthorModel";
import { Button } from "../Button";
import {
  GoPlusCircle,
  GoCheckCircle,
  GoCodeOfConduct,
  GoClock,
} from "react-icons/go";

import { ToastContainer, toast, ToastOptions } from "react-toastify";

const myToast: ToastOptions<unknown> = {
  position: "top-center",
  autoClose: 2000,
  hideProgressBar: false,
  pauseOnHover: false,
  closeOnClick: true,
  theme: "light",
  closeButton: false,
};

const MY_USERNAME = import.meta.env.VITE_USERNAME;
const MY_USERPASSWORD = import.meta.env.VITE_PASSWORD;

const Discover = () => {
  const [allAuthors, setAllAuthors] = useState<AuthorModel[]>([]);
  const [user, setUser] = useState<AuthorModel | null>(null);
  const [followers, setFollowers] = useState<AuthorModel[]>([]);
  const [refresh, setRefresh] = useState(false);
  const [followStatuses, setFollowStatuses] = useState<string[]>(
    [] as string[]
  );

  useEffect(() => {
    async function fetchAuthors() {
      const response = await axios.get("/espresso-api/all-authors/");
      if (response.status === 200) {
        setAllAuthors(response.data.items);
      }
    }
    fetchAuthors();

    async function fetchUser() {
      const response = await axios.get("/curUser");
      if (response.status === 200) {
        setUser(response.data);
      }
    }

    fetchUser();
  }, [refresh]);

  useEffect(() => {
    async function fetchFollowers() {
      if (!user) return;
      const response = await axios.get(
        `/espresso-api/authors/${user.id}/followers`
      );
      if (response.status === 200) {
        setFollowers(response.data.items);
      }
    }
    fetchFollowers();
  }, [user, refresh]);

  useEffect(() => {
    async function fetchFollowStatus(author: AuthorModel) {
      if (!user) return "";
      try {
        await axios.get(
          `${author.url}/followers/${encodeURIComponent(
            encodeURIComponent(user.url)
          )}`,
          { auth: { username: MY_USERNAME, password: MY_USERPASSWORD } }
        );
        if (followers.some((elem) => elem.id === author.id)) {
          return "friends";
        } else {
          return "followed";
        }
      } catch (error: any) {
        if (error.response?.data.status === "pending") {
          return "pending";
        } else return "stranger";
      }
    }

    async function fetchFollowStatuses() {
      const s = allAuthors.map(async (author) => {
        const response = await fetchFollowStatus(author);
        return response;
      });
      setFollowStatuses(await Promise.all(s));
    }
    fetchFollowStatuses();
  }, [user, allAuthors, followers, refresh]);

  const handleFollowRequest = async (author: AuthorModel) => {
    try {
      const actor_object = await axios.get(`/espresso-api/authors/${user?.id}`);
      const response = await axios.post(
        `${author.url}/inbox`,
        {
          type: "Follow",
          summary: `${user?.displayName} wants to follow ${author.displayName}`,
          actor: actor_object.data,
          object: author,
        },
        {
          auth: {
            username: "localhost",
            password: "canada123!",
          },
        }
      );
      if (response.status === 200) {
        toast.success("Follow request sent", myToast);
      }
      setRefresh(!refresh);
    } catch (error) {
      toast.error("Failed to send follow request", myToast);
    }
  };

  const handleUnffollowRequest = async (author: AuthorModel) => {
    try {
      const response = await axios.delete(
        `${author.url}/followers/${encodeURIComponent(
          encodeURIComponent(user!.url)
        )}`
      );
      if (response.data.success === true) {
        toast.success("Unfollowed", myToast);
      }
      setRefresh(!refresh);
    } catch (error) {
      toast.error("Failed to unfollow", myToast);
    }
  };

  //#endregion
  return (
    <div className="flex flex-col items-center justify-center w-full">
      {/* <AuthorSearch></AuthorSearch> */}
      <ToastContainer />
      <h1 className="mb-8 text-4xl font-bold">Discover</h1>
      <div className="flex flex-col w-4/5 gap-4">
        {allAuthors.map((author, key: number) => {
          if (author.url === user?.url) return null;
          return (
            <div
              key={key}
              className="flex items-center justify-start w-full gap-4 p-4 rounded-lg bg-secondary-light"
            >
              <h2 className="text-xl font-bold">{author.displayName}</h2>
              <span className="p-2 rounded-xl bg-accent-3">
                {author.host.includes(window.location.origin)
                  ? "Local"
                  : "Remote"}
              </span>
              {followStatuses[key] === "stranger" ? (
                <Button
                  buttonType="icon"
                  icon={<GoPlusCircle />}
                  onClick={() => {
                    handleFollowRequest(author);
                  }}
                  className="text-xl text-white"
                />
              ) : followStatuses[key] === "followed" ? (
                <Button
                  buttonType="icon"
                  icon={<GoCheckCircle />}
                  onClick={() => {
                    handleUnffollowRequest(author);
                  }}
                  className="text-xl text-white"
                />
              ) : followStatuses[key] === "pending" ? (
                <Button
                  buttonType="icon"
                  icon={<GoClock />}
                  onClick={() => {
                    toast.info("Follow request pending", myToast);
                  }}
                  className="text-xl text-white"
                />
              ) : (
                <Button
                  buttonType="icon"
                  icon={<GoCodeOfConduct />}
                  onClick={() => {
                    toast.info("Friends", myToast);
                  }}
                  className="text-xl text-white"
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Discover;
