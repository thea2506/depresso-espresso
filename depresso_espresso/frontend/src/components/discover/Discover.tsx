/* eslint-disable @typescript-eslint/no-explicit-any */

//#region imports
import { useContext, useEffect, useState } from "react";
import axios from "axios";
import { AuthorModel } from "../data/AuthorModel";
import { useNavigate } from "react-router";
import AuthContext from "../../contexts/AuthContext";

function checkSameOrigin(url: string) {
  let windowOrigin = window.location.origin;
  if (windowOrigin.includes("localhost")) {
    if (url.includes(windowOrigin)) return true;
    windowOrigin = windowOrigin.replace("localhost", "127.0.0.1");
    if (url.includes(windowOrigin)) return true;
  }

  if (windowOrigin.includes("127.0.0.1")) {
    if (url.includes(windowOrigin)) return true;
    windowOrigin = windowOrigin.replace("127.0.0.1", "localhost");
    if (url.includes(windowOrigin)) return true;
  }

  return false;
}

const Discover = () => {
  const [allAuthors, setAllAuthors] = useState<AuthorModel[]>([]);
  const { curUser } = useContext(AuthContext);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchAuthors() {
      const response = await axios.get("/api/discover/");
      if (response.status === 200) {
        setAllAuthors(response.data.items);
        setLoading(false);
      }
    }
    fetchAuthors();
  }, []);

  //#endregion

  if (!Object.entries(curUser).length) return <></>;

  return (
    <div className="flex flex-col items-center justify-center w-full">
      <div className="flex flex-col w-4/5 gap-4">
        {loading ? (
          <>Loading</>
        ) : (
          allAuthors.map((author, key: number) => {
            if (author.url === curUser?.url) return null;
            return (
              <div
                key={key}
                className="flex items-center justify-start w-full gap-4 p-4 rounded-xl bg-accent-3"
                onClick={() => {
                  navigate(`../authors/${author.url}`, {
                    state: { reload: true },
                  });
                }}
              >
                <h2 className="text-lg font-semibold text-primary">
                  {author.displayName}
                </h2>
                <span className="px-4 py-2 text-white rounded-xl bg-secondary-dark">
                  {checkSameOrigin(author.url) ? "Local" : "Remote"}
                </span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default Discover;
