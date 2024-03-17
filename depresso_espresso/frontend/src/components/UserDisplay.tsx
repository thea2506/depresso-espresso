import defaultProfileImage from "../assets/images/default_profile.jpg";

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
    <a
      className={`flex items-center justify-center gap-x-4 ${className}`}
      href={link}
    >
      <img
        className="object-cover w-12 h-12 rounded-full md:w-13 md:h-13 lg:w-14 lg:h-14"
        src={
          user_img_url && user_img_url != ""
            ? user_img_url
            : defaultProfileImage
        }
        alt="Profile picture"
      />
      <p className="text-primary">{displayName}</p>
    </a>
  );
};

export { UserDisplay };
