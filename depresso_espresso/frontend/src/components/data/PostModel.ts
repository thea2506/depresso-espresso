export interface PostModel {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  author: any;
  title?: string;
  id: string;
  source?: string;
  origin?: string;
  image_file?: string;
  description: string;
  contenttype: string;
  content: string;
<<<<<<< HEAD
  count: number;
  published: string;
=======
  authorid: string;
  commentcount: number;
  sharecount: number;
  publishdate: string;
>>>>>>> 2e4b932bf163ceb21552df24c9597bde6bd64de1
  visibility: string;
  likes?: number;
}
