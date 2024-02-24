//#region imports
import { useState } from "react";
import { twMerge } from "tailwind-merge";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { ToastOptions, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

// components
import { Button } from "./Button";

// icons
import { GoHome, GoPerson, GoInbox } from "react-icons/go";
import { PiNewspaperClipping } from "react-icons/pi";
import { LiaSignOutAltSolid } from "react-icons/lia";
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

const NavBar = () => {
  const iconStyling = "text-3xl text-black hover:text-secondary-dark";
  console.log(window.location.pathname);
  console.log("I ammmm", window.location.pathname.split("/")[1]);
  const [currentPage, setCurrentPage] = useState<string>(
    window.location.pathname.split("/")[1]
  );
  const nav = useNavigate();

  // TODO: add the correct authorID to the link (dynamic route)
  // Inbox and Discover are not implemented yet
  const navContents = [
    { icon: <GoHome />, link: "/", name: "" },
    { icon: <GoPerson />, link: "/authors/:authorId", name: "authors" },
    { icon: <GoInbox />, link: "/inbox", name: "inbox" },
    { icon: <PiNewspaperClipping />, link: "/discover", name: "discover" },
  ];

  //#region functions
  /**
   * Changes the current page and navigates to the new page
   * @param name The name of the page
   * @param link The link to the page
   */
  const changePage = (name: string, link: string) => {
    setCurrentPage(name);
    nav(link);
  };

  /**
   * Logs the user out
   */
  const handleLogout = async () => {
    try {
      const response = await axios.post("/logoutUser");

      if (response.data.success) {
        toast.success("You have been logged out", myToast);
        nav("/signin");
      } else {
        toast.error("Logout failed", myToast);
      }
    } catch (error) {
      console.error("An error occurred", error);
      toast.error("An error occurred", myToast);
    }
    }

  //#endregion

  return (
    <nav className="z-50 flex items-center justify-between w-full px-8 my-8 sm:px-12 md:px-20">
      {/* Logo */}
      <a
        className="hidden w-1/4 text-2xl transition duration-150 ease-in-out lg:block hover:text-primary"
        href="/"
      >
        <span className="text-primary">E</span>spresso
      </a>
      {/* Nav Links */}
      <ul className="flex items-center justify-center w-full gap-x-20 lg:gap-x-36">
        {navContents.map((item, index) => (
          <Button
            buttonType="icon"
            icon={item.icon}
            key={index}
            className={twMerge(
              iconStyling,
              currentPage === item.name ? "text-primary" : ""
            )}
            onClick={() => changePage(item.name, item.link)}
          ></Button>
        ))}
      </ul>
      {/* Logout */}
      <Button
        buttonType="icon"
        icon={<LiaSignOutAltSolid />}
        className={twMerge(
          iconStyling,
          "hidden w-1/4 lg:flex items-end justify-end"
        )}
        onClick={handleLogout}
      />
    </nav>
  );
};

export { NavBar };
