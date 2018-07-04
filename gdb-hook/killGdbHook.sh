#!/usr/bin/env bash

kill  -s 9 `ps fux | grep GdbHook | grep -v grep | awk '{print $2}'`
