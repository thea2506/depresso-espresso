import React from "react";
import { twMerge } from "tailwind-merge";

// interfaces
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  buttonType: "text" | "icon";
  icon?: string;
}

// Button component
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, buttonType, icon, ...props }, ref) => {
    // REGULAR BUTTON
    if (buttonType === "text") {
      return (
        <button
          className={twMerge(
            className,
            "px-4 py-3 md:py-4 text-white rounded-lg bg-primary transition duration-75 ease-in-out hover:bg-secondary-light"
          )}
          ref={ref}
          {...props}
        ></button>
      );
    }

    // ICON BUTTON
    else if (buttonType === "icon") {
      return (
        <button
          className={twMerge(className, "text-primary  font-bold")}
          ref={ref}
          {...props}
        >
          <img
            src={icon}
            alt="Icon"
            className="w-7 h-7 md:w-9 md:h-9"
          />
        </button>
      );
    }
  }
);

Button.displayName = "Button";
export { Button };
