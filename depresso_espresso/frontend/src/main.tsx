import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import Login from "./components/Login.tsx";
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
        <Route
          path="/register"
          element={<Register />}
        />
      </Routes>
    </BrowserRouter>
  );
}
