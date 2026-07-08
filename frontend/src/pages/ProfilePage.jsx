import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AnimatePresence, motion } from "motion/react";
import PageTransition from "../components/PageTransition.jsx";
import PageHeader from "../components/PageHeader.jsx";
import Card from "../components/ui/Card.jsx";
import Input from "../components/ui/Input.jsx";
import Button from "../components/ui/Button.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import { useToast } from "../components/ui/Toast.jsx";
import { userApi } from "../api/endpoints.js";
import { extractError } from "../api/client.js";

function formatDate(ts) {
  if (!ts) return "";
  return new Date(ts * 1000).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function Stat({ label, value }) {
  return (
    <div className="text-center">
      <div className="text-xl font-bold text-white">{value ?? 0}</div>
      <div className="text-xs text-slate-400">{label}</div>
    </div>
  );
}

function PostCard({ post, onDelete, onUpdate }) {
  const [comment, setComment] = useState("");
  const [commentLoading, setCommentLoading] = useState(false);
  const [likeLoading, setLikeLoading] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [showComments, setShowComments] = useState(false);
  const [comments, setComments] = useState([]);
  const [commentsLoading, setCommentsLoading] = useState(false);
  const [commentsLoaded, setCommentsLoaded] = useState(false);
  const toast = useToast();

  const postId = post._id;

  const handleLike = async () => {
    setLikeLoading(true);
    try {
      const { data } = await userApi.like(postId);
      toast.success(data?.message || "Done");
      if (typeof data?.like === "boolean") {
        onUpdate(postId, {
          likes_count: post.likes_count + (data.like ? 1 : -1),
        });
      }
    } catch (err) {
      toast.error(extractError(err, "Could not like post."));
    } finally {
      setLikeLoading(false);
    }
  };

  const handleComment = async (e) => {
    e.preventDefault();
    if (!comment.trim()) return;
    setCommentLoading(true);
    try {
      const { data } = await userApi.comment(postId, comment.trim());
      toast.success(data?.message || "Comment added!");
      setComment("");
      onUpdate(postId, { comments_count: (post.comments_count ?? 0) + 1 });
      if (commentsLoaded) {
        const { data: fresh } = await userApi.getComments(postId);
        setComments(Array.isArray(fresh) ? fresh : []);
      }
    } catch (err) {
      toast.error(extractError(err, "Could not add comment."));
    } finally {
      setCommentLoading(false);
    }
  };

  const toggleComments = async () => {
    const next = !showComments;
    setShowComments(next);
    if (next && !commentsLoaded) {
      setCommentsLoading(true);
      try {
        const { data } = await userApi.getComments(postId);
        setComments(Array.isArray(data) ? data : []);
        setCommentsLoaded(true);
      } catch (err) {
        toast.error(extractError(err, "Could not load comments."));
        setShowComments(false);
      } finally {
        setCommentsLoading(false);
      }
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Delete this post? This cannot be undone.")) return;
    setDeleteLoading(true);
    try {
      const { data } = await userApi.deletePost(postId);
      toast.success(data?.message || "Post deleted.");
      onDelete(postId);
    } catch (err) {
      toast.error(extractError(err, "Could not delete post."));
    } finally {
      setDeleteLoading(false);
    }
  };

  const copyId = async () => {
    try {
      await navigator.clipboard.writeText(postId);
      toast.info("Post ID copied.");
    } catch {
      toast.error("Could not copy ID.");
    }
  };

  return (
    <Card className="flex flex-col gap-4">
      <div className="flex aspect-video items-center justify-center rounded-xl bg-white/5 text-slate-500">
        <span className="text-sm">Image preview unavailable</span>
      </div>

      <div>
        <p className="text-slate-100">{post.caption}</p>
        <p className="mt-1 text-xs text-slate-500">{formatDate(post.created_at)}</p>
      </div>

      <div className="flex items-center gap-4 text-sm text-slate-400">
        <span>{post.likes_count ?? 0} likes</span>
        <span>{post.comments_count ?? 0} comments</span>
        <button
          type="button"
          onClick={copyId}
          className="ml-auto font-mono text-[10px] text-slate-600 hover:text-slate-400"
          title="Copy post ID"
        >
          {postId.slice(0, 8)}…
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        <Button variant="ghost" loading={likeLoading} onClick={handleLike} className="px-3 py-1.5">
          Like
        </Button>
        <Button variant="ghost" onClick={toggleComments} className="px-3 py-1.5">
          {showComments ? "Hide comments" : "View comments"}
        </Button>
        <Button
          variant="danger"
          loading={deleteLoading}
          onClick={handleDelete}
          className="ml-auto px-3 py-1.5"
        >
          Delete
        </Button>
      </div>

      <form onSubmit={handleComment} className="flex flex-col gap-2">
        <Input
          as="textarea"
          label="Add a comment"
          rows={2}
          placeholder="Write a comment..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        />
        <Button type="submit" loading={commentLoading} className="w-full sm:w-auto">
          Comment
        </Button>
      </form>

      <AnimatePresence>
        {showComments && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="rounded-xl border border-white/10 bg-white/5 p-3">
              {commentsLoading ? (
                <div className="flex items-center gap-2 py-2 text-sm text-slate-400">
                  <Spinner size={14} /> Loading comments...
                </div>
              ) : comments.length === 0 ? (
                <p className="py-2 text-sm text-slate-500">No comments yet.</p>
              ) : (
                <ul className="flex flex-col gap-3">
                  {comments.map((c) => (
                    <li key={c._id} className="text-sm">
                      <span className="font-medium text-slate-200">
                        @{c.user?.username ?? "unknown"}
                      </span>
                      <span className="text-slate-400"> · {formatDate(c.created_at)}</span>
                      <p className="mt-0.5 text-slate-300">{c.comment}</p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  );
}

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await userApi.getProfile();
      setUser(data.user ?? null);
      const allPosts = Array.isArray(data.posts) ? data.posts : [];
      setPosts(allPosts.filter((p) => !p.is_deleted));
    } catch (err) {
      toast.error(extractError(err, "Could not load profile."));
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    load();
  }, [load]);

  const handleDelete = (postId) => {
    setPosts((prev) => prev.filter((p) => p._id !== postId));
    setUser((u) => (u ? { ...u, posts_count: Math.max(0, (u.posts_count ?? 1) - 1) } : u));
  };

  const handleUpdate = (postId, patch) => {
    setPosts((prev) => prev.map((p) => (p._id === postId ? { ...p, ...patch } : p)));
  };

  return (
    <PageTransition>
      <PageHeader
        title="Your profile"
        description="View your posts, like, comment, and manage your content."
      />

      {loading ? (
        <div className="flex items-center justify-center gap-3 py-20 text-slate-400">
          <Spinner /> Loading profile...
        </div>
      ) : (
        <>
          {user && (
            <Card className="mb-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-white">{user.name}</h2>
                  <p className="text-slate-400">@{user.username}</p>
                </div>
                <div className="flex gap-6">
                  <Stat label="Posts" value={user.posts_count} />
                  <Stat label="Followers" value={user.followers_count} />
                  <Stat label="Following" value={user.following_count} />
                </div>
              </div>
            </Card>
          )}

          {posts.length === 0 ? (
            <Card className="py-12 text-center">
              <p className="text-slate-400">You haven&apos;t posted anything yet.</p>
              <Link
                to="/app/create"
                className="mt-4 inline-block text-sm font-medium text-brand-2 hover:underline"
              >
                Create your first post
              </Link>
            </Card>
          ) : (
            <div className="grid gap-6 md:grid-cols-2">
              {posts.map((post) => (
                <PostCard
                  key={post._id}
                  post={post}
                  onDelete={handleDelete}
                  onUpdate={handleUpdate}
                />
              ))}
            </div>
          )}
        </>
      )}
    </PageTransition>
  );
}
