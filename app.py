import streamlit as st
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="A Message for You 💌",
    page_icon="💌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Session State ────────────────────────────────────────────────────────────
for key, default in {
    "phase": "intro",        # intro → letter → proposal → responded | left
    "choice": None,          # "yes" | "no"
    "no_count": 0,           # tracks how many times they clicked No
    "yes_timestamp": None,   # exact moment she said yes 💑
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Global Styles ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Hide Streamlit chrome ──────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Fonts ──────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Raleway:wght@300;400;500&display=swap');

/* ── Root palette ───────────────────────────────────────── */
:root {
    --blush:    #f7d6d0;
    --rose:     #e8a0a0;
    --deep:     #c0686a;
    --cream:    #fdf6f0;
    --warm:     #8b5e5e;
    --text:     #4a2c2c;
    --muted:    #9a7070;
}

/* ── App background ─────────────────────────────────────── */
.stApp {
    background: radial-gradient(ellipse at 20% 10%, #fde8e8 0%, #fdf6f0 40%, #f5e6f5 100%);
    min-height: 100vh;
    font-family: 'Raleway', sans-serif;
    color: var(--text);
}

/* ── Center the content block ───────────────────────────── */
[data-testid="stVerticalBlock"] {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* ── Hero card ──────────────────────────────────────────── */
.hero-card {
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(232, 160, 160, 0.35);
    border-radius: 28px;
    padding: 3rem 3.5rem;
    max-width: 560px;
    width: 100%;
    text-align: center;
    box-shadow:
        0 4px 32px rgba(192, 104, 106, 0.10),
        0 1px 4px rgba(0,0,0,0.04);
    margin: 2rem auto;
    animation: fadeUp 0.9s cubic-bezier(.22,.68,0,1.2) both;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Letter card (scrollable) ───────────────────────────── */
.letter-card {
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(232, 160, 160, 0.35);
    border-radius: 28px;
    padding: 2.5rem 3rem;
    max-width: 560px;
    width: 100%;
    text-align: left;
    box-shadow:
        0 4px 32px rgba(192, 104, 106, 0.10),
        0 1px 4px rgba(0,0,0,0.04);
    margin: 2rem auto 0;
    animation: fadeUp 0.9s cubic-bezier(.22,.68,0,1.2) both;
}

.letter-scroll {
    max-height: 420px;
    overflow-y: auto;
    padding-right: 0.5rem;
    scrollbar-width: thin;
    scrollbar-color: var(--rose) transparent;
}
.letter-scroll::-webkit-scrollbar { width: 4px; }
.letter-scroll::-webkit-scrollbar-thumb {
    background: var(--rose);
    border-radius: 4px;
}

.letter-eyebrow {
    font-family: 'Raleway', sans-serif;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--deep);
    margin-bottom: 1rem;
    text-align: center;
}

.letter-body {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.05rem;
    font-weight: 400;
    line-height: 1.9;
    color: var(--text);
    white-space: pre-line;
}

.letter-fade {
    position: relative;
}
.letter-fade::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 48px;
    background: linear-gradient(to bottom, transparent, rgba(255,255,255,0.85));
    border-radius: 0 0 8px 8px;
    pointer-events: none;
}

/* ── Scene strip ────────────────────────────────────────── */
.scene-strip {
    font-size: 2.4rem;
    letter-spacing: 1rem;
    margin: 1.2rem 0 0.8rem;
    animation: walkIn 3.2s ease forwards;
}
@keyframes walkIn {
    0%   { letter-spacing: 4rem; opacity: 0; }
    60%  { opacity: 1; }
    100% { letter-spacing: 1rem; }
}

/* ── Divider ────────────────────────────────────────────── */
.divider {
    width: 48px;
    height: 1.5px;
    background: linear-gradient(to right, transparent, var(--rose), transparent);
    margin: 1.4rem auto;
}

/* ── Typography ─────────────────────────────────────────── */
.eyebrow {
    font-family: 'Raleway', sans-serif;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--deep);
    margin-bottom: 0.6rem;
}
.headline {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 2.4rem;
    font-weight: 300;
    line-height: 1.25;
    color: var(--text);
    margin: 0 0 0.4rem;
}
.headline em {
    font-style: italic;
    color: var(--deep);
}
.subline {
    font-size: 0.92rem;
    font-weight: 300;
    color: var(--muted);
    line-height: 1.75;
    max-width: 380px;
    margin: 0 auto;
}

/* ── Buttons ─────────────────────────────────────────────── */
.stButton > button {
    border-radius: 50px !important;
    border: 1.5px solid var(--rose) !important;
    background: transparent !important;
    color: var(--text) !important;
    font-family: 'Raleway', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    padding: 0.65rem 1.2rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
    min-width: unset !important;
}
.stButton > button:hover {
    background: var(--deep) !important;
    border-color: var(--deep) !important;
    color: white !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(192,104,106,0.3) !important;
}

/* ── Constrain ALL column rows to card width ────────────── */
[data-testid="stHorizontalBlock"] {
    max-width: 560px !important;
    width: 100% !important;
    margin: 0 auto !important;
}

/* ── Align columns to same baseline ─────────────────────── */
[data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
    display: flex !important;
    align-items: center !important;
}

/* ── Response card ───────────────────────────────────────── */
.response-card {
    background: linear-gradient(135deg, #fff5f5 0%, #fff0fa 100%);
    border: 1px solid rgba(232,160,160,0.4);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-top: 1.8rem;
    animation: popIn 0.5s cubic-bezier(.22,.68,0,1.2) both;
}
@keyframes popIn {
    from { opacity: 0; transform: scale(0.88); }
    to   { opacity: 1; transform: scale(1); }
}
.response-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.7rem;
    font-weight: 300;
    color: var(--deep);
    margin-bottom: 0.5rem;
}
.response-body {
    font-size: 0.9rem;
    color: var(--muted);
    line-height: 1.75;
}

/* ── Celebration background (fireworks) ─────────────────── */
.celebration-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.firework {
    position: absolute;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    animation: fireworkBurst 1.8s ease-out infinite;
    opacity: 0;
}

@keyframes fireworkBurst {
    0%   { transform: scale(0) translateY(0); opacity: 1; }
    50%  { opacity: 0.9; }
    100% { transform: scale(1) translateY(-120px); opacity: 0; }
}

.confetti {
    position: absolute;
    top: -10px;
    width: 8px;
    height: 14px;
    border-radius: 2px;
    animation: confettiFall linear infinite;
    opacity: 0.85;
}

@keyframes confettiFall {
    0%   { transform: translateY(-20px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}

/* ── Floating hearts ─────────────────────────────────────── */
.hearts-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.heart {
    position: absolute;
    bottom: -60px;
    opacity: 0;
    font-size: 1.1rem;
    animation: floatHeart 7s ease-in infinite;
}
@keyframes floatHeart {
    0%   { bottom: -60px; opacity: 0; transform: translateX(0) rotate(0deg); }
    10%  { opacity: 0.6; }
    90%  { opacity: 0.2; }
    100% { bottom: 105vh; opacity: 0; transform: translateX(40px) rotate(25deg); }
}

/* ── Intro page: muted style for "Not interested" button ─── */
.intro-muted-btn [data-testid="column"]:nth-child(2) .stButton > button {
    border-color: var(--muted) !important;
    color: var(--muted) !important;
    opacity: 0.7 !important;
}
.intro-muted-btn [data-testid="column"]:nth-child(2) .stButton > button:hover {
    background: var(--muted) !important;
    border-color: var(--muted) !important;
    color: white !important;
    opacity: 1 !important;
}

/* ── Spinner override ────────────────────────────────────── */
.stSpinner { display: none !important; }
</style>

<!-- Floating hearts background (non-celebration phases) -->
<div class="hearts-bg" id="hearts-bg">
  <span class="heart" style="left:7%;  animation-delay:0s;    animation-duration:8s;  font-size:0.9rem;">♡</span>
  <span class="heart" style="left:18%; animation-delay:1.4s;  animation-duration:6.5s;font-size:0.7rem;">♡</span>
  <span class="heart" style="left:33%; animation-delay:0.6s;  animation-duration:9s;  font-size:1.2rem;">♡</span>
  <span class="heart" style="left:50%; animation-delay:2.1s;  animation-duration:7.5s;font-size:0.8rem;">♡</span>
  <span class="heart" style="left:65%; animation-delay:0.3s;  animation-duration:8.5s;font-size:1rem;">♡</span>
  <span class="heart" style="left:79%; animation-delay:1.8s;  animation-duration:6s;  font-size:0.75rem;">♡</span>
  <span class="heart" style="left:91%; animation-delay:0.9s;  animation-duration:9.5s;font-size:0.85rem;">♡</span>
</div>
""", unsafe_allow_html=True)

# ─── Letter text ──────────────────────────────────────────────────────────────
LETTER = """Hi Yunna 👋

Nice to meet you again haha, 10 years na pala tayong magkakilala pero magkakilala lang hahaha.

I'd told you that you are my first gf as well as yun din sinabi mo sakin na I'm your first. Hehe totoo ba? Hahaha just want to make it quick summary simula ng simula…

First thing first — medyo cringe and awkward na sabihin kase trentahin na tayo, alam mo ba yung feeling ko matured na ko pero baby mo pa pala.. Hahaha.

Anyways, ito na nga. I pursued you within 4 mos and naging tayo ng May 7, 2016. Our breakup was Nov 29, 2016 — so bale 6 mos lang naging tayo plus yung 4 months na niligawan kita.

When I first saw you, di ako naniniwala sa love at first sight pero baka yun nga yung na feel ko. Parang may kuryente, tapos ang bagal ng paligid. Basta everything becomes slow and ikaw lang nakikita ko. So, baka yun nga yung first sight na sinasabi nila. HAHAHA Sorry OA and medyo childish.

Pero yun nga, medyo mdami din nangyari — hindi ko na sasabihin dito and di na ko magbabanggit ng mga names hahaha, baka maging dragon ka nanaman HAHAHA. Pero ewan ko, mapaglaro talaga ang tadhana — bigla nalang ewan.

Matagal na kitang gusto talaga pansinin pero I have my pride, I have my ego and never ko makakalimutan yung mga ginawa mo sakin dati. Pero that one night… that one night na bday talaga ni Mama pa — parang nakalimutan ko yung ego ko and kinausap kita.

Tapos naglasing ka pa, then sabi namin ni Mama dito ka nalang muna mag-sleep kase 12:15 na yun e. Tapos — putsa — pinagpalit kita ng damit, naghubad ka sa harapan ko. Tingin mo ano mararamdaman ko nun?? INAKIT MO ATA TALAGA AKO E? Just kiddin hahaha 😂

Tapos yun na, lahat ng emotions ko that time halo-halo — yung pain habang nakatitig ako sayo while you were sleeping. Tapos on the other side, this is the girl that I loved so much back then, willing to give her everything I had, willing to be converted — religion does not matter anymore basta ma-express and mapatunayan ko lang na mahal na mahal ko sya.

Ito yung babaeng yun.

That night tumulo yung luha ko, then bigla na kong na-blank. I kissed you pero nagising ka kaagad — ambabaw lang pala ng tulog mo. Mababaw ba or tulog-manok ka lang? HAHAHA

So, let's talk about now.

Yunnaizah Kinudalan — I decided, everything that happened in the past ibabaon ko na sa limot. I will be focusing more on you nalang, our current situations, and the future if willing kang makasama ako hanggang sa tumanda tayo.

Ready ka bang makasama ako sa saya, lungkot, problema, etc.?
Ready ka bang mag-take ng risks sa mga bagay-bagay para sakin?
Ready ka bang harapin ang mga problems and pagsubok sa buhay with me?

If yes, Yunna… 💌"""

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE: INTRO  — animated entrance with two choices
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.phase == "intro":

    st.markdown("""
    <div class="hero-card">
        <p class="eyebrow">Yunnaizah Queen Kinudalan</p>
        <div class="scene-strip">👦 &nbsp;💌&nbsp; 👧</div>
        <div class="divider"></div>
        <h1 class="headline">Something <em>important</em><br>to tell you…</h1>
        <p class="subline">He's been rehearsing this for a while.<br>Are you willing to listen?</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="intro-muted-btn">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("What is it? 👀", use_container_width=True):
            st.session_state.phase = "letter"
            st.rerun()
    with col2:
        if st.button("Not interested 🚶", use_container_width=True):
            st.session_state.phase = "left"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE: LETTER  — the heartfelt message, scrollable
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "letter":

    st.markdown(f"""
    <div class="letter-card">
        <p class="letter-eyebrow">💌 &nbsp; A letter for you</p>
        <div style="width:48px;height:1.5px;background:linear-gradient(to right,transparent,#e8a0a0,transparent);margin:0 auto 1.5rem;"></div>
        <div class="letter-fade">
            <div class="letter-scroll">
                <div class="letter-body">{LETTER}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("💖 Click me…", use_container_width=True):
            st.session_state.phase = "proposal"
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE: LEFT  — they walked away 😔
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "left":

    st.markdown("""
    <div class="hero-card">
        <p class="eyebrow">Oh…</p>
        <div class="scene-strip" style="animation:none; letter-spacing:1rem;">👦 &nbsp;💔&nbsp; 🚶‍♀️</div>
        <div class="divider"></div>
        <h1 class="headline">That's okay.<br><em>Take your time.</em></h1>
        <p class="subline">
            He'll be right here — patient as ever.<br>
            The message isn't going anywhere. 💌
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Actually, wait…"):
        st.session_state.phase = "intro"
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE: PROPOSAL — the actual question
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "proposal":
    no_labels = [
        "Nah…",
        "Are you sure? 😶",
        "Really sure? 🥺",
        "Last chance! 😭",
        "Okay fine, but… 💔",
    ]
    no_idx = min(st.session_state.no_count, len(no_labels) - 1)
    no_size = max(60, 160 - st.session_state.no_count * 22)

    st.markdown(f"""
    <style>
    [data-testid="column"]:nth-child(2) .stButton > button {{
        font-size: {max(0.65, 0.85 - st.session_state.no_count * 0.06):.2f}rem !important;
        opacity: {max(0.35, 1.0 - st.session_state.no_count * 0.15):.2f} !important;
        border-color: var(--muted) !important;
        max-width: {no_size}px !important;
        margin-left: auto !important;
    }}
    [data-testid="column"]:nth-child(2) .stButton > button:hover {{
        background: var(--muted) !important;
        border-color: var(--muted) !important;
    }}
    </style>

    <div class="hero-card">
        <p class="eyebrow">Yunnaizah Queen Kinudalan</p>
        <div class="divider"></div>
        <h1 class="headline">Will you be my<br><em>Girlfriend again?</em> 💌</h1>
        <p class="subline">
            Every song I hear reminds me of you.<br>
            Every quiet moment — I wish you were there.<br>
            Will you be my last?
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💖  Yes, of course!", use_container_width=True):
            st.session_state.choice = "yes"
            st.session_state.phase = "responded"
            st.session_state.yes_timestamp = datetime.now().strftime("%B %d, %Y · %I:%M %p")
            st.rerun()
    with col2:
        if st.button(no_labels[no_idx], use_container_width=True):
            st.session_state.no_count += 1
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE: RESPONDED — reaction screen
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "responded":

    if st.session_state.choice == "yes":
        timestamp = st.session_state.get("yes_timestamp", "")

        # ── Fireworks + confetti celebration background ──
        st.markdown("""
        <style>
        /* Override app bg to deep celebration gradient */
        .stApp {
            background: radial-gradient(ellipse at 30% 20%, #ffe0ec 0%, #fdf0f8 35%, #fff0e6 70%, #fde8ff 100%) !important;
        }
        #hearts-bg { display: none; }
        </style>

        <div class="celebration-bg">
          <!-- Confetti pieces -->
          <div class="confetti" style="left:5%;  background:#f7a8c4; animation-duration:3.2s; animation-delay:0s;   width:7px; height:12px;"></div>
          <div class="confetti" style="left:12%; background:#ffd6a5; animation-duration:2.8s; animation-delay:0.3s; width:9px; height:9px; border-radius:50%;"></div>
          <div class="confetti" style="left:20%; background:#c9b8f5; animation-duration:3.6s; animation-delay:0.1s;"></div>
          <div class="confetti" style="left:28%; background:#f7a8c4; animation-duration:2.5s; animation-delay:0.7s; width:6px; height:16px;"></div>
          <div class="confetti" style="left:35%; background:#a8d8f0; animation-duration:3.1s; animation-delay:0.4s;"></div>
          <div class="confetti" style="left:42%; background:#ffd6a5; animation-duration:2.9s; animation-delay:0.2s; border-radius:50%;"></div>
          <div class="confetti" style="left:50%; background:#f7a8c4; animation-duration:3.4s; animation-delay:0.6s; width:10px;"></div>
          <div class="confetti" style="left:58%; background:#c9b8f5; animation-duration:2.7s; animation-delay:0.1s;"></div>
          <div class="confetti" style="left:65%; background:#ffd6a5; animation-duration:3.0s; animation-delay:0.5s; width:7px; height:7px; border-radius:50%;"></div>
          <div class="confetti" style="left:72%; background:#a8d8f0; animation-duration:2.6s; animation-delay:0.3s; width:9px; height:14px;"></div>
          <div class="confetti" style="left:80%; background:#f7a8c4; animation-duration:3.3s; animation-delay:0.8s;"></div>
          <div class="confetti" style="left:88%; background:#c9b8f5; animation-duration:2.4s; animation-delay:0.2s; border-radius:50%;"></div>
          <div class="confetti" style="left:94%; background:#ffd6a5; animation-duration:3.5s; animation-delay:0.6s; width:6px; height:18px;"></div>
          <!-- Extra wave -->
          <div class="confetti" style="left:8%;  background:#c9b8f5; animation-duration:4.0s; animation-delay:1.2s; width:8px;"></div>
          <div class="confetti" style="left:25%; background:#f7a8c4; animation-duration:3.8s; animation-delay:1.5s; border-radius:50%;"></div>
          <div class="confetti" style="left:45%; background:#a8d8f0; animation-duration:4.2s; animation-delay:1.0s; width:11px; height:11px;"></div>
          <div class="confetti" style="left:70%; background:#ffd6a5; animation-duration:3.9s; animation-delay:1.3s; width:7px; height:13px;"></div>
          <div class="confetti" style="left:90%; background:#f7a8c4; animation-duration:4.1s; animation-delay:1.1s;"></div>

          <!-- Firework bursts -->
          <div class="firework" style="left:20%; top:25%; background:#f7a8c4; animation-duration:1.6s; animation-delay:0s; box-shadow: 0 0 6px 3px #f7a8c4;"></div>
          <div class="firework" style="left:50%; top:15%; background:#ffd6a5; animation-duration:1.9s; animation-delay:0.4s; box-shadow: 0 0 6px 3px #ffd6a5;"></div>
          <div class="firework" style="left:78%; top:30%; background:#c9b8f5; animation-duration:1.7s; animation-delay:0.8s; box-shadow: 0 0 6px 3px #c9b8f5;"></div>
          <div class="firework" style="left:35%; top:60%; background:#a8d8f0; animation-duration:2.0s; animation-delay:0.2s; box-shadow: 0 0 6px 3px #a8d8f0;"></div>
          <div class="firework" style="left:65%; top:55%; background:#f7a8c4; animation-duration:1.5s; animation-delay:1.0s; box-shadow: 0 0 6px 3px #f7a8c4;"></div>
          <div class="firework" style="left:10%; top:70%; background:#ffd6a5; animation-duration:1.8s; animation-delay:0.6s; box-shadow: 0 0 6px 3px #ffd6a5;"></div>
          <div class="firework" style="left:88%; top:20%; background:#c9b8f5; animation-duration:2.1s; animation-delay:0.3s; box-shadow: 0 0 6px 3px #c9b8f5;"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="hero-card" style="border-color: rgba(247,168,196,0.5); box-shadow: 0 8px 48px rgba(247,168,196,0.25), 0 2px 8px rgba(0,0,0,0.04);">
            <p class="eyebrow">She said yes 🎉</p>
            <div class="scene-strip">👦🌸👧</div>
            <div class="divider"></div>
            <h1 class="headline">You just made me<br>the <em>happiest person</em>.</h1>
            <div class="response-card">
                <p class="response-title">💑 Our story begins now.</p>
                <p class="response-body" style="font-size:0.78rem; letter-spacing:0.06em; color: var(--deep); font-weight:500; margin-bottom:1rem;">
                    🗓️ &nbsp;{timestamp}
                </p>
                <p class="response-body">
                    I promise to make every moment worth your time —<br>
                    every laugh, every memory, every quiet evening.<br><br>
                    I LOVE YOU SO MUCH YUNNA. 💌
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:  # "no" — forced happy ending
        st.markdown("""
        <div class="hero-card">
            <p class="eyebrow">Plot twist 😈</p>
            <div class="scene-strip">👦💘👧</div>
            <div class="divider"></div>
            <h1 class="headline">You have<br><em>no choice.</em></h1>
            <div class="response-card">
                <p class="response-title">💫 The universe decided.</p>
                <p class="response-body">
                    Your heart already said yes — your fingers just got confused. 😏<br><br>
                    I'll be waiting. Take your time. I'm very patient. 💌
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↩ Start over"):
        for k in ["phase", "choice", "no_count", "yes_timestamp"]:
            del st.session_state[k]
        st.rerun()