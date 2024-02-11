import React from "react";
import { cn } from "../utils/cn";

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
          className={cn(
            "px-4 py-3 md:py-4 text-white text-base rounded-lg bg-primary transition duration-75 ease-in-out hover:bg-secondary-light",
            className
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
          className={cn("text-primary  font-bold", className)}
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
