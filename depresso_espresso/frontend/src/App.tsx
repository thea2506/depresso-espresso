import "./App.css";
import React, { useState, createContext, Dispatch, useEffect } from "react";
import axios from "axios";

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

  useEffect(() => {
    const getId = async () => {
      try {
        const response = await axios.get("/curUser");
        setId0(response.data.id);
      } catch (error) {
        console.error("An error occurred", error);
      }
    };
    getId();
  }, [id0]);

  return (
    <AuthContext.Provider value={{ id0 }}>
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
