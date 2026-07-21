import client from "./client.js";

export const authApi = {
  login: (username, password) =>
    client.post("/api/auth/login", { username, password }),
  logout: (token) =>
    client.post("/api/auth/logout", null, { params: { token } }),
};

export const userApi = {
  signup: (payload) => client.post("/api/user/signup", payload),
  edit: (payload) => client.patch("/api/user/edit", payload),
  changePassword: (payload) => client.patch("/api/user/change_password", payload),
  deactivate: () => client.patch("/api/user/deactivate"),
  deleteAccount: () => client.patch("/api/user/delete"),
  createPost: (caption, file) => {
    const form = new FormData();
    form.append("caption", caption);
    form.append("post", file);
    return client.post("/api/user/post", form);
  },
  like: (postId) => client.post("/api/user/like", null, { params: { post_id: postId } }),
  comment: (postId, comment) =>
    client.post("/api/user/comment", null, {
      params: { post_id: postId, comment },
    }),
  getProfile: () => client.get("/api/user/profile"),
  whoami: () => client.get("/api/whoami/whoami"),
  getComments: (postId) =>
    client.get("/api/user/comments", { params: { post_id: postId } }),
  deletePost: (postId) =>
    client.patch("/api/user/delete_post", null, { params: { post_id: postId } }),
};

export const adminApi = {
  listUsers: () => client.get("/api/admin/users"),
  undelete: (userId) =>
    client.get("/api/admin/undelete", { params: { user_id: userId } }),
};
