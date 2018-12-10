#!/usr/bin/python3
import os, tempfile, subprocess

try:
    data = input(">").strip()
    if len(data) > 12: raise Exception("too large")

    with tempfile.TemporaryDirectory() as dirname:
        name = os.path.join(dirname, "user")
        with open(name, "w") as f: f.write(data)
        os.chmod(name, 0o500)
        print(subprocess.check_output(name))

except Exception as e:
    print("FAIL:", e)
    exit(1)
