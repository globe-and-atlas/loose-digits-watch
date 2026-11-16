"""Clean three-platform Pebble build. Fixtures never enter dist."""
from pathlib import Path
import argparse, os, shutil, subprocess, zipfile, json
ROOT=Path(__file__).resolve().parents[1]
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--fixture',action='store_true');opt=parser.parse_args()
 env={k:v for k,v in os.environ.items() if not k.startswith('LD_')}
 if opt.fixture:env['LD_FIXTURE']='1'
 for command in [['pebble','clean'],['pebble','build']]:subprocess.run(command,cwd=ROOT/'watchface',env=env,check=True,timeout=180)
 source=ROOT/'watchface/build/watchface.pbw'
 with zipfile.ZipFile(source) as z:
  for platform in ['emery','chalk','gabbro']:assert f'{platform}/pebble-app.bin' in z.namelist()
 version=json.loads((ROOT/'watchface/package.json').read_text())['version']
 dest=ROOT/('.tmp/Loose-Digits-fixture.pbw' if opt.fixture else f'dist/Loose-Digits-{version}.pbw');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
 (ROOT/'.tmp/last-build.json').write_text(json.dumps({'fixture':opt.fixture,'path':str(dest)},indent=2))
 print(dest)
if __name__=='__main__':main()
