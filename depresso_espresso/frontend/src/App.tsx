import { useEffect } from "react";
import "./App.css";

import {
  RouterProvider,
  createBrowserRouter,
  Navigate,
} from "react-router-dom";

import axios from "axios";

const router = createBrowserRouter([
  {
    path: "/site",
    element: <div>Site</div>,
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
  useEffect(() => {
    async function getId() {
      const response = await axios.get(
        `${import.meta.env.VITE_BACKEND_URL}/auth/curUser`
      );
      console.log("response", response.data);
    }
    getId();
  }, []);
  console.log("ENV", import.meta.env.MODE);

  return <RouterProvider router={router}></RouterProvider>;
}

export default App;
