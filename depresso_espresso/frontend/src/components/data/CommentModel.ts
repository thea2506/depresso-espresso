export interface CommentModel {
  postid: any;
  id: string;
  author: any;
  
  contenttype: string | null;
  comment: string;

  publishdate: string;
  
  visibility: string;
  profile_image: string;
}
