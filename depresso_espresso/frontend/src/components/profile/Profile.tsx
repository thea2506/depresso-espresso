import { Button } from "../Button";

interface ProfileProps {
  username: string;
  github?: string;
  avatarURL?: string;
}

const Profile = ({ username, github, avatarURL }: ProfileProps) => {
  return (
    <div className="flex flex-col items-center justify-first-line:center gap-y-4">
      <div className="relative">
        <div className="w-48 h-48 rounded-full md:w-60 md:h-60 bg-accent-3">
          <img
            className="object-cover w-full h-full rounded-full"
            src={avatarURL}
            alt="Profile Picture"
          />
        </div>
        <Button
          className="absolute right-0 top-2"
          buttonType="icon"
          icon="src/assets/icons/edit.svg"
        ></Button>
      </div>

      <div className="flex flex-col">
        <p className="text-xl font-semibold md:text-2xl opacity-95">
          {username}
        </p>
        {github && (
          <a
            className="text-sm md:text-base text-secondary-dark"
            href={github}
          >
            {github}
          </a>
        )}
      </div>
    </div>
  );
};

export { Profile };
