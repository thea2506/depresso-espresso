export interface CommentModel {
  id: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  author: any;

  contenttype: string | null;
  comment: string;

  published: string;
  profileImage: string;

  likecount: number;
}
