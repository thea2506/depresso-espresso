import React from "react";
import { twMerge } from "tailwind-merge";

// interfaces
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  buttonType: "regular" | "icon";
  icon?: string;
}

// Button component
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, buttonType, icon, ...props }, ref) => {
    // REGULAR BUTTON
    if (buttonType === "regular") {
      return (
        <button
          className={twMerge(
            className,
            "px-4 py-2 text-white rounded-lg bg-primary"
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
