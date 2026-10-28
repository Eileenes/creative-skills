#!/usr/bin/env python3
"""Create a new film workspace from bundled templates; never downloads dependencies."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

REQUIRED = (
    'lib/motion.js', 'scripts/stills.py', 'scripts/render.py',
    'scripts/verify_promo.py', 'scripts/sfx_palette.py',
)


def prepare(platform, output, onetake=None):
    # Do not resolve a dangling destination symlink into a different target.
    dest = Path(os.path.abspath(Path(output).expanduser()))
    if os.path.lexists(dest):
        raise ValueError(f'Output already exists; choose a new directory: {dest}')
    source = Path(__file__).resolve().parents[1] / 'assets' / 'promo-kit'
    dependency = Path(onetake).expanduser().resolve() if onetake else None
    if dependency:
        missing = [name for name in REQUIRED if not (dependency / name).is_file()]
        if missing:
            raise ValueError('Incomplete Onetake installation: ' + ', '.join(missing))
    dest.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.promo-', dir=dest.parent))
    try:
        shutil.copytree(source, staging, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        shutil.copyfile(staging / 'examples' / f'{platform}.json', staging / 'config.json')
        state = {'platform': platform, 'demo_data': True, 'onetake': None,
                 'status': 'prepared; replace demo data and install rendering dependencies'}
        if dependency:
            (staging / 'onetake').symlink_to(dependency, target_is_directory=True)
            (staging / 'motion.js').symlink_to(dependency / 'lib' / 'motion.js')
            revision = None
            if (dependency / '.git').exists():
                result = subprocess.run(['git', '-C', str(dependency), 'rev-parse', 'HEAD'],
                                        capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    revision = result.stdout.strip()
            state['onetake'] = {'path': str(dependency), 'git_revision': revision,
                                 'license': 'check the linked installation; not inferred by this tool'}
        (staging / 'project-state.json').write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        # mkdir fails if another operation creates this destination in the meantime.
        dest.mkdir()
        try:
            for item in staging.iterdir():
                shutil.move(str(item), str(dest / item.name))
        except Exception:
            shutil.rmtree(dest)
            raise
    finally:
        shutil.rmtree(staging)
    return dest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform', choices=['x', 'xhs', 'wechat', 'web'], required=True)
    parser.add_argument('--output', required=True, help='New, non-existing film directory')
    parser.add_argument('--onetake', help='Existing, appropriately licensed Onetake installation')
    args = parser.parse_args()
    try:
        output = prepare(args.platform, args.output, args.onetake)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Cannot prepare project: {exc}\n')
    print(f'Prepared: {output}')
    print('Replace demo config, prepare dependencies, then build and inspect stills before rendering.')


if __name__ == '__main__':
    main()
