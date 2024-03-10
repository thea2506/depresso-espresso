import "./App.css";
import React, { useState, createContext, Dispatch } from "react";

import Signin from "./components/auth/Signin.tsx";
import Signup from "./components/auth/Signup.tsx";
import ProfilePage from "./components/profile/ProfilePage.tsx";
import Home from "./components/home/Home.tsx";
import InboxPage from "./components/inbox/InboxPage.tsx";
import Discover from "./components/discover/Discover.tsx";
import { NavBar } from "./components/NavBar.tsx";

import { BrowserRouter, Route, Routes } from "react-router-dom";

interface UserInfo {
  id0: string;
  host0: string;
  displayName0: string;
  url0: string;
  github0: string | undefined | null;
  profileImage0: string | undefined | null;
  setId0: Dispatch<React.SetStateAction<string>>;
  setHost0: Dispatch<React.SetStateAction<string>>;
  setDisplayName0: Dispatch<React.SetStateAction<string>>;
  setUrl0: Dispatch<React.SetStateAction<string>>;
  setGithub0: Dispatch<React.SetStateAction<string>>;
  setProfileImage0: Dispatch<React.SetStateAction<string>>;
}

export const AuthContext = createContext({} as UserInfo);

const General = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="w-full mb-20">
      <NavBar />
      {children}
    </div>
  );
};

function App() {
  /**
   * Retrieves the id from the backend
   */
  const [id0, setId0] = useState<string>("");
  const [host0, setHost0] = useState<string>("");
  const [displayName0, setDisplayName0] = useState<string>("");
  const [url0, setUrl0] = useState<string>("");
  const [github0, setGithub0] = useState<string>("");
  const [profileImage0, setProfileImage0] = useState<string>("");

  return (
    <AuthContext.Provider
      value={{
        id0,
        host0,
        displayName0,
        url0,
        github0,
        profileImage0,
        setId0,
        setHost0,
        setDisplayName0,
        setUrl0,
        setGithub0,
        setProfileImage0,
      }}
    >
      <BrowserRouter>
        <Routes>
          <Route
            path="/signup"
            element={<Signup />}
          />
          <Route
            path="/signin"
            element={<Signin />}
          />
          <Route
            path="/"
            element={
              <General>
                <Home />
              </General>
            }
          />
          <Route
            path="/authors/:authorId"
            element={
              <General>
                <ProfilePage />
              </General>
            }
          />
          <Route
            path="/inbox"
            element={
              <General>
                <InboxPage />
              </General>
            }
          />
          <Route
            path="/discover"
            element={
              <General>
                <Discover />
              </General>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthContext.Provider>
  );
}

export default App;
