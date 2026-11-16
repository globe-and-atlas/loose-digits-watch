"""Exercise case-knock inputs and persistent custom colors on the active native fixture."""
from pathlib import Path
import argparse,json,time
from capture_native import ROOT,run,capture,monitor_port

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--platform',choices=['emery','chalk','gabbro'],required=True);opt=parser.parse_args()
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid'];port=monitor_port()
 dest=ROOT/'.tmp/knocks-colors'/opt.platform;dest.mkdir(parents=True,exist_ok=True)
 def send(v):run(['pebble','send-app-message','--emulator',opt.platform,'--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={value}' for k,value in v.items()]);time.sleep(.12)
 def neutral():run(['pebble','emu-accel','--emulator',opt.platform,'gravity-z']);time.sleep(.35)
 def replay(name,double):
  samples=['0,0,-1000']*5+['0,1200,-1000']*2+['0,0,-1000']*8
  if double:samples+=['0,1200,-1000']*2
  samples+=['0,0,-1000']*200
  path=ROOT/f'.tmp/{name}.csv';path.write_text('\n'.join(samples)+'\n');run(['pebble','emu-accel','--emulator',opt.platform,'custom',str(path)])
 def observe(seconds,base):
  frames=[];states=[];start=time.monotonic()
  while time.monotonic()-start<seconds:
   elapsed=time.monotonic()-start;im=capture(port);frames.append(im);states.append((elapsed,im.tobytes()!=base.tobytes()));time.sleep(.07)
  return frames,states
 defaults={'Motion':1,'Trigger':0,'DateFormat':0,'Background':0xFFFFAA,'Foreground':0,'Accent':0xFF5500,11003:-1,11000:10,11001:42,11002:2}
 send(defaults);neutral()
 # Reject an old version of the same face left running after installation.
 send({'Background':0x000055});probe=capture(port);assert probe.getpixel((probe.width//2,probe.height*15//100))==(0,0,85),'Old active face version: custom color probe failed'
 send({'Background':0xFFFFAA});baseline=capture(port);assert baseline.getpixel((baseline.width//2,baseline.height*15//100))==(255,255,170),'Wrong active face'
 replay('single-knock',False);_,single_states=observe(1.0,baseline);assert not any(c for _,c in single_states),'Single knock triggered double mode';neutral()
 replay('double-knock',True);frames,states=observe(4.1,baseline);neutral()
 assert any(c for _,c in states),'Double knock did not trigger';assert not any(c for t,c in states if t>3.8),'Double knock did not automatically reassemble'
 frames[0].save(dest/'double-knock.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
 send({'Motion':0});neutral();replay('off-double',True);_,off=observe(1.0,baseline);assert not any(c for _,c in off),'Motion Off allowed knock';neutral()
 send({'Motion':1,'Trigger':1});neutral();replay('single-mode',False);_,single_mode=observe(.9,baseline);assert any(c for _,c in single_mode),'Single mode failed';neutral();time.sleep(3)
 send({'Background':0x000055,'Foreground':0xFFFFFF,'Accent':0xFF5500,'DateFormat':1,11003:3000});custom=capture(port)
 assert custom.getpixel((custom.width//2,custom.height*15//100))==(0,0,85)
 assert sum(p==(255,255,255) for p in custom.get_flattened_data())>100
 assert sum(p==(255,85,0) for p in custom.get_flattened_data())>0
 custom.save(dest/'custom.png')
 run(['pebble','install','--emulator',opt.platform,str(ROOT/'.tmp/Loose-Digits-fixture.pbw')]);time.sleep(.5)
 deadline=time.monotonic()+5
 while True:
  persisted=capture(port)
  if persisted.tobytes()==custom.tobytes():break
  if time.monotonic()>deadline:
   persisted.save(dest/'persistence-failure.png');raise AssertionError('Custom colors/date did not persist after reinstall')
  time.sleep(.1)
 persisted.save(dest/'persisted.png')
 # Equal palette entries must still leave a readable clock.
 send({'Foreground':0x000055,'Accent':0x000055});same=capture(port);assert sum(p==(255,255,255) for p in same.get_flattened_data())>100;same.save(dest/'contrast-fallback.png')
 send({'Background':0x00FF00,'Foreground':0x00FF00,'Accent':0x00FF00});green=capture(port);assert sum(p==(0,0,0) for p in green.crop((green.width*20//100,green.height*35//100,green.width*80//100,green.height*60//100)).get_flattened_data())>100;green.save(dest/'green-contrast.png')
 send({'Background':0xFFFFAA,'Foreground':0,'Accent':0xFF5500,'Trigger':0,'DateFormat':0,11003:3000})
 (dest/'checks.json').write_text(json.dumps({'synthetic_peak_samples':2,'double_knock':True,'single_ignored_in_double_mode':True,'single_mode':True,'motion_off':True,'automatic_return':True,'custom_colors':True,'color_persistence':True,'contrast_fallback':True,'states':states},indent=2));print('PASS knocks, colors, persistence, contrast:',opt.platform)
if __name__=='__main__':main()
