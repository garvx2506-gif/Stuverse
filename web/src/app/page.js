"use client";

import { marked } from "marked";
import katex from "katex";

import { useState, useEffect, useRef } from "react";
import {
  Paperclip,
  ArrowUp,
  Plus,
  Trash2,
  Menu,
  X,
  FileText,
  Download,
  GraduationCap,
  Sparkles,
  BookOpen,
  Camera,
  Layers,
} from "lucide-react";

const LEVELS = [
  "College",
  "Class 11-12",
  "Class 9-10",
  "Class 6-8",
  "Competitive Exams (JEE / NEET / UPSC / CUET)",
];

const SUBJECTS = [
  "All subjects",
  "Maths",
  "Physics",
  "Chemistry",
  "Biology",
  "Computer / Programming",
  "English",
  "History & Civics",
  "General Knowledge",
];

const SUGGESTIONS = [
  { label: "📐 Quadratic formula", prompt: "What is the quadratic formula and how do you solve equations with it step by step?" },
  { label: "⚛️ Newton's laws", prompt: "Explain Newton's three laws of motion with simple, real-life examples." },
  { label: "💻 Python loops", prompt: "How do for loops and while loops work in Python? Give a practical example." },
  { label: "🌿 Photosynthesis", prompt: "Explain the process of photosynthesis step by step in simple language." },
];

// Exact 8-pointed star (Octagram {8/3}) with outer pink tip dots that pulses "in then out, in then out"
function OctagramSymbol({ size = 28, isThinking = false, className = "" }) {
  const points = [
    [50, 6],
    [81.1, 18.9],
    [94, 50],
    [81.1, 81.1],
    [50, 94],
    [18.9, 81.1],
    [6, 50],
    [18.9, 18.9],
  ];

  return (
    <div
      className={`octagram-symbol-wrapper ${isThinking ? "is-thinking" : ""} ${className}`}
      style={{
        width: size,
        height: size,
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
      }}
    >
      {/* Outer cosmic ripple ring when thinking */}
      {isThinking && <div className="octagram-ripple-ring" />}

      <svg
        viewBox="0 0 100 100"
        width={size}
        height={size}
        className={`octagram-svg ${isThinking ? "pulse-in-out" : ""}`}
        style={{ overflow: "visible" }}
      >
        {isThinking && (
          <circle
            cx="50"
            cy="50"
            r="46"
            fill="none"
            stroke="rgba(244, 63, 94, 0.35)"
            strokeWidth="1.5"
            strokeDasharray="4 6"
            className="octagram-halo-spin"
          />
        )}

        {/* 8/3 Octagram Star Path */}
        <path
          d="M 50 6 L 81.1 81.1 L 6 50 L 81.1 18.9 L 50 94 L 18.9 18.9 L 94 50 L 18.9 81.1 Z"
          fill={isThinking ? "rgba(244, 63, 94, 0.12)" : "rgba(236, 72, 153, 0.08)"}
          stroke="#f43f5e"
          strokeWidth="2.8"
          strokeLinejoin="round"
          strokeLinecap="round"
          className="octagram-path"
        />

        {/* Inner geometric diamond cross */}
        <polygon
          points="50,22 78,50 50,78 22,50"
          fill="none"
          stroke="rgba(236, 72, 153, 0.55)"
          strokeWidth="1.5"
          className="octagram-inner-ring"
        />

        {/* 8 Pink circular dots at the outer tips (identical to user screenshot) */}
        {points.map(([px, py], idx) => (
          <circle
            key={idx}
            cx={px}
            cy={py}
            r="3.8"
            fill="#f43f5e"
            stroke="#ffffff"
            strokeWidth="1.2"
            className="octagram-tip-dot"
          />
        ))}

        {/* Central glowing bindu dot */}
        <circle cx="50" cy="50" r="3.2" fill="#ffffff" />
      </svg>
    </div>
  );
}


// Artistic Dolphin with a glowing Blue Paintbrush Symbol
function DolphinBrushSymbol({ size = 46, className = "" }) {
  return (
    <div
      className={`dolphin-brush-wrapper ${className}`}
      style={{
        width: size,
        height: size,
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        flexShrink: 0,
      }}
    >
      <svg
        viewBox="0 0 100 100"
        width={size}
        height={size}
        style={{ overflow: "visible" }}
      >
        <defs>
          {/* Blue Paint Glow Gradient */}
          <linearGradient id="blueBrushPaint" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#38bdf8" />
            <stop offset="50%" stopColor="#0ea5e9" />
            <stop offset="100%" stopColor="#0284c7" />
          </linearGradient>

          {/* Dolphin Body Gradient */}
          <linearGradient id="dolphinBodyGrad" x1="10%" y1="0%" x2="90%" y2="100%">
            <stop offset="0%" stopColor="#f0f9ff" />
            <stop offset="35%" stopColor="#7dd3fc" />
            <stop offset="100%" stopColor="#0369a1" />
          </linearGradient>

          {/* Belly Gradient */}
          <linearGradient id="dolphinBellyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.95" />
            <stop offset="100%" stopColor="#bae6fd" stopOpacity="0.65" />
          </linearGradient>

          {/* Brush Handle Gradient */}
          <linearGradient id="woodHandleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#fbbf24" />
            <stop offset="50%" stopColor="#d97706" />
            <stop offset="100%" stopColor="#78350f" />
          </linearGradient>
        </defs>

        {/* Dynamic Glowing Blue Paint Splash Wave */}
        <path
          d="M 12 78 C 30 89, 66 86, 92 68 C 76 80, 42 86, 18 80 Z"
          fill="url(#blueBrushPaint)"
          filter="drop-shadow(0 0 10px rgba(56, 189, 248, 0.85))"
        />
        <path
          d="M 20 74 C 38 82, 65 79, 88 65"
          fill="none"
          stroke="#a5f3fc"
          strokeWidth="1.8"
          strokeLinecap="round"
          opacity="0.85"
        />

        {/* Leaping Dolphin Body */}
        <path
          d="M 26 63 C 20 53, 23 37, 39 26 C 55 16, 75 22, 85 36 C 89 42, 89 48, 84 50 C 78 52, 70 42, 58 40 C 44 38, 31 51, 26 63 Z"
          fill="url(#dolphinBodyGrad)"
          filter="drop-shadow(0 0 5px rgba(56, 189, 248, 0.4))"
        />

        {/* Dolphin Underbelly */}
        <path
          d="M 30 59 C 35 48, 46 41, 58 41 C 67 41, 74 46, 81 48 C 76 52, 65 52, 54 53 C 42 54, 34 57, 30 59 Z"
          fill="url(#dolphinBellyGrad)"
        />

        {/* Dolphin Snout */}
        <path
          d="M 85 36 C 92 37, 96 39, 95 43 C 94 46, 88 47, 83 45 Z"
          fill="#38bdf8"
        />

        {/* Dolphin Eye with twinkle */}
        <circle cx="78" cy="34" r="2.2" fill="#0f172a" />
        <circle cx="78.8" cy="33.4" r="0.9" fill="#ffffff" />

        {/* Dorsal Fin */}
        <path
          d="M 52 23 C 54 13, 61 11, 66 16 C 62 20, 60 23, 58 24 Z"
          fill="#0284c7"
        />

        {/* Pectoral Flipper */}
        <path
          d="M 57 46 C 62 55, 68 60, 64 62 C 60 63, 56 56, 53 48 Z"
          fill="#0369a1"
        />

        {/* Tail Fluke */}
        <path
          d="M 26 63 C 22 67, 16 71, 10 69 C 12 65, 17 64, 19 60 C 15 58, 9 55, 10 50 C 16 53, 21 57, 26 63 Z"
          fill="#0284c7"
        />

        {/* Artist's Paint Brush with Celestial Blue Paint */}
        {/* Wooden Handle */}
        <path
          d="M 74 48 L 88 64 L 85 66 L 71 50 Z"
          fill="url(#woodHandleGrad)"
        />
        {/* Silver Ferrule */}
        <path
          d="M 87 63 L 90 67 L 88 68 L 85 65 Z"
          fill="#f1f5f9"
        />
        {/* Blue Paint Bristles */}
        <path
          d="M 89 66 C 94 71, 96 76, 92 78 C 88 78, 87 73, 86 68 Z"
          fill="url(#blueBrushPaint)"
          filter="drop-shadow(0 0 8px rgba(56, 189, 248, 1))"
        />

        {/* Glowing Paint Droplets & Sparkles */}
        <circle cx="94" cy="80" r="2" fill="#38bdf8" filter="drop-shadow(0 0 4px #38bdf8)" />
        <circle cx="89" cy="84" r="1.4" fill="#67e8f9" />
        <circle cx="82" cy="83" r="1.2" fill="#bae6fd" />
      </svg>
    </div>
  );
}



// Configure marked for clean GFM markdown
marked.setOptions({
  breaks: true,
  gfm: true,
});

function renderMarkdownWithMath(rawText) {
  if (!rawText) return "";

  // 1. Process block math: $$ formula $$
  let processed = rawText.replace(/\$\$([\s\S]*?)\$\$/g, (match, formula) => {
    try {
      return `<div class="katex-display-block">${katex.renderToString(formula.trim(), { displayMode: true, throwOnError: false })}</div>`;
    } catch {
      return match;
    }
  });

  // 2. Process inline math: $ formula $
  processed = processed.replace(/(?<!\\|\$)\$([^\$\n]+?)\$(?!\$)/g, (match, formula) => {
    try {
      return katex.renderToString(formula.trim(), { displayMode: false, throwOnError: false });
    } catch {
      return match;
    }
  });

  // 3. Render markdown to clean HTML
  try {
    return marked.parse(processed);
  } catch {
    return rawText;
  }
}

export default function Home() {
  const [chats, setChats] = useState({});
  const [currentChatId, setCurrentChatId] = useState(null);
  const [level, setLevel] = useState("College");
  const [subject, setSubject] = useState("All subjects");
  const [input, setInput] = useState("");
  const [attachedFile, setAttachedFile] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [streamingText, setStreamingText] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const [greeting, setGreeting] = useState("Night hustle?");

  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);
  const canvasRef = useRef(null);

  // Load chats from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem("stuverse_chats");
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Object.keys(parsed).length > 0) {
          setChats(parsed);
          setCurrentChatId(Object.keys(parsed)[0]);
          return;
        }
      }
    } catch (e) {
      console.error(e);
    }
    initNewChat();
  }, []);

  // Save chats to localStorage
  useEffect(() => {
    if (Object.keys(chats).length > 0) {
      try {
        localStorage.setItem("stuverse_chats", JSON.stringify(chats));
      } catch (e) {
        console.error(e);
      }
    }
  }, [chats]);

  // Compute time-based greeting on client mount
  useEffect(() => {
    const hour = new Date().getHours();
    if (hour >= 21 || hour < 5) setGreeting("Night hustle?");
    else if (hour >= 5 && hour < 12) setGreeting("Morning study?");
    else if (hour >= 12 && hour < 17) setGreeting("Afternoon focus?");
    else setGreeting("Evening hustle?");
  }, []);

  // Auto-scroll chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chats, streamingText]);

  // 3D Parallax tilt on mouse move
  useEffect(() => {
    const handleMouseMove = (e) => {
      const cx = window.innerWidth / 2;
      const cy = window.innerHeight / 2;
      const dx = (e.clientX - cx) / cx;
      const dy = (e.clientY - cy) / cy;
      setTilt({ x: dy * -10, y: dx * 10 });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  // Persistent Twinkling Cosmic Stars + Cursor Trail Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // 180 persistent cosmic background stars
    const starCount = 180;
    const stars = [];
    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.6 + 0.4,
        alpha: Math.random() * 0.75 + 0.25,
        twinkleSpeed: Math.random() * 0.025 + 0.008,
        twinklePhase: Math.random() * Math.PI * 2,
        vx: (Math.random() - 0.5) * 0.12,
        vy: (Math.random() - 0.5) * 0.12,
        color:
          Math.random() > 0.88
            ? "rgba(244, 63, 94," // pink star
            : Math.random() > 0.75
            ? "rgba(56, 189, 248," // cyan star
            : Math.random() > 0.6
            ? "rgba(192, 132, 252," // lavender star
            : "rgba(255, 255, 255,", // pure white star
      });
    }

    const onResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", onResize);

    const particles = [];
    const addParticle = (x, y) => {
      if (particles.length > 45) particles.shift();
      const isCyan = Math.random() > 0.5;
      particles.push({
        x: x + (Math.random() - 0.5) * 8,
        y: y + (Math.random() - 0.5) * 8,
        vx: (Math.random() - 0.5) * 1.2,
        vy: (Math.random() - 0.5) * 1.2 - 0.2,
        size: Math.random() * 2.2 + 1,
        color: isCyan ? "rgba(56, 189, 248," : "rgba(236, 72, 153,",
        life: 1.0,
        decay: Math.random() * 0.02 + 0.015,
      });
    };

    const onMouseMove = (e) => {
      addParticle(e.clientX, e.clientY);
    };
    window.addEventListener("mousemove", onMouseMove);

    let animId;
    let t = 0;
    const render = () => {
      ctx.clearRect(0, 0, width, height);
      t += 0.015;

      // Render persistent twinkling background stars
      for (let i = 0; i < stars.length; i++) {
        const s = stars[i];
        s.x += s.vx;
        s.y += s.vy;
        if (s.x < 0) s.x = width;
        if (s.x > width) s.x = 0;
        if (s.y < 0) s.y = height;
        if (s.y > height) s.y = 0;

        const currentAlpha =
          s.alpha * (0.55 + 0.45 * Math.sin(t * s.twinkleSpeed * 100 + s.twinklePhase));

        ctx.save();
        ctx.fillStyle = s.color + currentAlpha + ")";
        if (s.radius > 1.2) {
          ctx.shadowBlur = 5;
          ctx.shadowColor = s.color + "0.75)";
        }
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      // Render cursor particle trail
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life -= p.decay;
        if (p.life <= 0) {
          particles.splice(i, 1);
          continue;
        }
        ctx.save();
        ctx.fillStyle = p.color + p.life * 0.85 + ")";
        ctx.shadowBlur = 6;
        ctx.shadowColor = p.color + "1)";
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
      animId = requestAnimationFrame(render);
    };
    render();

    return () => {
      window.removeEventListener("resize", onResize);
      window.removeEventListener("mousemove", onMouseMove);
      cancelAnimationFrame(animId);
    };
  }, []);

  const initNewChat = () => {
    const id = "chat_" + Date.now();
    const newChat = {
      id,
      title: "New Chat",
      createdAt: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }),
      level,
      subject,
      messages: [],
    };
    setChats((prev) => ({ [id]: newChat, ...prev }));
    setCurrentChatId(id);
    setStreamingText("");
    setAttachedFile(null);
    setInput("");
    setSidebarOpen(false);
  };

  const currentChat = (currentChatId && chats[currentChatId]) || {
    messages: [],
    title: "New Chat",
  };

  // Handle file selection from paperclip button
  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setAttachedFile({
        name: file.name,
        mimeType: file.type || "application/octet-stream",
        sizeKb: Math.round(file.size / 1024),
        data: reader.result, // base64 data url
      });
    };
    reader.readAsDataURL(file);
    e.target.value = "";
  };

  // Send message to Next.js API route with streaming
  const handleSend = async (customPrompt) => {
    const promptToSend = (customPrompt || input).trim();
    if (!promptToSend && !attachedFile) return;
    if (isGenerating) return;

    const currentMsgText = promptToSend || `Please analyze and solve the attached file (${attachedFile?.name}) step by step.`;

    const userMsg = {
      role: "user",
      text: currentMsgText,
      fileName: attachedFile ? attachedFile.name : null,
    };

    const updatedMessages = [...currentChat.messages, userMsg];

    // Update state with user message immediately
    setChats((prev) => ({
      ...prev,
      [currentChatId]: {
        ...prev[currentChatId],
        title: prev[currentChatId].messages.length === 0 ? currentMsgText.slice(0, 26) + "..." : prev[currentChatId].title,
        messages: updatedMessages,
      },
    }));

    setInput("");
    const fileToSend = attachedFile;
    setAttachedFile(null);
    setIsGenerating(true);
    setStreamingText("");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: currentChat.messages,
          message: currentMsgText,
          file: fileToSend,
          level,
          subject,
        }),
      });

      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let fullAssistantText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        fullAssistantText += chunk;
        setStreamingText(fullAssistantText);
      }

      // Finalize assistant message
      setChats((prev) => ({
        ...prev,
        [currentChatId]: {
          ...prev[currentChatId],
          messages: [...updatedMessages, { role: "assistant", text: fullAssistantText }],
        },
      }));
    } catch (err) {
      console.error("Chat error:", err);
      setChats((prev) => ({
        ...prev,
        [currentChatId]: {
          ...prev[currentChatId],
          messages: [
            ...updatedMessages,
            { role: "assistant", text: "Sorry, I encountered a temporary connection error. Please try asking again." },
          ],
        },
      }));
    } finally {
      setIsGenerating(false);
      setStreamingText("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const deleteChat = (id, e) => {
    e.stopPropagation();
    const updated = { ...chats };
    delete updated[id];
    setChats(updated);
    if (currentChatId === id) {
      const remainingIds = Object.keys(updated);
      if (remainingIds.length > 0) {
        setCurrentChatId(remainingIds[0]);
      } else {
        initNewChat();
      }
    }
  };

  const downloadNotes = () => {
    if (!currentChat.messages.length) return;
    let md = `# 🎓 Stuverse AI Study Notes\n`;
    md += `**Topic**: ${currentChat.title}\n`;
    md += `**Level**: ${currentChat.level || level} | **Subject**: ${currentChat.subject || subject}\n\n---\n\n`;
    for (const m of currentChat.messages) {
      const speaker = m.role === "user" ? "🧑‍🎓 Student" : "🤖 Stuverse AI";
      const fileInfo = m.fileName ? ` *(Attached: ${m.fileName})*` : "";
      md += `### ${speaker}${fileInfo}:\n${m.text}\n\n`;
    }
    const blob = new Blob([md], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Stuverse_Notes_${currentChat.title.replace(/[^a-zA-Z0-9]/g, "_")}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <main style={{ minHeight: "100vh", position: "relative" }}>
      {/* Background canvas for stardust particles */}
      <canvas ref={canvasRef} style={{ position: "fixed", top: 0, left: 0, pointerEvents: "none", zIndex: 0 }} />

      {/* Background Starfield & Shooting Stars */}
      <div className="stars-layer-1" />
      <div className="stars-layer-2" />
      <div className="shooting-star-1" />
      <div className="shooting-star-2" />

      {/* Top Navigation */}
      <header className="top-nav">
        <button className="sidebar-toggle-btn" onClick={() => setSidebarOpen(true)} title="Open Sidebar">
          <Menu size={22} />
        </button>

        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <span style={{ fontSize: "1.15rem", fontWeight: 700, fontFamily: "var(--font-outfit)", letterSpacing: "-0.3px" }}>
            Stuverse AI
          </span>
          <span style={{ fontSize: "0.75rem", background: "rgba(139, 92, 246, 0.2)", color: "#c084fc", padding: "2px 8px", borderRadius: "10px", border: "1px solid rgba(139, 92, 246, 0.3)" }}>
            v3.5 Web
          </span>
        </div>

        <button className="sidebar-toggle-btn" onClick={initNewChat} title="New Chat">
          <Plus size={20} />
        </button>
      </header>

      {/* Sidebar Drawer */}
      {sidebarOpen && <div className="sidebar-backdrop" onClick={() => setSidebarOpen(false)} />}
      <aside className={`sidebar-drawer ${sidebarOpen ? "open" : ""}`}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
            <GraduationCap size={22} color="#c084fc" />
            <span style={{ fontWeight: 700, fontFamily: "var(--font-outfit)" }}>Stuverse AI</span>
          </div>
          <button className="sidebar-toggle-btn" onClick={() => setSidebarOpen(false)}>
            <X size={20} />
          </button>
        </div>

        <button className="new-chat-btn" onClick={initNewChat}>
          <Plus size={18} /> New Chat
        </button>

        {/* Study Level & Subject Selectors */}
        <div style={{ marginTop: "1.2rem" }}>
          <label style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>Your Grade / Level</label>
          <select className="dropdown-select" value={level} onChange={(e) => setLevel(e.target.value)}>
            {LEVELS.map((lvl) => (
              <option key={lvl} value={lvl}>{lvl}</option>
            ))}
          </select>
        </div>

        <div style={{ marginTop: "0.8rem" }}>
          <label style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>Subject</label>
          <select className="dropdown-select" value={subject} onChange={(e) => setSubject(e.target.value)}>
            {SUBJECTS.map((sub) => (
              <option key={sub} value={sub}>{sub}</option>
            ))}
          </select>
        </div>

        <div style={{ marginTop: "1.2rem", fontSize: "0.8rem", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.5px" }}>
          Recent Chats
        </div>

        <div className="history-list">
          {Object.values(chats).map((c) => (
            <div
              key={c.id}
              className={`history-item ${c.id === currentChatId ? "active" : ""}`}
              onClick={() => {
                setCurrentChatId(c.id);
                setSidebarOpen(false);
              }}
            >
              <div style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", flex: 1 }}>
                {c.title || "Chat"}
              </div>
              <button
                style={{ background: "transparent", border: "none", color: "#64748b", cursor: "pointer", padding: "2px 4px" }}
                onClick={(e) => deleteChat(c.id, e)}
                title="Delete Chat"
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))}
        </div>

        {currentChat.messages.length > 0 && (
          <button
            onClick={downloadNotes}
            style={{
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid rgba(255, 255, 255, 0.1)",
              borderRadius: "8px",
              padding: "0.6rem",
              color: "#e2e8f0",
              fontSize: "0.85rem",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "0.4rem",
              cursor: "pointer",
            }}
          >
            <Download size={16} /> Download Notes (.md)
          </button>
        )}
      </aside>

      {/* Main Content Area */}
      <div className="chat-container">
        {/* Centered Front & Mid Initial View (When no messages exist yet) */}
        {currentChat.messages.length === 0 && !streamingText && (
          <div className="center-hero-view">
            <div className="center-hero-badge">
              <span>Free plan &bull; Gemini 2.5 Flash</span>
            </div>

            {/* Greeting with Dolphin + Blue Brush */}
            <div className="greeting-container">
              <DolphinBrushSymbol size={52} />
              <h1 className="greeting-heading">{greeting}</h1>
            </div>

            {/* Center Front & Mid Typing Box (Claude-style) */}
            <div className="center-input-card">
              <textarea
                ref={textareaRef}
                className="center-input-textarea"
                placeholder="How can I help you today?"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                rows={3}
              />

              {attachedFile && (
                <div className="attached-file-chip">
                  <Paperclip size={13} />
                  <span className="file-name-trim">{attachedFile.name}</span>
                  <button className="file-remove-x" onClick={() => setAttachedFile(null)}>×</button>
                </div>
              )}

              <div className="center-card-bottom-row">
                <div className="center-card-tools-left">
                  <button
                    className="icon-attach-btn"
                    title="Attach notes / photos / PDF"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <Paperclip size={17} />
                  </button>
                  <button className="mode-pill-active">Chat</button>
                  <button
                    className="mode-pill-subtle"
                    onClick={() => setSidebarOpen(true)}
                    title="Change level or subject"
                  >
                    {level} &bull; {subject}
                  </button>
                </div>

                <div className="center-card-tools-right">
                  <span className="model-chip-tag">Sonnet-speed &bull; 2.5 Flash</span>
                  <button
                    className="center-submit-arrow"
                    disabled={!input.trim() && !attachedFile}
                    onClick={() => handleSend()}
                    title="Send message"
                  >
                    <ArrowUp size={17} />
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
        

        {/* Existing Messages (PURE TEXT ONLY, ZERO BOXES) */}
        {currentChat.messages.map((msg, i) => (
          <div key={i} className={`message-row ${msg.role}`}>
            <div className="message-content-wrapper">
              <div className={`avatar ${msg.role}`}>
                {msg.role === "user" ? (
                  "🧑‍🎓"
                ) : (
                  <OctagramSymbol size={26} isThinking={false} />
                )}
              </div>
              <div className="message-text">
                {msg.fileName && (
                  <div>
                    <span className="attached-badge">
                      <FileText size={12} /> {msg.fileName}
                    </span>
                  </div>
                )}
                <div
                  className="markdown-body"
                  dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(msg.text) }}
                />
              </div>
            </div>
          </div>
        ))}

        {/* Thinking Indicator (Octagram Star on left corner going in then out) */}
        {isGenerating && !streamingText && (
          <div className="message-row assistant thinking-active-row">
            <div className="message-content-wrapper">
              <div className="avatar assistant thinking-corner-symbol">
                <OctagramSymbol size={30} isThinking={true} />
              </div>
              <div className="message-text">
                <div className="thinking-corner-box">
                  <span className="thinking-text">Thinking...</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Live Streaming Message */}
        {streamingText && (
          <div className="message-row assistant">
            <div className="message-content-wrapper">
              <div className="avatar assistant">
                <OctagramSymbol size={28} isThinking={true} />
              </div>
              <div className="message-text">
                <div className="streaming-content-wrapper">
                  <div
                    className="markdown-body streaming-active"
                    dangerouslySetInnerHTML={{ __html: renderMarkdownWithMath(streamingText) }}
                  />
                  <span className="typing-cursor" />
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Classical Floating Pill Typing Bar (ONLY THE BAR, NO OUTER BOXES) */}
      {(currentChat.messages.length > 0 || streamingText) && (
      <div className="typing-bar-sticky-container">
        <div className="typing-bar-capsule">
          {/* Hidden File Input */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*,application/pdf,text/*"
            style={{ display: "none" }}
          />

          {/* Paperclip Button inside bar */}
          <button
            type="button"
            className="attach-btn"
            onClick={() => fileInputRef.current?.click()}
            title="Attach textbook question photo or notes PDF"
          >
            <Paperclip size={19} />
          </button>

          {/* Attached File Preview Chip */}
          {attachedFile && (
            <div className="file-preview-chip">
              <FileText size={13} />
              <span>{attachedFile.name}</span>
              <button className="clear-file-btn" onClick={() => setAttachedFile(null)}>
                <X size={13} />
              </button>
            </div>
          )}

          {/* Text Input */}
          <textarea
            ref={textareaRef}
            className="input-area"
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={attachedFile ? `Ask about "${attachedFile.name}"...` : "Type your doubt or attach textbook photos / notes..."}
          />

          {/* Send Button */}
          <button
            type="button"
            className="send-btn"
            onClick={() => handleSend()}
            disabled={isGenerating || (!input.trim() && !attachedFile)}
            title="Send"
          >
            <ArrowUp size={18} />
          </button>
        </div>
      </div>
      )}
    </main>
  );
}
