"""Capture deterministic fixture states from the currently owned emulator; never boots it."""
from pathlib import Path
import argparse, json, re, socket, subprocess, time
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def run(args):
 return subprocess.run(args,cwd=ROOT/'watchface',check=True,capture_output=True,text=True,timeout=60).stdout
def monitor_port():
 # Keep process arguments private; inspect only the qemu command in memory.
 rows=run(['ps','-axo','comm,args']).splitlines()
 rows=[r for r in rows if r.split()[0].endswith('qemu-pebble')]
 if len(rows)!=1:raise RuntimeError('Expected exactly one QEMU owner')
 return int(re.search(r'-monitor tcp::(\d+)',rows[0]).group(1))
def capture(port):
 path=ROOT/'.tmp/native.ppm';path.unlink(missing_ok=True)
 with socket.create_connection(('localhost',port),timeout=5) as conn:
  conn.recv(65536);conn.sendall(f'screendump "{path}"\n'.encode())
  deadline=time.monotonic()+5
  while time.monotonic()<deadline:
   try:
    with Image.open(path) as source:im=source.convert('RGB');im.load()
    break
   except (OSError,FileNotFoundError):time.sleep(.01)
  else:raise TimeoutError('Native framebuffer missing')
 # QEMU screen brightness scales its palette. Restore the known full-scale palette.
 peak=max(max(pixel) for pixel in im.get_flattened_data())
 im=im.point(lambda c:round(c/max(peak,1)*3)*85);path.unlink(missing_ok=True);return im

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--platform',choices=['emery','chalk','gabbro'],required=True);opt=parser.parse_args()
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid'];port=monitor_port()
 def send(values):run(['pebble','send-app-message','--emulator',opt.platform,'--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={v}' for k,v in values.items()])
 dest=ROOT/'.tmp/native'/opt.platform;dest.mkdir(parents=True,exist_ok=True)
 expected={'emery':(200,228),'chalk':(180,180),'gabbro':(260,260)}[opt.platform]
 cases=[('rest',{11000:10,11001:42,11002:2,11003:3000,'DateFormat':0,'Trigger':0,'Background':0xFFFFAA,'Foreground':0,'Accent':0xFF5500}),('tumble',{11003:1500}),('left',{11004:-1,11003:1500}),('return',{11003:2300}),('iso',{11003:3000,'DateFormat':1}),('us',{'DateFormat':2}),('eu',{'DateFormat':3}),('single-hour',{11000:1,11001:8,11002:1,'DateFormat':0}),('midnight',{11000:0,11001:0,11002:1,'DateFormat':0}),('noon',{11000:12,11001:0,11002:1}),('late',{11000:23,11001:59,11002:2})]
 for name,values in cases:
  send(values);time.sleep(.15);im=capture(port);assert im.size==expected
  assert im.getpixel((im.width//2,im.height*15//100))==(255,255,170), 'Wrong face or stale emulator: background identity failed'
  im.save(dest/f'{name}.png');print('PASS native',opt.platform,name,flush=True)
 assert (dest/'rest.png').read_bytes()!=(dest/'tumble.png').read_bytes(), 'Tumble did not change native image'
 assert (dest/'rest.png').read_bytes()!=(dest/'late.png').read_bytes(), 'Fixture clock is not updating; wrong app active'
 # 16 sampled phases are captured from the real renderer, not reconstructed artwork.
 send({11000:10,11001:42,11002:2,11004:1,'DateFormat':0})
 frames=[]
 for elapsed in range(0,3001,200):
  send({11003:elapsed});time.sleep(.05);frames.append(capture(port));frames[-1].save(dest/f'phase-{elapsed}.png')
 frames[0].save(dest/'native-motion.gif',save_all=True,append_images=frames[1:],duration=200,loop=0)
 send({11003:-1,11000:10,11001:42,11002:2,'Motion':1,'DateFormat':0})
 (dest/'checks.json').write_text(json.dumps({'platform':opt.platform,'size':expected,'cases':[n for n,v in cases],'motion':'fixture phases; live sensor trial separate'},indent=2))
if __name__=='__main__':main()
