// Test component for User register, to be replaced or updated
// References:
// https://www.youtube.com/watch?v=xtQ74HKTOwY&t=1017s Django + React Part-3 | Add Product Form Data in React Using Axios POST Method to Django API by Great Adib 2/19/2024

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast, ToastOptions } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

/**
 * Submits a custom userCreationForm using POST request to register endpoint
 */
function Register() {
  const [username, setUsername] = useState("");
  const [display_name, setDisplayName] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const nav = useNavigate();

  const myToast: ToastOptions<unknown> = {
    position: "top-center",
    autoClose: 7000,
    hideProgressBar: false,
    pauseOnHover: false,
    closeOnClick: true,
    theme: "light",
    closeButton: false,
  };
  /**
   * Sends POST request upon form submission
   */
  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      const formField = new FormData();
      formField.append("username", username);
      formField.append("display_name", display_name);
      formField.append("password1", password1);
      formField.append("password2", password2);
      const response = await axios.post(
        `${
          import.meta.env.DEV === true ? "http://127.0.0.1:8000" : ""
        }/register`,
        formField
      );

      if (response.data.success) {
        toast.success("User Created Successfully", myToast);
        console.log("User creation successful");

        // navigate to user's profile page on success
        nav("/profile");
      } else {
        console.log("Register Failed");

        // Show users why their registration failed
        for (const error of response.data.errors) {
          toast.error("Register failed: " + error, myToast);
        }
      }
    } catch (error) {
      console.error("An error occurred", error);
      toast.error("An error occurred", myToast);
    }
  };

  return (
    <div>
      <ToastContainer />
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="text"
          placeholder="Display Name"
          value={display_name}
          onChange={(e) => setDisplayName(e.target.value)}
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
