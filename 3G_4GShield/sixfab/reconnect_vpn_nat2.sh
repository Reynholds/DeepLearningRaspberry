#!/bin/sh

ROUTE_STATE=0
echo $ROUTE_STATE

while true; do
	echo "\n\n >>> test 3G-4G <<< "
	ping -I ppp0 -c 1 8.8.8.8

	if [ $? -eq 0 ]; then
		echo "Connection up, reconnect not required..."
	else
		echo "Connection down, reconnecting..."
		sudo pon
		#sudo ip route flush table main
		sudo route add 13.81.175.81 gw 10.64.64.64
		sudo ip route add 10.64.0.0/16 dev ppp0
		
	fi
	
	echo "\n\n >>> Test VPN <<<"
	ping -I tun0 -c 1 8.8.8.8
		if [ $? -eq 0 ]; then
			echo "VPN connected"
		else
			echo "Connection to VPN in progress"
			sudo openvpn --config "/home/pi/RREI/OpenVPN/client Caméra.ovpn"
			
		fi

	echo "\n\n >>> Test Route : $ROUTE_STATE <<<"
		if [ "$ROUTE_STATE" -eq 0 ]; then
			echo "Adding route to NAT the camera"
			sudo iptables -F
			sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -i tun0 -j DNAT --to 192.168.235.99:80
			sudo sysctl -w net.ipv4.ip_forward=1
			sudo iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE
			ROUTE_STATE=1
		else
			echo "Route is set"
		fi
			

	sleep 1
done

