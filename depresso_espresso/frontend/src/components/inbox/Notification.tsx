import defaultImg from "../../assets/images/default_profile.jpg";
import { Button } from "../Button";

interface NotificationProps {
  username: string;
  type: "follow" | "share";
}

const Notification = ({ username, type }: NotificationProps) => {
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

      {/* Buttons */}
      <div className="flex items-center gap-x-4">
        <Button
          buttonType="text"
          className="flex items-center justify-center grow md:grow-0"
        >
          Accept
        </Button>
        <Button
          buttonType="text"
          className="flex items-center justify-center bg-accent-2 hover:bg-accent-2 hover:opacity-80 grow md:grow-0"
        >
          Decline
        </Button>
      </div>
    </div>
  );
};

export { Notification };
