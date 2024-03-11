import { AuthorModel } from "./AuthorModel";

export interface PostModel {
  author: AuthorModel;
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
}
