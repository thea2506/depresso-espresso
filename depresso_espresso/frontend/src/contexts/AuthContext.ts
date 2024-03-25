import React, { createContext } from "react";
import { AuthorModel } from "../components/data/AuthorModel";

interface AuthContextProps {
  curUser: AuthorModel;
  setCurUser: React.Dispatch<React.SetStateAction<AuthorModel>>;
}

const AuthContext = createContext<AuthContextProps>({
  curUser: {} as AuthorModel,
  setCurUser: () => {},
});

export default AuthContext;
