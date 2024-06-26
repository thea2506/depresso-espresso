//#region imports
/* eslint-disable @typescript-eslint/no-explicit-any */
import { useContext, useEffect, useState } from "react";
import { PostView } from "../data/PostView";
import axios from "axios";
import AuthContext from "../../contexts/AuthContext";
//#endregion

const SinglePostView = () => {
  const [refresh, setRefresh] = useState(false);
  const { curUser } = useContext(AuthContext);
  const [post, setPost] = useState<any>();

  const url = window.location.href.split("/");
  const postid = url[url.length - 1];
  const authorid = url[url.length - 3];

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await axios.get(
          `/api/authors/${authorid}/posts/${postid}`
        );

        const post = response.data;

        const postModel = {
          title: post.title,
          id: post.id,
          author: post.author,
          description: post.description,
          contentType: post.contentType,
          content: post.content,
          count: post.count,
          published: post.published,
          visibility: post.visibility,
          likecount: post.like_count,
          origin: post.origin,
          source: post.source,
        };

        setPost(postModel);
      } catch (error) {
        console.error("An error occurred", error);
      }
    };
    fetchPost();
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
