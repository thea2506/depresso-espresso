import defaultProfileImage from "../assets/images/default_profile.jpg";
import { Link } from "react-router-dom";

interface UserDisplayProps {
  displayName: string;
  user_img_url: string | undefined;
  link: string;
  className?: string;
}

const UserDisplay = ({
  displayName,
  user_img_url,
  link,
  className,
}: UserDisplayProps) => {
  return (
    <Link
      className={`flex items-center justify-center gap-x-4 ${className}`}
      to={link}
      reloadDocument
      state={{ reload: true }}
    >
      <img
        className="object-cover w-12 h-12 rounded-full md:w-13 md:h-13 lg:w-14 lg:h-14"
        src={
          user_img_url && user_img_url != ""
            ? user_img_url
            : defaultProfileImage
        }
        onError={(event) => (event.currentTarget.src = defaultProfileImage)}
        alt="Profile picture"
      />
      <p className="text-primary">{displayName}</p>
    </Link>
  );
};

export { UserDisplay };
