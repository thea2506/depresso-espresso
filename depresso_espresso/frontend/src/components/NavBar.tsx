//#region imports
import { useEffect, useState } from "react";
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
  const [currentPage, setCurrentPage] = useState<string>(
    window.location.pathname.substring(window.location.pathname.indexOf("/"))
  );
  const [id0, setId0] = useState<string>("");
  const authorIDPath = `/authors/${id0}`;
  const authorInboxPath = `/authors/${id0}/inbox`;

  const nav = useNavigate();

  useEffect(() => {
    const getId = async () => {
      try {
        const response = await axios.get("/curUser");
        if (response.data.success) {
          setId0(response.data.id);
        }
      } catch (error) {
        console.error("An error occurred", error);
      }
    };
    getId();
  });

  const navContents = [
    { icon: <GoHome />, link: "/", name: "" },
    { icon: <GoPerson />, link: authorIDPath, name: "authors" },
    { icon: <GoInbox />, link: authorInboxPath, name: "inbox" },
    { icon: <PiNewspaperClipping />, link: "/discover", name: "discover" },
  ];

  //#region functions
  /**
   * Changes the current page and navigates to the new page
   * @param name The name of the page
   * @param link The link to the page
   */
  const changePage = (link: string) => {
    setCurrentPage(link);
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
        localStorage.clear();
        nav("/signin");
      } else {
        toast.error("Logout failed", myToast);
      }
    } catch (error) {
      console.error("An error occurred", error);
      toast.error("An error occurred", myToast);
    }
  };

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
              currentPage === item.link ? "text-primary" : ""
            )}
            onClick={() => changePage(item.link)}
          ></Button>
        ))}
      </ul>
      {/* Logout */}
      <Button
        buttonType="icon"
        icon={<LiaSignOutAltSolid />}
        className={twMerge(
          iconStyling,
          "hidden w-1/4 lg:flex items-center justify-center"
        )}
        onClick={handleLogout}
      />
    </nav>
  );
};

export { NavBar };
