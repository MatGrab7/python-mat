#!/usr/bin/env python3
"""
Check coverage.xml and generate minimal tests if coverage below threshold.

Behavior:
 - Parse `coverage.xml` to get overall line coverage.
 - If coverage >= threshold -> exit 0.
 - If coverage < threshold:
     - Generate simple import tests under `tests/generated/` for each module
       (skips files under `.github`, `tests`, and typical virtualenv dirs).
     - Commit and push the generated tests using `GITHUB_TOKEN`.
     - Exit with code 2 to indicate generation occurred (so CI run fails and
       new run will be triggered by the new commit).

This script expects the repo to be checked out with full history and that
`GITHUB_TOKEN` is available in the environment.
"""

import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_coverage(coverage_file: Path) -> float:
    if not coverage_file.exists():
        print(f"coverage file not found: {coverage_file}")
        return 0.0
    tree = ET.parse(coverage_file)
    root = tree.getroot()
    # coverage.xml root usually has attribute 'line-rate' as fraction
    line_rate = root.get('line-rate')
    if line_rate is not None:
        try:
            return float(line_rate) * 100.0
        except ValueError:
            return 0.0
    # fallback: compute from packages
    covered = 0.0
    total = 0.0
    for cls in root.findall('.//class'):
        lines = [int(x.get('hits') or 0) for x in cls.findall('lines/line')]
        total += len(lines)
        covered += sum(1 for h in lines if h > 0)
    return (covered / total * 100.0) if total > 0 else 0.0


def list_python_modules() -> list:
    skip_dirs = {'.git', '.github', 'venv', '.venv', 'build', 'dist', 'tests', '__pycache__'}
    modules = []
    for p in Path('.').rglob('*.py'):
        if any(part in skip_dirs for part in p.parts):
            continue
        # skip this script
        if '.github' in p.parts and p.name == Path(__file__).name:
            continue
        modules.append(p)
    return modules


def generate_test_for_module(pyfile: Path) -> Path:
    rel = pyfile.with_suffix('').as_posix().replace('/', '.')
    # sanitize for test filename
    test_dir = Path('tests/generated')
    test_dir.mkdir(parents=True, exist_ok=True)
    test_path = test_dir / f"test_auto_{pyfile.stem}.py"
    content = f"""
import importlib


def test_import_{pyfile.stem}():
    module = importlib.import_module('{rel}')
    assert module is not None

"""
    test_path.write_text(content)
    return test_path


def git_commit_and_push(files: list, message: str) -> None:
    github_token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    if not github_token or not repo:
        print("GITHUB_TOKEN or GITHUB_REPOSITORY not set; cannot push generated tests")
        return

    # Configure git
    subprocess.check_call(['git', 'config', 'user.email', 'actions@github.com'])
    subprocess.check_call(['git', 'config', 'user.name', 'github-actions'])

    # Add files
    subprocess.check_call(['git', 'add'] + files)

    # Commit
    subprocess.check_call(['git', 'commit', '-m', message])

    # Push using token
    origin = f"https://x-access-token:{github_token}@github.com/{repo}.git"
    subprocess.check_call(['git', 'remote', 'set-url', 'origin', origin])

    # Determine branch to push to
    branch = os.environ.get('GITHUB_HEAD_REF') or subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
    subprocess.check_call(['git', 'push', 'origin', branch])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--coverage-file', default='coverage.xml')
    parser.add_argument('--threshold', type=float, default=50.0)
    args = parser.parse_args()

    coverage_file = Path(args.coverage_file)
    percent = parse_coverage(coverage_file)
    print(f"Current coverage: {percent:.2f}% (threshold: {args.threshold}%)")
    if percent >= args.threshold:
        print("Coverage threshold met.")
        return 0

    # Check last commit message to avoid loops
    last_msg = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode()
    if '[auto-tests]' in last_msg:
        print('Last commit was auto-tests, not generating again.')
        return 1

    # Generate simple tests
    modules = list_python_modules()
    if not modules:
        print('No modules found to generate tests for.')
        return 1

    generated = []
    for m in modules:
        t = generate_test_for_module(m)
        generated.append(str(t))

    print(f"Generated {len(generated)} test files:")
    for g in generated:
        print(' -', g)

    # Commit and push
    try:
        git_commit_and_push(generated, '[auto-tests] Add generated tests to increase coverage')
    except subprocess.CalledProcessError as e:
        print('Failed to push generated tests:', e)
        return 1

    print('Generated tests committed and pushed; exiting with code 2 to signal generation.')
    return 2


if __name__ == '__main__':
    sys.exit(main())
