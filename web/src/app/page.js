"use client";

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

  // Stardust cursor particle trail canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const onResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", onResize);

    const particles = [];
    const addParticle = (x, y) => {
      if (particles.length > 60) particles.shift();
      const isCyan = Math.random() > 0.5;
      particles.push({
        x: x + (Math.random() - 0.5) * 10,
        y: y + (Math.random() - 0.5) * 10,
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 1.5 - 0.3,
        size: Math.random() * 2.5 + 1,
        color: isCyan ? "rgba(56, 189, 248," : "rgba(192, 132, 252,",
        life: 1.0,
        decay: Math.random() * 0.02 + 0.015,
      });
    };

    const onMouseMove = (e) => {
      addParticle(e.clientX, e.clientY);
    };
    window.addEventListener("mousemove", onMouseMove);

    let animId;
    const render = () => {
      ctx.clearRect(0, 0, width, height);
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
        {/* Black Hole Header Hero (Shown when no messages) */}
        {currentChat.messages.length === 0 && !streamingText && (
          <div className="blackhole-container">
            <div
              className="blackhole-wrapper"
              style={{
                transform: `perspective(800px) rotateX(${tilt.x}deg) rotateY(${tilt.y}deg)`,
              }}
            >
              <div className="blackhole-glow" />
              <div className="blackhole-accretion" />
              <div className="blackhole-ring-1" />
              <div className="blackhole-ring-2" />
              <div className="blackhole-event-horizon" />
            </div>

            <h1 className="brand-title">Stuverse AI</h1>
            <p className="brand-subtitle">Your Personal AI Teacher &bull; Ask Doubts &bull; Learn with Confidence</p>

            <div className="feature-pills-row">
              <span className="feature-pill">⚡ Instant Solutions</span>
              <span className="feature-pill">📖 Clear Explanations</span>
              <span className="feature-pill">📸 Photo & PDF Doubts</span>
              <span className="feature-pill">🎓 Built for Students</span>
            </div>

            {/* Suggestions Chips */}
            <div className="suggestions-grid">
              {SUGGESTIONS.map((item, idx) => (
                <button key={idx} className="suggestion-chip" onClick={() => handleSend(item.prompt)}>
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Existing Messages (PURE TEXT ONLY, ZERO BOXES) */}
        {currentChat.messages.map((msg, i) => (
          <div key={i} className={`message-row ${msg.role}`}>
            <div className="message-content-wrapper">
              <div className={`avatar ${msg.role}`}>
                {msg.role === "user" ? "🧑‍🎓" : "🤖"}
              </div>
              <div className="message-text">
                {msg.fileName && (
                  <div>
                    <span className="attached-badge">
                      <FileText size={12} /> {msg.fileName}
                    </span>
                  </div>
                )}
                <div className="markdown-body" style={{ whiteSpace: "pre-wrap" }}>
                  {msg.text}
                </div>
              </div>
            </div>
          </div>
        ))}

        {/* Live Streaming Message */}
        {streamingText && (
          <div className="message-row assistant">
            <div className="message-content-wrapper">
              <div className="avatar assistant">🤖</div>
              <div className="message-text">
                <div className="markdown-body" style={{ whiteSpace: "pre-wrap" }}>
                  {streamingText}
                  <span className="typing-cursor" />
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Classical Floating Pill Typing Bar (ONLY THE BAR, NO OUTER BOXES) */}
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
    </main>
  );
}
