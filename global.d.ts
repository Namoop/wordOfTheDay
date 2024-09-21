interface Document {
  data: {
    name: string;
    posts: Posts;
  };
}
type Post = {
    id: string;
    title: string;
    content: string;
    created: string;
    author: string;
    author_email: string;
};
type Posts = Post[];