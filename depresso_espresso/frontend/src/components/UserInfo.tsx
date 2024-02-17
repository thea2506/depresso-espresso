import { twMerge } from "tailwind-merge";

interface UserInfoProps {
  className?: string;
  username: string;
  avatarURL: string;
  time: string;
}

const UserInfo = ({ username, avatarURL, time, className }: UserInfoProps) => {
  const date = new Date(time);
  const formattedDate = date.toLocaleString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
  return (
    <div
      className={twMerge(
        "flex items-center w-full gap-x-4 bg-accent",
        className
      )}
    >
      <img
        src={avatarURL}
        alt="Profile Github"
        className="object-cover w-12 h-12 rounded-full md:w-13 md:h-13 lg:w-14 lg:h-14"
      />
      <div className="flex flex-col items-start flex-grow md:justify-between md:flex-row">
        <p className="text-primary">{username}</p>
        <div className="flex items-center md:justify-center gap-x-1 opacity-90">
          <img
            src="src/assets/icons/public.svg"
            alt="Public Icon"
          />
          <p className="text-sm">{formattedDate}</p>
        </div>
      </div>
    </div>
  );
};

export { UserInfo };
