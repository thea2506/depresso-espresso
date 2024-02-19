import { useState } from "react";
import axios from "axios";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      
      const response = await axios.post("/api/login/", { username, password });
      if (response.data.success) {
        
        console.log("Login successful");
        // Redirect or update UI accordingly

        // Example of redirecting to the home page
        window.location.href = "/";
      } else {
        console.log("Login failed");
        // Show error message

        // Example of updating the UI to show an error message
        const errorMessage = document.createElement("p");
        errorMessage.textContent = "Login failed";
        document.body.appendChild(errorMessage);
      }
    } catch (error) {
      console.error("An error occurred", error);

      // Handle error
      // Example of updating the UI to show an error message
      const errorMessage = document.createElement("p");
      errorMessage.textContent = "An error occurred";
      document.body.appendChild(errorMessage);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input type="submit" />
      </form>
    </div>
  );
}

export default Login;
