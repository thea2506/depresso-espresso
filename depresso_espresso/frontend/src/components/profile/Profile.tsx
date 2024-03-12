//#region Imports
import { Button } from "../Button";
import Popup from "reactjs-popup";
import { ToastContainer, toast, ToastOptions } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useEffect, useState } from "react";
import axios from "axios";
import editIcon from "../../assets/icons/edit.svg";
import defaultPic from "../../assets/images/default_profile.jpg";
import { AuthorModel } from "../data/AuthorModel";
//#endregion

//#region interfaces
interface ProfileProps {
  id: string | undefined;
  display_name: string;
  github?: string;
  imageURL?: string;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}
//#endregion

/**
 * Renders a profile component with the given username, GitHub link, and avatar URL.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {string} props.display_name - The username to display.
 * @param {string} props.github - The GitHub link to display.
 * @param {string} props.imageURL - The URL of the avatar image to display.
 * @oaram {boolean} props.loading - The loading state.
 * @param {Function} props.setLoading - The function to set the loading state.
 * @returns {JSX.Element} The rendered profile component.
 */
const Profile = ({
  id,
  display_name,
  github,
  imageURL,
  loading,
  setLoading,
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
    { label: "Display Name", value: "display_name", placeholder: display_name },
    { label: "GitHub URL", value: "github", placeholder: github },
    { label: "Image URL", value: "image", placeholder: imageURL },
  ];

  const [newDisplayName, setDisplayName] = useState<string>(display_name);
  const [newGithub, setGithub] = useState<string>(github || "");
  const [newImageURL, setImageURL] = useState<string>(imageURL || "");
  const [curUser, setCurUser] = useState<AuthorModel>();

  const [open, setOpen] = useState<boolean>(false);
  const closeModal = () => setOpen(false);
  //#endregion

  //#region Functions
  useEffect(() => {
    const getCurrentUser = async () => {
      try {
        const response = await axios.get("/curUser");
        if (response.data.success == true) setCurUser(response.data);
      } catch (error) {
        console.error("Failed to fetch current user in ProfilePage", error);
      }
    };
    getCurrentUser();
  }, []);

  /**
   * Extracts the new value input by the user and updates the corresponding state.
   * @param value The new value input by the user
   * @param field The field of that new value (username, GitHub, or image URL)
   */
  const extractValue = (value: string, field: string) => {
    switch (field) {
      case "display_name":
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
        toast.success("Profile updated successfully", myToast);
        closeModal();
      })
      .catch((error) => {
        toast.error(error.message, myToast);
      });

    const formField = new FormData();
    if (newDisplayName !== "") formField.append("displayName", newDisplayName);
    formField.append("github", newGithub);
    formField.append("profileImage", newImageURL);
    await axios.post(`${id}/edit_profile`, formField);
    setLoading(!loading);
  };
  //#endregion

  return (
    <div className="flex flex-col items-center justify-first-line:center gap-y-4">
      <ToastContainer />
      {/* Profile picture */}
      <div className="relative">
        <div className="w-48 h-48 rounded-full md:w-60 md:h-60 bg-accent-3">
          <img
            className="object-cover w-full h-full rounded-full"
            src={imageURL || defaultPic}
          />
        </div>

        {/* Edit button */}
        {curUser?.id === id ? (
          <Button
            buttonType="icon"
            icon={editIcon}
            className="absolute top-0 right-0 w-12 h-12 p-2 rounded-full"
            onClick={() => setOpen(true)}
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
            setDisplayName(display_name);
            setGithub(github || "");
            setImageURL(imageURL || "");
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
        <p className="text-xl font-semibold md:text-2xl opacity-95">
          {display_name}
        </p>
        {github && (
          <a
            className="text-sm md:text-base text-secondary-dark"
            href={github}
          >
            {github}
          </a>
        )}
      </div>
    </div>
  );
};

export { Profile };
