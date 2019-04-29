#!/bin/sh

while true; do

	ping -I ppp0 -c 1 8.8.8.8

	if [ $? -eq 0 ]; then
		echo "Connection up, reconnect not required..."
	else
		echo "Connection down, reconnecting..."
		sudo pon
		sudo route add 13.81.175.81 gw 10.64.64.64
		sudo openvpn --config "/home/pi/RREI/OpenVPN/client Caméra.ovpn"
	fi

	sleep 1
done
