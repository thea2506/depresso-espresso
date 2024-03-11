import { Notification } from "./Notification";

const InboxPage = () => {
  return (
    <div className="flex flex-col justify-center mx-8 sm:mx-12 lg:mx-[20%] gap-y-8 md:item-center">
      <div className="flex items-center justify-between text-secondary-dark">
        <p>Your inbox</p>
        <p className="cursor-pointer hover:text-primary">Clear Activity</p>
      </div>
      <Notification
        username="biguser" // Manually enter name of user sending follow request for now
        type="follow"
        link=""
      />
      <Notification
        username="Katarina"
        type="share"
        link=""
      />
    </div>
  );
};

export default InboxPage;
