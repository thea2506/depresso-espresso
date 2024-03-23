//References: https://stackoverflow.com/questions/43164554/how-to-implement-authenticated-routes-in-react-router-4/43171515#43171515 answer from fermmm
import axios from "axios";
import { FC, useEffect, useContext } from "react";
import AuthContext from "../../contexts/AuthContext";
import { useNavigate } from "react-router";

const backendURL = import.meta.env.VITE_BACKEND_URL;

const AuthCheck: FC<{ children: React.ReactNode }> = ({ children }) => {
  const navigate = useNavigate();
  const { curUser, setCurUser } = useContext(AuthContext);
  console.log("backendURL", backendURL);

  useEffect(() => {
    console.log("AuthCheck");
    const getCurUser = async () => {
      const res = await axios.get(`${backendURL}/api/auth/curUser`);
      if (!res.data.success) navigate("/signin");

      setCurUser(res.data);
    };
    getCurUser();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  if (!Object.entries(curUser).length) return <></>;
  return <>{children}</>;
};

export default AuthCheck;
