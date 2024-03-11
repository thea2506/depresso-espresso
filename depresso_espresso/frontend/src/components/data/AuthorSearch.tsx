import axios from "axios";
import React, { FC, useState, useEffect } from "react";
import { AuthorModel } from "./AuthorModel";
import { UserDisplay } from "../UserDisplay";

interface AuthorSearchProps {}

const AuthorSearch: FC<AuthorSearchProps> = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [authors, setAuthors] = useState<AuthorModel[]>([]);

  useEffect(() => {
    const fetchAuthors = async () => {
      try {
        const response = await axios.get(`/authors?search=${searchTerm}`);

        const authorModels = response.data?.map(
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          (rawauthor: any) => {
            return {
              type: rawauthor.type,
              id: rawauthor.id,
              url: rawauthor.url,
              host: rawauthor.host,
              displayName: rawauthor.displayName,
              github: rawauthor.github,
              profileImage: rawauthor.profileImage,
            };
          }
        );
        console.log("authorModels", authorModels);
        setAuthors(authorModels);
        console.log("authors", authors);
      } catch (error) {
        console.error(error);
      }
    };

    const debounceTimer = setTimeout(() => {
      console.log("Searching for:", searchTerm);
      fetchAuthors();
    }, 500);

    return () => {
      clearTimeout(debounceTimer);
    };
  }, [searchTerm]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  return (
    <div className="max-w-[600px] flex flex-col w-full px-4 gap-y-4 sm:px-12 md:px-20 md:items-center md:justify-center">
      <input
        className="resize-none focus:outline-none w-full p-4 bg-secondary rounded-[1.4rem] overflow-none"
        type="text"
        value={searchTerm}
        onChange={handleInputChange}
        placeholder="Search for users"
      />
      <div className="w-full">
        {authors &&
          authors?.map((author) => (
            <div
              className="resize-none focus:outline-none w-full p-4 bg-accent-3 rounded-[1.4rem] overflow-none m-2 hover:bg-primary md:hover:bg-secondary-light hover:text-white"
              onClick={() => window.location.href = `/authors/${author.id}/`}
            >
              <UserDisplay
                username={author.displayName}
                user_img_url={author.profileImage}
                link={author.url}
              />
            </div>
          ))}
      </div>
    </div>
  );
};

export default AuthorSearch;
