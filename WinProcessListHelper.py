import paramiko
import os
import sys
import ConfigParser

sys.path.append(os.path.dirname(sys.argv[0]))
import config_place

config = ConfigParser.ConfigParser()
config.read(config_place.configFilePath)

class SSHCmd:
    def __init__(self, hostName, userName, password):
        self.hostName = hostName
        self.userName = userName
        self.password = password

    def run(self, cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostName, username=self.userName, password=self.password)
        self.chan = ssh._transport.open_session(timeout=5)
        self.chan.exec_command(cmd)

        retData = []
        while True:
            data = self.chan.recv(1024)
            if not data:
                break
            retData.append(data.strip())
        return retData


if __name__ == "__main__":
    outData = ""
    # winProcListCmd = "WinProcessListHelper.exe.bak"
    # for arg in sys.argv:
    #     winProcListCmd += " " + arg
    # output = os.popen(winProcListCmd)
    # for line in output:
    #     outData += line

    sshcmd = SSHCmd(config.get("server", "host"),
                    config.get("server", "user"),
                    config.get("server", "password"))
    data = sshcmd.run("for pid in `ps xu | grep -v PID | awk '{print $2}'`; do echo $pid  ` ls -l /proc/$pid/exe | awk -F'->' '{print $2}'` ; done")
    for line in data:
        sp = line.split()
        if len(sp) != 2:
            continue
        pid, cmdLine = sp
        sp1 = cmdLine.split("/")
        exe = sp1[len(sp1)-1]
        outData += "%s\n%s\n%s\n" % (pid, exe, cmdLine)

    sys.stdout.write(outData)

