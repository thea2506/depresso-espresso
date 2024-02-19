import ReactDOM from "react-dom/client";
import "./index.css";

// Pages
import App from "./App";
import Login from "./components/auth/Login.tsx";
import ProfilePage from "./components/profile/ProfilePage.tsx";
import Register from "./components/Register.tsx";

import { BrowserRouter, Route, Routes } from "react-router-dom";


const rootElement = document.getElementById("root") as Element;

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<App />}
        />
        <Route
          path="/login"
          element={<Login />}
        />
      </Routes>
    </BrowserRouter>
  );
}
