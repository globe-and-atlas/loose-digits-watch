"""Run host policy tests, settings lifecycle tests, and production bundle checks."""
from pathlib import Path
import subprocess,zipfile,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def main():
 binary=ROOT/'.tmp/test-motion';binary.parent.mkdir(parents=True,exist_ok=True)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=undefined,address','-Iwatchface/src/c','tests/test_motion.c','watchface/src/c/motion.c','-o',str(binary)],cwd=ROOT,check=True,timeout=60)
 subprocess.run([str(binary)],cwd=ROOT,check=True,timeout=60)
 subprocess.run(['node','tests/test_settings.js'],cwd=ROOT,check=True,timeout=30)
 version=json.loads((ROOT/'watchface/package.json').read_text())['version']
 path=ROOT/f'dist/Loose-Digits-{version}.pbw'
 with zipfile.ZipFile(path) as bundle:
  for target in ['emery','chalk','gabbro']:
   assert f'{target}/pebble-app.bin' in bundle.namelist()
   data=bundle.read(f'{target}/pebble-app.bin');assert data
   assert b'LD knock' not in data
   assert b'LD x=' not in data, 'Fixture sample logging in production'
  assert b'Loose Digits' in bundle.read('emery/pebble-app.bin')
 assert not json.loads((ROOT/'.tmp/last-build.json').read_text())['fixture'], 'Final build must be production'
 # ELF symbol table proves fixture-only dispatch state was removed by preprocessing.
 nm=Path.home()/'Library/Application Support/Pebble SDK/SDKs/current/toolchain/arm-none-eabi/bin/arm-none-eabi-nm'
 for target in ['emery','chalk','gabbro']:
  symbols=subprocess.run([str(nm),str(ROOT/f'watchface/build/{target}/pebble-app.elf')],check=True,capture_output=True,text=True,timeout=30).stdout
  for name in ['s_frame','s_hour','s_minute','s_format']:assert name not in symbols, f'Fixture state in {target}: {name}'
 print('PASS: production bundle',hashlib.sha256(path.read_bytes()).hexdigest())
if __name__=='__main__':main()
