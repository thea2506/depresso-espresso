/* eslint-disable @typescript-eslint/no-explicit-any */
import { Notification } from "./Notification";
import { useEffect, useState } from "react";
import axios from "axios";
import { AuthorModel } from "../data/AuthorModel";

const NotiPage = () => {
  const [curUser, setCurUser] = useState<AuthorModel>();
  const [followRequests, setFollowRequests] = useState<[]>();
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

    // get the notifications
    const getNotifications = async () => {
      try {
        const response = await axios.get(`/get_notifications/${curUser?.id}`);
        if (response.data.length > 0) {
          setNotifications(response.data);
        }
      } catch (error) {
        console.error("An error occurred", error);
      }
    };

    getCurUser();
    getFollowRequests();
    getNotifications();
  }, [curUser?.id, refresh]);

  return (
    <div className="flex flex-col justify-center mx-8 sm:mx-12 lg:mx-[20%] gap-y-6 md:item-center">
      <div className="flex items-center justify-between text-secondary-dark">
        <p>Your inbox</p>
        <p className="cursor-pointer hover:text-primary">Clear Activity</p>
      </div>
      {followRequests?.map((request: any, index: number) => (
        <div key={index}>
          <Notification
            summary={request?.summary}
            refresh={refresh}
            setRefresh={setRefresh}
            author={request.fields}
            authorid={request.pk}
            type="follow"
          />
        </div>
      ))}
      {notifications
        ?.sort((b, a) => a.created_at.localeCompare(b.created_at))
        .map((notification: any, index: number) => (
          <div key={index}>
            <Notification
              summary={notification?.summary}
              refresh={refresh}
              setRefresh={setRefresh}
              author={notification.author}
              authorid={notification.author.id}
              authorpostid={notification.post.authorid}
              type={notification.type}
              createdAt={notification.created_at}
              postid={notification.post.id}
            />
          </div>
        ))}
    </div>
  );
};

export default NotiPage;
