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
            "Today the world celebrates the day it got you, and nobody "
            "celebrates it more than I do.\n\n"
            "We have never met, but you are the most real thing in my life. "
            "A text message felt far too small for everything I feel, so I "
            "made this card for you. Take your time and turn the pages. "
            "Every single word here is true."
        ),
    },
    {
        "type": "photo",
        "photo": "1.jpg",
        "caption": "my little goblin ♡",
        "title": "January, on Discord",
        "text": (
            "Back then, I had no one. Then in January you walked into my "
            "life through a screen, and I had no idea how much was about "
            "to change.\n\n"
            "Somehow a stranger on Discord became the person I wanted to "
            "tell everything to. You didn't just come into my life. You "
            "made it start."
        ),
    },
    {
        "type": "letter",
        "title": "Every day since",
        "text": (
            "We started talking every single day, and I never got tired "
            "of it. We were dating for a bit, and then on the 20th you "
            "officially became mine.\n\n"
            "I still can't believe how lucky I am. Some people spend their "
            "whole lives looking for someone like you. I got a rude, "
            "loud, beautiful girlfriend who somehow chose me back."
        ),
    },
    {
        "type": "photo",
        "photo": "2.jpg",
        "caption": "rude, but only for me",
        "title": "My rude little goblin",
        "text": (
            "You are rude, you are stubborn, you are chaos in the "
            "cutest way, and I love every bit of it. You are my little "
            "goblin and nobody else gets to have that title.\n\n"
            "And when you get mad at me, I feel broken. Nothing feels "
            "right until we are okay again, because I don't want anything "
            "in this world but you."
        ),
    },
    {
        "type": "photo",
        "photo": "3.jpg",
        "caption": "my cappuccino",
        "title": "You feel like home",
        "text": (
            "You are my cappuccino: warm, a little bitter sometimes, and "
            "the best part of every single morning.\n\n"
            "I have never met you, but you make me feel like home. "
            "A place I never had until you showed up. Wherever you are "
            "is where I want to be."
        ),
    },
    {
        "type": "reasons",
        "title": "19 reasons I love you",
        "text": "One for every year of you. Tap each heart.",
        "reasons": [
            "You came into my life when I had no one.",
            "The way you laugh with your whole face.",
            "Your rudeness. I would not trade it for anything.",
            "You make me feel like home.",
            "You are my cappuccino, my favourite part of the day.",
            "How you fix my bad days without trying.",
            "Your stubborn streak. I secretly love it.",
            "The way you care about the little things.",
            "How you believe in me.",
            "Your terrible jokes that I still laugh at.",
            "Your long messages and your voice notes.",
            "How brave you are, even when you're scared.",
            "The hug I'm saving for the day we finally meet.",
            "How you make me want to be better.",
            "Everything I have is because of you.",
            "Every day we have talked since January.",
            "Even your angry face. Especially your angry face.",
            "That you chose me.",
            "Because you are you, my little goblin, and you're mine.",
        ],
    },
    {
        "type": "letter",
        "title": "Everything I have",
        "text": (
            "Everything I have in my life today is because of you. "
            "The smiles, the hope, the reasons to wake up. All of it "
            "started the day you showed up.\n\n"
            "I am so grateful. Someone out there can be this lucky to have "
            "a girlfriend like you, and I am that someone. Thank you for "
            "staying, for loving me, and for being my home."
        ),
    },
    {
        "type": "bengali",
        "title": "In the language of my heart",
        "bengali": "আমি তোমাকে ভালোবাসি, প্রেরণা",
        "translit": "Ami tomake bhalobashi, Prerana",
        "meaning": "I love you, Prerana.",
        "text": (
            "I could say it in any language, but this one feels the "
            "closest to my heart."
        ),
    },
    {
        "type": "letter",
        "title": "To the moon and back",
        "text": (
            "I love you to the moon and back, and I promise to keep "
            "loving you even when you're mad at me, even when you're "
            "rude, and most of all on the days you need it the most.\n\n"
            "My love is always yours, and it always will be. "
            "One day I will hold your hand for real, and until then "
            "I will keep choosing you every single morning.\n\n"
            "You are not just my girlfriend. You are my best friend, my "
            "home, and my favourite person."
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
            "more than all the hearts on this screen.\n\n"
            "আমি তোমাকে ভালোবাসি, প্রেরণা. "
            "Happy 19th Birthday, my little goblin. ♡"
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
        background:
            radial-gradient(ellipse 55% 40% at 14% 18%, rgba(225,29,90,.38), transparent 70%),
            radial-gradient(ellipse 45% 38% at 86% 78%, rgba(255,150,120,.24), transparent 70%),
            radial-gradient(ellipse 38% 30% at 74% 14%, rgba(170,60,140,.30), transparent 70%),
            radial-gradient(ellipse 34% 26% at 22% 86%, rgba(255,120,170,.20), transparent 70%),
            linear-gradient(118deg, transparent 34%, rgba(255,160,190,.09) 46%, rgba(255,215,130,.13) 50%, rgba(255,160,190,.09) 54%, transparent 66%),
            radial-gradient(circle at 20% 10%, #5a1030 0%, #2a0716 45%, #14030b 100%);
    }}
    .stApp::before {{
        content: ""; position: fixed; inset: 0; z-index: 0; pointer-events: none;
        background-image:
            radial-gradient(1.2px 1.2px at 20px 30px, #fff, transparent),
            radial-gradient(1px 1px at 90px 140px, #ffe3b0, transparent),
            radial-gradient(1.5px 1.5px at 160px 70px, #fff, transparent),
            radial-gradient(1px 1px at 50px 90px, #ffd9e4, transparent),
            radial-gradient(1.3px 1.3px at 210px 190px, #fff, transparent),
            radial-gradient(1px 1px at 130px 250px, #ffe3b0, transparent),
            radial-gradient(1.8px 1.8px at 120px 40px, #fff1b8, transparent),
            radial-gradient(2.2px 2.2px at 330px 260px, #fff, transparent);
        background-size: 220px 220px, 220px 220px, 220px 220px, 330px 330px, 330px 330px, 330px 330px, 470px 470px, 470px 470px;
        animation: twinkleBg 5s ease-in-out infinite alternate;
    }}
    .stApp::after {{
        content: ""; position: fixed; top: 12%; left: -10%; width: 150px; height: 2px; z-index: 0; pointer-events: none;
        background: linear-gradient(90deg, transparent, #fff1b8);
        border-radius: 2px; opacity: 0;
        animation: shootBg 11s ease-in infinite;
    }}
    @keyframes twinkleBg {{ from {{ opacity: .55; }} to {{ opacity: 1; }} }}
    @keyframes shootBg {{
        0%, 88% {{ opacity: 0; transform: translate(0, 0) rotate(25deg); }}
        90% {{ opacity: 1; }}
        100% {{ opacity: 0; transform: translate(120vw, 56vw) rotate(25deg); }}
    }}
    .block-container {{ position: relative; z-index: 1; }}
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
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=DM+Sans:wght@400;500;700&family=DM+Serif+Display:ital@0;1&family=Great+Vibes&family=Noto+Serif+Bengali:wght@500;700&display=swap" rel="stylesheet">
<style>
  :root{
    --rose:#e11d5a; --blush:#ffd9e4; --wine:#5b0f2e; --gold1:#fff1b8; --gold2:#e8b74a; --gold3:#a8741a;
    --paper:#fff8f1; --ink:#4a2432;
  }
  *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
  html,body{height:100%;background:transparent;overflow:hidden;font-family:'DM Sans','Noto Serif Bengali',sans-serif;color:var(--ink);user-select:none}
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
  .bn{font-family:'Noto Serif Bengali','DM Serif Display',serif;font-size:clamp(26px,7.5vw,32px);line-height:1.5;text-align:center;color:var(--rose);margin:6px 0 4px}
  .bn-tr{font-family:'DM Serif Display',serif;font-style:italic;font-size:19px;text-align:center;color:#7a3550;margin-bottom:4px}
  .bn-mean{font-family:'Caveat',cursive;font-size:24px;text-align:center;color:#7a3550;margin-bottom:22px}
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

  .title{font-family:'DM Serif Display','Noto Serif Bengali',serif;font-size:clamp(26px,7.5vw,32px);line-height:1.15;text-align:center;color:var(--rose);margin-bottom:12px}
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

  /* ═════════ CRAZY MODE ═════════ */
  @property --a{syntax:'<angle>';initial-value:0deg;inherits:false}
  .tilt{transition:transform .2s ease-out;will-change:transform}
  .card{animation:floaty 6s ease-in-out infinite}
  .card.opened{animation:floaty2 5s ease-in-out infinite}
  @keyframes floaty{0%,100%{transform:translateY(0) rotate(-1.4deg)}50%{transform:translateY(-16px) rotate(1.4deg)}}
  @keyframes floaty2{0%,100%{transform:translateY(0) rotate(-.5deg)}50%{transform:translateY(-7px) rotate(.5deg)}}
  .card::before{content:"";position:absolute;inset:-4px;border-radius:34px;z-index:-1;
    background:conic-gradient(from var(--a),#e11d5a,#e8b74a,#fff1b8,#ff85a8,#e11d5a);
    filter:blur(14px);opacity:.9;animation:ring 4s linear infinite}
  @keyframes ring{to{--a:360deg}}

  .orb{position:absolute;width:300px;height:300px;border-radius:50%;pointer-events:none;filter:blur(30px);opacity:.6}
  .orb.o1{left:calc(50% - 280px);top:6%;background:radial-gradient(circle,rgba(225,29,90,.65),transparent 68%);animation:drift1 9s ease-in-out infinite}
  .orb.o2{left:calc(50% - 20px);bottom:2%;background:radial-gradient(circle,rgba(232,183,74,.5),transparent 68%);animation:drift2 11s ease-in-out infinite}
  .orb.o3{left:calc(50% - 150px);top:36%;background:radial-gradient(circle,rgba(255,133,168,.5),transparent 68%);animation:drift1 13s ease-in-out infinite reverse}
  @keyframes drift1{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(40px,60px) scale(1.25)}}
  @keyframes drift2{0%,100%{transform:translate(0,0) scale(1.1)}50%{transform:translate(-50px,-60px) scale(.85)}}

  .spark{position:absolute;left:0;top:0;color:#ffe08a;text-shadow:0 0 8px #ffb347;pointer-events:none;will-change:transform,opacity}
  .shake{animation:shake .7s}
  @keyframes shake{0%,100%{transform:none}15%{transform:translate(-9px,5px) rotate(-1deg)}30%{transform:translate(8px,-6px) rotate(1deg)}45%{transform:translate(-7px,-4px)}60%{transform:translate(6px,5px)}80%{transform:translate(-3px,2px)}}

  .c-big div{white-space:nowrap}
  .jl{display:inline-block}
  @keyframes jump{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-11px) rotate(-4deg)}}
  .ribbon{position:absolute;left:-12%;right:-12%;bottom:80px;height:34px;overflow:hidden;transform:rotate(-7deg);
    background:rgba(63,6,24,.72);border-top:1px solid rgba(255,215,130,.6);border-bottom:1px solid rgba(255,215,130,.6);display:flex;align-items:center}
  .rt{white-space:nowrap;font-size:13px;font-weight:700;letter-spacing:.3em;text-transform:uppercase;animation:shimmer 4s linear infinite,marq 14s linear infinite}
  @keyframes marq{to{transform:translateX(-50%)}}
  .seal{animation:sealwob 3.4s ease-in-out infinite}
  @keyframes sealwob{0%,100%{transform:rotate(-7deg) scale(1)}50%{transform:rotate(7deg) scale(1.08)}}

  .page{transform:translateX(70px) rotate(5deg) scale(.88);transition:opacity .5s ease,transform .8s cubic-bezier(.34,1.56,.64,1)}
  .page.before{transform:translateX(-70px) rotate(-5deg) scale(.88)}
  .page.active{transform:none}
  .title .w{display:inline-block;white-space:nowrap}
  .title .ch{display:inline-block;opacity:0}
  .page.active .title .ch{animation:chpop .8s cubic-bezier(.3,1.8,.5,1) both,wob 2.6s ease-in-out infinite;
    animation-delay:calc(var(--k) * .045s + .2s),calc(var(--k) * .15s + 1.2s)}
  @keyframes chpop{from{opacity:0;transform:translateY(-40px) scale(.2) rotate(-40deg)}to{opacity:1;transform:none}}
  @keyframes wob{0%,100%{translate:0 0}50%{translate:0 -4px}}

  .polaroid{rotate:-3deg}
  .page.active .polaroid.reveal{animation:rise .9s cubic-bezier(.2,.7,.2,1) both,polwob 4.5s ease-in-out infinite;
    animation-delay:calc(var(--i) * .3s + .2s),1.4s}
  @keyframes polwob{0%,100%{rotate:-3deg}50%{rotate:3deg}}
  .polaroid::after{content:"\2605";position:absolute;top:-18px;right:-12px;font-size:38px;color:#f1c766;text-shadow:0 0 12px #e8b74a;animation:spinstar 5s linear infinite}
  @keyframes spinstar{to{transform:rotate(360deg)}}

  .rbtn{animation:bob 2.2s ease-in-out infinite;animation-delay:calc(var(--k) * -.19s)}
  @keyframes bob{0%,100%{transform:translateY(0) rotate(-5deg)}50%{transform:translateY(-6px) rotate(5deg)}}
  .rbtn.done svg{animation:thump .6s}
  @keyframes thump{0%{transform:scale(1)}40%{transform:scale(1.6) rotate(12deg)}100%{transform:scale(1)}}
  .nbtn:hover{transform:scale(1.18) rotate(10deg)}
</style>
</head>
<body>
<div class="stage">
  <div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>

  <div class="tilt" id="tilt"><div class="card" id="card">
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
        <div class="ribbon"><div class="rt foil">happy birthday ♡ my little goblin ♡ happy birthday ♡ my little goblin ♡ happy birthday ♡ my little goblin ♡ happy birthday ♡ my little goblin ♡ happy birthday ♡ my little goblin ♡ happy birthday ♡ my little goblin ♡ </div></div>
        <div class="c-small foil">a card for you</div>
        <div class="c-big">Happy<br>Birthday</div>
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
  </div></div>
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

/* letters on the cover jump */
(function () {
  const big = document.querySelector('.c-big');
  big.innerHTML = '';
  let k = 0;
  ['Happy', 'Birthday'].forEach(w => {
    const line = document.createElement('div');
    [...w].forEach(c => {
      const sp = document.createElement('span');
      sp.className = 'foil jl'; sp.textContent = c;
      sp.style.animation = 'shimmer 4s linear infinite, jump 1.8s ease-in-out infinite';
      sp.style.animationDelay = '0s, ' + (k++ * 0.09) + 's';
      line.appendChild(sp);
    });
    big.appendChild(line);
  });
})();

/* golden sparkle trail + 3D tilt that follows the pointer */
let lastSpark = 0;
const tiltEl = document.getElementById('tilt');
document.addEventListener('pointermove', e => {
  const now = performance.now();
  if (now - lastSpark > 45) {
    lastSpark = now;
    const sp = document.createElement('div');
    sp.className = 'spark';
    sp.textContent = Math.random() > .5 ? '✦' : '✧';
    sp.style.fontSize = (9 + Math.random() * 14) + 'px';
    fx.appendChild(sp);
    const x = e.clientX, y = e.clientY, dx = (Math.random() - .5) * 50;
    sp.animate([
      { transform: 'translate(' + x + 'px,' + y + 'px) scale(1)', opacity: 1 },
      { transform: 'translate(' + (x + dx) + 'px,' + (y + 30 + Math.random() * 40) + 'px) scale(.2) rotate(160deg)', opacity: 0 }
    ], { duration: 800 + Math.random() * 500, easing: 'ease-out' }).onfinish = () => sp.remove();
  }
  const rx = (e.clientX / innerWidth - .5), ry = (e.clientY / innerHeight - .5);
  tiltEl.style.transform = 'perspective(1000px) rotateY(' + (rx * 16) + 'deg) rotateX(' + (-ry * 12) + 'deg)';
});
document.addEventListener('pointerleave', () => { tiltEl.style.transform = ''; });

/* title letters */
function wavy(cls, text) {
  const d = document.createElement('div');
  d.className = cls;
  let k = 0;
  const words = text.split(' ');
  words.forEach((w, wi) => {
    const ws = document.createElement('span'); ws.className = 'w';
    [...w].forEach(c => {
      const s = document.createElement('span'); s.className = 'ch'; s.textContent = c;
      s.style.setProperty('--k', k++);
      ws.appendChild(s);
    });
    d.appendChild(ws);
    if (wi < words.length - 1) d.appendChild(document.createTextNode(' '));
  });
  return d;
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
}, 650);

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

  const title = wavy('title', pg.title || '');
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
      b.style.setProperty('--k', k);
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
  } else if (pg.type === 'bengali') {
    const bn = el('div', 'bn reveal', pg.bengali); bn.style.setProperty('--i', 3);
    const tr = el('div', 'bn-tr reveal', pg.translit); tr.style.setProperty('--i', 4);
    const mean = el('div', 'bn-mean reveal', pg.meaning); mean.style.setProperty('--i', 5);
    page.appendChild(bn); page.appendChild(tr); page.appendChild(mean);
    page.appendChild(paragraphs(pg.text, 6));
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
      const stg = document.querySelector('.stage'); stg.classList.add('shake'); setTimeout(() => stg.classList.remove('shake'), 750);
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
  const was = idx;
  idx = Math.max(0, Math.min(pageEls.length - 1, n));
  pageEls.forEach((p, i) => {
    p.classList.toggle('active', i === idx);
    p.classList.toggle('before', i < idx);
  });
  dotEls.forEach((d, i) => d.classList.toggle('on', i === idx));
  prev.disabled = idx === 0;
  next.disabled = idx === pageEls.length - 1;
  if (pageEls[idx]) pageEls[idx].scrollTop = 0;
  if (opened && was !== idx) { confettiRain(18); burst(innerWidth / 2, innerHeight * .82, 6); }
}
function openCard() {
  if (opened) return; opened = true;
  card.classList.add('opened');
  if (audio) audio.play().catch(() => {});
  confettiRain(140);
  burst(innerWidth / 2, innerHeight / 2, 24);
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
