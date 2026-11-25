import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = "#101820"
PAPER = "#efeae0"
GOLD = "#d4a017"
WHITE = "#f6f5f1"
GRAY = "#aab2b7"
INK = "#202a32"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
REG = ImageFont.truetype(f"{FONT_DIR}/DejaVuSans.ttf", 15)
BOLD = lambda n: ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", n)
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def label(x, y, s, font, color):
    d.text((x, y), s, font=font, fill=color)

def line(points, color, width=3):
    d.line(points, fill=color, width=width, joint="curve")

def icon(cx, cy, kind):
    r = 31
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill="#263744")
    c = "#e8edf0"
    if kind == "rocket":
        line([(cx-7,cy+10),(cx-7,cy-5),(cx+4,cy-17),(cx+11,cy-10),(cx+2,cy+2),(cx-7,cy+10)], c, 3)
        line([(cx-7,cy+1),(cx-13,cy+7),(cx-12,cy+13),(cx-5,cy+8)], c, 2)
        line([(cx+1,cy+9),(cx-3,cy+16),(cx+4,cy+12)], "#e6a640", 3)
        d.ellipse((cx+1,cy-10,cx+5,cy-6), fill=BG)
    elif kind == "coin":
        d.ellipse((cx-15,cy-15,cx+15,cy+15), outline=c, width=3)
        label(cx-6, cy-14, "$", BOLD(23), c)
        line([(cx-21,cy+20),(cx-12,cy+16),(cx-4,cy+19),(cx+5,cy+10),(cx+13,cy+12),(cx+21,cy+3)], "#72c6a7", 2)
    elif kind == "leaf":
        d.ellipse((cx-16,cy-19,cx+16,cy+18), outline=c, width=3)
        line([(cx-12,cy+14),(cx+12,cy-14)], c, 2)
        line([(cx-6,cy+2),(cx-10,cy-7)], c, 2)
        line([(cx+2,cy-6),(cx+11,cy-8)], c, 2)
    else:
        for offset in (-9, 1, 11):
            pts = [(cx-19,cy+offset)]
            pts += [(cx+x, cy+offset + int(5*((x+19)/8)%2)) for x in range(-11,20,8)]
            line(pts, c, 2)

def draw_card(x, y, color, kicker, title, body, meta, kind):
    w, h = 446, 206
    d.rounded_rectangle((x,y,x+w,y+h), radius=17, fill=PAPER)
    d.rounded_rectangle((x,y,x+7,y+h), radius=4, fill=color)
    label(x+26,y+17,kicker,BOLD(13),color)
    label(x+26,y+45,title[0],BOLD(25),INK)
    label(x+26,y+74,title[1],BOLD(25),INK)
    for i, row in enumerate(textwrap.wrap(body, width=39)[:3]):
        label(x+26,y+112+i*19,row,REG,"#59636a")
    label(x+26,y+177,meta,BOLD(11),"#798187")
    icon(x+390,y+74,kind)

label(56,25,"THE GLOBAL LEDGER",BOLD(18),GOLD)
label(723,29,"NO. 118  •  GLOBAL EDITION",BOLD(12),"#d1d7da")
d.rectangle((56,60,968,62), fill="#34414b")
label(56,82,"Wednesday 25 November 2026",BOLD(49),WHITE)
label(59,148,"Five stories shaping the day",REG,GRAY)

draw_card(56,196,"#b94350","SPACE · CAPE CANAVERAL",["Lunar lander","aces descent test"],"Reusable crewed lander clears final hover trial","24 Nov  /  RN","rocket")
draw_card(522,196,"#138b83","MARKETS · TOKYO",["Yen steadies as","boj holds rates"],"Exporters rally after hold decision","24 Nov  /  NK","coin")
draw_card(56,420,"#555da8","CLIMATE · NAIROBI",["Solar microgrids","reach 2m homes"],"Off-grid program scales across East Africa","24 Nov  /  UN","leaf")
draw_card(522,420,"#d17738","CHESS · DOHA",["Chess worlds: Game 7","ends in draw"],"Tiebreaks loom after quiet endgame","24 Nov  /  FID","wave")

# The day's lead story
x,y,w,h = 56,650,912,236
d.rounded_rectangle((x,y,x+w,y+h), radius=18, fill="#1c2a38")
green = "#62d0a1"
label(224,674,"ENERGY  /  BRUSSELS",BOLD(13),green)
d.rounded_rectangle((850,667,932,697),radius=15,fill="#176f70")
label(870,674,"GRID",BOLD(12),"#e1f2ec")
# transmission pylon
px, py = 143, 768
line([(px,py-58),(px-30,py+67),(px+30,py+67),(px,py-58)],"#83a0a8",3)
line([(px-18,py-11),(px+18,py-11)],"#83a0a8",3)
line([(px-23,py+14),(px+23,py+14)],"#83a0a8",3)
line([(px-27,py+42),(px+27,py+42)],"#83a0a8",3)
line([(px-36,py-31),(px+36,py-31)],"#83a0a8",3)
for a,b in [(-18,-11),(18,-11),(-23,14),(23,14),(-27,42),(27,42)]:
    line([(px,py-58),(px+a,py+b)],"#526975",2)
label(224,707,"Europe's offshore grid links three seas for the first time",BOLD(26),WHITE)
label(224,758,"Interconnectors cut curtailment and smooth",REG,GRAY)
label(224,782,"winter peaks across the North and Baltic.  /  24 Nov",REG,GRAY)

d.rectangle((56,916,968,918),fill="#34414b")
label(56,939,"WORLD DESK  •  Reported 25 November 2026",BOLD(12),"#b8c0c4")
label(785,939,"5 STORIES / ONE DAY",BOLD(12),GOLD)

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "entry.png")
img.save(out_path)
print(f"wrote {out_path}")
