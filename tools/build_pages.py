#!/usr/bin/env python3
"""Builds the DuckyHug static pages from one shared template.

Run from the repo root:  python3 tools/build_pages.py

Generates: index.html, about/, privacy/, free/, 404.html, one kit page per book
(/village, /moving, /school, /friends) and one book page per book
(/books/<slug>/). Edit the BOOKS data or the templates here, then rebuild.

Covers: drop a file at img/covers/<key>.webp|jpg|png (square) and rebuild.
Until then a themed placeholder is shown.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.duckyhug.com"
KIT_ACTION = "https://app.kit.com/forms/8775431/subscriptions"
FACEBOOK = "https://www.facebook.com/duckyhug"

BOOKS = [
    {
        "key": "village",
        "title": "The Magic Village",
        "short": "The Magic Village",
        "series": None,
        "slug": "the-magic-village",
        "kit_slug": "village",
        "asin": "B0HRF2Y773",
        "published": "2026-11-06",
        "published_text": "6 November 2026",
        "pages": 34,
        "ages": "3–9",
        "promise": "A gentle story to share with your child, with a free coloring kit to match.",
        "page_title": "The Magic Village – Storybook for Kids Ages 3–9 | DuckyHug",
        "meta": "The Magic Village is a 34-page paperback story for kids ages 3–9 by DuckyHug, with a free printable coloring kit for parents.",
        "intro": "The Magic Village is a paperback story for children ages 3–9, written by the two parents behind DuckyHug for their own kids.",
        "inside": [
            "34 pages in a square 8.5 × 8.5 inch paperback",
            "Made for children ages 3–9, to read together",
            "A free Magic Village Coloring Kit with bonus coloring pages from the story",
        ],
        "kit": {
            "name": "Magic Village Coloring Kit",
            "line": "Bonus coloring pages from the story.",
            "bullets": [
                "Bonus coloring pages from The Magic Village story",
                "A printable PDF, sent straight to your inbox",
                "Made by two parents for their own children",
            ],
        },
    },
    {
        "key": "moving",
        "title": "We Are Moving! A Cozy Moving Coloring & Activity Book for Kids Ages 3–9",
        "short": "We Are Moving!",
        "series": 1,
        "slug": "we-are-moving",
        "kit_slug": "moving",
        "asin": "B0HSFWDXKW",
        "published": "2026-11-20",
        "published_text": "20 November 2026",
        "pages": 96,
        "ages": "3–9",
        "promise": "A cozy coloring and activity book for children facing a move.",
        "page_title": "We Are Moving! – Cozy Moving Coloring & Activity Book for Kids 3–9 | DuckyHug",
        "meta": "We Are Moving! is a cozy 96-page coloring and activity book for kids ages 3–9 who are getting ready for a move. Book 1 of the Little Big Changes series.",
        "intro": "We Are Moving! A Cozy Moving Coloring & Activity Book for Kids Ages 3–9 is the first book in the Little Big Changes series, made for children who are facing a big move.",
        "inside": [
            "96 pages, with 30 coloring pages and 11 activities, in a square 8.5 × 8.5 inch paperback",
            "Made for children ages 3–9",
            "Look for Lucy the cat on every page",
        ],
        "kit": {
            "name": "Moving Day Kit",
            "line": "A free printable extra for moving day.",
            "bullets": [
                "A printable extra to go with the We Are Moving! book",
                "A PDF sent straight to your inbox",
                "Made by two parents for their own children",
            ],
        },
    },
    {
        "key": "school",
        "title": "Our New School! A Cozy First-Day Coloring & Activity Book for Kids Ages 3–9",
        "short": "Our New School!",
        "series": 2,
        "slug": "our-new-school",
        "kit_slug": "school",
        "asin": None,
        "pages": 96,
        "ages": "3–9",
        "promise": "Coming soon: a coloring and activity book for the first days at a new school.",
        "page_title": "Our New School! – First-Day Coloring & Activity Book for Kids 3–9 | DuckyHug",
        "meta": "Our New School! is a coming-soon first-day coloring and activity book for kids ages 3–9 starting at a new school. Book 2 of the Little Big Changes series by DuckyHug.",
        "intro": "Our New School! A Cozy First-Day Coloring & Activity Book for Kids Ages 3–9 is the second book in the Little Big Changes series, made for children starting at a new school. It is coming soon.",
        "inside": [
            "30 coloring pages and 12 activities in a square 8.5 × 8.5 inch paperback",
            "Made for children ages 3–9",
            "Look for Lucy the cat on every page",
            "A free First Day Brave Kit to print at home",
        ],
        "kit": {
            "name": "First Day Brave Kit",
            "line": "A certificate, a photo sign, coloring pages and a feelings chart.",
            "bullets": [
                "A Brave Explorer certificate and a “My First Day of School” photo sign",
                "3 bonus coloring pages with Lucy the cat hidden in each",
                "A feelings chart to talk about the big day together",
            ],
        },
    },
    {
        "key": "friends",
        "title": "Our New Friends! A Cozy Friendship Coloring & Activity Book for Kids Ages 3–9",
        "short": "Our New Friends!",
        "series": 3,
        "slug": "our-new-friends",
        "kit_slug": "friends",
        "asin": None,
        "pages": None,
        "ages": "3–9",
        "promise": "Coming soon: a cozy coloring and activity book about making new friends.",
        "page_title": "Our New Friends! – Friendship Coloring & Activity Book for Kids 3–9 | DuckyHug",
        "meta": "Our New Friends! is a coming-soon friendship coloring and activity book for kids ages 3–9. Book 3 of the Little Big Changes series by DuckyHug.",
        "intro": "Our New Friends! A Cozy Friendship Coloring & Activity Book for Kids Ages 3–9 is the third book in the Little Big Changes series, made for children making new friends. It is coming soon.",
        "inside": [
            "30 coloring pages and 14 activities",
            "Made for children ages 3–9",
            "Look for Lucy the cat on every page",
            "A free Friendship Kit to print at home",
        ],
        "kit": {
            "name": "Friendship Kit",
            "line": "A free printable to go with the book.",
            "bullets": [
                "A printable extra to go with Our New Friends!",
                "A PDF sent to your inbox when the book comes out",
                "Made by two parents for their own children",
            ],
        },
    },
]

SERIES_NAME = "Little Big Changes"


# ------------------------------------------------------------------ helpers
def amazon(b):
    return f"https://www.amazon.com/dp/{b['asin']}" if b.get("asin") else None


def cover_file(b):
    for ext in ("webp", "jpg", "jpeg", "png"):
        p = ROOT / "img" / "covers" / f"{b['key']}.{ext}"
        if p.exists():
            return p
    return None


def cover_html(b, cls="cover", eager=False):
    p = cover_file(b)
    if p:
        size = ""
        try:
            from PIL import Image
            with Image.open(p) as im:
                size = f' width="{im.width}" height="{im.height}"'
        except Exception:
            pass
        loading = "" if eager else ' loading="lazy"'
        return (f'<div class="{cls}"><img src="/img/covers/{p.name}"{size}{loading} '
                f'alt="Cover of {escape(b["title"])}"></div>')
    return (f'<div class="{cls} cover-ph" role="img" aria-label="Cover of {escape(b["title"])} (coming soon)">'
            f'<span>{escape(b["short"])}</span></div>')


def kit_art(b):
    return (f'<div class="cover kit-art cover-ph" role="img" aria-label="{escape(b["kit"]["name"])}">'
            f'<span>{escape(b["kit"]["name"])}</span></div>')


def book_url(b):
    return f"/books/{b['slug']}/"


def kit_url(b):
    return f"/{b['kit_slug']}/"


def head(title, desc, path, extra=""):
    canon = f"{SITE}{path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
    <meta name="description" content="{escape(desc, quote=True)}">
    <link rel="canonical" href="{canon}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="DuckyHug">
    <meta property="og:title" content="{escape(title, quote=True)}">
    <meta property="og:description" content="{escape(desc, quote=True)}">
    <meta property="og:url" content="{canon}">
    <meta name="theme-color" content="#25556c">
    <link rel="icon" type="image/png" sizes="32x32" href="/img/png/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/img/png/apple-touch-icon.png">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
{extra}</head>
"""


LOGO = """<div class="logo">
            <a class="logo-circle" href="/" aria-label="DuckyHug home"><img src="/img/ducky_hug_logo.png" width="60" height="60" alt=""></a>
            <div class="logo-text"><a href="/">DuckyHug</a></div>
        </div>"""


def header(nav=True):
    links = ""
    if nav:
        links = """
        <nav class="site-nav" aria-label="Main">
            <a href="/#books">Books</a>
            <a href="/free/">Free Kits</a>
            <a href="/about/">About</a>
        </nav>"""
    return f"""<body>
    <header class="site-header">
        {LOGO}{links}
    </header>
"""


def form(label="Send me the free kit", note_extra=""):
    return f"""<form class="email-form" action="{KIT_ACTION}" method="post">
                <input type="email" name="email_address" class="email-input" placeholder="Your email address" aria-label="Your email address" autocomplete="email" required>
                <button type="submit" class="email-submit">{escape(label)}</button>
            </form>
            <p class="form-note">For parents and guardians. {note_extra}<a href="/privacy/">Privacy</a></p>"""


def footer(full=True):
    if not full:
        return """    <footer>
        <p><strong>DuckyHug</strong> - Stories that embrace the soul</p>
        <p><a href="/privacy/">Privacy</a> · &copy; 2026 DuckyHug</p>
    </footer>
</body>
</html>
"""
    return f"""    <footer>
        <p><strong>DuckyHug</strong> - Stories that embrace the soul</p>
        <div class="footer-signup">
            <p>Get a free printable kit for your child's next big change.</p>
            {form("Send me the free kit")}
        </div>
        <p class="footer-nav"><a href="/#books">Books</a> · <a href="/free/">Free Kits</a> · <a href="/about/">About</a> · <a href="/privacy/">Privacy</a></p>
        <p>Send us a message anytime <a href="{FACEBOOK}" rel="noopener">@duckyhug</a> - we’d love to hear from you!</p>
        <p>&copy; 2026 DuckyHug. All rights reserved.</p>
    </footer>
</body>
</html>
"""


def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


# -------------------------------------------------------------------- pages
def book_card(b):
    azn = amazon(b)
    ages = f"Ages {b['ages']}" if b.get("ages") else None
    meta = " · ".join(x for x in [ages, f"{b['pages']} pages" if b.get("pages") else None] if x)
    if azn:
        action = f'<a href="{azn}" class="book-link" target="_blank" rel="noopener">Get it on Amazon →</a>'
    else:
        action = '<span class="book-link is-soon">Coming soon</span>'
    kit_label = "Free kit" if azn else "Get the kit when it's out"
    return f"""<article class="book-card">
                {cover_html(b)}
                <h3><a href="{book_url(b)}">{escape(b['short'])}</a></h3>
                <p>{escape(b['promise'])}</p>
                {f'<p class="book-meta">{escape(meta)}</p>' if meta else ''}
                {action}
                <p class="card-links"><a href="{book_url(b)}">About the book</a> · <a href="{kit_url(b)}">{kit_label}</a></p>
            </article>"""


def build_home():
    v = BOOKS[0]
    series = [b for b in BOOKS if b["series"]]
    org = json.dumps({
        "@context": "https://schema.org", "@type": "Organization", "name": "DuckyHug",
        "url": SITE + "/", "logo": SITE + "/img/ducky_hug_logo.png", "sameAs": [FACEBOOK],
    }, indent=2)
    extra = f'    <script type="application/ld+json">\n{org}\n    </script>\n'
    h = head("DuckyHug – Coloring Stories for Kids Ages 3–9 | Free Printable Kits",
             "Gentle coloring stories and activity books for children ages 3–9, made by two parents. Start with a free Magic Village Coloring Kit.",
             "/", extra)
    body = f"""{header()}
    <div class="social-sidebar">
        <a href="{FACEBOOK}" target="_blank" rel="noopener" class="social-icon facebook" aria-label="Follow DuckyHug on Facebook">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
        </a>
    </div>

    <main class="page">
        <section class="hero-card home-hero">
            <div class="hero-text">
                <h1>Gentle coloring stories for life's little big changes</h1>
                <p class="lead">Stories and coloring books for children ages 3–9, made by two parents for their own kids.</p>
                <p class="cta-row">
                    <a class="book-link cta" href="{kit_url(v)}">Get the free Magic Village Coloring Kit</a>
                    <a class="text-link" href="{book_url(v)}">See The Magic Village →</a>
                </p>
            </div>
            <a class="hero-cover" href="{book_url(v)}">{cover_html(v, "cover", eager=True)}</a>
        </section>

        <section id="books" class="books-section">
            <h2 class="section-title">Our books</h2>
            <article class="book-card featured">
                <a class="featured-cover" href="{book_url(v)}">{cover_html(v)}</a>
                <div class="featured-text">
                    <p class="eyebrow">Our newest story</p>
                    <h3><a href="{book_url(v)}">{escape(v['title'])}</a></h3>
                    <p>{escape(v['promise'])}</p>
                    <p class="book-meta">Ages {v['ages']} · {v['pages']} pages · Paperback</p>
                    <p><a href="{amazon(v)}" class="book-link" target="_blank" rel="noopener">Get your copy on Amazon →</a></p>
                    <p class="card-links"><a href="{book_url(v)}">About the book</a> · <a href="{kit_url(v)}">Free coloring kit</a></p>
                </div>
            </article>

            <h3 class="series-title">The “{SERIES_NAME}” series</h3>
            <p class="series-note">Little books for big moments in a child's life. Look for Lucy the cat on every page.</p>
            <div class="books-grid">
            {chr(10).join(book_card(b) for b in series)}
            </div>
        </section>

        <section class="email-signup" id="free-kit">
            <div class="flourish">✉</div>
            <h3>Get your free printable kit</h3>
            <p>Pick up the free Magic Village Coloring Kit, and hear about new books from two parents who write for their own kids.</p>
            {form("Send me the free kit")}
            <p class="form-note"><a href="/free/">See all free kits</a></p>
        </section>

        <section class="hero-card story-short">
            <div class="avatar-row">
                <img src="/img/Ducky_Hug_Female_Avatar.png" width="300" height="300" loading="lazy" alt="Illustrated portrait of Mom, one of the two DuckyHug authors" class="avatar">
                <img src="/img/Ducky_Hug_Male_Avatar.png" width="300" height="300" loading="lazy" alt="Illustrated portrait of Dad, one of the two DuckyHug authors" class="avatar">
            </div>
            <h2 class="section-title">Hello, we're the DuckyHug parents</h2>
            <p>We grew up in the mountains and now live in the suburbs of a big city, raising three children between two worlds. We started writing stories for our own kids, and now we share them with you.</p>
            <p>We believe love, creativity and staying true to who you are can work magic.</p>
            <p><a class="text-link" href="/about/">Read our story →</a></p>
        </section>
    </main>

{footer()}"""
    write("index.html", h + body)


def build_kit(b):
    azn = amazon(b)
    live = bool(azn)
    kit = b["kit"]
    title = f"Free {kit['name']} | DuckyHug"
    desc = f"{kit['name']}: {kit['line']} A free printable for parents, from the DuckyHug book {b['short']}"
    h = head(title, desc, kit_url(b))
    heading = f"Your free {kit['name']}" if live else f"Get the {kit['name']} when the book comes out"
    label = "Send me the free kit" if live else "Send me the kit when it's ready"
    intro = (f"A free printable from the DuckyHug book <strong>{escape(b['short'])}</strong>." if live
             else f"A free printable to go with <strong>{escape(b['short'])}</strong>, coming soon. Leave your email and we'll send the kit when the book comes out.")
    bullets = "\n".join(f"                <li>{x}</li>" for x in kit["bullets"])
    body = f"""{header(nav=False)}
    <main class="page narrow">
        <section class="hero-card kit-page">
            <p class="eyebrow">Free printable kit</p>
            <h1>{escape(heading)}</h1>
            <p class="lead">{intro}</p>
            {kit_art(b)}
            <ul class="kit-list">
{bullets}
            </ul>
            {form(label)}
            <p class="small-link"><a href="{book_url(b)}">About the book: {escape(b['short'])} →</a></p>
        </section>
    </main>

{footer(full=False)}"""
    write(f"{b['kit_slug']}/index.html", h + body)


def build_book(b):
    azn = amazon(b)
    live = bool(azn)
    ld = {
        "@context": "https://schema.org", "@type": "Book", "name": b["title"],
        "author": {"@type": "Organization", "name": "DuckyHug"},
        "publisher": {"@type": "Organization", "name": "Independently published"},
        "url": SITE + book_url(b), "inLanguage": "en",
        "description": b["meta"],
    }
    if b.get("pages"): ld["numberOfPages"] = b["pages"]
    if live:
        ld["bookFormat"] = "https://schema.org/Paperback"
        ld["datePublished"] = b["published"]
        ld["sameAs"] = azn
    if b.get("ages"): ld["audience"] = {"@type": "PeopleAudience", "suggestedMinAge": 3, "suggestedMaxAge": 9}
    if b["series"]: ld["isPartOf"] = {"@type": "BookSeries", "name": SERIES_NAME}
    if cover_file(b): ld["image"] = f"{SITE}/img/covers/{cover_file(b).name}"
    extra = f'    <script type="application/ld+json">\n{json.dumps(ld, indent=2, ensure_ascii=False)}\n    </script>\n'
    h = head(b["page_title"], b["meta"], book_url(b), extra)

    details = [("Format", "Paperback, 8.5 × 8.5 in" if b.get("pages") else "Paperback")]
    if b.get("pages"): details.append(("Pages", str(b["pages"])))
    if b.get("ages"): details.append(("Ages", b["ages"]))
    if b["series"]: details.append(("Series", f"{SERIES_NAME}, book {b['series']}"))
    details.append(("Publisher", "Independently published"))
    details.append(("Published", b["published_text"] if live else "Coming soon"))
    dl = "\n".join(f"                <div><dt>{k}</dt><dd>{escape(v)}</dd></div>" for k, v in details)
    inside = "\n".join(f"                <li>{escape(x)}</li>" for x in b["inside"])
    buy = (f'<a href="{azn}" class="book-link cta" target="_blank" rel="noopener">Get it on Amazon →</a>' if live
           else '<span class="book-link is-soon">Coming soon</span>')
    kit = b["kit"]
    kit_text = (f"Free: the {kit['name']}. {kit['line']}" if live
                else f"Free: the {kit['name']}. {kit['line']} Leave your email and we'll send it when the book comes out.")
    body = f"""{header()}
    <main class="page narrow">
        <article class="hero-card book-page">
            <div class="book-top">
                {cover_html(b, "cover", eager=True)}
                <div>
                    <h1>{escape(b['title'])}</h1>
                    <p class="lead">{escape(b['intro'])}</p>
                    <p>{buy}</p>
                </div>
            </div>

            <h2 class="section-title">What's inside</h2>
            <ul class="kit-list">
{inside}
            </ul>

            <h2 class="section-title">Book details</h2>
            <dl class="details">
{dl}
            </dl>

            <aside class="kit-box">
                <h3>{escape(kit['name'])}</h3>
                <p>{escape(kit_text)}</p>
                <p><a class="book-link" href="{kit_url(b)}">{"Get the free kit" if live else "Get the kit when it's out"} →</a></p>
            </aside>
            <p class="small-link"><a href="/#books">← All DuckyHug books</a></p>
        </article>
    </main>

{footer()}"""
    write(f"books/{b['slug']}/index.html", h + body)


def build_free():
    h = head("Free Printable Kits for Parents | DuckyHug",
             "Free printable coloring and activity kits from DuckyHug, made by two parents to go with each book.",
             "/free/")
    cards = []
    for b in BOOKS:
        live = bool(amazon(b))
        cards.append(f"""<article class="book-card">
                {kit_art(b)}
                <h3><a href="{kit_url(b)}">{escape(b['kit']['name'])}</a></h3>
                <p>{escape(b['kit']['line'])}</p>
                <a class="book-link" href="{kit_url(b)}">{"Get the free kit" if live else "Get it when the book is out"}</a>
                <p class="card-links">From the book: <a href="{book_url(b)}">{escape(b['short'])}</a></p>
            </article>""")
    body = f"""{header()}
    <main class="page">
        <section class="hero-card">
            <h1>Free printable kits</h1>
            <p class="lead">Each DuckyHug book comes with a free printable kit for parents. Pick one and we'll send it to your inbox.</p>
        </section>
        <div class="books-grid kits-grid">
            {chr(10).join(cards)}
        </div>
        <section class="email-signup">
            <h3>Not sure which one?</h3>
            <p>Start with the Magic Village Coloring Kit.</p>
            <p><a class="book-link" href="{kit_url(BOOKS[0])}">Get the Magic Village Coloring Kit</a></p>
        </section>
    </main>

{footer()}"""
    write("free/index.html", h + body)


ABOUT_STORY = """
                    <p>We're so glad you found us. We're just two parents who grew up in the mountains, surrounded by rich traditions and a close-knit community. Life brought us to the suburbs of a big city, and honestly? We weren't sure how we'd navigate raising our children between two worlds.</p>
                    <p>But here's what we discovered: <strong>love, creativity, and staying true to who you are can work magic.</strong></p>
                    <p>Today, our three kids are thriving in ways that still amaze us. Our 8-year-old daughter plays both cello and violin, her sister, 6-year-old, has fallen in love with the piano. And our 2-year-old? He's already speaking three languages alongside his sisters. They're excelling in school, they're proud of where they come from, and they've embraced their new community with open hearts.</p>
                    <p>The best part? None of this required expensive programs, intense pressure, or sacrificing family time. It happened through storytelling, simple creative resources, and an approach that honors both heritage and growth.</p>
                    <p>We created stories for our children – tales that taught values, sparked imagination, and connected them to their roots. We found methods that didn't cost a dime but gave us priceless results. And now, we want to share all of it with you. Here, you'll find:</p>
                    <ul class="plain-list">
                        <li>📚 Original stories and books we created for our kids</li>
                        <li>💡 Practical parenting advice that actually works</li>
                        <li>🌟 Resources for raising bilingual, culturally-grounded children</li>
                        <li>❤️ Real experiences from our family to yours</li>
                    </ul>
                    <p>Whether you're raising kids across cultures, looking for meaningful ways to connect with your children, or just trying to figure out this whole parenting thing – you're in the right place. Let's walk this journey together.</p>
"""


def build_about():
    h = head("About DuckyHug – Two Parents Writing for Their Own Kids",
             "DuckyHug is two parents who grew up in the mountains and now write stories and coloring books for their own children.",
             "/about/")
    body = f"""{header()}
    <main class="page narrow">
        <section class="hero-card">
            <div class="avatar-row">
                <img src="/img/Ducky_Hug_Female_Avatar.png" width="300" height="300" alt="Illustrated portrait of Mom, one of the two DuckyHug authors" class="avatar">
                <img src="/img/Ducky_Hug_Male_Avatar.png" width="300" height="300" alt="Illustrated portrait of Dad, one of the two DuckyHug authors" class="avatar">
            </div>
            <h1>Welcome to Our Family's Journey</h1>
            <h2 class="subtitle">From Mountain Roots to City Streets – Raising Extraordinary Kids Through Love, Stories, and Tradition</h2>
            <div class="divider"></div>
            <div class="prose">{ABOUT_STORY}            </div>
            <p class="small-link"><a href="/#books">See our books →</a> · <a href="/free/">Free kits</a></p>
        </section>
    </main>

{footer()}"""
    write("about/index.html", h + body)


def build_privacy():
    h = head("Privacy Policy | DuckyHug",
             "How DuckyHug collects and uses your email address, and how to unsubscribe or ask us to delete it.",
             "/privacy/")
    body = f"""{header()}
    <main class="page narrow">
        <section class="hero-card prose-page">
            <p class="review-note"><strong>Template – please review.</strong> This page is a starting template and has not been checked by a lawyer. Remove this note once you have reviewed it.</p>
            <h1>Privacy Policy</h1>
            <p><em>Last updated: 24 November 2026</em></p>

            <h2 class="section-title">Who we are</h2>
            <p>DuckyHug (“we”) is a small family business that writes and publishes children's books. This site is at {SITE.replace('https://', '')}.</p>

            <h2 class="section-title">What we collect</h2>
            <p>If you join our list, we collect your email address (and your first name, if a form asks for it). We do not ask for anything else.</p>

            <h2 class="section-title">Why we collect it</h2>
            <p>To send you the free printable kit you asked for, and to send occasional news about our books. Nothing else.</p>

            <h2 class="section-title">Who handles it</h2>
            <p>We use Kit (kit.com) to store your email address and to send our emails. Kit processes this data on our behalf.</p>

            <h2 class="section-title">Unsubscribe or delete your data</h2>
            <p>Every email has an unsubscribe link at the bottom. To have your data deleted, message us on <a href="{FACEBOOK}" rel="noopener">Facebook</a> and we will remove it.</p>

            <h2 class="section-title">Children</h2>
            <p>Our sign-up forms are for parents and guardians only. We do not knowingly collect personal data from children under 13 (US) or under 16 in the EU without a parent's consent. If you think a child has given us their email address, tell us and we will delete it.</p>

            <h2 class="section-title">Contact</h2>
            <p>Message us on <a href="{FACEBOOK}" rel="noopener">Facebook</a>.</p>
        </section>
    </main>

{footer(full=False)}"""
    write("privacy/index.html", h + body)


def build_404():
    h = head("Page not found | DuckyHug", "This page could not be found.", "/404.html")
    h = h.replace("<title>", '<meta name="robots" content="noindex">\n    <title>', 1)
    body = f"""{header()}
    <main class="page narrow">
        <section class="hero-card">
            <h1>Oops, this page wandered off</h1>
            <p class="lead">Let's get you back to the story.</p>
            <p class="cta-row"><a class="book-link cta" href="/">Go to the homepage</a> <a class="text-link" href="/free/">Free kits →</a></p>
        </section>
    </main>

{footer(full=False)}"""
    write("404.html", h + body)


if __name__ == "__main__":
    build_home()
    for b in BOOKS:
        build_kit(b)
        build_book(b)
    build_free()
    build_about()
    build_privacy()
    build_404()
    print("built")
