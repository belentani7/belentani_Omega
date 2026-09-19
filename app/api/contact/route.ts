import { z } from "zod";

const schema = z.object({
  name: z.string().trim().min(2).max(80),
  email: z.string().email().max(160),
  subject: z.string().trim().min(3).max(120),
  message: z.string().trim().min(20).max(4000),
  website: z.string().max(0),
});

export async function POST(request: Request) {
  const parsed = schema.safeParse(await request.json().catch(() => null));
  if (!parsed.success) return Response.json({ error: "Revisa los campos de la transmisión." }, { status: 400 });
  const webhook = process.env.CONTACT_WEBHOOK_URL;
  if (!webhook) return Response.json({ error: "El canal privado aún no está configurado." }, { status: 503 });
  const response = await fetch(webhook, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ ...parsed.data, website: undefined, source: "judas-era" }),
    signal: AbortSignal.timeout(8000),
  });
  if (!response.ok) return Response.json({ error: "La red no pudo completar la transmisión." }, { status: 502 });
  return Response.json({ accepted: true, configured: true });
}
