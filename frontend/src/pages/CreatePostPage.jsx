import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "motion/react";
import PageTransition from "../components/PageTransition.jsx";
import Card from "../components/ui/Card.jsx";
import Input from "../components/ui/Input.jsx";
import Button from "../components/ui/Button.jsx";
import { useToast } from "../components/ui/Toast.jsx";
import { userApi } from "../api/endpoints.js";
import { extractError } from "../api/client.js";

export default function CreatePostPage() {
  const [caption, setCaption] = useState("");
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);
  const navigate = useNavigate();
  const toast = useToast();

  const onFile = (selected) => {
    if (!selected) return;
    setFile(selected);
    if (selected.type.startsWith("image/")) {
      setPreview(URL.createObjectURL(selected));
    } else {
      setPreview(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      toast.error("Please choose a file to upload.");
      return;
    }
    setLoading(true);
    try {
      await userApi.createPost(caption, file);
      toast.success("Post uploaded! View it on your profile.");
      setCaption("");
      setFile(null);
      setPreview(null);
      if (inputRef.current) inputRef.current.value = "";
      navigate("/app/profile");
    } catch (err) {
      toast.error(extractError(err, "Could not upload post."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageTransition>
      <div className="mx-auto max-w-xl">
        <Card>
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <label
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                onFile(e.dataTransfer.files?.[0]);
              }}
              className="group relative flex min-h-44 cursor-pointer flex-col items-center justify-center gap-2 overflow-hidden rounded-2xl border-2 border-dashed border-white/15 bg-white/5 p-4 text-center transition hover:border-brand/50 hover:bg-white/10"
            >
              <input
                ref={inputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={(e) => onFile(e.target.files?.[0])}
              />
              <AnimatePresence mode="wait">
                {preview ? (
                  <motion.img
                    key="preview"
                    src={preview}
                    alt="preview"
                    initial={{ opacity: 0, scale: 0.96 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0 }}
                    className="max-h-64 w-full rounded-xl object-contain"
                  />
                ) : (
                  <motion.div
                    key="prompt"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="flex flex-col items-center gap-1 text-slate-400"
                  >
                    <span className="text-3xl">+</span>
                    <span className="text-sm font-medium">
                      Click or drag an image here
                    </span>
                    {file && (
                      <span className="text-xs text-slate-500">{file.name}</span>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </label>

            <Input
              as="textarea"
              rows={3}
              placeholder="Add a caption . . ."
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
            />

            <Button type="submit" loading={loading} className="w-full">
              Upload post
            </Button>
          </form>
        </Card>
      </div>
    </PageTransition>
  );
}
