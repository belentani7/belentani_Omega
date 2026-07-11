import { convertToModelMessages, createUIMessageStreamResponse, streamText, toUIMessageStream, type UIMessage } from "ai";
import { JUDAS_CONTEXT } from "@/lib/judas-context";

export const maxDuration = 60;

export async function POST(request: Request) {
  const body = await request.json().catch(() => null) as { messages?: UIMessage[]; mode?: string } | null;
  if (!body?.messages || !Array.isArray(body.messages) || body.messages.length > 40) {
    return Response.json({ error: "Invalid transmission" }, { status: 400 });
  }
  const mode = typeof body.mode === "string" ? body.mode.slice(0, 40) : "CORE";
  const result = streamText({
    model: "google/gemini-3.5-flash",
    instructions: `${JUDAS_CONTEXT}\nModo activo: ${mode}. Mantén respuestas claras, de máximo 500 palabras salvo petición explícita.`,
    messages: await convertToModelMessages(body.messages),
  });
  return createUIMessageStreamResponse({ stream: toUIMessageStream({ stream: result.stream }) });
}
