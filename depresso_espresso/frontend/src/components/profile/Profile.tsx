/* eslint-disable @typescript-eslint/no-explicit-any */
//#region Imports
import { Button } from "../Button";
import Popup from "reactjs-popup";
import { ToastContainer, toast, ToastOptions } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useContext, useEffect, useState } from "react";
import axios from "axios";
import editIcon from "../../assets/icons/edit.svg";
import {
  GoPlusCircle,
  GoCheckCircle,
  GoCodeOfConduct,
  GoClock,
} from "react-icons/go";
import defaultPic from "../../assets/images/default_profile.jpg";
import { AuthorModel } from "../data/AuthorModel";
import AuthContext from "../../contexts/AuthContext";
//#endregion

//#region interfaces
interface ProfileProps {
  user: AuthorModel;
  setUser: React.Dispatch<React.SetStateAction<AuthorModel | null>>;
  refresh: boolean;
  setRefresh: (loading: boolean) => void;
}
//#endregion

/**
 * Renders a profile component with the given username, GitHub link, and avatar URL.
 *
 * @component
 * @param {Object} props - The component props.
 * @oaram {Boolean} props.refresh - The loading state.
 * @param {Function} props.setRefresh - The function to set the loading state.
 * @returns {JSX.Element} The rendered profile component.
 */
const Profile = ({
  user,
  setUser,
  refresh,
  setRefresh,
}: ProfileProps): JSX.Element => {
  //#region variables
  const myToast: ToastOptions<unknown> = {
    position: "top-center",
    autoClose: 2000,
    hideProgressBar: false,
    pauseOnHover: false,
    closeOnClick: true,
    theme: "light",
    closeButton: false,
  };
  const editFields = [
    {
      label: "Display Name",
      value: "displayName",
      placeholder: user.displayName,
    },
    { label: "GitHub URL", value: "github", placeholder: user.github },
    { label: "Image URL", value: "image", placeholder: user.profileImage },
  ];

  const [newDisplayName, setDisplayName] = useState<string>(user.displayName);
  const [newGithub, setGithub] = useState<string>(user.github || "");
  const [newImageURL, setImageURL] = useState<string>(user.profileImage || "");
  const { curUser, setCurUser } = useContext(AuthContext);
  const [otherUser, setOtherUser] = useState<AuthorModel>();

  // Follow
  const [status, setStatus] = useState<string>();

  const [open, setOpen] = useState<boolean>(false);
  const closeModal = () => setOpen(false);

  //#endregion
  //#region Functions

  useEffect(() => {
    const getOtherUser = async () => {
      const response = await axios.get(`${user.url}`);
      const data = response.data;
      setOtherUser(data);
    };

    const getFollowStatus = async () => {
      try {
        try {
          const response = await axios.get(
            `${user.url}/followers/${encodeURIComponent(
              encodeURIComponent(curUser?.id)
            )}`
          );

          if (response.status === 200) {
            // further check if they are friends
            // sent a request to "my_id" to check for followers of "id
            try {
              const response2 = await axios.get(
                `${curUser?.url}/followers/${encodeURIComponent(
                  encodeURIComponent(user.url!)
                )}`
              );
              if (response2.status === 200) {
                setStatus("friends");
              } else {
                setStatus("followed");
              }
            } catch (error) {
              // empty
            }
          } else {
            setStatus("stranger");
          }
        } catch (error: any) {
          if (error.response.data.status === "pending") {
            setStatus("pending");
          } else setStatus("stranger");
        }
      } catch (error: any) {
        if (error.response.data.status === "pending") {
          setStatus("pending");
        } else setStatus("stranger");
      }
    };
    if (curUser && curUser.url !== user.url) getOtherUser();
    if (curUser && curUser.url !== user.url) getFollowStatus();
  }, [curUser, user, refresh]);

  /**
   * Extracts the new value input by the user and updates the corresponding state.
   * @param value The new value input by the user
   * @param field The field of that new value (username, GitHub, or image URL)
   */
  const extractValue = (value: string, field: string) => {
    switch (field) {
      case "displayName":
        setDisplayName(value);
        break;
      case "github":
        setGithub(value);
        break;
      case "image":
        setImageURL(value);
        break;
    }
  };

  /**
   * Checks if the given URL is a valid GitHub profile URL.
   * @param {string} githubURL - The URL of the GitHub profile to check.
   */
  async function checkGitHubProfile(githubURL: string) {
    const match = githubURL.match(/^https:\/\/github\.com\/([^/]+)\/?$/);
    const tryUsername = match ? match[1] : null;
    const apiURL = `https://api.github.com/users/${tryUsername}`;

    try {
      await axios(apiURL);
    } catch (error) {
      throw new Error("GitHub profile does not exist");
    }
  }

  /**
   * Saves the new profile information to the database.
   */
  const saveEdits = async () => {
    checkGitHubProfile(newGithub)
      .then(() => {
        const data = {
          displayName: newDisplayName,
          github: newGithub,
          profileImage: newImageURL,
        };
        return axios.put(`${user.url}`, data);
      })
      .then((response) => {
        setUser(response.data);
        if (curUser?.url === user.url) {
          setCurUser(response.data);
        }
        closeModal();
        setRefresh(!refresh);
      })
      .catch((error) => {
        toast.error(error.message, myToast);
      });
  };

  /**
   * Sends a follow request to the user.
   */
  const handleFollowRequest = async () => {
    try {
      const response = await axios.post(`${otherUser?.url}/inbox`, {
        type: "follow",
        summary: `${curUser?.displayName} wants to follow ${otherUser?.displayName}`,
        actor: curUser,
        object: otherUser,
      });
      if (response.status === 201) {
        setStatus("pending");
        setRefresh(!refresh);
      }
    } catch (error) {
      toast.error("Failed to send follow request", myToast);
    }
  };

  /**
   * Unfollow a user
   */
  const handleUnffollowRequest = async () => {
    try {
      const response = await axios.delete(
        `${user.url}/followers/${curUser?.url}`
      );
      if (response.data.success === true) {
        setStatus("stranger");
      }
      setRefresh(!refresh);
    } catch (error) {
      toast.error("Failed to unfollow", myToast);
    }
  };
  //#endregion

  if (Object.entries(curUser).length === 0) return <></>;

  return (
    <div className="flex flex-col items-center justify-first-line:center gap-y-4">
      <ToastContainer />
      {/* Profile picture */}
      <div className="relative">
        <div className="w-48 h-48 rounded-full md:w-60 md:h-60 bg-accent-3">
          <img
            className="object-cover w-full h-full rounded-full"
            src={user.profileImage || defaultPic}
          />
        </div>

        {/* Edit button */}
        {curUser?.url === user.url ? (
          <Button
            buttonType="icon"
            icon={editIcon}
            className="absolute top-0 right-0 w-12 h-12 p-2 rounded-full"
            onClick={() => setOpen(true)}
          ></Button>
        ) : null}

        {/* Follow button */}
        {curUser?.url !== user.url && status === "stranger" ? (
          <Button
            buttonType="icon"
            icon={<GoPlusCircle className="w-8 h-8" />}
            className="absolute top-0 right-0 p-2 font-semibold rounded-full"
            onClick={handleFollowRequest}
          ></Button>
        ) : null}

        {/* Pending */}
        {curUser?.url !== user.url && status === "pending" ? (
          <Button
            buttonType="icon"
            icon={<GoClock className="w-8 h-8" />}
            className="absolute top-0 right-0 p-2 font-semibold rounded-full cursor-default"
          ></Button>
        ) : null}

        {/* Unfollow button */}
        {curUser?.url !== user.url &&
        status !== "stranger" &&
        status !== "pending" ? (
          <Button
            buttonType="icon"
            icon={<GoCheckCircle className="w-8 h-8" />}
            className="absolute top-0 right-0 p-2 font-semibold rounded-full"
            onClick={handleUnffollowRequest}
          ></Button>
        ) : null}

        {/* Edit popup screen */}
        <Popup
          overlayStyle={{ background: "rgba(0, 0, 0, 0.5)" }}
          open={open}
          modal
          lockScroll={true}
          onClose={() => {
            setOpen(false);
            setDisplayName(user.displayName);
            setGithub(user.github || "");
            setImageURL(user.profileImage || "");
          }}
        >
          <div className="flex flex-col py-4 px-6 bg-white rounded-xl gap-y-8 w-[20rem] sm:w-[30rem] md:w-[40rem]">
            <p className="text-2xl font-semibold text-center text-primary">
              Edit Profile
            </p>
            {editFields.map((field, index) => (
              <div
                key={index}
                className="flex flex-col gap-y-3"
              >
                <label
                  className="font-semibold text-secondary-dark"
                  htmlFor={field.value}
                >
                  {field.label}
                </label>
                <input
                  type="text"
                  name={field.value}
                  maxLength={field.value === "display_name" ? 30 : 200}
                  id={field.value}
                  defaultValue={field.placeholder}
                  className="flex-grow px-4 py-4 bg-accent-3 rounded-xl"
                  onChange={(e) => extractValue(e.target.value, field.value)}
                />
              </div>
            ))}
            <Button
              buttonType="text"
              className="flex items-center justify-center h-12 px-12 m-auto"
              onClick={() => {
                saveEdits();
              }}
            >
              Save
            </Button>
          </div>
        </Popup>
      </div>
      {/* Display profile info */}
      <div className="flex flex-col items-center">
        <div className="flex items-center justify-center gap-x-4">
          <p className="text-xl font-semibold md:text-2xl opacity-95">
            {user.displayName}
          </p>
          {status?.toLowerCase() === "friends" && (
            <GoCodeOfConduct className="w-6 h-6 text-primary" />
          )}
        </div>
        {user.github && (
          <a
            className="text-sm md:text-base text-secondary-dark"
            href={user.github}
          >
            {user.github}
          </a>
        )}
      </div>
    </div>
  );
};
export { Profile };
