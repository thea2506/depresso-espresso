//#regioin imports
import defaultImg from "../../assets/images/default_profile.jpg";
import { Button } from "../Button";
//#endregion

//#region interface
interface NotificationProps {
  username: string;
  type: "follow" | "share";
  // This should be either a link to the user's profile or the post that was shared
  link: string;
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
const Notification = ({ username, type }: NotificationProps) => {
  //#region functions
  const handleAccept = () => {
    console.log("Accepted");
  };

  const handleDecline = () => {
    console.log("Declined");
  };
  //#endregion

  return (
    <div className="flex flex-col justify-between flex-grow p-4 md:items-center md:flex-row rounded-2xl bg-accent-3 gap-y-6">
      {/* Notification info */}
      <div className="flex items-center gap-x-4">
        <img
          className="rounded-full w-14 h-14"
          src={defaultImg}
          alt="Profile Picture"
        />
        <div>
          <span className="font-semibold text-secondary-dark">{username} </span>
          {type === "follow" ? "wants to follow you" : "shared a post with you"}
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
