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
      (notificationObject.type &&
      notificationObject.type.toLowerCase() === "like" &&
      notificationObject.object.includes("comments")
        ? "comment"
        : "post"),
    comment: "commented on your post",
  };

  //#region functions
  const handleAccept = async () => {
    const data = {
      actor: curUser,
      object: notificationObject.actor,
      type: "FollowResponse",
      summary: `${notificationObject.actor.displayName} accepted ${curUser.displayName}'s follow request`,
      accepted: true,
    };

    try {
      const response = await axios.put(
        `${curUser.id}/followers/${encodeURIComponent(
          notificationObject.actor.id
        )}`,
        data
      );

      if (response.status === 200) {
        setRefresh(!refresh);
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };

  const handleDecline = async () => {
    const data = {
      actor: curUser,
      object: notificationObject.actor,
      type: "FollowResponse",
      summary: `${notificationObject.actor.displayName} declined ${curUser.displayName}'s follow request`,
      accepted: false,
    };

    try {
      const response = await axios.post(
        `/api/authors/${curUser.id.split("/").pop()}/decline`,
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

  if (!notificationObject.type) return <></>;

  return (
    <div className="flex flex-col justify-between flex-grow p-4 md:items-center md:flex-row rounded-2xl bg-accent-3 gap-y-6">
      {/* Notification info */}
      <div className="flex items-center gap-x-4">
        <img
          className="rounded-full w-14 h-14"
          src={
            (notificationObject.author
              ? notificationObject.author
              : notificationObject.actor
            ).profileImage || defaultImg
          }
          onError={(event) => (event.currentTarget.src = defaultImg)}
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
      </div>

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
