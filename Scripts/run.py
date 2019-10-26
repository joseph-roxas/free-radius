import subprocess
import re
import serialconn

def account(time):
    if time == 6:
        path = "/home/joseph/Scripts/request_account_6hrs.sh"
    if time == 12:
        path = "/home/joseph/Scripts/request_account_12hrs.sh"
    if time == 24:
        path = "/home/joseph/Scripts/request_account_24hrs.sh"

    rc = subprocess.check_output(path).decode("utf-8")
    out = re.findall(r"[\w']+", rc)
    return out[2], out[3]


def print_account(time):
    username, password = account(time)

    serialconn.connect(username, password, time)

    return None
