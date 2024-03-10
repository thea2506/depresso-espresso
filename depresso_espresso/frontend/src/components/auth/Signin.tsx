//#region imports
import Circle_1 from "../../assets/images/circle_1.svg";
import Circle_2 from "../../assets/images/circle_2.svg";
import visibleOn from "../../assets/icons/visible_on.svg";
import visibleOff from "../../assets/icons/visible_off.svg";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { ToastContainer, ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { animated, useSpring } from "@react-spring/web";
import { useContext } from "react";
import { AuthContext } from "../../App";

// components
import { Button } from "../Button";
//#endregion

const myToast: ToastOptions = {
  position: "top-center",
  autoClose: 1000,
  hideProgressBar: true,
  closeOnClick: true,
  closeButton: false,
  pauseOnHover: false,
  draggable: false,
  progress: undefined,
};

/**
 * Renders a signup page.
 * @returns The rendered signup page.
 */
const Signin = () => {
  const inputs: string[] = ["Display Name", "Password"];
  const [displayName, setDisplayName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [visible, setVisible] = useState<boolean>(false);
  const nav = useNavigate();
  const springs = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 },
  });
  const {
    setId0,
    setHost0,
    setDisplayName0,
    setUrl0,
    setGithub0,
    setProfileImage0,
  } = useContext(AuthContext);

  //#region functions
  /**
   * Handles and saves the inputs from the user.
   * @param e The event object to extract the value input by users
   */
  const handleInputs = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === "Display Name") {
      setDisplayName(value);
    } else if (name === "Password") {
      setPassword(value);
    }
  };

  /**
   * Verifies the inputs from the user and sends a request to the server.
   */

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    try {
      const formField = new FormData();
      formField.append("displayName", displayName);
      formField.append("password", password);

      const response = await axios.post("/signin", formField);

      if (response.data.success) {
        console.log(response.data);
        setId0(response.data.id);
        setHost0(response.data.host);
        setDisplayName0(response.data.displayName);
        setUrl0(response.data.url);
        setGithub0(response.data.github);
        setProfileImage0(response.data.profileImage);

        toast.success("Login Successful", myToast);
        nav("/");
      } else {
        toast.error("Login failed", myToast);
      }
    } catch (error) {
      console.error("An error occurred", error);
      toast.error("An error occurred", myToast);
    }
  };
  //#endregion

  return (
    <animated.div
      className="relative flex flex-col items-center justify-center h-screen px-4 gap-y-12 lg:flex-row lg:gap-x-20 sm:px-12 md:px-20"
      style={springs}
    >
      <ToastContainer />
      {/* Left - Text side */}
      <div className="z-10 flex flex-col w-full text-center gap-y-3 lg:text-start">
        <h1 className="text-4xl font-medium sm:text-4xl md:text-5xl lg:text-6xl text-secondary-dark whitespace-nowrap">
          Welcome back
        </h1>
        <p className="text-base sm:text-lg md:text-xl">
          Not registered for <b className=" text-secondary-dark">Espresso</b>{" "}
          yet?{" "}
          <a
            href="/signup"
            className="font-bold text-secondary-light"
          >
            Sign Up
          </a>
        </p>
      </div>

      {/* Right - Input side */}
      <form
        className="z-10 flex flex-col items-center justify-center w-full max-w-3xl px-4 gap-y-4 md:px-0"
        onSubmit={handleSubmit}
      >
        {inputs.map((input, index) => {
          return (
            <div
              key={index}
              className="flex flex-col justify-center w-full gap-y-1 text-start"
            >
              <label
                htmlFor={input}
                className="font-bold "
              >
                {input}
              </label>
              {input.toLowerCase() !== "password" ? (
                <input
                  type="text"
                  id={input}
                  name={input}
                  className="w-full h-12 px-4 py-2 bg-white border-2 rounded-xl border-primary"
                  onChange={handleInputs}
                />
              ) : (
                <div className="relative">
                  <input
                    type="password"
                    id={input}
                    name={input}
                    className="w-full h-12 px-4 py-2 bg-white border-2 rounded-xl border-primary"
                    onChange={handleInputs}
                  />
                  <Button
                    buttonType="icon"
                    icon={visible ? visibleOff : visibleOn}
                    className="absolute w-6 h-6 top-2 right-3"
                    onClick={() => {
                      setVisible(!visible);
                      const element = document.getElementsByName("Password")[0];
                      visible
                        ? element.setAttribute("type", "password")
                        : element.setAttribute("type", "text");
                    }}
                    type="button"
                  ></Button>
                </div>
              )}
            </div>
          );
        })}
        <Button
          buttonType="text"
          className="w-full mt-4 rounded-full hover:bg-primary md:hover:bg-secondary-light hover:text-white"
          type="submit"
        >
          Sign In
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

export default Signin;
