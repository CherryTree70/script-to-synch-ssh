import paramiko
import json
import os


def useFunction(fun):
    if fun == "overwrite":
        print("overwrite")
        overwrite(host, port, username, password, local, remote,formatedIgnore)
    elif fun == "update":
        print("update")
        update(host, port, username, password, local, remote,formatedIgnore)
    elif fun == "add_non_existing":
        print("add_non_existing")
        add_non_existing(host, port, username, password, local, remote,formatedIgnore)


def overwrite(host, port, username, password, local, remote,formatedIgnore):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    sf = paramiko.Transport(host, port)
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)

    try:
        if os.path.isdir(local):
            for f in os.listdir(local):
                iftrue = 1
                for ing in formatedIgnore:
                    if ing in f:
                        iftrue = 0
                if iftrue == 1:
                    print(f)
                    sftp.put(os.path.join(local + f), remote + "/" + f)

    except ValueError:
        print("Error")
    sf.close()


def update(host, port, username, password, local, remote,formatedIgnore):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    sf = paramiko.Transport(host, port)
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    remotef = sftp.listdir(remote)
    try:
        if os.path.isdir(local):
            for f in os.listdir(local):
                if f in remotef:
                    iftrue = 1
                    for ing in formatedIgnore:
                        if ing in f:
                            iftrue = 0
                    if iftrue == 1:
                        print(f)
                        sftp.put(os.path.join(local + f), remote + "/" + f)
    except ValueError:
        print("Error")
    sf.close()


def add_non_existing(host, port, username, password, local, remote,formatedIgnore):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    sf = paramiko.Transport(host, port)
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    remotef = sftp.listdir(remote)
    try:
        if os.path.isdir(local):
            for f in os.listdir(local):
                if f not in remotef:
                    iftrue = 1
                    for ing in formatedIgnore:
                        if ing in f:
                            iftrue = 0
                    if iftrue == 1:
                        print(f)
                        sftp.put(os.path.join(local + f), remote + "/" + f)
    except ValueError:
        print("Error")
    sf.close()


if __name__ == '__main__':

    with open("config.json") as json_data:
        d = json.load(json_data)

    host = d["server_address"]
    port = d["port"]
    username = d["username"]
    password = "n22piobf"
    local = d["local_folder"]
    remote = d["remote_folder"]
    mode = d["mode"]
    ignore = d["ignore"]
    formatedIgnore = ["." + ext for ext in ignore]
    modeString = str(mode)
    if "|" in modeString:
        functionsToUse = modeString.split("|")
        for fun in functionsToUse:
            useFunction(fun)
    else:
        useFunction(modeString)
