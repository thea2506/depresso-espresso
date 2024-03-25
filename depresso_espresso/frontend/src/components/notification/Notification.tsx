/* eslint-disable @typescript-eslint/no-explicit-any */
//#regioin imports
import defaultImg from "../../assets/images/default_profile.jpg";
import { Button } from "../Button";
import axios from "axios";
//#endregion

//#region interface
interface NotificationProps {
  curUser: any;
  type: "follow" | "share" | "post" | "like" | "comment";
  notificationObject: any;
  refresh?: boolean;
  setRefresh: React.Dispatch<React.SetStateAction<boolean>>;
}
//#endregion

/**
 * Represents a notification component.
 * @component
 *
 * @param {Object} props - The component props.
 * @param {string} props.id - The username associated with the notification.
 * @param {"follow" | "share" | "post" | "like" | "comment"} props.type - The type of notification.
 * @param {string} props.link - The link to the user's profile or the shared post.
 * @param {string} props.createdAt - The date and time the notification was created.
 * @param {boolean} props.refresh - The state of the notification.
 * @param {React.Dispatch<React.SetStateAction<boolean>>} props.setRefresh - The function to set the state of the notification.
 *
 * @returns {JSX.Element} The rendered notification component.
 */
const Notification = ({
  curUser,
  notificationObject,
  type,
  refresh,
  setRefresh,
}: NotificationProps): JSX.Element => {
  const messages = {
    follow: "wants to follow you",
    share: "shared a post with you",
    post: "made a post",
    like:
      "liked your " +
      (notificationObject.type.toLowerCase() === "like" &&
      notificationObject.object.includes("comments")
        ? "comment"
        : "post"),
    comment: "commented on your post",
  };

  //#region functions
  const handleAccept = async () => {
    const data = {
      actor: notificationObject.actor,
      object: curUser,
      type: "Follow",
      summary: `${notificationObject.actor.displayName} wants to follow ${curUser.displayName}`,
      decision: "accept",
    };

    try {
      const response = await axios.put(
        `${curUser.url}/followers/${encodeURIComponent(
          encodeURIComponent(notificationObject.actor.id)
        )}`,
        data
      );
      if (response.data.success) {
        setRefresh(!refresh);
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };

  const handleDecline = async () => {
    const data = {
      actor: notificationObject.actor,
      object: curUser,
      type: "Follow",
      summary: `${notificationObject.actor.displayName} wants to follow ${curUser.displayName}`,
      decision: "decline",
    };

    try {
      const response = await axios.put(
        `${curUser.url}/followers/${encodeURIComponent(
          encodeURIComponent(notificationObject.actor.id)
        )}`,
        data
      );
      if (response.data.success) {
        setRefresh(!refresh);
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };
  //#endregion
  return (
    <div className="flex flex-col justify-between flex-grow p-4 md:items-center md:flex-row rounded-2xl bg-accent-3 gap-y-6">
      {/* Notification info */}
      <a
        className="flex items-center gap-x-4"
        href={
          notificationObject.author
            ? notificationObject.author.url.substring(
                notificationObject.author.url.indexOf("espresso-api") +
                  "espresso-api".length
              )
            : notificationObject.actor.url.substring(
                notificationObject.actor.url.indexOf("espresso-api") +
                  "espresso-api".length
              )
        }
      >
        <img
          className="rounded-full w-14 h-14"
          src={
            (notificationObject.author
              ? notificationObject.author
              : notificationObject.actor
            ).profileImage || defaultImg
          }
          alt="Profile Picture"
        />
        <div>
          <span className="font-semibold text-secondary-dark">
            {
              (notificationObject.author
                ? notificationObject.author
                : notificationObject.actor
              ).displayName
            }{" "}
          </span>
          {messages[type]}
        </div>
      </a>

      {/* Buttons - Follow only */}
      {type === "follow" ? (
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
      ) : (
        <></>
      )}
    </div>
  );
};

export { Notification };
