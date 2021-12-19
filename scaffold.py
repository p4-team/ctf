#!/usr/bin/env python3

"""
Usage:

python3 scaffold.py new hxp "hxp CTF 2021" 10 1017
python3 scaffold.py add hxp "Log 4 Sanity" misc
"""

from pathlib import Path
from datetime import datetime
import argparse
import re


def new_ctf(args):
    stamp = datetime.now().isoformat()[:10]

    dirname = f"{stamp}-{args.slug}"

    readme = Path(__file__).parent / "README.md"
    readme_text = readme.read_text()

    pretty_stamp = stamp.replace("-", '.')
    headline = f"* [{pretty_stamp} **{args.name}**({args.place}th place/{args.teams} teams)]({dirname})"

    year = datetime.now().year
    mdyear = f"## {year}"
    if mdyear not in readme_text:
        raise RuntimeError(f"Not implemented: Add '{mdyear}' to the README manually")
    elif headline not in readme_text: 
        readme_text = re.sub(mdyear, f"{mdyear}\n{headline}", readme_text)
        readme.write_text(readme_text)

    newdir = Path(__file__).parent / dirname
    if newdir.exists():
        raise RuntimeError(f"Huh, {newdir} already exists, are you sure?")
    newdir.mkdir()

    content = f"""# {args.name}

### Table of contents

"""
    (newdir / "README.md").write_text(content)


def add_task(args):
    dirname = Path(__file__).parent.glob(f"*-{args.slug}")
    choices = list(sorted(dirname))
    dirname = choices[-1]
    if len(choices) > 1:
        print(f"Multiple matches, using {dirname}")
    
    slug = args.task.lower().replace("/", '_').replace(" ", "-")
    (dirname / slug).mkdir()
    (dirname / slug / "README.md").write_text(f"# {args.task}")

    readme = (dirname / "README.md").read_text()
    readme += f"* [{args.task} ({args.category})]({slug})\n"
    (dirname / "README.md").write_text(readme)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")
    subparsers.required = True

    newctf = subparsers.add_parser('new', description="Add a CTF template")
    newctf.add_argument("slug", help="CTF slug, like 'dragonctf'")
    newctf.add_argument("name", help="CTF name, like 'Dragon CTF 2021'")
    newctf.add_argument("place", help="Place achieved during the CTF, like '2'")
    newctf.add_argument("teams", help="How many teams competed?")
    newctf.set_defaults(func=new_ctf)

    addtask = subparsers.add_parser('add', description="Add a task to ctf")
    addtask.add_argument("slug", help="CTF slug, like 'dragonctf'")
    addtask.add_argument("task", help="task name, like 'Dragon Vm'")
    addtask.add_argument("category", help="task category, like 're'")
    addtask.set_defaults(func=add_task)

    args = parser.parse_args()
    args.func(args)



if __name__ == "__main__":
    main()