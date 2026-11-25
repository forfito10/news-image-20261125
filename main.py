from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 1080, 1350
BG = '#0f1720'
PANEL = '#17232e'
TEXT = '#f3f6f8'
MUTED = '#aab7c2'
TEAL = '#29d3c2'

stories = [
    ('Huang returns as Nvidia CEO', 'Jensen Huang resumes the top role as Nvidia enters its next growth chapter.'),
    ('CrowdStrike-Zscaler deal reaches $43.9B', 'The proposed tie-up would unite two major names in cloud security.'),
    ('700,000 Russian soldiers killed', 'A new estimate puts the human cost of Russia’s war at a staggering scale.'),
    ('RSF advances in Khartoum', 'Paramilitary forces push forward as fighting intensifies across Sudan’s capital.'),
    ('ICJ hears Myanmar genocide case', 'The court opens hearings on allegations tied to the Rohingya campaign.'),
]


def font(size, bold=False):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, face, max_width):
    words, lines, line = text.split(), [], ''
    for word in words:
        trial = f'{line} {word}'.strip()
        if draw.textbbox((0, 0), trial, font=face)[2] <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


im = Image.new('RGB', (WIDTH, HEIGHT), BG)
d = ImageDraw.Draw(im)
margin = 76
# Accent masthead
d.rectangle((margin, 68, margin + 10, 144), fill=TEAL)
d.text((margin + 32, 62), 'FIVE STORIES MOVING THE WORLD TODAY', font=font(39, True), fill=TEXT)
d.text((margin, 123), 'NOVEMBER 25, 2026', font=font(18, True), fill=MUTED)
d.text((margin, 171), 'THE WORLD, IN FIVE HEADLINES', font=font(17, True), fill=TEAL)
d.line((margin, 211, WIDTH - margin, 211), fill='#31404d', width=2)

card_top, card_gap = 238, 18
card_h = 197
for i, (headline, summary) in enumerate(stories):
    y = card_top + i * (card_h + card_gap)
    d.rounded_rectangle((margin, y, WIDTH - margin, y + card_h), radius=16, fill=PANEL)
    d.text((margin + 25, y + 21), f'{i + 1:02d}', font=font(20, True), fill=TEAL)
    hx = margin + 82
    hfont = font(30, True)
    for j, line in enumerate(wrap(d, headline, hfont, WIDTH - margin - hx - 28)):
        d.text((hx, y + 17 + j * 37), line, font=hfont, fill=TEXT)
    summary_y = y + 115
    sfont = font(18)
    for j, line in enumerate(wrap(d, summary, sfont, WIDTH - margin * 2 - 50)):
        d.text((margin + 25, summary_y + j * 26), line, font=sfont, fill=MUTED)

d.line((margin, HEIGHT - 74, WIDTH - margin, HEIGHT - 74), fill='#31404d', width=2)
d.text((margin, HEIGHT - 57), 'GLOBAL BRIEFING  /  FIVE DEVELOPMENTS TO KNOW', font=font(15, True), fill=MUTED)

out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '.')
os.makedirs(out_dir, exist_ok=True)
im.save(os.path.join(out_dir, 'entry.png'))
