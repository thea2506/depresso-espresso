import ReactDOM from "react-dom/client";
import "./index.css";

// Pages
// import App from "./App";
import Signin from "./components/auth/Signin.tsx";
import Signup from "./components/auth/Signup.tsx";
import ProfilePage from "./components/profile/ProfilePage.tsx";
import Home from "./components/home/Home.tsx";
import { NavBar } from "./components/NavBar.tsx";
import AuthCheck from "./components/auth/Authcheck.tsx";

import { BrowserRouter, Route, Routes } from "react-router-dom";

const rootElement = document.getElementById("root") as Element;

const General = ({ children }: { children: React.ReactNode }) => (
  <div className="w-full">
    <NavBar />
    {children}
  </div>
);

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
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
              <General>
                <Home />
              </General>
            </AuthCheck>
          }
        />
        <Route
          path="/authors/:authorId" // This is a dynamic route + project requirements
          element={
            <General>
              <ProfilePage />
            </General>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export { General };
