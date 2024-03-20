/* eslint-disable @typescript-eslint/no-explicit-any */
import { Notification } from "./Notification";
import { useEffect, useState } from "react";
import axios from "axios";
import { AuthorModel } from "../data/AuthorModel";

const NotiPage = () => {
  const [curUser, setCurUser] = useState<AuthorModel>();
  // const [followRequests, setFollowRequests] = useState<[]>();
  const [refresh, setRefresh] = useState(false);
  const [notifications, setNotifications] = useState<any[]>([]);

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
    // const getFollowRequests = async () => {
    //   try {
    //     const response = await axios.get("/get_follow_requests", {
    //       params: { id: curUser?.id },
    //     });
    //     if (response.data.message != "No new requests")
    //       setFollowRequests(response.data);
    //   } catch (error) {
    //     console.error("An error occurred", error);
    //   }
    // };

    // get the notifications
    const getNotifications = async () => {
      if (!curUser?.id) return;
      try {
        const response = await axios.get(
          `/espresso-api/authors/${curUser?.id}/inbox`
        );
        console.log(response.data);
        if (response.status === 200) setNotifications(response.data.items);
      } catch (error) {
        console.error("An error occurred", error);
      }
    };

    getCurUser();
    //getFollowRequests();
    getNotifications();
  }, [curUser?.id, refresh]);

  return (
    <div className="flex flex-col justify-center mx-8 sm:mx-12 lg:mx-[20%] gap-y-6 md:item-center">
      <div className="flex items-center justify-between text-secondary-dark">
        <p>Your inbox</p>
        <p className="cursor-pointer hover:text-primary">Clear Activity</p>
      </div>
      {/* {followRequests?.map((request: any, index: number) => (
        <div key={index}>
          <Notification
            refresh={refresh}
            setRefresh={setRefresh}
            author={request.fields}
            authorid={request.pk}
            type="follow"
          />
        </div>
      ))} */}
      {notifications?.map((notification: any, index: number) => {
        if (!notification) return;
        const type = notification.type.toLowerCase();
        if (type === "follow")
          return (
            <div key={index}>
              <Notification
                curUser={curUser}
                refresh={refresh}
                setRefresh={setRefresh}
                notificationObject={notification}
                type="follow"
              />
            </div>
          );
        return (
          <div key={index}>
            <Notification
              curUser={curUser}
              refresh={refresh}
              setRefresh={setRefresh}
              notificationObject={notification}
              type={type}
            />
          </div>
        );
      })}
    </div>
  );
};

export default NotiPage;
