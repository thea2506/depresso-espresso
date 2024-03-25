import "./App.css";

import {
  RouterProvider,
  createBrowserRouter,
  Navigate,
} from "react-router-dom";

import AuthCheck from "./components/auth/AuthCheck";
import SignIn from "./components/auth/SignIn";
import SignUp from "./components/auth/SignUp";
import Home from "./components/home/Home";
import { NavBar } from "./components/NavBar";
import AuthContext from "./contexts/AuthContext";
import { useState } from "react";
import { AuthorModel } from "./components/data/AuthorModel";
import { Outlet } from "react-router-dom";
import ProfilePage from "./components/profile/ProfilePage";
import NotiPage from "./components/notification/NotiPage";
import SinglePostView from "./components/notification/SinglePostView";

const router = createBrowserRouter([
  {
    path: "/site",
    element: (
      <AuthCheck>
        <NavBar />
        <Outlet />
      </AuthCheck>
    ),
    children: [
      {
        path: "",
        element: <Home />,
      },
      {
        path: "authors/:authorId/posts/:postId",
        element: <SinglePostView />,
      },
      {
        path: "authors/:authorId/inbox",
        element: <NotiPage />,
      },
      {
        path: "authors/*",
        element: <ProfilePage />,
      },
    ],
  },

  {
    path: "/site/signin",
    element: <SignIn></SignIn>,
  },
  {
    path: "/site/signup",
    element: <SignUp />,
  },
  {
    path: "*",
    element: (
      <Navigate
        to="/site"
        replace
      />
    ),
  },
]);

function App() {
  const [curUser, setCurUser] = useState<AuthorModel>({} as AuthorModel);
  return (
    <AuthContext.Provider value={{ curUser: curUser, setCurUser: setCurUser }}>
      <RouterProvider router={router}></RouterProvider>
    </AuthContext.Provider>
  );
}

export default App;
