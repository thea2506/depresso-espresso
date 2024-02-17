//#region imports
import React from "react";
import { cn } from "../utils/cn";
//#endregion

//#region interfaces
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  buttonType: "text" | "icon";
  icon?: string;
}
//#endregion

/**
 * Renders the Button component.
 * @param {string} className - The CSS class name for the button.
 * @param {string} buttonType - The type of button ("text" or "icon").
 * @param {string} icon - The URL of the icon image (only applicable for "icon" button type).
 * @param props - Additional props for the button element.
 * @param ref - The ref object for the button element.
 * @returns The rendered Button component.
 */
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, buttonType, icon, ...props }, ref) => {
    // Regular Button
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

    // Icon Button
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
            className="w-7 h-7 md:w-8 md:h-8"
          />
        </button>
      );
    }
  }
);

Button.displayName = "Button";
export { Button };
