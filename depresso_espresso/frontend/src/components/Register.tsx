// Test component for User register, to be replaced or updated
// References:
// https://www.youtube.com/watch?v=xtQ74HKTOwY&t=1017s Django + React Part-3 | Add Product Form Data in React Using Axios POST Method to Django API by Great Adib 2/19/2024

import { useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios";

function Register() {
  const [username, setUsername] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");

  const nav = useNavigate()

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {

      let formField = new FormData()
      formField.append('username', username)
      formField.append('password1', password1)
      formField.append('password2', password2)
      formField.append('first_name', first_name)
      formField.append('last_name', last_name)

      const response = await axios.post("register", formField);
      console.log(formField);
      if (response.data.success) {
        console.log("User creation successful");
        nav('/');
        // Redirect or update UI accordingly

        // Example of redirecting to the home page
        window.location.href = "/";
      } else {
        console.log("Login failed");
        // Show error message

        // Example of updating the UI to show an error message
        const errorMessage = document.createElement("p");
        errorMessage.textContent = "Register failed";

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
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="text"
          placeholder="First name"
          value={first_name}
          onChange={(e) => setFirstName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Last name"
          value={last_name}
          onChange={(e) => setLastName(e.target.value)}
        />
        <input
          type="Password"
          placeholder="Password"
          value={password1}
          onChange={(e) => setPassword1(e.target.value)}
        />
        <input
          type="Password"
          placeholder="Retype Password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
        />
        <input type="submit" />
      </form>
    </div>
  );
}

export default Register;
