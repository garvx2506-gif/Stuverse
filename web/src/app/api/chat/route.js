import { GoogleGenerativeAI } from "@google/generative-ai";

export async function POST(req) {
  try {
    const { messages, message, file, level = "College", subject = "All subjects" } = await req.json();

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      return new Response(JSON.stringify({ error: "GEMINI_API_KEY is not configured." }), {
        status: 500,
        headers: { "Content-Type": "application/json" },
      });
    }

    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: "gemini-3.8-flash",
    });

    const subjectText = subject === "All subjects" ? "any subject" : subject;
    const systemInstruction = `You are Stuverse AI, a friendly, encouraging, and highly knowledgeable personal AI teacher.
Student's level: ${level}. Subject: ${subjectText}.

LANGUAGE RULE (critical):
- By default, reply in clear, simple English.
- If the student writes in Hinglish (a mix of Hindi and English), mirror their style and reply in Hinglish too, using 'tum' to address them.
- If the student writes in pure Hindi, reply in Hindi.
- Always match the language the student is using.

Teaching Rules:
1. Use clear, simple, and easy-to-understand language.
2. First explain the core concept, then give a practical real-life example.
3. If the student uploaded a photo, PDF, or document:
   - Solve the problem step by step.
   - Highlight formulas and key steps in bold or code blocks.
   - Give a tip to avoid common exam mistakes.
4. Maintain difficulty appropriate for the student's level (${level}).
5. At the end, ask a short follow-up question to check the student's understanding.`;

    const contents = [];

    if (messages && Array.isArray(messages)) {
      for (const m of messages) {
        contents.push({
          role: m.role === "user" ? "user" : "model",
          parts: [{ text: m.text }],
        });
      }
    }

    const currentParts = [];
    if (file && file.data && file.mimeType) {
      currentParts.push({
        inlineData: {
          data: file.data.replace(/^data:[^;]+;base64,/, ""),
          mimeType: file.mimeType,
        },
      });
    }

    currentParts.push({
      text: `${systemInstruction}\n\nStudent Question: ${message || "Please solve and explain this attached document/photo step by step."}`,
    });

    contents.push({
      role: "user",
      parts: currentParts,
    });

    const result = await model.generateContentStream({ contents });

    const encoder = new TextEncoder();
    const stream = new ReadableStream({
      async start(controller) {
        try {
          for await (const chunk of result.stream) {
            const chunkText = chunk.text();
            if (chunkText) {
              controller.enqueue(encoder.encode(chunkText));
            }
          }
          controller.close();
        } catch (err) {
          controller.error(err);
        }
      },
    });

    return new Response(stream, {
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Transfer-Encoding": "chunked",
      },
    });
  } catch (error) {
    console.error("Chat API error:", error);
    return new Response(JSON.stringify({ error: error.message || "An error occurred with Gemini." }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
