/* eslint-disable @typescript-eslint/no-explicit-any */
import { Notification } from "./Notification";
import { useEffect, useState } from "react";
import axios from "axios";
import { AuthorModel } from "../data/AuthorModel";

const NotiPage = () => {
  const [curUser, setCurUser] = useState<AuthorModel>();
  const [followRequests, setFollowRequests] = useState<[]>();
  const [refresh, setRefresh] = useState(false);

  useEffect(() => {
    // Get the current user's ID
    const getCurUser = async () => {
      try {
        const response = await axios.get("/curUser");
        if (response.data.success) {
          setCurUser(response.data);
        }
      } catch (error) {
        console.error("An error occurred", error);
      }
    };

    // get follow requests
    const getFollowRequests = async () => {
      try {
        const response = await axios.get("/get_follow_requests", {
          params: { id: curUser?.id },
        });
        if (response.data.message != "No new requests")
          setFollowRequests(response.data);
      } catch (error) {
        console.error("An error occurred", error);
      }
    };

    getCurUser();
    getFollowRequests();
  }, [curUser?.id, refresh]);

  return (
    <div className="flex flex-col justify-center mx-8 sm:mx-12 lg:mx-[20%] gap-y-8 md:item-center">
      <div className="flex items-center justify-between text-secondary-dark">
        <p>Your inbox</p>
        <p className="cursor-pointer hover:text-primary">Clear Activity</p>
      </div>
      {followRequests?.map((request: any, index: number) => (
        <div key={index}>
          <Notification
            refresh={refresh}
            setRefresh={setRefresh}
            author={request.fields}
            authorid={request.pk}
            type="follow"
          />
        </div>
      ))}
    </div>
  );
};

export default NotiPage;
