import "./App.css";

// import App from "./App";
import Signin from "./components/auth/Signin.tsx";
import Signup from "./components/auth/Signup.tsx";
import ProfilePage from "./components/profile/ProfilePage.tsx";
import Home from "./components/home/Home.tsx";
import { NavBar } from "./components/NavBar.tsx";
import AuthCheck from "./components/auth/Authcheck.tsx";
import React, { useState, useEffect, createContext } from "react";
import axios from "axios";

import { BrowserRouter, Route, Routes } from "react-router-dom";

export const AuthContext = createContext({
  authorid: "",
  setAuthorID: (authorid: string) => {
    console.log(authorid);
  },
});

const General = ({
  children,
  authorid,
  setAuthorID,
}: {
  children: React.ReactNode;
  authorid: string;
  setAuthorID: (authorid: string) => void;
}) => {
  return (
    <AuthContext.Provider value={{ authorid, setAuthorID }}>
      <div className="w-full">
        <NavBar />
        {children}
      </div>
    </AuthContext.Provider>
  );
};

function App() {
  /**
   * Retrieves the authorid from the backend
   */
  const [authorid, setAuthorID] = useState<string>("");
  useEffect(() => {
    const retrieveAuthorID = async () => {
      try {
        const response = await axios.get("/user_data");
        setAuthorID(response.data.authorid);
        console.log(response.data.authorid);
      } catch (error) {
        console.error(error);
      }
    };
    retrieveAuthorID();
  }, []);

  return (
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
            <AuthCheck>
              <General
                authorid={authorid}
                setAuthorID={setAuthorID}
              >
                <Home />
              </General>
            </AuthCheck>
          }
        />
        <Route
          path="/authors/:authorId" // This is a dynamic route + project requirements
          element={
            <>
              <General
                authorid={authorid}
                setAuthorID={setAuthorID}
              >
                <ProfilePage />
              </General>
            </>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
