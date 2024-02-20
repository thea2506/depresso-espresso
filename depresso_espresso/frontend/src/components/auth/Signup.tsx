const Signup = () => {
  const inputs = ["Username", "Email", "Password", "Retype Password"];

  return (
    <div className="flex items-center justify-between h-full gap-x-20">
      <div className="flex flex-col text-start gap-y-3">
        <h1 className="text-6xl text-secondary-dark">Create an Account</h1>
        <p className="text-xl">
          Already have an account for{" "}
          <b className=" text-secondary-dark">Espresso</b>?{" "}
          <a
            href=""
            className="font-bold text-secondary-light"
          >
            Sign In
          </a>
        </p>
      </div>
      <div className="flex flex-col items-center flex-grow gap-y-4">
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
                className="h-12 px-4 py-2 bg-white border-2 md:w-96 rounded-xl border-primary"
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Signup;
