//
// Created by hyj on 2018/7/4.
//

#include <iostream>
#include <cstring>
#include <unistd.h>
#include <vector>
#include <signal.h>
#include <stdlib.h>
#include "GdbHook.h"

using namespace std;

void SplitString(const std::string s, std::vector<std::string>& v, const std::string c)
{
    std::string::size_type pos1, pos2;
    pos2 = s.find(c);
    pos1 = 0;
    while(std::string::npos != pos2)
    {
        string item = s.substr(pos1, pos2-pos1);
        if (item.length() > 0) {
            v.push_back(item);
        }

        pos1 = pos2 + c.size();
        pos2 = s.find(c, pos1);
    }
    if(pos1 != s.length())
        v.push_back(s.substr(pos1));
}

void testSplit()
{
    {
        vector<string> v;
        SplitString("ls   -a -s a ", v, " ");
        for (int i = 0; i < v.size(); ++i) {
            cout << v[i] << endl;
        }
    }

}

int main()
{
    int ret = 0;
    while (1) {
        char *cmd = new char[500];
        strcpy(cmd, "ls");
        ret = 1; /*nothing, break here, and set env  __GDB_HOOK__RUNCMD=your_cmd*/
/*
        call setenv("__GDB_HOOK__RUNCMD", "SetData TIMER 6 ALL", 1)
*/
        if (NULL != getenv("__GDB_HOOK__RUNCMD")) {
            strcpy(cmd, getenv("__GDB_HOOK__RUNCMD"));
        }
        if (strcmp(cmd, "ls") == 0) {
            sleep(1);
            delete(cmd);
            continue;
        }
        signal(SIGTRAP, SIG_IGN);
        int pid = fork();
        if (pid > 0) {
            /*continue*/
            setsid();
        } else if (pid == 0) {
            signal(SIGCHLD, NULL);

            char *cmdArgv[100];
            vector<string> cmdList;
            SplitString(cmd, cmdList, " ");
            int i;
            for (i = 0; i < cmdList.size(); ++i) {
                cmdArgv[i] = const_cast<char *>(cmdList[i].c_str());
            }
            cmdArgv[i] = NULL;
            execvp(cmdArgv[0], cmdArgv);
            exit(0);
        }

        delete(cmd);
        setenv("__GDB_HOOK__RUNCMD", "ls", 1);
    }
}