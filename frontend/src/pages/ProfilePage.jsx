import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AnimatePresence, motion } from "motion/react";
import PageTransition from "../components/PageTransition.jsx";
import Card from "../components/ui/Card.jsx";
import Input from "../components/ui/Input.jsx";
import Button from "../components/ui/Button.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import { useToast } from "../components/ui/Toast.jsx";
import { userApi } from "../api/endpoints.js";
import { extractError } from "../api/client.js";
import { Heart, MessageSquare, SendHorizontalIcon, Trash } from "lucide-react";

function formatDate(ts) {
  if (!ts) return "";
  return new Date(ts * 1000).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
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
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [showComments, setShowComments] = useState(false);
  const [comments, setComments] = useState([]);
  const [commentsLoading, setCommentsLoading] = useState(false);
  const [commentsLoaded, setCommentsLoaded] = useState(false);
  const toast = useToast();

  const postId = post._id;
  const [liked, setLiked] = useState(post.liked ?? false);
  const handleLike = async () => {
    const previousLiked = liked;

    setLiked(!liked);

    onUpdate(postId, {
      likes_count: post.likes_count + (liked ? -1 : 1),
    });

    try {
      const { data } = await userApi.like(postId);

      setLiked(data.like);
    } catch (err) {
      setLiked(previousLiked);

      onUpdate(postId, {
        likes_count: post.likes_count,
      });

      toast.error(extractError(err, "Could not update like."));
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

  return (
    <Card className="flex flex-col gap-4">
      <div className="flex aspect-video items-center justify-center rounded-xl bg-white/5 text-slate-500">
        <img
          src={post.file_url}
          alt="Post"
          className="h-full w-full rounded-xl object-cover"
        />
      </div>
      <div className="flex flex-wrap">
        <Button
          variant=""
          onClick={handleLike}
          className="flex items-center"
        >
          <Heart
          size={20}
          fill={liked ? "#fff" : "none"}
          color={liked ? "#fff" : "#fff"}
        />
          <span>{post.likes_count ?? 0}</span>
        </Button>
        <Button variant="" onClick={toggleComments} className="px-3 py-1">
          {showComments ?
              <MessageSquare
          size={20}
        /> : <MessageSquare
          size={20}
        />}
          <span>{post.comments_count ?? 0}</span>
        </Button>
        <Button
          variant="danger"
          loading={deleteLoading}
          onClick={handleDelete}
          className="ml-auto px-3 py-1.5 cursor-pointer"
        >
          <Trash size={15} />
        </Button>
      </div>

      <div>
        <p className="text-slate-100">{post.caption}</p>
        <p className="mt-1 text-xs text-slate-500">{formatDate(post.created_at)}</p>
      </div>

      <form onSubmit={handleComment}>
        <div className="flex gap-2">
          <Input
            as="textarea"
            rows={1}
            placeholder="Write a comment..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            className="flex-1 resize-none"
          />

          <Button
            type="submit"
            loading={commentLoading}
            className="self-end cursor-pointer"
          >
            <SendHorizontalIcon size={20} />
          </Button>
        </div>
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
