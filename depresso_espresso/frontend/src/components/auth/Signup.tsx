//#region imports
import Circle_1 from "../../assets/images/circle_1.svg";
import Circle_2 from "../../assets/images/circle_2.svg";
import { Button } from "../Button";
//#endregion

const Signup = () => {
  const inputs = ["Username", "Email", "Password", "Retype Password"];

  return (
    <div className="relative flex flex-col items-center justify-center h-full px-4 gap-y-12 lg:justify-between lg:flex-row lg:gap-x-20 sm:px-12 md:px-20">
      {/* Left - Text side */}
      <div className="z-10 flex flex-col text-center lg:text-start gap-y-3">
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
              <input
                type="text"
                id={input}
                name={input}
                className="w-full h-12 max-w-3xl px-4 py-2 bg-white border-2 rounded-xl border-primary"
              />
            </div>
          );
        })}
        <Button
          buttonType="text"
          className="max-w-3xl mt-4 rounded-full"
        >
          Sign Up
        </Button>
      </div>

      {/* Decorations */}
      <img
        src={Circle_1}
        className="absolute bottom-0 left-0 object-cover"
      ></img>
      <img
        src={Circle_2}
        className="absolute top-0 left-0 object-cover"
      ></img>
    </div>
  );
};

export default Signup;
