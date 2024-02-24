
import axios from "axios";
import { FC, useState } from "react";
import MakePost from "../data/MakePost";

const Logo = "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500";

const Home: FC<{}> = () => {
  const [display_name, setDisplayName] = useState<string>("");


  const retrieveData = async () => {
    try {

      const response = await axios.get(
        `${import.meta.env.DEV === true ? "http://127.0.0.1:8000" : ""}/user_data`
      );

      setDisplayName(response.data.display_name);
    }catch(error){
      console.log("User fetch Failed");
    }

  }

  retrieveData();

  return (
    <div>
      <h3>{display_name} home page</h3>
      <div>
        <img height="250" src={Logo} alt="Logo" /> 
      </div>
      <p>This component shows a cat.</p>
      <p>You must be signed in to view</p>
      <MakePost/>
    </div>
  );
};

export default Home;
