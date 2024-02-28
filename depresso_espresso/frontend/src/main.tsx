import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

const rootElement = document.getElementById("root") as Element;
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(<App />);
}
