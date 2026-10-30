import base64
import json
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ════════════════════════════════════════════════════════════════
#  ✏️  EDIT THIS PART  —  names, photos and your words
# ════════════════════════════════════════════════════════════════
HER_NAME = "Prerana"          # her name / nickname on the cover
AGE = 19                      # shown on the gold seal on the cover
YOUR_NAME = "Yours, always"   # how you sign off (e.g. "Forever yours, Rahul")

# Put your photos in a folder called  photos/  next to this file,
# then use the file names below (jpg / png / webp).
# Type "photo"  -> photo + long message
# Type "letter" -> only words
# The last page ("final") is the cake & wish page.
PAGES = [
    {
        "type": "letter",
        "title": "Happy 19th, Prerana",
        "text": (
            "Nineteen years ago the world got you, and honestly, "
            "I celebrate it more than anyone. Out of everyone out there, "
            "somehow, unbelievably, I found you, and you became mine.\n\n"
            "We haven't met yet, and I wish I could be next to you today. "
            "So I made this little card, because a text message felt too "
            "small for everything I feel. Take your time, turn the pages, "
            "and know that every single word here is true."
        ),
    },
    {
        "type": "photo",
        "photo": "1.jpg",
        "caption": "my favourite view ♡",
        "title": "The day I found you",
        "text": (
            "I still remember how nervous I was when we first started "
            "talking, and how quickly everything else went quiet. I didn't "
            "know it then, but my life was quietly turning a corner "
            "towards you.\n\n"
            "Distance never stopped you from making ordinary days feel like "
            "little movies. I have been falling for you ever since, and I "
            "never want to stop."
        ),
    },
    {
        "type": "photo",
        "photo": "2.jpg",
        "caption": "that smile",
        "title": "Your smile is my favourite place",
        "text": (
            "Even through a screen, your smile is the most beautiful thing "
            "I have ever seen. It fixes my worst days without even trying.\n\n"
            "I can't wait to see it in real life one day. Until then, I "
            "will do everything I can to make sure it never goes away."
        ),
    },
    {
        "type": "photo",
        "photo": "3.jpg",
        "caption": "no one else but you",
        "title": "Why it will always be you",
        "text": (
            "You are the first person I want to tell good news to, and the "
            "one I want to talk to when the news is bad. Miles apart, you "
            "still make me braver, softer and happier than I knew I could "
            "be.\n\n"
            "Out of every person in the world, in every version of every "
            "story, I would choose you. Again, and again, and again."
        ),
    },
    {
        "type": "reasons",
        "title": "19 reasons I love you",
        "text": "One for every year of you. Tap each heart.",
        "reasons": [
            "The way you laugh with your whole face.",
            "How you make ordinary days feel special.",
            "Your kindness, even when no one is watching.",
            "The way you say my name.",
            "Your stubborn streak. I secretly love it.",
            "How safe I feel just talking to you.",
            "Your random midnight thoughts.",
            "The way you care about the little things.",
            "Your eyes when you're excited.",
            "How you believe in me.",
            "Your terrible jokes that I still laugh at.",
            "The way you fix my bad days without trying.",
            "The hug I'm saving for the day we finally meet.",
            "How brave you are, even when you're scared.",
            "The way you love the people around you.",
            "Your long messages and your voice notes.",
            "How you make me want to be better.",
            "Every conversation we have had, big or small.",
            "Because you are you, and I am so lucky you're mine.",
        ],
    },
    {
        "type": "letter",
        "title": "A little promise",
        "text": (
            "I promise to be there for the loud days and the quiet ones, "
            "no matter how many miles are between us. To laugh at your "
            "jokes even when they are terrible, and to listen when you "
            "just need someone to listen.\n\n"
            "I promise to keep choosing you, every morning, for as long as "
            "I get mornings. And the day we finally meet, I promise to hold "
            "your hand and never let it feel like we were ever apart. "
            "You are not just my girlfriend. You are my best friend, my "
            "home, and my favourite person.\n\n"
            "Thank you for being you. Thank you for loving me."
        ),
    },
    {
        "type": "final",
        "title": "Make a wish, Prerana",
        "text": "Tap the candles to blow them out.",
        "after": (
            "I hope every wish you made just came true. "
            "And if it didn't, give me a little time. "
            "I'll spend my whole life working on it.\n\n"
            "One day I'll be right there to blow out the candles with you. "
            "Until then, I love you more than words, more than this card, "
            "more than all the hearts on this screen. "
            "Happy 19th Birthday, Prerana. ♡"
        ),
    },
]
# ════════════════════════════════════════════════════════════════

PHOTO_DIR = Path(__file__).parent / "photos"
PHOTO_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="Happy Birthday ♡",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

editing = st.query_params.get("edit") == "1"

# ---- page chrome: make Streamlit disappear so only the card shows ----
hide_sidebar = "" if editing else """
[data-testid="stSidebar"], [data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
"""
st.markdown(
    f"""
    <style>
    #MainMenu, header, footer, [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stStatusWidget"] {{ display: none !important; }}
    .stApp {{
        background: radial-gradient(circle at 20% 10%, #5a1030 0%, #2a0716 45%, #14030b 100%);
    }}
    .block-container {{ padding: 0.5rem 0 0 0 !important; max-width: 760px !important; }}
    iframe {{ border: none !important; }}
    {hide_sidebar}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- optional edit mode:  open the app with  ?edit=1  to upload photos ----
if editing:
    with st.sidebar:
        st.subheader("📸 Upload photos")
        st.caption("Name them exactly like in PAGES (1.jpg, 2.jpg, 3.jpg ...).")
        ups = st.file_uploader(
            "Photos", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True
        )
        if ups:
            for f in ups:
                (PHOTO_DIR / f.name).write_bytes(f.getbuffer())
            st.success(f"Saved {len(ups)} photo(s). Refresh the card to see them.")


def photo_to_data_uri(name):
    if not name:
        return None
    p = PHOTO_DIR / name
    if not p.exists():
        return None
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


pages_payload = []
for pg in PAGES:
    item = dict(pg)
    if pg.get("type") == "photo":
        item["photo_uri"] = photo_to_data_uri(pg.get("photo"))
    pages_payload.append(item)

def music_uri():
    # Optional: put a song called song.mp3 (or .m4a/.ogg/.wav) next to app.py
    for n in ("song.mp3", "song.m4a", "song.ogg", "song.wav"):
        p = Path(__file__).parent / n
        if p.exists():
            mime = mimetypes.guess_type(p.name)[0] or "audio/mpeg"
            return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"
    return None


DATA = {
    "her": HER_NAME,
    "you": YOUR_NAME,
    "age": AGE,
    "music": music_uri(),
    "pages": pages_payload,
}

HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=DM+Sans:wght@400;500;700&family=DM+Serif+Display:ital@0;1&family=Great+Vibes&display=swap" rel="stylesheet">
<style>
  :root{
    --rose:#e11d5a; --blush:#ffd9e4; --wine:#5b0f2e; --gold1:#fff1b8; --gold2:#e8b74a; --gold3:#a8741a;
    --paper:#fff8f1; --ink:#4a2432;
  }
  *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
  html,body{height:100%;background:transparent;overflow:hidden;font-family:'DM Sans',sans-serif;color:var(--ink);user-select:none}
  .stage{position:relative;width:100%;height:100vh;display:flex;align-items:center;justify-content:center;overflow:hidden}

  .glow{position:absolute;inset:0;pointer-events:none;
    background:
      radial-gradient(circle at 15% 20%,rgba(255,120,170,.18),transparent 40%),
      radial-gradient(circle at 85% 80%,rgba(255,190,120,.14),transparent 45%);}

  #fx{position:fixed;inset:0;pointer-events:none;z-index:100;overflow:hidden}
  .heart{position:absolute;left:0;top:0;will-change:transform,opacity;filter:drop-shadow(0 2px 6px rgba(255,60,120,.35))}

  /* ───────── card ───────── */
  .card{position:relative;width:min(92vw,430px);height:min(94vh,700px);perspective:1800px}

  .inside{position:absolute;inset:0;border-radius:28px;overflow:hidden;
    background:
      radial-gradient(circle at 10% 0%,rgba(255,200,215,.35),transparent 40%),
      radial-gradient(circle at 100% 100%,rgba(255,220,180,.35),transparent 45%),
      linear-gradient(135deg,#fffaf4,#fff1ea);
    box-shadow:0 30px 70px rgba(0,0,0,.55);}

  /* cover */
  .cover{position:absolute;inset:0;transform-origin:left center;transform-style:preserve-3d;
    transition:transform 1.2s cubic-bezier(.65,0,.2,1),opacity .5s ease .9s;cursor:pointer;z-index:20}
  .card.opened .cover{transform:rotateY(-172deg);opacity:0;pointer-events:none}
  .face{position:absolute;inset:0;border-radius:28px;backface-visibility:hidden;-webkit-backface-visibility:hidden;overflow:hidden}
  .front{
    background:
      radial-gradient(circle at 25% 15%,rgba(255,150,190,.45),transparent 45%),
      radial-gradient(circle at 80% 90%,rgba(255,120,150,.35),transparent 50%),
      linear-gradient(145deg,#a3123f 0%,#6d0b2c 55%,#3f0618 100%);
    box-shadow:0 30px 70px rgba(0,0,0,.6);
    display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px;text-align:center}
  .back-face{transform:rotateY(180deg);background:linear-gradient(135deg,#fff5f0,#ffe6ee)}

  .foil{background:linear-gradient(110deg,var(--gold3) 0%,var(--gold1) 25%,var(--gold2) 45%,var(--gold1) 60%,var(--gold3) 100%);
    background-size:250% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;
    animation:shimmer 4s linear infinite}
  @keyframes shimmer{0%{background-position:150% 0}100%{background-position:-100% 0}}
  .c-small{font-size:12px;font-weight:500;letter-spacing:.5em;text-transform:uppercase;margin-bottom:18px;padding-left:.5em}
  .c-big{font-family:'DM Serif Display',serif;font-size:clamp(44px,13vw,64px);line-height:1.02;letter-spacing:-.01em}
  .c-name{font-family:'DM Serif Display',serif;font-style:italic;font-size:clamp(26px,7.5vw,34px);margin-top:6px}
  .c-heart{width:44px;margin:22px 0 14px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.4));animation:beat 1.8s ease-in-out infinite}
  @keyframes beat{0%,100%{transform:scale(1)}15%{transform:scale(1.14)}30%{transform:scale(1)}45%{transform:scale(1.1)}}
  .tap{position:absolute;bottom:34px;left:0;right:0;text-align:center;font-size:12px;font-weight:500;letter-spacing:.3em;text-transform:uppercase;color:#ffe3b0;
    animation:pulse 2.2s ease-in-out infinite}
  @keyframes pulse{0%,100%{opacity:.5}50%{opacity:1}}

  /* ───────── pages ───────── */
  .pages{position:absolute;inset:0}
  .page{position:absolute;inset:0;padding:38px 30px 84px 30px;display:flex;flex-direction:column;align-items:center;overflow-y:auto;
    opacity:0;pointer-events:none;transform:translateY(18px);transition:opacity .55s ease,transform .6s cubic-bezier(.2,.7,.2,1);
    scrollbar-width:thin;scrollbar-color:#e9a9bd transparent}
  .page.before{transform:translateY(-18px)}
  .page.active{opacity:1;pointer-events:auto;transform:none}
  .page::-webkit-scrollbar{width:4px}.page::-webkit-scrollbar-thumb{background:#e9a9bd;border-radius:4px}

  .title{font-family:'DM Serif Display',serif;font-size:clamp(26px,7.5vw,32px);line-height:1.15;text-align:center;color:var(--rose);margin-bottom:12px}
  .divider{width:34px;height:3px;border-radius:3px;background:#e58aa6;margin:0 0 20px;opacity:.7}
  .body{width:100%}
  .body p{font-size:clamp(14.5px,4vw,16px);line-height:1.8;text-align:left;margin-bottom:16px;color:var(--ink)}
  .reveal{opacity:0}
  .page.active .reveal{animation:rise .8s cubic-bezier(.2,.7,.2,1) both;animation-delay:calc(var(--i) * .3s + .2s)}
  @keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
  .sign{font-family:'Great Vibes',cursive;font-size:30px;color:var(--rose);text-align:right;width:100%;margin-top:2px}

  /* photo frame */
  .polaroid{position:relative;width:min(80%,300px);background:#fff;padding:8px 8px 10px;margin:0 0 22px;flex:none;border-radius:22px;
    box-shadow:0 14px 34px rgba(110,30,60,.22)}
  .polaroid .ph{width:100%;aspect-ratio:1/1;max-height:clamp(150px,32vh,270px);object-fit:cover;display:block;background:#f6dbe4;border-radius:15px}
  .polaroid .cap{text-align:center;font-family:'Caveat',cursive;font-size:22px;color:#7a3550;margin-top:6px;line-height:1}
  .placeholder{width:100%;aspect-ratio:1/1;max-height:clamp(150px,32vh,270px);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;border-radius:15px;
    background:linear-gradient(135deg,#ffd0de,#ffe8d6);color:#b0476b;font-family:'Caveat',cursive;font-size:21px}
  .placeholder svg{width:42px;opacity:.8}

  /* cake */
  .cake{width:min(62%,240px);margin:4px 0 6px;cursor:pointer;flex:none;filter:drop-shadow(0 12px 18px rgba(110,30,60,.25))}
  .flame{transform-origin:50% 100%;animation:flicker .18s ease-in-out infinite alternate;transition:opacity .35s,transform .35s}
  .flame:nth-of-type(2){animation-delay:.07s}.flame:nth-of-type(3){animation-delay:.12s}
  @keyframes flicker{from{transform:scale(1,1) rotate(-2deg)}to{transform:scale(.92,1.1) rotate(2deg)}}
  .blown .flame{opacity:0;transform:scale(0)}
  .smoke{opacity:0}
  .blown .smoke{animation:smoke 2.2s ease-out forwards}
  @keyframes smoke{0%{opacity:.7;transform:translateY(0)}100%{opacity:0;transform:translateY(-34px)}}
  .after{display:none}
  .blown ~ .after,.after.show{display:block}

  /* nav */
  .nav{position:absolute;left:0;right:0;bottom:0;height:70px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;z-index:10;
    background:linear-gradient(0deg,rgba(255,248,241,.98) 55%,rgba(255,248,241,0));opacity:0;pointer-events:none;transition:opacity .6s ease .7s}
  .card.opened .nav{opacity:1;pointer-events:auto}
  .nbtn{width:38px;height:38px;border-radius:50%;border:1.5px solid #f2bccb;background:#fff;color:var(--rose);font-size:20px;cursor:pointer;
    transition:transform .2s,opacity .2s;display:flex;align-items:center;justify-content:center}
  .nbtn:active{transform:scale(.9)}
  .nbtn[disabled]{opacity:.25;cursor:default}
  .dots{display:flex;gap:7px}
  .dot{width:7px;height:7px;border-radius:50%;background:#f2bccb;transition:all .35s}
  .dot.on{background:var(--rose);width:20px;border-radius:6px}

  /* ───────── extras ───────── */
  .star{position:absolute;border-radius:50%;background:#fff;pointer-events:none;animation:tw 3s ease-in-out infinite}
  @keyframes tw{0%,100%{opacity:.1;transform:scale(.6)}50%{opacity:.9;transform:scale(1.2)}}

  .seal{position:relative;width:96px;height:96px;margin:6px 0 0;border-radius:50%;display:flex;align-items:center;justify-content:center;
    background:radial-gradient(circle at 30% 25%,#fff6cf,#f1c766 38%,#c58a22 72%,#8a5a10);
    box-shadow:0 10px 24px rgba(0,0,0,.45),inset 0 -6px 12px rgba(120,70,0,.4);overflow:hidden}
  .seal::after{content:"";position:absolute;top:-30%;left:-60%;width:40%;height:160%;transform:rotate(25deg);
    background:linear-gradient(90deg,transparent,rgba(255,255,255,.65),transparent);animation:sweep 3.2s ease-in-out infinite}
  @keyframes sweep{0%{left:-60%}55%,100%{left:140%}}
  .seal span{position:relative;font-family:'DM Serif Display',serif;font-size:48px;color:#5b0f2e;line-height:1;margin-top:-6px}
  .seal small{position:absolute;bottom:17px;left:0;right:0;text-align:center;font-size:8.5px;letter-spacing:.28em;color:#5b0f2e;font-weight:700;text-transform:uppercase}

  .music{position:absolute;top:14px;right:14px;z-index:12;width:34px;height:34px;border-radius:50%;border:none;cursor:pointer;
    background:rgba(255,255,255,.85);color:var(--rose);font-size:17px;box-shadow:0 4px 10px rgba(180,30,80,.25)}
  .music.off{opacity:.55}

  .rgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;width:100%;margin:2px 0 14px}
  .rbtn{position:relative;aspect-ratio:1;border:none;background:none;cursor:pointer;color:#ffb3c8;transition:transform .2s,color .3s}
  .rbtn svg{width:100%;height:100%;fill:currentColor;filter:drop-shadow(0 3px 4px rgba(200,30,80,.25))}
  .rbtn span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:12.5px;font-weight:700;color:#fff;padding-bottom:2px}
  .rbtn:hover{transform:scale(1.12)}
  .rbtn.done{color:#e11d5a}
  .rbox{width:100%;min-height:96px;padding:14px 16px;background:rgba(255,255,255,.75);border:1.5px solid #f2bccb;border-radius:20px;
    text-align:center;line-height:1.6;font-size:15.5px;display:flex;align-items:center;justify-content:center}
  .rbox .pop{animation:popin .45s cubic-bezier(.2,1.4,.4,1) both}
  .rbox b{display:block;font-family:'DM Serif Display',serif;font-size:26px;color:var(--rose);font-weight:400;line-height:1.1}
  @keyframes popin{from{opacity:0;transform:scale(.8) translateY(8px)}to{opacity:1;transform:none}}
</style>
</head>
<body>
<div class="stage">
  <div class="glow"></div>

  <div class="card" id="card">
    <div class="inside">
      <div class="pages" id="pages"></div>
      <div class="nav">
        <button class="nbtn" id="prev" aria-label="Previous">&#8249;</button>
        <div class="dots" id="dots"></div>
        <button class="nbtn" id="next" aria-label="Next">&#8250;</button>
      </div>
    </div>

    <div class="cover" id="cover">
      <div class="face front">
        <div class="c-small foil">a card for you</div>
        <div class="c-big foil">Happy<br>Birthday</div>
        <svg class="c-heart" viewBox="0 0 24 24">
          <defs><linearGradient id="hg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff1b8"/><stop offset=".5" stop-color="#e8b74a"/><stop offset="1" stop-color="#a8741a"/></linearGradient></defs>
          <path fill="url(#hg)" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>
        <div class="c-name foil" id="cname"></div>
        <div class="seal"><span id="sealn">19</span><small>years</small></div>
        <div class="tap">tap to open</div>
      </div>
      <div class="face back-face"></div>
    </div>
  </div>
</div>
<div id="fx"></div>

<script>
const DATA = __DATA__;

const HEART_PATH = "M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z";
const COLORS = ["#ff4d88","#ff2e63","#ff85a8","#ff6f91","#f43f7a","#ffb3c8","#e11d5a","#ff9ec0","#ffd166"];
const fx = document.getElementById('fx');
document.getElementById('sealn').textContent = DATA.age;

/* twinkling stars */
(function () {
  const stage = document.querySelector('.stage');
  for (let i = 0; i < 50; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const z = 1 + Math.random() * 2;
    s.style.cssText = 'left:' + Math.random() * 100 + '%;top:' + Math.random() * 100 + '%;width:' + z + 'px;height:' + z + 'px;animation-delay:' + (Math.random() * 3) + 's;animation-duration:' + (2 + Math.random() * 3) + 's';
    stage.insertBefore(s, stage.firstChild);
  }
})();

/* confetti rain */
function confettiRain(n = 70) {
  const cols = ['#ff4d88', '#ffd166', '#fff', '#ff85a8', '#f1c766', '#ffb3c8'];
  for (let i = 0; i < n; i++) {
    const c = document.createElement('div');
    const w = 6 + Math.random() * 6;
    c.style.cssText = 'position:absolute;left:0;top:0;width:' + w + 'px;height:' + (w * 1.7) + 'px;background:' + cols[(Math.random() * cols.length) | 0] + ';border-radius:2px;opacity:.95';
    fx.appendChild(c);
    const x = Math.random() * innerWidth, sway = (Math.random() - .5) * 160;
    c.animate([
      { transform: 'translate(' + x + 'px,-20px) rotate(0deg)', opacity: 1 },
      { transform: 'translate(' + (x + sway) + 'px,' + (innerHeight + 30) + 'px) rotate(' + (360 + Math.random() * 720) + 'deg)', opacity: 1 }
    ], { duration: 2200 + Math.random() * 2200, delay: Math.random() * 900, easing: 'cubic-bezier(.3,.5,.6,1)' }).onfinish = () => c.remove();
  }
}

/* optional music (put song.mp3 next to app.py) */
let audio = null;
if (DATA.music) {
  audio = new Audio(DATA.music);
  audio.loop = true; audio.volume = .7;
  const mb = document.createElement('button');
  mb.className = 'music'; mb.innerHTML = '&#9835;';
  document.querySelector('.inside').appendChild(mb);
  mb.addEventListener('click', e => {
    e.stopPropagation();
    if (audio.paused) { audio.play(); mb.classList.remove('off'); } else { audio.pause(); mb.classList.add('off'); }
  });
}

/* ───────── heart bubbles ───────── */
function spawnHeart(x, y, opts = {}) {
  const size = opts.size || (16 + Math.random() * 30);
  const color = COLORS[(Math.random() * COLORS.length) | 0];
  const el = document.createElement('div');
  el.className = 'heart';
  el.style.width = el.style.height = size + 'px';
  el.innerHTML =
    '<svg viewBox="0 0 24 24" width="100%" height="100%">' +
    '<path d="' + HEART_PATH + '" fill="' + color + '" fill-opacity="' + (opts.faint ? .35 : .72) + '" stroke="#fff" stroke-opacity=".85" stroke-width=".7"/>' +
    '<path d="M6.2 6.6c.9-1.2 2.3-1.6 3.4-1" fill="none" stroke="#fff" stroke-opacity=".9" stroke-width="1.1" stroke-linecap="round"/>' +
    '<circle cx="5.6" cy="9.3" r=".8" fill="#fff" fill-opacity=".9"/></svg>';
  fx.appendChild(el);

  const rise = opts.rise || (140 + Math.random() * 280);
  const drift = (Math.random() - .5) * 160;
  const sway = 18 + Math.random() * 26;
  const rot = (Math.random() - .5) * 50;
  const dur = opts.dur || (2400 + Math.random() * 2200);
  const x0 = x - size / 2, y0 = y - size / 2;
  const pos = (t, dx, dy, s, r) => 'translate(' + (x0 + dx) + 'px,' + (y0 - dy) + 'px) scale(' + s + ') rotate(' + r + 'deg)';

  const anim = el.animate([
    { transform: pos(0, 0, 0, .2, 0), opacity: 0 },
    { transform: pos(0, drift * .15 + sway * .5, rise * .12, 1, rot * .3), opacity: 1, offset: .12 },
    { transform: pos(0, drift * .45 - sway, rise * .45, 1.05, rot * .7), opacity: .95, offset: .45 },
    { transform: pos(0, drift * .75 + sway, rise * .78, 1.1, rot), opacity: .8, offset: .75 },
    { transform: pos(0, drift, rise, 1.35, rot * 1.2), opacity: 0 }
  ], { duration: dur, easing: 'cubic-bezier(.3,.6,.4,1)', fill: 'forwards', delay: opts.delay || 0 });
  anim.onfinish = () => el.remove();
}

function burst(x, y, n = 8) {
  for (let i = 0; i < n; i++) {
    const a = Math.random() * Math.PI * 2, r = Math.random() * 26;
    spawnHeart(x + Math.cos(a) * r, y + Math.sin(a) * r, { delay: Math.random() * 220 });
  }
}

/* click / tap ANYWHERE */
document.addEventListener('pointerdown', e => burst(e.clientX, e.clientY));

/* ambient hearts drifting up from the bottom */
setInterval(() => {
  if (document.hidden) return;
  spawnHeart(Math.random() * innerWidth, innerHeight + 10,
    { size: 10 + Math.random() * 16, faint: true, rise: innerHeight * (.5 + Math.random() * .6), dur: 6500 + Math.random() * 3500 });
}, 1200);

function confettiShower(ms = 3500) {
  const t0 = performance.now();
  const id = setInterval(() => {
    if (performance.now() - t0 > ms) return clearInterval(id);
    for (let i = 0; i < 3; i++)
      spawnHeart(Math.random() * innerWidth, innerHeight + 10,
        { size: 16 + Math.random() * 32, rise: innerHeight * (.7 + Math.random() * .6), dur: 2800 + Math.random() * 1800 });
  }, 120);
}

/* ───────── build pages ───────── */
document.getElementById('cname').textContent = DATA.her;

const pagesEl = document.getElementById('pages');
const dotsEl = document.getElementById('dots');

function el(tag, cls, text) {
  const d = document.createElement(tag);
  if (cls) d.className = cls;
  if (text != null) d.textContent = text;
  return d;
}
function paragraphs(text, startIdx = 1) {
  const body = el('div', 'body');
  (text || '').split(/\n\s*\n/).forEach((t, i) => {
    const p = el('p', 'reveal', t.trim());
    p.style.setProperty('--i', startIdx + i);
    body.appendChild(p);
  });
  return body;
}

const heartIcon = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="' + HEART_PATH + '"/></svg>';

DATA.pages.forEach((pg, i) => {
  const page = el('section', 'page');

  if (pg.type === 'photo') {
    const pol = el('div', 'polaroid reveal');
    pol.style.setProperty('--i', 0);
    if (pg.photo_uri) {
      const img = document.createElement('img');
      img.className = 'ph'; img.src = pg.photo_uri; img.alt = '';
      pol.appendChild(img);
    } else {
      const ph = el('div', 'placeholder');
      ph.innerHTML = heartIcon + '<span>your photo here</span>';
      pol.appendChild(ph);
    }
    pol.appendChild(el('div', 'cap', pg.caption || ''));
    page.appendChild(pol);
  }

  const title = el('div', 'title reveal', pg.title || '');
  title.style.setProperty('--i', 1);
  page.appendChild(title);
  const dv = el('div', 'divider reveal');
  dv.style.setProperty('--i', 2);
  page.appendChild(dv);

  if (pg.type === 'reasons') {
    page.appendChild(paragraphs(pg.text, 3));
    const grid = el('div', 'rgrid reveal'); grid.style.setProperty('--i', 4);
    const box = el('div', 'rbox reveal'); box.style.setProperty('--i', 5);
    const first = el('div', 'pop', 'tap a heart \u2661');
    box.appendChild(first);
    (pg.reasons || []).forEach((r, k) => {
      const b = el('button', 'rbtn');
      b.innerHTML = '<svg viewBox="0 0 24 24"><path d="' + HEART_PATH + '"/></svg><span>' + (k + 1) + '</span>';
      b.addEventListener('click', () => {
        b.classList.add('done');
        box.innerHTML = '';
        const inner = el('div', 'pop');
        inner.appendChild(el('b', null, '#' + (k + 1)));
        inner.appendChild(el('div', null, r));
        box.appendChild(inner);
      });
      grid.appendChild(b);
    });
    page.appendChild(grid);
    page.appendChild(box);
  } else if (pg.type === 'final') {
    const hint = paragraphs(pg.text, 3);
    page.appendChild(hint);

    const cake = el('div', 'cake reveal'); cake.style.setProperty('--i', 4);
    cake.innerHTML =
      '<svg viewBox="0 0 240 230" width="100%">' +
      '<ellipse cx="120" cy="212" rx="108" ry="12" fill="#e8c3cf"/>' +
      '<rect x="30" y="140" width="180" height="70" rx="14" fill="#ff9ab7"/>' +
      '<path d="M30 156c15 14 25-6 40 6s25-8 40 6 25-8 40 6 25-8 40 6v-30H30z" fill="#fff"/>' +
      '<rect x="62" y="92" width="116" height="56" rx="12" fill="#ff6f9c"/>' +
      '<path d="M62 106c12 12 20-4 32 6s20-8 32 4 20-8 32 4 14-4 20 2v-14H62z" fill="#fff4f7"/>' +
      '<circle cx="60" cy="176" r="5" fill="#ffd166"/><circle cx="100" cy="186" r="5" fill="#fff"/><circle cx="145" cy="176" r="5" fill="#ffd166"/><circle cx="182" cy="188" r="5" fill="#fff"/>' +
      '<g fill="#ffe08a"><rect x="86" y="62" width="9" height="32" rx="3" fill="#7cc6ff"/><rect x="116" y="58" width="9" height="36" rx="3" fill="#ffd166"/><rect x="146" y="62" width="9" height="32" rx="3" fill="#b9f0a8"/></g>' +
      '<ellipse class="flame" cx="90.5" cy="52" rx="6" ry="11" fill="#ffb347"/><ellipse class="flame" cx="120.5" cy="48" rx="6" ry="11" fill="#ffb347"/><ellipse class="flame" cx="150.5" cy="52" rx="6" ry="11" fill="#ffb347"/>' +
      '<g class="smoke" stroke="#c9b3bb" stroke-width="2" fill="none" stroke-linecap="round"><path d="M90 52c-6-8 6-12 0-20"/><path d="M120 48c-6-8 6-12 0-20"/><path d="M150 52c-6-8 6-12 0-20"/></g>' +
      '</svg>';
    page.appendChild(cake);

    const after = paragraphs(pg.after, 0);
    after.classList.add('after');
    after.style.marginTop = '8px';
    page.appendChild(after);
    const sign = el('div', 'sign', DATA.you);
    sign.style.display = 'none';
    page.appendChild(sign);

    let blown = false;
    cake.addEventListener('click', () => {
      if (blown) return; blown = true;
      cake.classList.add('blown');
      hint.style.display = 'none';
      after.classList.add('show'); after.style.display = 'block';
      after.querySelectorAll('p').forEach((p, k) => { p.style.animation = 'rise .9s cubic-bezier(.2,.7,.2,1) both'; p.style.animationDelay = (k * .5 + .4) + 's'; });
      sign.style.display = 'block'; sign.classList.add('reveal'); sign.style.setProperty('--i', 4);
      confettiShower(4200);
      confettiRain(110);
      setTimeout(() => page.scrollTo({ top: page.scrollHeight, behavior: 'smooth' }), 600);
    });
  } else {
    page.appendChild(paragraphs(pg.text, 3));
    if (pg.type === 'letter' && i === DATA.pages.length - 2) {
      const sign = el('div', 'sign reveal', DATA.you);
      sign.style.setProperty('--i', 7);
      page.appendChild(sign);
    }
  }

  pagesEl.appendChild(page);
  dotsEl.appendChild(el('div', 'dot'));
});

/* ───────── navigation ───────── */
const card = document.getElementById('card');
const pageEls = [...document.querySelectorAll('.page')];
const dotEls = [...document.querySelectorAll('.dot')];
const prev = document.getElementById('prev'), next = document.getElementById('next');
let idx = 0, opened = false;

function show(n) {
  idx = Math.max(0, Math.min(pageEls.length - 1, n));
  pageEls.forEach((p, i) => {
    p.classList.toggle('active', i === idx);
    p.classList.toggle('before', i < idx);
  });
  dotEls.forEach((d, i) => d.classList.toggle('on', i === idx));
  prev.disabled = idx === 0;
  next.disabled = idx === pageEls.length - 1;
  if (pageEls[idx]) pageEls[idx].scrollTop = 0;
}
function openCard() {
  if (opened) return; opened = true;
  card.classList.add('opened');
  if (audio) audio.play().catch(() => {});
  confettiRain(60);
  show(0);
  setTimeout(() => confettiShower(1800), 500);
}
document.getElementById('cover').addEventListener('click', openCard);
prev.addEventListener('click', () => show(idx - 1));
next.addEventListener('click', () => show(idx + 1));
document.addEventListener('keydown', e => {
  if (!opened) { if (e.key === 'Enter' || e.key === ' ') openCard(); return; }
  if (e.key === 'ArrowRight') show(idx + 1);
  if (e.key === 'ArrowLeft') show(idx - 1);
});
let sx = null;
card.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
card.addEventListener('touchend', e => {
  if (!opened || sx == null) return;
  const dx = e.changedTouches[0].clientX - sx;
  if (Math.abs(dx) > 60) show(idx + (dx < 0 ? 1 : -1));
  sx = null;
});
show(0);
</script>
</body>
</html>
"""

payload = json.dumps(DATA).replace("</", "<\\/")
components.html(HTML.replace("__DATA__", payload), height=820, scrolling=False)
