/*
 * Google Analytics 4 de jpmarson.com.br
 *
 * - Consent Mode v2 (modo avançado): o GA carrega com tudo negado e envia só
 *   sinais sem cookies; ao "Aceitar", libera a medição completa. Anúncios: sempre negados.
 * - Aviso de cookies discreto em PT/EN/ES, escolha guardada no navegador.
 * - Não roda no /admin/.
 * - Exclusão das suas visitas: abra jpmarson.com.br/?nao-contar uma vez em cada
 *   navegador. Para voltar a contar: ?contar
 * - Eventos: cv_download, contact_click, company_click, cta_click,
 *   language_change, share, consent_choice.
 */
(function () {
  "use strict";

  var GA_ID = "G-97BMHRZFZ5";
  var KEY_OPTOUT = "jpm-nao-contar";
  var KEY_CONSENT = "jpm-consent";

  // --- utilidades ------------------------------------------------------------
  function store(k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
  function read(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function onReady(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  var TXT = {
    pt: { msg: "Uso o Google Analytics para saber, de forma agregada, quantas pessoas visitam o site e de onde vêm. Posso usar cookies de medição?", yes: "Aceitar", no: "Recusar",
          off: "✓ Este navegador não será contado nas estatísticas do site.", on: "✓ Este navegador voltou a ser contado nas estatísticas do site." },
    en: { msg: "I use Google Analytics to understand, in aggregate, how many people visit this site and where they come from. May I use measurement cookies?", yes: "Accept", no: "Decline",
          off: "✓ This browser will not be counted in the site statistics.", on: "✓ This browser is counted in the site statistics again." },
    es: { msg: "Uso Google Analytics para saber, de forma agregada, cuántas personas visitan el sitio y de dónde vienen. ¿Puedo usar cookies de medición?", yes: "Aceptar", no: "Rechazar",
          off: "✓ Este navegador no se contará en las estadísticas del sitio.", on: "✓ Este navegador vuelve a contarse en las estadísticas del sitio." }
  };
  function lang() {
    var l = (document.documentElement.lang || "pt").slice(0, 2).toLowerCase();
    return TXT[l] ? l : "pt";
  }

  var CSS = ""
    + "#jpm-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:60;max-width:560px;margin:0 auto;"
    + "background:var(--surface,#fff);color:var(--text,#0f172a);border:1px solid var(--border,#e4e9f2);border-radius:14px;"
    + "box-shadow:0 14px 40px rgba(15,23,42,.18);padding:14px 16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;"
    + "font:14px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,sans-serif}"
    + "#jpm-consent p{flex:1 1 260px;margin:0;color:var(--muted,#5b6b83);font-size:.86rem}"
    + "#jpm-consent .b{display:flex;gap:8px}"
    + "#jpm-consent button{font:600 .84rem/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;border-radius:9px;padding:9px 14px;cursor:pointer;"
    + "border:1px solid var(--border,#e4e9f2);background:var(--surface,#fff);color:var(--text,#0f172a)}"
    + "#jpm-consent button.y{background:var(--accent,#0a66ff);border-color:var(--accent,#0a66ff);color:#fff}"
    + "[data-theme='dark'] #jpm-consent button.y{color:#0b1120}"
    + "#jpm-toast{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:61;background:#0f172a;color:#fff;max-width:92vw;"
    + "padding:11px 16px;border-radius:11px;font:14px -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;"
    + "box-shadow:0 10px 30px rgba(0,0,0,.25)}";

  function addCSS() {
    if (document.getElementById("jpm-consent-css")) return;
    var st = document.createElement("style");
    st.id = "jpm-consent-css";
    st.textContent = CSS;
    document.head.appendChild(st);
  }

  function toast(msg) {
    addCSS();
    var t = document.createElement("div");
    t.id = "jpm-toast";
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 5000);
  }

  // --- não medir o painel de escrita -------------------------------------------
  if (location.pathname.indexOf("/admin") === 0) return;

  // --- exclusão das visitas do dono do site ------------------------------------
  var params = new URLSearchParams(location.search);
  var optMsg = null;
  if (params.has("nao-contar")) { store(KEY_OPTOUT, "1"); optMsg = "off"; }
  if (params.has("contar")) { store(KEY_OPTOUT, null); optMsg = "on"; }
  if (optMsg) {
    params.delete("nao-contar");
    params.delete("contar");
    var qs = params.toString();
    history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
    onReady(function () { toast(TXT[lang()][optMsg]); });
  }
  if (read(KEY_OPTOUT) === "1") return;

  // --- Google tag com Consent Mode ---------------------------------------------
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;

  var choice = read(KEY_CONSENT); // "granted" | "denied" | null
  gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: choice === "granted" ? "granted" : "denied",
    wait_for_update: 500
  });
  gtag("js", new Date());
  gtag("config", GA_ID, {
    allow_google_signals: false,
    allow_ad_personalization_signals: false
  });

  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
  document.head.appendChild(s);

  function track(name, p) { try { gtag("event", name, p || {}); } catch (e) {} }

  // --- aviso de cookies --------------------------------------------------------
  function renderBanner() {
    var b = document.getElementById("jpm-consent");
    if (!b) return;
    var t = TXT[lang()];
    b.querySelector("p").textContent = t.msg;
    b.querySelector(".y").textContent = t.yes;
    b.querySelector(".n").textContent = t.no;
  }

  function showBanner() {
    addCSS();
    var b = document.createElement("div");
    b.id = "jpm-consent";
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-live", "polite");
    b.innerHTML = '<p></p><div class="b"><button class="n" type="button"></button><button class="y" type="button"></button></div>';
    document.body.appendChild(b);
    renderBanner();
    b.querySelector(".y").addEventListener("click", function () {
      store(KEY_CONSENT, "granted");
      gtag("consent", "update", { analytics_storage: "granted" });
      track("consent_choice", { choice: "accepted" });
      b.remove();
    });
    b.querySelector(".n").addEventListener("click", function () {
      store(KEY_CONSENT, "denied");
      track("consent_choice", { choice: "declined" });
      b.remove();
    });
  }

  // --- eventos -------------------------------------------------------------------
  function onClick(e) {
    var el = e.target && e.target.closest ? e.target.closest("a, button") : null;
    if (!el || el.closest("#jpm-consent")) return;

    // troca de idioma (home e blog)
    if (el.closest(".lang")) {
      var l = (el.dataset && el.dataset.lang) || (el.textContent || "").trim().toLowerCase();
      if (l) track("language_change", { language: l });
      setTimeout(renderBanner, 0);
      return;
    }
    if (el.tagName !== "A") return;
    var href = el.getAttribute("href") || "";

    if (/joao-paulo-marson-cv-pt\.pdf/.test(href)) return track("cv_download", { cv_language: "pt" });
    if (/joao-paulo-marson-resume-en\.pdf/.test(href)) return track("cv_download", { cv_language: "en" });
    if (/linkedin\.com\/sharing|share-offsite/.test(href)) return track("share", { method: "linkedin", content_type: "post" });
    if (/api\.whatsapp\.com|wa\.me/.test(href)) return track("share", { method: "whatsapp", content_type: "post" });
    if (/linkedin\.com\/in\//.test(href)) return track("contact_click", { channel: "linkedin" });
    if (/^mailto:/.test(href)) return track("contact_click", { channel: "email" });
    if (/github\.com/.test(href)) return track("contact_click", { channel: "github" });

    // CTAs da home
    if (href === "#cases" && el.classList.contains("btn")) return track("cta_click", { cta: "ver_resultados" });
    if (href === "#contato") return track("cta_click", { cta: "fale_comigo" });

    // sites das empresas (trajetória, cases e link do produto)
    if (el.closest(".ti, .kicker") || el.classList.contains("prod-link")) {
      return track("company_click", { company: (el.textContent || "").replace("↗", "").trim().slice(0, 60), link_domain: el.hostname });
    }
  }

  onReady(function () {
    document.addEventListener("click", onClick, true);
    if (!choice) showBanner();
  });
})();
