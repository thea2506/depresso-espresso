// Test component for User sign up, to be replaced or updated

import { useState } from "react";
import axios from "axios";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [firstname, setFirstName] = useState("");
  const [lastname, setLastName] = useState("");

  console.log("help");

  const handleRegister = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      const response = await axios.post("/api/register/", { username, password, firstname, lastname});
      if (response.data.success) {
        console.log("User creation successful");
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
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="firstname"
          placeholder="firstname"
          value={firstname}
          onChange={(e) => setFirstName(e.target.value)}
        />
        <input
          type="lastname"
          placeholder="lastname"
          value={lastname}
          onChange={(e) => setLastName(e.target.value)}
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

export default Register;
