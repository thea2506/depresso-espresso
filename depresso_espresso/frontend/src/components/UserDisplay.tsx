import defaultProfileImage from "../assets/images/default_profile.jpg";

interface UserDisplayProps {
  username: string;
  user_img_url: string | undefined;
}

const UserDisplay = ({ username, user_img_url }: UserDisplayProps) => {
  return (
    <div className="flex items-center justify-center gap-x-4">
      <img
        className="object-cover w-12 h-12 rounded-full md:w-13 md:h-13 lg:w-14 lg:h-14"
        src={user_img_url != null ? user_img_url : defaultProfileImage}
        alt="Profile picture"
      />
      <p className="text-primary">{username}</p>
    </div>
  );
};

export { UserDisplay };
