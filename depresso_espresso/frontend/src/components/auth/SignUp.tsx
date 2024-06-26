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
const SignUp = () => {
  const inputs: string[] = [
    "Username",
    "Display Name",
    "Password",
    "Retype Password",
  ];
  const [visible, setVisible] = useState<boolean>(false);
  const nav = useNavigate();
  const springs = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 },
  });

  //#region functions

  /**
   * Posts the inputs to the backend.
   */
  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    const username = (document.getElementById("username") as HTMLInputElement)
      .value;
    const password = (document.getElementById("password") as HTMLInputElement)
      .value;
    const displayName = (
      document.getElementById("display name") as HTMLInputElement
    ).value;
    const retypePassword = (
      document.getElementById("retype password") as HTMLInputElement
    ).value;
    try {
      const formField = new FormData();
      formField.append("username", username);
      formField.append("displayName", displayName);
      formField.append("password1", password);
      formField.append("password2", retypePassword);
      const response = await axios.post(`/api/auth/signup`, formField);

      if (response.data.success) {
        toast.success("User Created Successfully", myToast);

        // navigate to user's profile page on success
        nav("/site/signin");
      } else {
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
      <animated.div className="z-10 flex flex-col w-full text-center lg:text-start gap-y-3">
        <h1 className="text-4xl font-medium sm:text-4xl md:text-5xl lg:text-6xl text-secondary-dark whitespace-nowrap">
          Create an Account
        </h1>
        <p className="text-base sm:text-lg md:text-xl">
          Already have an account for{" "}
          <b className=" text-secondary-dark">Espresso</b>?{" "}
          <a
            href="/site/signin"
            className="font-bold text-secondary-light"
          >
            Sign In
          </a>
        </p>
      </animated.div>

      {/* Right - Input side */}
      <form
        className="z-10 flex flex-col items-center justify-center w-full max-w-2xl px-4 gap-y-4 md:px-0"
        onSubmit={handleSubmit}
      >
        {inputs.map((input, index) => {
          return (
            <div
              key={index}
              className="flex flex-col w-full gap-y-1 text-start"
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
                  id={input.toLowerCase()}
                  name={input.toLowerCase()}
                  className="w-full h-12 px-4 py-2 bg-white border-2 rounded-xl border-primary"
                  autoComplete={input === "username" ? "username" : ""}
                />
              ) : (
                <div className="relative w-full">
                  <input
                    type="password"
                    id={input.toLowerCase()}
                    name={input.toLowerCase()}
                    className="w-full h-12 px-4 py-2 bg-white border-2 rounded-xl border-primary"
                    autoComplete="new-password"
                  />
                  <Button
                    buttonType="icon"
                    type="button"
                    icon={visible ? visibleOff : visibleOn}
                    className="absolute w-6 h-6 top-2 right-3"
                    onClick={() => {
                      setVisible(!visible);
                      const element1 =
                        document.getElementsByName("password")[0];
                      const element2 =
                        document.getElementsByName("retype password")[0];
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
          className="w-full mt-4 rounded-full hover:bg-primary md:hover:bg-secondary-light hover:text-white"
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

export default SignUp;
