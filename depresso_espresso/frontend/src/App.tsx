import "./App.css";

// import App from "./App";
import Signin from "./components/auth/Signin.tsx";
import Signup from "./components/auth/Signup.tsx";
import ProfilePage from "./components/profile/ProfilePage.tsx";
import Home from "./components/home/Home.tsx";
import { NavBar } from "./components/NavBar.tsx";
import AuthCheck from "./components/auth/Authcheck.tsx";
import React, { useState, useEffect } from "react";
import axios from "axios";

import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {
  const General = ({
    authorId,
    children,
  }: {
    authorId: string;
    children: React.ReactNode;
  }) => (
    <div className="w-full">
      <NavBar authorId={authorId} />
      {children}
    </div>
  );

  /**
   * Retrieves the authorid from the backend
   */
  const [authorid, setAuthorID] = useState<string>(
    localStorage.getItem("authorid") !== null
      ? (localStorage.getItem("authorid") as string)
      : ""
  );
  useEffect(() => {
    const retrieveAuthorID = async () => {
      try {
        const response = await axios.get("/user_data");
        setAuthorID(response.data.authorid);
        localStorage.setItem("authorid", response.data.authorid);
        console.log(response.data.authorid);
      } catch (error) {
        console.error(error);
      }
    };

    retrieveAuthorID();
  }, []);

  const authorIDPath = `/authors/${authorid}`;

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
              <General authorId={authorid}>
                <Home />
              </General>
            </AuthCheck>
          }
        />
        <Route
          path={authorIDPath} // This is a dynamic route + project requirements
          element={
            <General authorId={authorid}>
              <ProfilePage />
            </General>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
