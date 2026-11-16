"""Capture native runtime poses/colors and produce per-platform lossless store previews."""
from pathlib import Path
import argparse,json,time,hashlib
from PIL import Image,ImageOps
from capture_native import ROOT,run,capture,monitor_port
PALETTES=[('original',0xFFFFAA,0,0xFF5500,0),('midnight',0x000055,0xFFFFFF,0xFF5500,1),('mint',0xAAFFAA,0,0xAA0055,0),('paper',0xFFFFFF,0,0x0000AA,0)]
SIZES={'emery':(200,228),'chalk':(180,180),'gabbro':(260,260)}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--platform',choices=list(SIZES),required=True);opt=parser.parse_args()
 platform=opt.platform;port=monitor_port();dest=ROOT/'media/store';dest.mkdir(parents=True,exist_ok=True)
 raw=ROOT/'.tmp/store-native'/platform;raw.mkdir(parents=True,exist_ok=True)
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid']
 def send(v):run(['pebble','send-app-message','--emulator',platform,'--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={value}' for k,value in v.items()]);time.sleep(.12)
 def shot():
  im=capture(port);assert im.size==SIZES[platform];return im
 def palette(p):
  name,bg,fg,accent,date=p;send({'Background':bg,'Foreground':fg,'Accent':accent,'DateFormat':date,11003:3000});im=shot()
  assert im.getpixel((im.width//2,im.height*15//100))==((bg>>16)&255,(bg>>8)&255,bg&255),'Wrong active face/palette'
  return im
 send({'Motion':0,'Trigger':0,11000:10,11001:42,11002:2,11004:1,11003:3000})
 stills={p[0]:palette(p) for p in PALETTES}
 for name,im in stills.items():im.save(raw/f'{name}.png')
 palette(PALETTES[0]);frames=[stills['original']];durations=[1000]
 for elapsed in range(150,3000,150):
  send({11003:elapsed});im=shot();im.save(raw/f'phase-{elapsed}.png');frames.append(im);durations.append(150)
 send({11003:3000});last=shot();assert last.tobytes()==stills['original'].tobytes(),'Rest did not restore exactly'
 assert frames[8].tobytes()!=last.tobytes(),'Fixture pose override not active; wrong build'
 frames.append(last);durations.append(1000)
 for name in ['midnight','mint','paper']:frames.append(stills[name]);durations.append(1800)
 frames.append(stills['original']);durations.append(800)
 compacted=[];timings=[]
 for frame,duration in zip(frames,durations):
  if compacted and frame.tobytes()==compacted[-1].tobytes():timings[-1]+=duration
  else:compacted.append(frame);timings.append(duration)
 frames,durations=compacted,timings
 gif=dest/f'{platform}_01_tumble_colors.gif'
 frames[0].save(gif,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2,optimize=False)
 with Image.open(gif) as decoded:
  assert decoded.n_frames==len(frames)
  for i,source in enumerate(frames):decoded.seek(i);assert decoded.convert('RGB').tobytes()==source.tobytes();assert decoded.info['duration']==durations[i]
 outputs=[gif]
 for i,name in enumerate(['original','midnight','mint'],2):
  path=dest/f'{platform}_{i:02}_{name}.gif';stills[name].save(path)
  with Image.open(path) as saved:assert saved.convert('RGB').tobytes()==stills[name].tobytes()
  outputs.append(path)
 if platform=='emery':
  for size,label in [(80,'small'),(144,'large')]:
   icon=Image.new('RGB',(size,size),(255,255,170));source=ImageOps.contain(stills['original'].crop((10,72,190,135)),(size-8,size-8),Image.Resampling.NEAREST);icon.paste(source,((size-source.width)//2,(size-source.height)//2));icon.save(dest/f'icon-{label}.png')
 (raw/'manifest.json').write_text(json.dumps({'platform':platform,'source':'native fixture renderer','size':SIZES[platform],'gif_frames':len(frames),'gif_duration_ms':sum(durations),'assets':[{'path':str(p),'sha256':digest(p)} for p in outputs]},indent=2))
 send({'Motion':1,'Trigger':0,'Background':0xFFFFAA,'Foreground':0,'Accent':0xFF5500,'DateFormat':0,11003:-1})
 print('STAGED',platform,len(outputs),'assets;',len(frames),'GIF frames;',sum(durations),'ms',flush=True)
if __name__=='__main__':main()
