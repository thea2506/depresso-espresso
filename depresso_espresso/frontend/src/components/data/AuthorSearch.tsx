//#region imports
import axios from "axios";
import React, { useState, useEffect } from "react";
import { AuthorModel } from "./AuthorModel";
import { UserDisplay } from "../UserDisplay";
import { useNavigate } from "react-router-dom";
//#endregion

const AuthorSearch = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [authors, setAuthors] = useState<AuthorModel[]>([]);
  const nav = useNavigate();

  useEffect(() => {
    const fetchAuthors = async () => {
      try {
        const response = await axios.get(`/authors?search=${searchTerm}`);

        const authorModels = response.data?.map(
          
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          (rawauthor: any) => {
            return {
              type: rawauthor.fields.type,
              id: rawauthor.pk,
              url: rawauthor.fields.url,
              host: rawauthor.fields.host,
              displayName: rawauthor.fields.displayName,
              username: rawauthor.fields.username,
              github: rawauthor.fields.github,
              profileImage: rawauthor.fields.profileImage,
            };
          }
        );
        setAuthors(authorModels);
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
    <div className="flex flex-col items-center justify-center w-full gap-y-6 px-[4%] md:px-[8%]">
      <input
        className="focus:outline-none w-full p-4 bg-secondary rounded-[1.4rem]"
        type="text"
        value={searchTerm}
        onChange={handleInputChange}
        placeholder="Search for users"
      />
      <div className="flex flex-col w-full gap-y-4">
        {authors &&
          authors?.map(
            (author) =>
              author.displayName &&
              author.displayName != "" && (
                <div
                  className="focus:outline-none w-full px-4 py-6 bg-accent-3 rounded-[1.4rem] hover:bg-secondary-light hover:bg-opacity-40 transition ease-in-out duration-150 cursor-pointer flex"
                  onClick={() => nav(`/authors/${author.id}`)}
                >
                  <UserDisplay
                    displayName={author.displayName}
                    user_img_url={author.profileImage}
                    link={`/authors/${author.id}`}
                    className="text-lg font-semibold text-secondary-dark hover:text-white"
                  />
                </div>
              )
          )}
      </div>
    </div>
  );
};

export default AuthorSearch;
