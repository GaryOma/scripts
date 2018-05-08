#! /usr/bin/python
import sys

for i in range(1,len(sys.argv)):
    if ('-o' or '--output') == sys.argv[i]:
        i = i + 1
        print sys.argv[i]
    if ('-t' or '--thread') == sys.argv[i]:
        i = i + 1
        print sys.argv[i]
    if ('-u' or '--user') == sys.argv[i]:
        i = i + 1
        print sys.argv[i]
