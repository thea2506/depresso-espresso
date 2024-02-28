
export interface CommentModel {
  authorid: string;
  authorname: string;
  comment: string;
  commentlikecount: number | null;
  contenttype: string | null;
  editdate: string | null;
  liked_by: string[];
  postid: string;
  publishdate: string;
}


