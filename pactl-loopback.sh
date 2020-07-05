#!/bin/sh

pactl list modules short | grep module-loopback

if [ $? -eq 0 ]
then
	pactl unload-module module-loopback
else
	pactl load-module module-loopback latency_msec=1
fi

# update dwmblocks 10th signal
kill -44 $(pidof dwmblocks)
