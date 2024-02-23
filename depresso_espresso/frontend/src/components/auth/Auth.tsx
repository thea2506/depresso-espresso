//References: https://stackoverflow.com/questions/43164554/how-to-implement-authenticated-routes-in-react-router-4/43171515#43171515 answer from fermmm 
import axios from "axios";
import Signin from "./Signin";
import { FC, useState } from "react";
import {ToastOptions, toast } from "react-toastify";

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

const AuthCheck: FC<{ children: React.ReactNode }> = ({ children }) => {

    const log_status = useLoginStatus();
  
    if (!log_status) {
        return <Signin />;
    }
    return children;
    
 };

 const useLoginStatus = async () => {
    const [log_status, setLog] = useState<boolean>();
  
    try {
      const response = await axios.get(`${import.meta.env.DEV === true ? "http://127.0.0.1:8000" : ""}/is_authenticated`)
      
      if (response.data.success) {
        console.log("Loggd in");
        toast.success("Loggd in", myToast);
          setLog(true);
      } 
      else{
          setLog(false);
          toast.success("not Loggd in", myToast);
      }
      return log_status;
  
  }catch (error) {
      console.error("An error occurred", error);
  }

}

export default AuthCheck;

