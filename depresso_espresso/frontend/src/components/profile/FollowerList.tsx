import { UserDisplay } from "../UserDisplay";
import { AuthorModel } from "../data/AuthorModel";
import { useNavigate } from "react-router-dom";

interface FollowerListProps {
  followers: AuthorModel[];
}

const FollowerList = ({ followers }: FollowerListProps) => {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col items-center justify-center w-full gap-y-4">
      {followers &&
        followers?.map((follower: AuthorModel) => (
          <div
            className="focus:outline-none w-full px-4 py-6 bg-accent-3 rounded-[1.4rem] hover:bg-secondary-light hover:bg-opacity-40 transition ease-in-out duration-150 cursor-pointer flex"
            onClick={() => {
              navigate(`${follower.url}`, { state: { reload: true } }); // Client-side navigation to the author's profile
            }}
          >
            <UserDisplay
              displayName={follower.displayName}
              user_img_url={follower.profileImage}
              link={`/site/authors/${follower.url}`}
              className="text-lg font-semibold text-secondary-dark hover:text-white"
            />
          </div>
        ))}
    </div>
  );
};

export default FollowerList;
