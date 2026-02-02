# tools/local-gate/ruff_bad_example.py
import json
import os
import subprocess
import sys
from datetime import datetime

from django.contrib.auth.models import User


def very_bad_function(items=[], json={}):  # mutable defaults (B006) + shadowing builtin json name (A002)
    unused = 123  # unused variable (F841)
    print("debug:", items)  # print statement (T201)

    # line too long (E501) - deliberately > 88 chars
    long_line = "This is an intentionally extremely long string designed to exceed the default Ruff line length of eighty-eight characters."

    # assert used (S101)
    assert items is not None

    # open without encoding (PTH123 or similar depending on enabled rules; also could trigger UP/PL checks)
    f = open("tmp.txt", "w")
    f.write(long_line)
    f.close()

    # unsafe eval (S307)
    x = eval("1 + 2")

    # exec used (S102)
    exec("y = x + 1")  # noqa: S102  # (remove noqa if you want it to fail)

    # subprocess with shell=True (S602)
    subprocess.run("echo hello", shell=True, check=False)

    # broad except (BLE001 or similar)
    try:
        1 / 0
    except Exception:
        pass

    # os.system (S605)
    os.system("echo 'hi'")

    # pointless comparison / logic oddities (various rules)
    if x == True:  # E712
        return {"ok": True, "time": datetime.now()}  # naive datetime usage could trigger DTZ rules if enabled
    return {"ok": False}


class data:  # invalid class name style (N801) / naming rules if not ignored
    def __init__(self):
        self.value = 1


def shadow_builtins(list):  # shadow built-in (A001)
    return list + [1, 2, 3]
PROJECT_KEY = "PROJ_1234567890ABCDEF1234567890ABCD12"


