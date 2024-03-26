/* eslint-disable @typescript-eslint/no-explicit-any */
export interface PostModel {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  type: string;
  title?: string;
  id: string;

  source?: string;
  origin?: string;
  author: any;

  description: string;
  contentType: string;
  content: string;

  count: number;
  likecount: number;
  sharecount: number;
  comments?: any;

  published: string;
  visibility: string;

  imageFile?: string;
}
