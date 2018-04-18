# gdb-remote-debug
fake gdb use paramiko(ssh) to debug program on remote server, now use for Clion
### how to install:
#### step1:
    cd gdb-remote-debug dir
	run: python setup.py
#### step2:
	copy gdb-remote-debug/dist/WinProcessListHelper.exe to Clion's install dir's bin/WinProcessListHelper.exe (backup it)
#### step3:
	edit gdb-remote-debug/config.ini
	make sure the server files sync local files
#### step4:
	Clion:[File]-->[Settings...]-->[Build,Exection,Develoyment]-->[Debugger] choise gdb-remote-debug/dist/gdb.exe
	if can not choise, please replace the Cygwin/Mingw's gdb.exe with our gdb.exe

#### how to use:
	compile your code with -g on server and run it with user in the gdb-remote-dubug/config.ini
	use Clion make breakpoint
	Clion:[run]-->[Attach to Local Process...] choise program that you run
good luck
