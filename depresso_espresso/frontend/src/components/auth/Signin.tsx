//#region imports
import Circle_1 from "../../assets/images/circle_1.svg";
import Circle_2 from "../../assets/images/circle_2.svg";
import visibleOn from "../../assets/icons/visible_on.svg";
import visibleOff from "../../assets/icons/visible_off.svg";
import { useState } from "react";
import { ToastContainer, ToastOptions, toast } from "react-toastify";

// components
import { Button } from "../Button";
//#endregion

/**
 * Renders a signup page.
 * @returns The rendered signup page.
 */
const Signin = () => {
  const inputs: string[] = ["Email", "Password"];
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [visible, setVisible] = useState<boolean>(false);

  //#region functions
  /**
   * Handles the visibility of the password.
   */
  const handleVisibility = () => {
    setVisible(!visible);
    const element = document.getElementsByName("Password")[0];
    visible
      ? element.setAttribute("type", "password")
      : element.setAttribute("type", "text");
  };

  /**
   * Handles and saves the inputs from the user.
   * @param e The event object to extract the value input by users
   */
  const handleInputs = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === "Email") {
      setEmail(value);
    } else if (name === "Password") {
      setPassword(value);
    }
  };

  /**
   * Posts the inputs to the backend.
   */
  const verifyInputs = () => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
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

    if (!pattern.test(email)) {
      toast.error("Invalid email", myToast);
      return;
    } else if (password.length < 8) {
      toast.error("Password must be at least 8 characters", myToast);
      return;
    }

    //TODO: verify the inputs to the backend + redirect to the home page
    console.log(email, password);
  };
  //#endregion

  return (
    <div className="relative flex flex-col items-center justify-center h-full px-4 gap-y-12 lg:justify-between lg:flex-row lg:gap-x-20 sm:px-12 md:px-20">
      <ToastContainer />
      {/* Left - Text side */}
      <div className="z-10 flex flex-col text-center lg:text-start gap-y-3">
        <h1 className="text-3xl font-medium sm:text-4xl md:text-5xl lg:text-6xl text-secondary-dark whitespace-nowrap">
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
      <div className="z-10 flex flex-col w-3/4 lg:w-1/2 gap-y-4">
        {inputs.map((input, index) => {
          return (
            <div
              key={index}
              className="flex flex-col gap-y-1 text-start"
            >
              <label
                htmlFor={input}
                className="font-bold "
              >
                {input}
              </label>
              {input.toLowerCase() !== "password" ? (
                <input
                  type={input.toLowerCase() === "email" ? "email" : "text"}
                  id={input}
                  name={input}
                  className="w-full h-12 max-w-3xl px-4 py-2 bg-white border-2 rounded-xl border-primary"
                  onChange={handleInputs}
                />
              ) : (
                <div className="relative">
                  <input
                    type="password"
                    id={input}
                    name={input}
                    className="w-full h-12 max-w-3xl px-4 py-2 bg-white border-2 rounded-xl border-primary"
                    onChange={handleInputs}
                  />
                  <Button
                    buttonType="icon"
                    icon={visible ? visibleOff : visibleOn}
                    className="absolute w-6 h-6 top-2 right-3"
                    onClick={handleVisibility}
                  ></Button>
                </div>
              )}
            </div>
          );
        })}
        <Button
          buttonType="text"
          className="max-w-3xl mt-4 rounded-full hover:bg-primary md:hover:bg-secondary-light hover:text-white"
          onClick={verifyInputs}
        >
          Sign In
        </Button>
      </div>

      {/* Decorations */}
      <img
        src={Circle_1}
        className="absolute bottom-0 left-0 object-cover opacity-80"
      ></img>
      <img
        src={Circle_2}
        className="absolute top-0 left-0 object-cover"
      ></img>
    </div>
  );
};

export default Signin;
