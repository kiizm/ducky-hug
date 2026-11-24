# DuckyHug theme notes

Extracted from `styles.css` (Nov 2026). New elements must reuse these values.

## Colors
| Token | Value | Use |
|---|---|---|
| page background | `linear-gradient(135deg, #F5EFE0, #E8DCC4)` | `body` |
| paper | `linear-gradient(#FFFEF9, #F9F7F0)` + 1px `#E8DCC4` border | cards, hero paper, sign-up box |
| ink (headings) | `#2C2416` | h1/h2/h3 |
| body text | `#4A4338` | paragraphs |
| muted text | `#6B6158` | card copy, notes |
| warm brown | `#8B6F47` | h2 italics, flourish, dividers |
| teal (brand) | `#2B5F6F` | logo circle, links, focus, theme-color |
| orange (buttons) | `#E89A3C`, hover `#D68A2C`, white text | `.book-link`, `.email-submit` |
| footer / borders | `#E8DCC4` | footer bg, input borders |

## Fonts
- Headings: **Playfair Display** 400/700 (h1 42px, mobile 32px; h2 italic 24px/20px; card h3 22px).
- Body: **Open Sans** 400/600 (18px paper text, 16px mobile, 15px card text).

## Shapes
- Paper card: radius 8px, shadow `0 10px 40px rgba(0,0,0,.15)`, slight `rotate(-0.5deg)` (none on mobile), torn-edge strip `::before`.
- Book card: white, radius 12px, padding 25px, shadow `0 4px 15px rgba(0,0,0,.1)`, centered text.
- Buttons: pill (radius 25–30px), orange, white 600 text, hover `scale(1.05)`.
- Inputs: pill, 2px `#E8DCC4` border, teal focus ring.
- Dividers: 100px gradient line in brown; flourish glyph `❦`.
- Avatars: 200px circles (100px mobile), white border, float animation.

## Tone
Warm, personal "two parents" voice, simple English, emoji used sparingly in lists.

## Breakpoints
Mobile `<=767px`, tablet `768–1279px`, desktop `>=1280px`.
