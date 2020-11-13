# Dojo IPv6

## Requirements

- Vagrant
- VirtualBox
- The custom box `dojo_ipv6.box`, it is a `debian/buster64` box with `vim`, `dnsutils`, `tcpdump`, `python3-pip` and `net-tools` apt packages and `google-api-python-client`, `google-auth-httplib2` and `google-auth-oauthlib` pip packages installed

## Setup

- Run once `vagrant box add dojo_ipv6 dojo_ipv6.box`
- Create a NAT natwork in VirtualBox named `dojonetwork` with network CIDR `192.168.0.0/24` then enable `Supports IPv6` and `Advertise Default IPv6 Route`
- Run `vagrant up`

## Commands Cheat Sheet

Show MAC adress + IP adress

```shell
ip addr
ip addr show eth1
```

Show routes

```shell
ip route
```

Enable/disable an interface

```shell
sudo ip link set eth1 up
sudo ip link set eth1 down
```

Add/remove IP from interface

```shell
sudo ip addr add 192.168.50.5/24 dev eth1
sudo ip addr del 192.168.50.5/24 dev eth1
```

Ping IPv4/IPv6

```shell
ping -4 www.google.com
ping -6 www.google.com
```

Ping with specifing the interface

```shell
ping -I eth1 fe80::a00:27ff:fe42:f1a2
```

Listen all IPv6 traffic

```shell
sudo tcpdump -i eth1 'ip6'
```

## Usefull links

[VirtualBox networks guide](https://www.nakivo.com/blog/virtualbox-network-setting-guide/)
