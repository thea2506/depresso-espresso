//#region imports
import Circle_1 from "../../assets/images/circle_1.svg";
import Circle_2 from "../../assets/images/circle_2.svg";
import visibleOn from "../../assets/icons/visible_on.svg";
import visibleOff from "../../assets/icons/visible_off.svg";
import { useState } from "react";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { animated, useSpring } from "@react-spring/web";

// components
import { Button } from "../Button";
//#endregion

const myToast: ToastOptions = {
  position: "top-center",
  autoClose: 1000,
  hideProgressBar: true,
  closeOnClick: true,
  pauseOnHover: false,
  draggable: false,
  progress: undefined,
  closeButton: false,
};

/**
 * Renders a signup page.
 * @returns The rendered signup page.
 */
const Signup = () => {
  const inputs: string[] = [
    "Username",
    "Display Name",
    "Password",
    "Retype Password",
  ];
  const [username, setUsername] = useState<string>("");
  const [displayName, setDisplayName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [retypePassword, setRetypePassword] = useState<string>("");
  const [visible, setVisible] = useState<boolean>(false);
  const nav = useNavigate();
  const springs = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 },
  });

  //#region functions
  /**
   * Handles and saves the inputs from the user.
   * @param e The event object to extract the value input by users
   */
  const handleInputs = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === "Username") {
      setUsername(value);
    } else if (name === "Display Name") {
      setDisplayName(value);
    } else if (name === "Password") {
      setPassword(value);
    } else if (name === "Retype Password") {
      setRetypePassword(value);
    }
  };

  /**
   * Posts the inputs to the backend.
   */
  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      const formField = new FormData();
      formField.append("username", username);
      formField.append("display_name", displayName);
      formField.append("password1", password);
      formField.append("password2", retypePassword);
      const response = await axios.post(
        `${
          import.meta.env.VITE_ENVIRONMENT === "dev"
            ? "http://127.0.0.1:8000"
            : "https://espresso-a3b726fa7f99.herokuapp.com"
        }/signup`,
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
  //#endregion

  return (
    <animated.div
      className="relative flex flex-col items-center justify-center h-screen px-4 gap-y-12 lg:justify-start lg:flex-row lg:gap-x-20 sm:px-12 md:px-20"
      style={springs}
    >
      <ToastContainer />
      {/* Left - Text side */}
      <animated.div className="z-10 flex flex-col text-center lg:text-start gap-y-3">
        <h1 className="text-3xl font-medium sm:text-4xl md:text-5xl lg:text-6xl text-secondary-dark whitespace-nowrap">
          Create an Account
        </h1>
        <p className="text-base sm:text-lg md:text-xl">
          Already have an account for{" "}
          <b className=" text-secondary-dark">Espresso</b>?{" "}
          <a
            href="/signin"
            className="font-bold text-secondary-light"
          >
            Sign In
          </a>
        </p>
      </animated.div>

      {/* Right - Input side */}
      <form
        className="z-10 flex flex-col w-3/4 lg:w-1/2 gap-y-4"
        onSubmit={handleSubmit}
      >
        {inputs.map((input, index) => {
          return (
            <div
              key={index}
              className="flex flex-col gap-y-1 text-start"
            >
              <label
                htmlFor={input}
                className="font-bold"
              >
                {input}
              </label>
              {input.toLowerCase() !== "password" &&
              input.toLowerCase() !== "retype password" ? (
                <input
                  type="text"
                  id={input}
                  name={input}
                  className="w-full h-12 max-w-3xl px-4 py-2 bg-white border-2 rounded-xl border-primary"
                  onChange={handleInputs}
                />
              ) : (
                <div className="relative max-w-3xl">
                  <input
                    type="password"
                    id={input}
                    name={input}
                    className="w-full h-12 px-4 py-2 bg-white border-2 rounded-xl border-primary"
                    onChange={handleInputs}
                  />
                  <Button
                    buttonType="icon"
                    type="button"
                    icon={visible ? visibleOff : visibleOn}
                    className="absolute w-6 h-6 top-2 right-3"
                    onClick={() => {
                      setVisible(!visible);
                      const element1 =
                        document.getElementsByName("Password")[0];
                      const element2 =
                        document.getElementsByName("Retype Password")[0];
                      visible
                        ? element1.setAttribute("type", "password")
                        : element1.setAttribute("type", "text");
                      visible
                        ? element2.setAttribute("type", "password")
                        : element2.setAttribute("type", "text");
                    }}
                  ></Button>
                </div>
              )}
            </div>
          );
        })}
        <Button
          buttonType="text"
          className="max-w-3xl mt-4 rounded-full hover:bg-primary md:hover:bg-secondary-light hover:text-white"
          type="submit"
        >
          Sign Up
        </Button>
      </form>

      {/* Decorations */}
      <img
        src={Circle_1}
        className="absolute bottom-0 left-0 object-cover opacity-80"
      ></img>
      <img
        src={Circle_2}
        className="absolute top-0 left-0 object-cover"
      ></img>
    </animated.div>
  );
};

export default Signup;
