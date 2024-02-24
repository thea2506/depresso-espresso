//References: https://stackoverflow.com/questions/43164554/how-to-implement-authenticated-routes-in-react-router-4/43171515#43171515 answer from fermmm
import axios from "axios";
import Signin from "./Signin";
import { FC, useState } from "react";

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
    const response = await axios.get("/get_auth");
    console.log(response);
    if (response.data.success) {
      console.log("Logged in");
      setLog(true);
    } else {
      setLog(false);
      console.log("Not logged in");
    }
    return log_status;
  } catch (error) {
    console.error("An error occurred", error);
  }
};

export default AuthCheck;
