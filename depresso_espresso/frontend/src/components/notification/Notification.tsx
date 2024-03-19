/* eslint-disable @typescript-eslint/no-explicit-any */
//#regioin imports
import defaultImg from "../../assets/images/default_profile.jpg";
import { Button } from "../Button";
import axios from "axios";
import { GoSearch } from "react-icons/go";
import { useNavigate } from "react-router";
//#endregion

//#region interface
interface NotificationProps {
  author: any;
  authorid: string;
  authorpostid?: string;
  summary: string;
  type: "follow" | "share" | "post" | "like" | "comment";
  postid?: string;
  createdAt?: string;
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
 * @param {"follow" | "share"} props.type - The type of notification.
 * @param {string} props.link - The link to the user's profile or the shared post.
 * @param {string} props.createdAt - The date and time the notification was created.
 * @param {boolean} props.refresh - The state of the notification.
 * @param {React.Dispatch<React.SetStateAction<boolean>>} props.setRefresh - The function to set the state of the notification.
 *
 * @returns {JSX.Element} The rendered notification component.
 */
const Notification = ({
  author,
  authorid,
  authorpostid,
  type,
  summary,
  postid,
  createdAt,
  refresh,
  setRefresh,
}: NotificationProps): JSX.Element => {
  const formatDateString = (inputDateString: string) => {
    const date = new Date(inputDateString);
    const formattedDate = date.toLocaleString("en-US", {
      hour: "numeric",
      minute: "numeric",
      month: "short",
      day: "numeric",
      year: "numeric",
    });
    return formattedDate;
  };
  const navigate = useNavigate();

  //#region functions
  const handleAccept = async () => {
    const formField = new FormData();
    formField.append("id", authorid);
    formField.append("decision", "accept");

    const data = { id: authorid, decision: "accept" };

    try {
      const response = await axios.put(
        `/authors/respond_to_follow_request/from/${authorid}`,
        data
      );
      if (response.data.success) {
        setRefresh(!refresh);
        console.log(response.data.message);
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };

  const handleDecline = async () => {
    const formField = new FormData();
    formField.append("id", authorid);
    formField.append("decision", "decline");

    const data = { id: authorid, decision: "decline" };

    try {
      const response = await axios.put(
        "/respond_to_follow_request/from/" + authorid,
        data
      );
      if (response.data.success) {
        setRefresh(!refresh);
        console.log(response.data.message);
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };

  const handleSeeMore = async () => {
    navigate(`/authors/${authorpostid}/posts/${postid}`);
  };
  //#endregion

  return (
    <div className="flex flex-col justify-between flex-grow p-4 md:items-center md:flex-row rounded-2xl bg-accent-3 gap-y-6">
      {/* Notification info */}
      <a
        className="flex items-center gap-x-4"
        href={author.url}
      >
        <img
          className="rounded-full w-14 h-14"
          src={author.profileImage || defaultImg}
          alt="Profile Picture"
        />
        <div>
          <span className="font-semibold text-secondary-dark">
            {author.displayName}
          </span>
          {summary.replace(author.displayName, "")}
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
        <div className="flex items-center justify-center gap-x-4">
          <div className="text-sm opacity-95">
            {formatDateString(createdAt!)}
          </div>
          <Button
            buttonType="icon"
            icon={<GoSearch />}
            className="flex items-center justify-center"
            onClick={handleSeeMore}
          />
        </div>
      )}
    </div>
  );
};

export { Notification };
