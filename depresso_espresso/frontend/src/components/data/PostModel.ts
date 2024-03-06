export interface PostModel {
  username: string;
  user_img_url?: string;

  title?: string;
  postid: string;
  source?: string;
  origin?: string;
  image_url?: string;
  image_file?: string;
  description?: string;
  contenttype: string;
  content: string;
  authorid: string;
  commentcount: number;
  publishdate: string;
  visibility: string;
  likes?: number;
}
