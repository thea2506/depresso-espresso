import { UserDisplay } from "../UserDisplay";
import { AuthorModel } from "../data/AuthorModel";

interface FollowerListProps {
  followers: AuthorModel[];
}

const FollowerList = ({ followers }: FollowerListProps) => {
  return (
    <div className="max-w-[600px] flex flex-col w-full px-4 gap-y-4 sm:px-12 md:px-20 md:items-center md:justify-center">
      <div className="w-full">
        {followers &&
          followers?.map((follower: AuthorModel) => (
            <div
              className="resize-none focus:outline-none w-full p-4 bg-accent-3 rounded-[1.4rem] overflow-none m-2 hover:bg-primary md:hover:bg-secondary-light hover:text-white"
              onClick={() => (
                console.log(follower.id),
                (window.location.href = `${follower.id}`)
              )}
            >
              <UserDisplay
                username={follower.username}
                user_img_url={follower.profileImage}
                link={follower.github}
              />
            </div>
          ))}
      </div>
    </div>
  );
};

export default FollowerList;
