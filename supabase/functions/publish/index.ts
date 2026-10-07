// Edge Function "publish" — chamada pelo /admin/ ao publicar, atualizar ou
// despublicar um post. Confere que quem chamou é o dono do blog e dispara o
// workflow "Publicar blog" no GitHub, que regenera o site a partir do banco.
//
// Segredo necessário (Supabase → Edge Functions → Secrets):
//   GH_DISPATCH_TOKEN  token fine-grained do GitHub, apenas o repositório
//                      jpmarson/jpmarson.com.br, permissão "Actions: Read and write".

import { createClient } from "jsr:@supabase/supabase-js@2";

const OWNER_EMAIL = "jpmarson@gmail.com";
const REPO = "jpmarson/jpmarson.com.br";
const WORKFLOW = "blog.yml";
const ALLOWED_ORIGINS = ["https://jpmarson.com.br", "https://www.jpmarson.com.br"];

function cors(origin: string | null) {
  const allow = origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
}

// Chave pública do projeto: a nova (publishable) ou a antiga (anon), o que existir.
function publicKey(): string {
  try {
    const keys = JSON.parse(Deno.env.get("SUPABASE_PUBLISHABLE_KEYS") ?? "{}");
    const first = Object.values(keys)[0];
    if (typeof first === "string" && first) return first;
  } catch (_) { /* segue para a chave antiga */ }
  return Deno.env.get("SUPABASE_ANON_KEY") ?? "";
}

function json(status: number, body: unknown, origin: string | null) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors(origin), "Content-Type": "application/json" },
  });
}

Deno.serve(async (req) => {
  const origin = req.headers.get("Origin");
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(origin) });
  if (req.method !== "POST") return json(405, { error: "Método não permitido" }, origin);

  // 1. Quem está chamando? (o token do usuário é validado no servidor de Auth)
  const authHeader = req.headers.get("Authorization") ?? "";
  const jwt = authHeader.replace(/^Bearer\s+/i, "");
  if (!jwt) return json(401, { error: "Faça login no painel" }, origin);
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, publicKey());
  const { data: { user }, error } = await supabase.auth.getUser(jwt);
  if (error || !user || user.email !== OWNER_EMAIL) {
    return json(403, { error: "Acesso negado" }, origin);
  }

  // 2. Dispara o workflow no GitHub
  const token = Deno.env.get("GH_DISPATCH_TOKEN");
  if (!token) {
    return json(500, { error: "Segredo GH_DISPATCH_TOKEN não configurado no Supabase" }, origin);
  }
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}/dispatches`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "jpmarson-blog-publish",
      },
      body: JSON.stringify({ ref: "main" }),
    },
  );

  if (res.status !== 204) {
    const detail = await res.text();
    console.error("GitHub dispatch falhou", res.status, detail);
    return json(502, { error: "GitHub recusou o disparo", status: res.status, detail }, origin);
  }

  return json(200, {
    ok: true,
    actions: `https://github.com/${REPO}/actions/workflows/${WORKFLOW}`,
  }, origin);
});
