import base64
import json
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ════════════════════════════════════════════════════════════════
#  ✏️  EDIT THIS PART  —  names, photos and your words
# ════════════════════════════════════════════════════════════════
HER_NAME = "My Love"          # her name / nickname on the cover
YOUR_NAME = "Yours, always"   # how you sign off (e.g. "Forever yours, Rahul")

# Put your photos in a folder called  photos/  next to this file,
# then use the file names below (jpg / png / webp).
# Type "photo"  -> polaroid photo + long message
# Type "letter" -> only words
# The last page ("final") is the cake & wish page.
PAGES = [
    {
        "type": "letter",
        "title": "Happy Birthday, my everything",
        "text": (
            "Today the world celebrates the day you were born, and honestly, "
            "I celebrate it more than anyone. Because somewhere in all the "
            "chaos of this universe, you were created, and somehow, "
            "unbelievably, you became mine.\n\n"
            "I made this little card for you because a text message felt too "
            "small for everything I feel. So take your time, turn the pages, "
            "and know that every single word here is true."
        ),
    },
    {
        "type": "photo",
        "photo": "1.jpg",
        "caption": "us, being us ♡",
        "title": "The day everything changed",
        "text": (
            "I still remember how nervous I was, and how the moment I saw you "
            "everything else just went quiet. I didn't know it then, but my "
            "life was quietly turning a corner towards you.\n\n"
            "You walked in and made ordinary days feel like little movies. "
            "I have been falling for you ever since, and I never want to "
            "stop."
        ),
    },
    {
        "type": "photo",
        "photo": "2.jpg",
        "caption": "my favourite smile",
        "title": "Your smile is my favourite place",
        "text": (
            "There is a specific way you smile when you think nobody is "
            "watching, and it is the most beautiful thing I have ever seen. "
            "It fixes my worst days without even trying.\n\n"
            "If I could keep only one thing in this life, I would keep that "
            "smile, and I would spend my whole life making sure it never "
            "goes away."
        ),
    },
    {
        "type": "photo",
        "photo": "3.jpg",
        "caption": "no one else but you",
        "title": "Why it will always be you",
        "text": (
            "You are the first person I want to tell good news to, and the "
            "only one I want beside me when the news is bad. You make me "
            "braver, softer and happier than I knew I could be.\n\n"
            "Out of every person in the world, in every version of every "
            "story, I would choose you. Again, and again, and again."
        ),
    },
    {
        "type": "letter",
        "title": "A little promise",
        "text": (
            "I promise to hold your hand through the loud days and the quiet "
            "ones. To laugh at your jokes even when they are terrible, and to "
            "listen when you just need someone to listen.\n\n"
            "I promise to keep choosing you, every morning, for as long as "
            "I get mornings. You are not just my girlfriend. You are my "
            "best friend, my home, and my favourite person.\n\n"
            "Thank you for being you. Thank you for loving me."
        ),
    },
    {
        "type": "final",
        "title": "Make a wish, my love",
        "text": "Tap the candles to blow them out.",
        "after": (
            "I hope every wish you made just came true. "
            "And if it didn't, give me a little time. "
            "I'll spend my whole life working on it.\n\n"
            "I love you more than words, more than this card, "
            "more than all the hearts on this screen. "
            "Happy Birthday, my love. ♡"
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

DATA = {"her": HER_NAME, "you": YOUR_NAME, "pages": pages_payload}

HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Great+Vibes&family=Playfair+Display:ital,wght@0,500;0,700;1,500&display=swap" rel="stylesheet">
<style>
  :root{
    --rose:#e11d5a; --blush:#ffd9e4; --wine:#5b0f2e; --gold1:#fff1b8; --gold2:#e8b74a; --gold3:#a8741a;
    --paper:#fff8f1; --ink:#4a2432;
  }
  *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
  html,body{height:100%;background:transparent;overflow:hidden;font-family:'Playfair Display',serif;color:var(--ink);user-select:none}
  .stage{position:relative;width:100%;height:100vh;display:flex;align-items:center;justify-content:center;overflow:hidden}

  /* floating sparkles in background */
  .glow{position:absolute;inset:0;pointer-events:none;
    background:
      radial-gradient(circle at 15% 20%,rgba(255,120,170,.18),transparent 40%),
      radial-gradient(circle at 85% 80%,rgba(255,190,120,.14),transparent 45%);}

  #fx{position:fixed;inset:0;pointer-events:none;z-index:100;overflow:hidden}
  .heart{position:absolute;left:0;top:0;will-change:transform,opacity;filter:drop-shadow(0 2px 6px rgba(255,60,120,.35))}

  /* ───────── card ───────── */
  .card{position:relative;width:min(92vw,430px);height:min(94vh,700px);perspective:1800px;animation:float 5s ease-in-out infinite}
  .card.opened{animation:none}
  @keyframes float{0%,100%{transform:translateY(0) rotate(-.4deg)}50%{transform:translateY(-8px) rotate(.4deg)}}

  .inside{position:absolute;inset:0;border-radius:6px 16px 16px 6px;overflow:hidden;
    background:
      radial-gradient(circle at 10% 0%,rgba(255,200,215,.35),transparent 40%),
      radial-gradient(circle at 100% 100%,rgba(255,220,180,.35),transparent 45%),
      linear-gradient(135deg,#fffaf4,#fff1ea);
    box-shadow:0 30px 70px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.4) inset;}
  .inside::before{content:"";position:absolute;left:0;top:0;bottom:0;width:18px;z-index:3;pointer-events:none;
    background:linear-gradient(90deg,rgba(120,40,70,.22),transparent)}

  /* cover */
  .cover{position:absolute;inset:0;transform-origin:left center;transform-style:preserve-3d;
    transition:transform 1.4s cubic-bezier(.65,0,.2,1),opacity .5s ease 1.0s;cursor:pointer;z-index:20}
  .card.opened .cover{transform:rotateY(-172deg);opacity:0;pointer-events:none}
  .face{position:absolute;inset:0;border-radius:6px 16px 16px 6px;backface-visibility:hidden;-webkit-backface-visibility:hidden;overflow:hidden}
  .front{
    background:
      radial-gradient(circle at 25% 15%,rgba(255,150,190,.45),transparent 45%),
      radial-gradient(circle at 80% 90%,rgba(255,120,150,.35),transparent 50%),
      linear-gradient(145deg,#a3123f 0%,#6d0b2c 55%,#3f0618 100%);
    box-shadow:0 30px 70px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.12) inset;
    display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px;text-align:center}
  .front::before{content:"";position:absolute;inset:14px;border:1.5px solid rgba(255,215,130,.75);border-radius:4px 12px 12px 4px;pointer-events:none}
  .front::after{content:"";position:absolute;inset:22px;border:1px dashed rgba(255,215,130,.35);border-radius:3px 10px 10px 3px;pointer-events:none}
  .spine{position:absolute;left:0;top:0;bottom:0;width:16px;background:linear-gradient(90deg,rgba(0,0,0,.45),transparent);z-index:2}
  .back-face{transform:rotateY(180deg);background:linear-gradient(135deg,#fff5f0,#ffe6ee)}

  .foil{background:linear-gradient(110deg,var(--gold3) 0%,var(--gold1) 25%,var(--gold2) 45%,var(--gold1) 60%,var(--gold3) 100%);
    background-size:250% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;
    animation:shimmer 3.5s linear infinite;filter:drop-shadow(0 2px 3px rgba(0,0,0,.35))}
  @keyframes shimmer{0%{background-position:150% 0}100%{background-position:-100% 0}}
  .c-small{font-size:13px;letter-spacing:.45em;text-transform:uppercase;margin-bottom:10px}
  .c-big{font-family:'Great Vibes',cursive;font-size:clamp(52px,16vw,76px);line-height:1}
  .c-name{font-family:'Great Vibes',cursive;font-size:clamp(30px,9vw,42px);margin-top:14px}
  .c-heart{width:92px;margin:22px 0 8px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.4));animation:beat 1.6s ease-in-out infinite}
  @keyframes beat{0%,100%{transform:scale(1)}15%{transform:scale(1.14)}30%{transform:scale(1)}45%{transform:scale(1.1)}}
  .tap{position:absolute;bottom:38px;left:0;right:0;text-align:center;font-family:'Caveat',cursive;font-size:23px;color:#ffe3b0;
    letter-spacing:.04em;animation:pulse 2s ease-in-out infinite}
  @keyframes pulse{0%,100%{opacity:.55;transform:translateY(0)}50%{opacity:1;transform:translateY(-3px)}}
  .corner{position:absolute;width:44px;height:44px;opacity:.9}
  .corner.tl{top:22px;left:26px}.corner.tr{top:22px;right:18px;transform:scaleX(-1)}
  .corner.bl{bottom:22px;left:26px;transform:scaleY(-1)}.corner.br{bottom:22px;right:18px;transform:scale(-1,-1)}

  /* ───────── pages ───────── */
  .pages{position:absolute;inset:0}
  .page{position:absolute;inset:0;padding:30px 26px 74px 34px;display:flex;flex-direction:column;align-items:center;overflow-y:auto;
    opacity:0;pointer-events:none;transform:translateX(40px) scale(.98);transition:opacity .6s ease,transform .7s cubic-bezier(.2,.7,.2,1);
    scrollbar-width:thin;scrollbar-color:#e9a9bd transparent}
  .page.before{transform:translateX(-40px) scale(.98)}
  .page.active{opacity:1;pointer-events:auto;transform:none}
  .page::-webkit-scrollbar{width:4px}.page::-webkit-scrollbar-thumb{background:#e9a9bd;border-radius:4px}

  .title{font-family:'Great Vibes',cursive;font-size:clamp(34px,10vw,46px);line-height:1.1;text-align:center;color:var(--rose);margin-bottom:6px}
  .divider{display:flex;align-items:center;gap:8px;margin:6px 0 16px;width:70%;color:#e58aa6}
  .divider i{flex:1;height:1px;background:linear-gradient(90deg,transparent,#e58aa6,transparent)}
  .divider svg{width:14px;height:14px}
  .body p{font-size:clamp(14.5px,4.1vw,16.5px);line-height:1.85;text-align:center;margin-bottom:14px;color:var(--ink);font-style:italic}
  .reveal{opacity:0}
  .page.active .reveal{animation:rise .9s cubic-bezier(.2,.7,.2,1) both;animation-delay:calc(var(--i) * .35s + .25s)}
  @keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
  .sign{font-family:'Great Vibes',cursive;font-size:30px;color:var(--rose);text-align:right;width:100%;margin-top:4px}

  /* polaroid */
  .polaroid{position:relative;width:min(78%,300px);background:#fff;padding:10px 10px 38px;margin:6px 0 20px;flex:none;
    box-shadow:0 14px 30px rgba(110,30,60,.28),0 2px 6px rgba(0,0,0,.12);transform:rotate(-2.2deg);transition:transform .4s}
  .polaroid:nth-child(odd){transform:rotate(2deg)}
  .polaroid .ph{width:100%;aspect-ratio:1/1;max-height:clamp(150px,34vh,280px);object-fit:cover;display:block;background:#f6dbe4}
  .polaroid .cap{position:absolute;left:0;right:0;bottom:7px;text-align:center;font-family:'Caveat',cursive;font-size:23px;color:#7a3550}
  .tape{position:absolute;top:-13px;left:50%;width:84px;height:26px;transform:translateX(-50%) rotate(-3deg);
    background:repeating-linear-gradient(45deg,rgba(255,200,215,.85) 0 6px,rgba(255,225,232,.85) 6px 12px);box-shadow:0 1px 3px rgba(0,0,0,.15)}
  .placeholder{width:100%;aspect-ratio:1/1;max-height:clamp(150px,34vh,280px);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;
    background:linear-gradient(135deg,#ffd0de,#ffe8d6);color:#b0476b;font-family:'Caveat',cursive;font-size:21px}
  .placeholder svg{width:46px;opacity:.8}

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
  .nav{position:absolute;left:0;right:0;bottom:0;height:62px;display:flex;align-items:center;justify-content:space-between;padding:0 16px 0 24px;z-index:10;
    background:linear-gradient(0deg,rgba(255,248,241,.98) 55%,rgba(255,248,241,0));opacity:0;pointer-events:none;transition:opacity .6s ease .8s}
  .card.opened .nav{opacity:1;pointer-events:auto}
  .nbtn{width:40px;height:40px;border-radius:50%;border:none;background:linear-gradient(145deg,#f43f7a,#c0124d);color:#fff;font-size:20px;cursor:pointer;
    box-shadow:0 6px 14px rgba(200,20,80,.35);transition:transform .2s,opacity .2s;display:flex;align-items:center;justify-content:center}
  .nbtn:active{transform:scale(.9)}
  .nbtn[disabled]{opacity:.25;box-shadow:none;cursor:default}
  .dots{display:flex;gap:7px}
  .dot{width:8px;height:8px;border-radius:50%;background:#f2bccb;transition:all .35s}
  .dot.on{background:var(--rose);width:22px;border-radius:6px}
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
        <div class="spine"></div>
        <svg class="corner tl" viewBox="0 0 44 44" fill="none" stroke="#f1c766" stroke-width="1.4"><path d="M2 42V14C2 7 7 2 14 2h28"/><path d="M10 42V18c0-5 3-8 8-8h24" opacity=".6"/><circle cx="14" cy="14" r="2.5" fill="#f1c766"/></svg>
        <svg class="corner tr" viewBox="0 0 44 44" fill="none" stroke="#f1c766" stroke-width="1.4"><path d="M2 42V14C2 7 7 2 14 2h28"/><path d="M10 42V18c0-5 3-8 8-8h24" opacity=".6"/><circle cx="14" cy="14" r="2.5" fill="#f1c766"/></svg>
        <svg class="corner bl" viewBox="0 0 44 44" fill="none" stroke="#f1c766" stroke-width="1.4"><path d="M2 42V14C2 7 7 2 14 2h28"/><path d="M10 42V18c0-5 3-8 8-8h24" opacity=".6"/><circle cx="14" cy="14" r="2.5" fill="#f1c766"/></svg>
        <svg class="corner br" viewBox="0 0 44 44" fill="none" stroke="#f1c766" stroke-width="1.4"><path d="M2 42V14C2 7 7 2 14 2h28"/><path d="M10 42V18c0-5 3-8 8-8h24" opacity=".6"/><circle cx="14" cy="14" r="2.5" fill="#f1c766"/></svg>

        <div class="c-small foil">a card for you</div>
        <div class="c-big foil">Happy<br>Birthday</div>
        <svg class="c-heart" viewBox="0 0 24 24">
          <defs><linearGradient id="hg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff1b8"/><stop offset=".5" stop-color="#e8b74a"/><stop offset="1" stop-color="#a8741a"/></linearGradient></defs>
          <path fill="url(#hg)" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>
        <div class="c-name foil" id="cname"></div>
        <div class="tap">tap to open &#9825;</div>
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

function burst(x, y, n = 11) {
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
}, 900);

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
const dividerHTML = '<div class="divider"><i></i><svg viewBox="0 0 24 24" fill="currentColor"><path d="' + HEART_PATH + '"/></svg><i></i></div>';

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
  const isLast = i === DATA.pages.length - 1;

  if (pg.type === 'photo') {
    const pol = el('div', 'polaroid reveal');
    pol.style.setProperty('--i', 0);
    pol.appendChild(el('div', 'tape'));
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
  const dv = el('div'); dv.innerHTML = dividerHTML; dv.firstChild.classList.add('reveal'); dv.firstChild.style.setProperty('--i', 2);
  page.appendChild(dv.firstChild);

  if (pg.type === 'final') {
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
