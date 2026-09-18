"""Vicky Executive — interactive live command center (voice + text, phone + desktop)."""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

import shared_memory as mem
import vicky_store as store
from agents import vicky_executive as vicky

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)
mem.configure_gemini()

# Re-exports for harvest scripts
open_sheet = mem.open_sheet
worksheet = mem.worksheet
LEAD_HEADERS = mem.LEAD_HEADERS
optimize_sheet = mem.optimize_sheet
run_harvest = lambda: __import__("lead_agent").run_harvest()


def _marble_data_uri() -> str:
    path = mem.MARBLE_PATH
    if not path.exists():
        return ""
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def inject_theme() -> None:
    marble = _marble_data_uri()
    bg = (
        f'url("{marble}")'
        if marble
        else "radial-gradient(900px 500px at 10% -10%, rgba(212,175,55,.18), transparent 55%)"
    )
    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Outfit:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
  background-color: #050505 !important;
  background-image:
    linear-gradient(180deg, rgba(5,5,5,.72), rgba(5,5,5,.92)),
    {bg} !important;
  background-size: cover !important;
  background-attachment: fixed !important;
  color: #f3e6c8 !important;
  font-family: 'Outfit', sans-serif !important;
}}
.block-container {{
  max-width: 1180px;
  padding: 0.8rem 1rem 5.5rem 1rem !important;
}}
h1, h2, h3 {{
  font-family: 'Cormorant Garamond', serif !important;
  color: #e8c547 !important;
  letter-spacing: 0.02em;
}}
[data-testid="stHeader"] {{ background: transparent !important; }}
div[data-testid="stBottomBlockContainer"] {{
  background: rgba(8,8,8,.92) !important;
  border-top: 1px solid rgba(232,197,71,.35) !important;
}}

.vicky-hero {{
  text-align: center;
  padding: 1.2rem 0.6rem 0.4rem;
}}
.vicky-core {{
  width: min(180px, 42vw);
  height: min(180px, 42vw);
  margin: 0 auto 0.8rem;
  border-radius: 50%;
  border: 2px solid rgba(232,197,71,.75);
  box-shadow:
    0 0 0 8px rgba(232,197,71,.08),
    0 0 40px rgba(232,197,71,.22),
    inset 0 0 36px rgba(232,197,71,.12);
  background:
    radial-gradient(circle at 40% 35%, rgba(232,197,71,.35), transparent 55%),
    radial-gradient(circle at 50% 50%, #1a1508, #050505 70%);
  display: grid;
  place-items: center;
  animation: pulse 3.6s ease-in-out infinite;
}}
.vicky-core span {{
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(1.6rem, 5vw, 2.2rem);
  color: #f0d56a;
  font-weight: 600;
}}
@keyframes pulse {{
  0%, 100% {{ box-shadow: 0 0 0 8px rgba(232,197,71,.08), 0 0 34px rgba(232,197,71,.18); }}
  50% {{ box-shadow: 0 0 0 12px rgba(232,197,71,.12), 0 0 52px rgba(232,197,71,.32); }}
}}
.vicky-title {{
  margin: 0;
  font-size: clamp(1.45rem, 4.5vw, 2rem);
  color: #e8c547 !important;
}}
.vicky-sub {{
  color: #cbb888;
  font-size: 0.92rem;
  margin: 0.25rem 0 0.8rem;
}}
.agent-grid {{
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.55rem;
  margin: 0.4rem 0 1rem;
}}
@media (max-width: 820px) {{
  .agent-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
}}
@media (max-width: 420px) {{
  .agent-grid {{ grid-template-columns: 1fr 1fr; }}
}}
.agent-card {{
  border: 1px solid rgba(232,197,71,.4);
  background: rgba(8,8,8,.72);
  border-radius: 10px;
  padding: 0.65rem 0.7rem;
  min-height: 76px;
}}
.agent-card .name {{ color: #e8c547; font-weight: 600; font-size: 0.95rem; }}
.agent-card .role {{ color: #b7a57a; font-size: 0.75rem; }}
.agent-card .stat {{
  margin-top: 0.35rem;
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  color: #8fd18f;
}}
.agent-card.waiting .stat {{ color: #d2b15a; }}
.agent-card.stub .stat {{ color: #9aa0a6; }}
.panel {{
  border: 1px solid rgba(232,197,71,.35);
  background: rgba(8,8,8,.78);
  border-radius: 12px;
  padding: 0.85rem 0.95rem;
  margin-bottom: 0.85rem;
}}
.panel h3 {{
  margin: 0 0 0.45rem 0;
  font-size: 1.05rem;
}}
div[data-testid="stChatMessage"] {{
  background: rgba(12,12,12,.65) !important;
  border: 1px solid rgba(232,197,71,.22);
  border-radius: 10px;
}}
div[data-testid="stButton"] > button {{
  background: rgba(10,10,10,.9) !important;
  color: #e8c547 !important;
  border: 1px solid rgba(232,197,71,.7) !important;
  border-radius: 999px !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )


def speak_browser(text: str) -> None:
    payload = json.dumps(vicky.speakable(text))
    components.html(
        f"""
<script>
  const text = {payload};
  if (window.speechSynthesis && text) {{
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'en-IN';
    u.rate = 1.02;
    window.speechSynthesis.speak(u);
  }}
</script>
""",
        height=0,
    )


def voice_mic_bar() -> None:
    """Browser mic (Chrome/Safari). Writes transcript into a hidden bridge field via query-less localStorage + manual apply."""
    components.html(
        """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  body { margin:0; background:transparent; font-family: Outfit, system-ui, sans-serif; }
  .bar {
    display:flex; gap:8px; align-items:center; flex-wrap:wrap;
    padding:6px 2px;
  }
  button {
    background:#0a0a0a; color:#e8c547; border:1px solid rgba(232,197,71,.8);
    border-radius:999px; padding:10px 16px; font-weight:600; cursor:pointer;
  }
  button.listening { background:#3a2a08; box-shadow:0 0 16px rgba(232,197,71,.35); }
  #out { color:#cbb888; font-size:13px; flex:1; min-width:160px; }
</style>
</head>
<body>
  <div class="bar">
    <button id="mic" type="button">Mic — speak to Vicky</button>
    <span id="out">Voice works on phone & desktop (Chrome / Safari). Then tap Apply voice.</span>
  </div>
<script>
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const mic = document.getElementById('mic');
  const out = document.getElementById('out');
  if (!SR) {
    out.textContent = 'Mic unavailable here — type below or use a Chromium browser.';
  } else {
    const rec = new SR();
    rec.lang = 'en-IN';
    rec.interimResults = true;
    let finalText = '';
    rec.onstart = () => { mic.classList.add('listening'); out.textContent = 'Listening…'; };
    rec.onend = () => { mic.classList.remove('listening'); };
    rec.onerror = (e) => { out.textContent = 'Mic error: ' + e.error; mic.classList.remove('listening'); };
    rec.onresult = (e) => {
      let interim = '';
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const t = e.results[i][0].transcript;
        if (e.results[i].isFinal) finalText += t + ' ';
        else interim += t;
      }
      const shown = (finalText + ' ' + interim).trim();
      out.textContent = shown || 'Listening…';
      try { localStorage.setItem('vicky_voice_transcript', shown); } catch (err) {}
    };
    mic.onclick = () => {
      finalText = '';
      try { rec.start(); } catch (err) { try { rec.stop(); } catch (e2) {} }
    };
  }
</script>
</body>
</html>
""",
        height=64,
    )


def sheet_call(fn, fallback=None):
    try:
        return fn()
    except PermissionError:
        st.error(mem.PERM_MSG)
        return fallback
    except Exception as exc:
        blob = str(exc).lower()
        if "403" in blob or "permission" in blob:
            st.error(mem.PERM_MSG)
            return fallback
        st.error(str(exc))
        return fallback


def push_message(role: str, content: str) -> None:
    st.session_state.setdefault("vicky_chat", [])
    st.session_state.vicky_chat.append({"role": role, "content": content})


def run_vicky(command: str, speak: bool = True) -> None:
    book = st.session_state.get("book")
    leads_ws = st.session_state.get("leads_ws")
    with st.spinner("Vicky is routing your command…"):
        result = vicky.handle_command(command, leads_ws=leads_ws, book=book)
    msg = result.get("message") or "No reply."
    push_message("assistant", msg)
    st.session_state["last_vicky_reply"] = msg
    if speak and st.session_state.get("voice_out", True):
        speak_browser(msg)


def ops_panel() -> None:
    """The admin surface: one queue, one SEO line, one campaign list, one log.

    Everything here reads `vicky_data/` through `vicky_store`, so the panel works
    before any agent exists — it simply shows empty sections until the agents
    start writing. The only write it makes is a decision on an approval, which
    stays local; publishing still happens in GitHub/Cloudflare.
    """
    st.markdown('<div class="panel"><h3>Operations</h3></div>', unsafe_allow_html=True)
    s = store.stats()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Waiting for you", s["pendingApprovals"])
    m2.metric("Campaign drafts", s["campaignsDraft"])
    m3.metric(
        "SEO last pulled",
        s["seoLastRun"] or "—",
        f'{s["seoClicks7dChangePct"]:+.1f}% clicks' if s["seoClicks7dChangePct"] is not None else None,
    )
    m4.metric("Files in inbox", s["inboxPhotos"] + s["inboxCatalogues"])

    tab_a, tab_s, tab_c, tab_l = st.tabs(["Approvals", "SEO", "Campaigns", "Agent runs"])

    with tab_a:
        pending = store.list_approvals("pending")
        if not pending:
            st.caption("Nothing waiting. Vicky files a request here whenever it wants to change the website or post something.")
        for item in pending:
            with st.container(border=True):
                st.markdown(f'**{item["title"]}**')
                st.write(item["summary"])
                st.caption(f'{item["kind"]} · asked {item["created"][:16].replace("T", " ")}')
                if item.get("previewUrl"):
                    st.markdown(f'[Open the preview]({item["previewUrl"]})')
                note = st.text_input("Note (optional)", key=f'note-{item["id"]}', label_visibility="collapsed", placeholder="Note back to Vicky (optional)")
                yes, no = st.columns(2)
                if yes.button("Approve", key=f'ok-{item["id"]}', use_container_width=True):
                    store.decide_approval(item["id"], "approved", note=note)
                    store.log_run("owner", f'approved {item["id"]}', True, item["title"])
                    st.rerun()
                if no.button("Reject", key=f'no-{item["id"]}', use_container_width=True):
                    store.decide_approval(item["id"], "rejected", note=note)
                    store.log_run("owner", f'rejected {item["id"]}', True, item["title"])
                    st.rerun()

    with tab_s:
        history = store.seo_history(30)
        if history:
            rows = {
                "date": [h["date"] for h in history],
                "clicks": [h.get("totals", {}).get("clicks") for h in history],
                "impressions": [h.get("totals", {}).get("impressions") for h in history],
                "indexed": [h.get("health", {}).get("indexed") for h in history],
            }
            st.dataframe(rows, use_container_width=True, hide_index=True)
            flags = (history[-1].get("flags") or [])
            for flag in flags:
                st.warning(flag)
        else:
            st.caption(
                "No snapshots yet. The SEO agent writes one file a day from Google Search Console "
                "once the site is live and verified — see docs/DAILY_OPS_AND_DASHBOARD.md."
            )

    with tab_c:
        campaigns = store.list_campaigns()
        if not campaigns:
            st.caption("No campaigns yet. The Marketing agent drafts these; a person posts them.")
        for c in campaigns:
            with st.expander(f'{c["channel"].upper()} · {c["name"]} · {c["status"]}'):
                st.text(c["body"])
                if c.get("scheduledFor"):
                    st.caption(f'Scheduled for {c["scheduledFor"]}')

    with tab_l:
        runs = store.recent_runs(25)
        if runs:
            st.dataframe(
                {
                    "when": [r["ts"][:16].replace("T", " ") for r in runs],
                    "agent": [r["agent"] for r in runs],
                    "action": [r["action"] for r in runs],
                    "ok": [r["ok"] for r in runs],
                    "detail": [r.get("detail", "") for r in runs],
                },
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.caption("No agent runs logged yet.")


def main() -> None:
    st.set_page_config(
        page_title="Vicky | Elite Balaji Command",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_theme()

    if "vicky_chat" not in st.session_state:
        st.session_state.vicky_chat = [
            {
                "role": "assistant",
                "content": (
                    "Vicky online. I run the council — Scraper, SEO, Marketing, Email — "
                    "from shared memory. Try: “run hunter”, “optimize sheet”, “seo granite tiles”, "
                    "or ask anything about Elite Balaji."
                ),
            }
        ]

    book = sheet_call(mem.open_sheet)
    leads_ws = sheet_call(lambda: mem.worksheet(book, "Sheet1", mem.LEAD_HEADERS)) if book else None
    st.session_state["book"] = book
    st.session_state["leads_ws"] = leads_ws

    st.markdown(
        f"""
<div class="vicky-hero">
  <div class="vicky-core"><span>VICKY</span></div>
  <h1 class="vicky-title">Executive Command Center</h1>
  <p class="vicky-sub">{mem.BUSINESS_NAME} · since {mem.ESTABLISHED_SINCE} · voice + text · phone & desktop</p>
</div>
""",
        unsafe_allow_html=True,
    )

    cards = []
    for a in mem.AGENT_ROSTER:
        klass = "agent-card"
        if "WAIT" in a["status"]:
            klass += " waiting"
        elif a["status"] == "STUB":
            klass += " stub"
        cards.append(
            f'<div class="{klass}"><div class="name">{a["name"]}</div>'
            f'<div class="role">{a["role"]}</div>'
            f'<div class="stat">{a["status"]}</div></div>'
        )
    st.markdown(f'<div class="agent-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Run Scraper", use_container_width=True):
        push_message("user", "run hunter")
        run_vicky("run hunter")
        st.rerun()
    if c2.button("Optimize ledger", use_container_width=True):
        push_message("user", "optimize sheet")
        run_vicky("optimize sheet")
        st.rerun()
    if c3.button("Council status", use_container_width=True):
        push_message("user", "council status")
        run_vicky("council status")
        st.rerun()
    st.session_state["voice_out"] = c4.toggle("Vicky speaks", value=st.session_state.get("voice_out", True))

    st.markdown('<div class="panel"><h3>Live channel</h3></div>', unsafe_allow_html=True)
    voice_mic_bar()
    vcol1, vcol2 = st.columns([3, 1])
    with vcol1:
        voice_box = st.text_input(
            "Voice transcript / quick command",
            key="voice_bridge",
            placeholder="After mic, paste or type here — or use chat below",
            label_visibility="collapsed",
        )
    with vcol2:
        if st.button("Send to Vicky", use_container_width=True) and mem.clean(voice_box):
            push_message("user", voice_box)
            run_vicky(voice_box)
            st.rerun()

    for msg in st.session_state.vicky_chat[-12:]:
        with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
            st.markdown(msg["content"])

    prompt = st.chat_input("Talk to Vicky — text on any device…")
    if prompt:
        push_message("user", prompt)
        run_vicky(prompt)
        st.rerun()

    ops_panel()

    # Lead ledger panel
    st.markdown('<div class="panel"><h3>Shared lead memory</h3></div>', unsafe_allow_html=True)
    ledger = sheet_call(lambda: mem.load_ledger(leads_ws), fallback=None) if leads_ws else None
    if ledger and ledger["Contractor Name"]:
        st.dataframe(ledger, use_container_width=True, hide_index=True)
        phone_n = sum(1 for p in ledger["Phone Number"] if p and p != "—")
        st.caption(
            f"{len(ledger['Contractor Name'])} leads · {phone_n} with phone · "
            f"{mem.PRIMARY_OFFICE_ADDRESS} · {mem.CONTACT_PHONE}"
        )
    else:
        st.info("Lead ledger empty. Tell Vicky: “run hunter”.")

    with st.expander("Specialist stubs (SEO / Marketing / Email)"):
        st.caption("SEO can run lightly now. Marketing + Email wait for the company website.")
        kw = st.text_input("SEO keyword", placeholder="granite tiles Coimbatore")
        if st.button("Run SEO Agent") and kw:
            push_message("user", f"seo {kw}")
            run_vicky(f"seo {kw}")
            st.rerun()
        if st.button("Ask Marketing Agent"):
            push_message("user", "marketing status")
            run_vicky("marketing status")
            st.rerun()
        if st.button("Ask Email Agent"):
            push_message("user", "email status")
            run_vicky("email status")
            st.rerun()


if __name__ == "__main__":
    main()
