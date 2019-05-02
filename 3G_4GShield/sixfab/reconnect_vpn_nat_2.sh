#!/bin/sh

ROUTE_STATE = 0
while true; do

	ping -I ppp0 -c 1 8.8.8.8

	if [ $? -eq 0 ]; then
		echo "Connection up, reconnect not required..."
	else
		echo "Connection down, reconnecting..."
		sudo pon
		sudo route add 13.81.175.81 gw 10.64.64.64
		
	fi
	
	ping -I tun0 -c 1 8.8.8.8
		if [ $? -eq 0 ]; then
			echo "VPN connected"
		else
			echo "Connection to VPN in progress"
			sudo openvpn --config "/home/pi/RREI/OpenVPN/client Caméra.ovpn"
		fi
		
		if [$ROUTE_STATE -eq 0]
			echo "Adding route to NAT the camera"
			sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -i tun0 -j DNAT --to 192.168.235.99:80
			sudo sysctl -w net.ipv4.ip_forward=1
			sudo iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE
			ROUTE_STATE = 1
		else
			echo "Route is set"
		fi
			

	sleep 1
done

