import { useState } from "react";
import axios from "axios";
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast, ToastOptions } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const nav = useNavigate()

  const myToast: ToastOptions<unknown> = {
    position: "top-center",
    autoClose: 7000,
    hideProgressBar: false,
    pauseOnHover: false,
    closeOnClick: true,
    theme: "light",
    closeButton: false,
  };

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {

      let formField = new FormData()
      formField.append('username', username)
      formField.append('password', password)
      
      const response = await axios.post("login", formField);
      if (response.data.success) {
        toast.success("Login Successful", myToast);
        console.log("Login successful");
      
        // Redirect to user's profile
        nav('/profile');
        
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
      <ToastContainer />
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
