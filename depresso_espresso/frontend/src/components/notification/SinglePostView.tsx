//#region imports
/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from "react";
import { PostView } from "../data/PostView";
import axios from "axios";
import { AuthorModel } from "../data/AuthorModel";
//#endregion

const SinglePostView = () => {
  const [refresh, setRefresh] = useState(false);
  const [curUser, setCurUser] = useState({} as AuthorModel);
  const [post, setPost] = useState<any>();

  const url = window.location.href.split("/");
  const postid = url[url.length - 1];
  const authorid = url[url.length - 3];

  useEffect(() => {
    const retrieveData = async () => {
      try {
        const response = await axios("/curUser");
        if (response.data.success) {
          setCurUser(response.data);
        }
      } catch (error) {
        console.error(error);
      }
    };
    const fetchPost = async () => {
      try {
        const response = await axios.get(
          `/espresso-api/authors/${authorid}/posts/${postid}`
        );

        const allData = response.data;
        const author = allData.author[0];
        const rawpost = allData.post[0];
        author.fields.id = author.pk;

        const postModel = {
          title: rawpost.fields.title,
          id: rawpost.pk,
          author: author,
          description: rawpost.fields.description,
          contenttype: rawpost.fields.contentType,
          content: rawpost.fields.content,
          count: rawpost.fields.count,
          published: rawpost.fields.published,
          visibility: rawpost.fields.visibility,
          likecount: rawpost.fields.likecount,
          sharecount: rawpost.fields.sharecount,
        };
        setPost(postModel);
      } catch (error) {
        console.error("An error occurred", error);
      }
    };
    fetchPost();
    retrieveData();
  }, [authorid, postid, refresh]);

  return (
    <div className="flex flex-col w-full px-4 gap-y-4 sm:px-12 md:px-20 md:items-center md:justify-center">
      {post && (
        <PostView
          curUser={curUser}
          post={post}
          refresh={refresh}
          setRefresh={setRefresh}
        />
      )}
    </div>
  );
};

export default SinglePostView;