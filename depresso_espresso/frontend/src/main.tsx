import ReactDOM from "react-dom/client";
import "./index.css";

// Pages
//import App from "./App";
import Login from "./components/auth/Login.tsx";
import ProfilePage from "./components/profile/ProfilePage.tsx";
import Register from "./components/auth/Register.tsx";

import { BrowserRouter, Route, Routes } from "react-router-dom";


const rootElement = document.getElementById("root") as Element;

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<ProfilePage />}
        />
        <Route
          path="/login"
          element={<Login />}
        />
        <Route
          path="/register"
          element={<Register />}
        />
        <Route
          path="/profile"
          element={<ProfilePage />}
        />
      </Routes>
    </BrowserRouter>
  );
}
