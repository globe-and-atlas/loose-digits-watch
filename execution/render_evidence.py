"""Compose native renderer phase captures into a labeled comparison animation."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
def main():
 frames=[];font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',22)
 for elapsed in range(0,3001,200):
  board=Image.new('RGB',(1160,640),(239,234,222));d=ImageDraw.Draw(board)
  d.text((580,40),'LOOSE DIGITS · NATIVE EMULATOR RENDERS',font=font,anchor='mm',fill=(30,30,30))
  for target,cx,label in [('emery',200,'Time 2'),('chalk',580,'Time Round'),('gabbro',960,'Round 2')]:
   im=Image.open(ROOT/f'.tmp/native/{target}/phase-{elapsed}.png').convert('RGB');scale=1.5
   im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
   mask=None
   if target!='emery':
    mask=Image.new('L',im.size,0);ImageDraw.Draw(mask).ellipse((0,0,im.width-1,im.height-1),fill=255)
   board.paste(im,(cx-im.width//2,300-im.height//2),mask);d.text((cx,540),label,font=font,anchor='mm',fill=(30,30,30))
  d.text((580,595),'Sampled renderer phases · live sensor tests passed separately',font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',17),anchor='mm',fill=(60,60,60))
  frames.append(board)
 frames[0].save(ROOT/'.tmp/native-comparison.gif',save_all=True,append_images=frames[1:],duration=200,loop=0)
 frames[0].save(ROOT/'.tmp/native-comparison.png')
 print(ROOT/'.tmp/native-comparison.gif')
if __name__=='__main__':main()
