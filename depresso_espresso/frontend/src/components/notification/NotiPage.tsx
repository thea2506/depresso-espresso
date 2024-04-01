/* eslint-disable @typescript-eslint/no-explicit-any */
import { Notification } from "./Notification";
import { useContext, useEffect, useState } from "react";
import axios from "axios";
import AuthContext from "../../contexts/AuthContext";

const NotiPage = () => {
  const { curUser } = useContext(AuthContext);
  // const [followRequests, setFollowRequests] = useState<[]>();
  const [refresh, setRefresh] = useState(false);
  const [notifications, setNotifications] = useState<any[]>([]);

  useEffect(() => {
    // get the notifications
    const getNotifications = async () => {
      if (!curUser?.id) return;
      try {
        const response = await axios.get(`${curUser?.url}/inbox`);
        if (response.status === 200) {
          const items = response.data.items.map((item: any) => {
            if (item && item.type && item.actor.id != curUser.id) return item;
          });

          setNotifications(items);
        }
      } catch (error) {
        console.error("An error occurred", error);
      }
    };
    //getFollowRequests();
    getNotifications();
  }, [curUser, refresh]);

  const handleClearInbox = async () => {
    await axios.delete(`${curUser?.url}/inbox`);
    setRefresh(!refresh);
  };

  return (
    <div className="flex flex-col justify-center mx-8 sm:mx-12 lg:mx-[20%] gap-y-6 md:item-center">
      <div className="flex items-center justify-between text-secondary-dark">
        <p>Your inbox</p>
        <p
          className="cursor-pointer hover:text-primary"
          onClick={handleClearInbox}
        >
          Clear Activity
        </p>
      </div>
      {notifications?.reverse().map((notification: any, index: number) => {
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
