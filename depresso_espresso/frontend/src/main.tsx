import ReactDOM from "react-dom/client";
import "./index.css";

// Pages
import App from "./App";
import Signin from "./components/auth/Signin.tsx";
import Signup from "./components/auth/Signup.tsx";
import ProfilePage from "./components/profile/ProfilePage.tsx";

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
          path="/signin"
          element={<Signin />}
        />
        <Route
          path="/signup"
          element={<Signup />}
        />
        <Route
          path="/authors/:userid"
          element={<ProfilePage />}
        />
      </Routes>
    </BrowserRouter>
  );
}
