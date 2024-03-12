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
  count: number;
  published: string;
  visibility: string;
  likes?: number;
  sharecount: number;
}
