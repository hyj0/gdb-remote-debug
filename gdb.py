import os
import thread
import paramiko
import sys
import ConfigParser

sys.path.append(os.path.dirname(sys.argv[0]))
import config_place
import utils

config = ConfigParser.ConfigParser()
config.read(config_place.configFilePath)

localMapPath = utils.replaceLess(
        config.get("mapping", "localMapPath").replace("\\", "/") + "/",
        "//", "/")
tmpPath = localMapPath.replace(":", "")
tmpPath = tmpPath[0].lower() + tmpPath[1:]
localMapPathCygwin = "/cygdrive/" + tmpPath

serverMapPath = utils.replaceLess(
        config.get("mapping", "serverMapPath").replace("\\", "/") + "/",
        "//", "/")
localEnv = 1  # always use Mingw style path


class SSHCmd:
    def __init__(self, hostName, userName, password):
        self.hostName = hostName
        self.userName = userName
        self.password = password

    def run(self, cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostName, username=self.userName, password=self.password)
        chan = ssh._transport.open_session()
        chan.exec_command(cmd)

        def doStdin(chan):
            while True:
                buff = ''
                sendBuff = ''
                while True:
                    d = sys.stdin.read(1)
                    if not d:
                        break
                    buff += d
                    sendBuff += d
                    sys.stderr.write(d)
                    if d == '\n':
                        if buff.find("-break-insert -f") == 0 \
                                or buff.find("-file-exec-and-symbols") == 0 \
                                or buff.find("-environment-cd") == 0:
                            sendBuff = sendBuff.replace(localMapPath, serverMapPath)
                            sendBuff = sendBuff.replace(localMapPathCygwin, serverMapPath)
                        break
                sys.stderr.write(sendBuff)
                sys.stderr.flush()
                chan.send(sendBuff)

        def doChan(sock):
            while True:
                data = sock.recv(2560)
                if not data:
                    sys.stderr.write('\r\nchan *** EOF ***\r\n\r\n')
                    sys.stderr.flush()
                    break
                if data.find(serverMapPath) > 0:
                    if localEnv == 1:
                        data = data.replace(serverMapPath, localMapPath)
                    if localEnv == 2:
                        data = data.replace(serverMapPath, localMapPathCygwin)
                sys.stderr.write(data)
                sys.stderr.flush()
                sys.stdout.write(data)
                sys.stdout.flush()

        thread.start_new_thread(doStdin, (chan,))
        doChan(chan)
        thread.exit_thread()


if __name__ == "__main__":
    sshcmd = SSHCmd(config.get("server", "host"),
                    config.get("server", "user"),
                    config.get("server", "password"))
    argStr = ""
    for s in sys.argv[1:]:
        argStr += " " + s
    sys.stderr.write("py:args=" + argStr + "\n")
    sshcmd.run(config.get("server", "gdb") + argStr)
