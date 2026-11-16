"""Check a real emulator sensor trigger through automatic return, using frozen fixture time."""
from pathlib import Path
import argparse,json,time
from capture_native import ROOT,run,capture,monitor_port

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--platform',choices=['emery','chalk','gabbro'],required=True);opt=parser.parse_args()
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid'];port=monitor_port();dest=ROOT/'.tmp/native'/opt.platform
 def send(v):run(['pebble','send-app-message','--emulator',opt.platform,'--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={value}' for k,value in v.items()])
 def neutral():run(['pebble','emu-accel','--emulator',opt.platform,'gravity-z']);time.sleep(.6)
 roll=ROOT/'.tmp/roll.csv';roll.write_text('750,0,-600\n')
 def trigger():run(['pebble','emu-accel','--emulator',opt.platform,'custom',str(roll)])
 send({11000:10,11001:42,11002:2,11003:-1,'Motion':1,'Trigger':2,'DateFormat':0});neutral();baseline=capture(port)
 trigger();start=time.monotonic();frames=[];changed=[]
 while time.monotonic()-start<6.5:
  elapsed=time.monotonic()-start;frame=capture(port);different=frame.tobytes()!=baseline.tobytes();changed.append((elapsed,different));frames.append(frame)
  time.sleep(.08)
 assert any(d for _,d in changed),'Sensor did not trigger visible motion'
 assert not any(d for t,d in changed if t>3.4),'Automatic reassembly or held-roll suppression failed'
 frames[0].save(dest/'sensor-motion.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
 send({'Motion':0});neutral();baseline=capture(port);trigger();time.sleep(1);assert capture(port).tobytes()==baseline.tobytes(),'Motion Off animated'
 send({'Motion':1});neutral();trigger();time.sleep(.5);send({11001:43});time.sleep(3.2);actual=capture(port)
 send({11003:3000});time.sleep(.2);expected=capture(port);assert actual.tobytes()==expected.tobytes(),'Minute change did not survive reassembly'
 actual.save(dest/'after-minute-change.png')
 send({11003:-1,11001:42,'Motion':1,'Trigger':2,'DateFormat':0});neutral()
 report={'sensor_triggered':True,'automatic_return':True,'held_roll_no_retrigger':True,'motion_off':True,'minute_change_during_animation':True,'samples':len(changed),'states':changed}
 (dest/'sensor-checks.json').write_text(json.dumps(report,indent=2));print('PASS sensor→animation→return, held-roll suppression, Motion Off, minute change:',opt.platform)
if __name__=='__main__':main()
