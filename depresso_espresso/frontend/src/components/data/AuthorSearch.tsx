import axios from "axios";
import React, { FC, useState, useEffect } from "react";
import { AuthorModel } from "./AuthorModel";

interface AuthorSearchProps {}

const AuthorSearch: FC<AuthorSearchProps> = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [authors, setAuthors] = useState<AuthorModel[]>([]);
  // const [authors_filtered, setAuthorsFiltered] = useState<AuthorModel[]>([]);

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
              profileImage: rawauthor.profileImage
            };
          }
        );
        console.log('authorModels', authorModels)
        setAuthors(authorModels);
        console.log('authors', authors )
      } catch (error) {
        console.error(error);
      }
    }

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
    <div>
      <input
        className="resize-none focus:outline-none w-full p-4 bg-secondary rounded-[1.4rem] overflow-none"
        type="text"
        value={searchTerm}
        onChange={handleInputChange}
        placeholder="Search for users"
      />
      <div>
        


        {authors && authors?.map((author) => (
          <div>{author.displayName}</div>
        ))}

      </div>
    </div>
  );
};

export default AuthorSearch;