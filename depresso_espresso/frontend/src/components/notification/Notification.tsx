//#regioin imports
import defaultImg from "../../assets/images/default_profile.jpg";
import { Button } from "../Button";
import axios from "axios";
//#endregion

//#region interface
interface NotificationProps {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  author: any;
  type: "follow" | "share" | "post" | "like" | "comment";
}
//#endregion

/**
 * Represents a notification component.
 * @component
 *
 * @param {Object} props - The component props.
 * @param {string} props.username - The username associated with the notification.
 * @param {"follow" | "share"} props.type - The type of notification.
 * @param {string} props.link - The link to the user's profile or the shared post.
 *
 * @returns {JSX.Element} The rendered notification component.
 */
const Notification = ({ author, type }: NotificationProps) => {
  const messages = {
    follow: "wants to follow you",
    share: "shared a post with you",
    post: "made a post",
    like: "liked your post",
    comment: "commented on your post",
  };

  //#region functions
  const handleAccept = async () => {
    console.log("Accept clicked");

    const formField = new FormData();
    formField.append("username", author.username);
    formField.append("decision", "accept");
    try {
      const response = await axios.post(
        "/respond_to_follow_request",
        formField
      );
      if (response.data.success) {
        console.log(response.data.message);
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };

  const handleDecline = async () => {
    console.log("Decline clicked");

    const formField = new FormData();
    formField.append("username", author.username);
    formField.append("decision", "decline");
    try {
      const response = await axios.post(
        "/respond_to_follow_request",
        formField
      );
      if (response.data.success) {
        console.log(response.data.message);
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };
  //#endregion

  return (
    <div className="flex flex-col justify-between flex-grow p-4 md:items-center md:flex-row rounded-2xl bg-accent-3 gap-y-6">
      {/* Notification info */}
      <div className="flex items-center gap-x-4">
        <img
          className="rounded-full w-14 h-14"
          src={author.profileImage || defaultImg}
          alt="Profile Picture"
        />
        <div>
          <span className="font-semibold text-secondary-dark">
            {author.username}{" "}
          </span>
          {messages[type]}
        </div>
      </div>

      {/* Buttons - Follow only */}
      {type === "follow" && (
        <div className="flex items-center gap-x-4">
          <Button
            buttonType="text"
            className="flex items-center justify-center grow md:grow-0"
            onClick={handleAccept}
          >
            Accept
          </Button>
          <Button
            buttonType="text"
            className="flex items-center justify-center bg-accent-2 hover:bg-accent-2 hover:opacity-80 grow md:grow-0"
            onClick={handleDecline}
          >
            Decline
          </Button>
        </div>
      )}
    </div>
  );
};

export { Notification };
