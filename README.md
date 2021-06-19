# Raspberry Pi 1U Server
There are server colocation providers that allow hosting a 1U server for as low as $30/month, but there's a catch: There are restrictions on power usage (1A @ 120v max, for example) because they're expecting small and power-efficient network equipment like firewalls.

This repo is about designing a server that fits within the 1U space and 1A @ 120v power constraint while maximizing computing power, storage, and value.

## Colocation Providers

* $30/month - [Nextarray](https://nextarray.com/bargain-dallas-colocation/)
    * 100Mbps Unmetered
    * 1 Amps 120V
    * 5 Usable IPs (/29)
    * GigE Port
    * 10 Gbps DDoS (Manual)
    * Location: Dallas, TX
* $50/month - [Joe’s Datacenter](https://joesdatacenter.com/products/colocation/)
    * IPv4 Addresses: 1 Usable (/30)
    * Bandwidth: 33TB on 1Gbps Port
    * Power: Up To 2 Amps 120V (Single Power Connection)
    * Network Connection: Single Network Cable
    * Location: Kansas City, MO

## Parts 

Total cost: $600-800

### 1U Chassis
* $85 - [Supermicro SuperChassis 1U Rackmount Server Case CSE-512L-200B](https://www.ebay.com/sch/i.html?_from=R40&_nkw=Supermicro+512&_sacat=0)
    * Comes with ATX power supply and blower fan.
    * Lots of supermicro recommendations: [1](https://www.reddit.com/r/HomeServer/comments/k7i03n/best_1u_chassis/), [2](https://www.reddit.com/r/homelab/comments/7fyren/1u_chassis_for_pfsense_build/dqfb7wh/)
    * This allows for a lot more flexibility and room for things than 

### Storage
* 4x $34.99 - [Kingston A400 240G Internal SSD M.2](https://www.amazon.com/gp/product/B07P22RK1G?th=1)
    * Need to use m.2 drives to save space.

### Storage Enclosure
*  4x $15.99 - [UGREEN M.2 Enclosure for SATA NGFF SSD Aluminum USB 3.1](https://www.amazon.com/dp/B07NPG5H83)
    * https://jamesachambers.com/best-ssd-storage-adapters-for-raspberry-pi-4-400/
    * Supports UART ([important](https://www.jeffgeerling.com/blog/2020/uasp-makes-raspberry-pi-4-disk-io-50-faster))

### Switch 
* $25.99 - [NETGEAR 8-Port Gigabit Ethernet Plus Switch (GS308E)](https://www.amazon.com/NETGEAR-8-Port-Gigabit-Ethernet-Managed/dp/B07PLFCQVK/)
    * 12v, so can use the ATX power supply easily.

### Raspberry Pi Case
* 4x $15.95 - [Flirc case](https://www.amazon.com/Flirc-Raspberry-Pi-Case-Silver/dp/B07WG4DW52)
    * It's a big heatsink and [improves cooling dramatically](https://www.jeffgeerling.com/blog/2019/best-way-keep-your-cool-running-raspberry-pi-4).
* 1x $12.99 - [Geekworm Raspberry Pi 4 Armor Case](https://www.amazon.com/gp/product/B07VD568FB)
    * Allows access to GPIO pins, which will be necessary for the Pi wired to the relay for remote power management.

### Single board computer
* 5x $35 - [Raspberry Pi 4b](https://www.canakit.com/raspberry-pi-4-2gb.html)
    * Best software support and battle-tested design.

### Power
* $12.99 - [ATX breakout board](https://www.amazon.com/Electronics-Salon-20-pin-Supply-Breakout-Module/dp/B01NBU2C64)
* $11.88 - [Standoffs for ATX breakout board](https://www.amazon.com/dp/B07D7828LC)
* 3x $7.99 - [USB 2.0 Female Screw Terminal Block Connector, 2-Pack](https://www.amazon.com/dp/B08Y8NKGHL) for wiring USB cables to breakout board
* Power switch for ATX power supply
    * $8.90 - [toggle switch](https://www.amazon.com/Nilight-Rocker-Toggle-Switch-Waterproof/dp/B078KBC5VH/)

### Remote Power Management
* $8.99 - [relay board](https://www.amazon.com/gp/aw/d/B00KTELP3I)

### Other Wiring
* $8.99 - [Ethernet Extension Cable w/ screws](https://www.amazon.com/gp/product/B06Y4J9MZ4)
* $7.49 - [Aluminum Case Resistor 10W 10 Ohm for power supply dummy load](https://www.amazon.com/dp/B07FF3GYVY)
* $26.99 - [Kill-a-watt](https://www.amazon.com/gp/product/B00009MDBU)
    * For measuring amperage and ensuring it's below the max.
* $20.95 - [Noctua NA-FC1, 4-Pin PWM Fan Controller](https://www.amazon.com/dp/B072M2HKSN)
    * For controlling PWM fan without motherboard.
* 2x $6.99 - [2-pack of 1ft USB C Cables](https://www.amazon.com/dp/B08933P982)
* $14.99 - [USB C Cables w/ right angle connectors, 6-pack](https://www.amazon.com/dp/B085ZVMZ9P)
    * These help save a ton of space.
* 4x $2.09 - [1 Foot Long Slim Ethernet cables](https://www.amazon.com/dp/B01C68CX9O)
* 1x $2.09 - [0.5 Foot Long Slim Ethernet cables](https://www.amazon.com/dp/B0195XY6F2)

* [Zip Tie Mounts](https://www.amazon.com/gp/product/B08F77YVYB)
* [Mounting tape](https://www.amazon.com/gp/aw/d/B07VNSXY31/)

## Power Usage

* Raspberry Pi 4 + SSD
    * idle: 0.44A @ 5V (0.018A @ 120v)
    * load: 0.84A @ 5V (0.035A @ 120v)
* Total w/ blower fan on low setting: 
    * idle: 0.30-32A @ 120V
    * load: 0.36A 
* Total w/ blower fan on high setting:
    * idle: 0.4A @ 120V

## Software Setup
1. Flash an SD cart with raspbian lite and enable SSH with:
1. `cd /Volumes/boot/`
1. `touch shh`
1. Insert the SD card, boot the Pi, ssh into the Pi with `ssh pi@<ip address>`.
1. Update the firmware on the Pi to allow booting from USB:
1. `sudo apt-get update`
1. `sudo apt full-upgrade`
1. `sudo rpi-update`
1. `sudo reboot`
1. Unplug the sd card and reboot again to use the SSD via usb.
1. `sudo apt-get update && sudo apt full-upgrade` again with the new OS on the SSD.
1. [Disable wifi and bluetooth](https://chrisapproved.com/blog/raspberry-pi-hardening.html#disable-wireless-interfaces)
1. [Add your public key](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md)
1. [Disable password authentication](https://gist.github.com/brpaz/10243211f3f7cd06cc11#file-deploy_user-sh-L14-L17)

## Hardware Setup

TODO

## Measuring Amperage
1. Plug the server into the Kill-A-Watt.
1. Press the button on the Kill-A-Watt for "amps".
1. `sudo apt-get install stress`
1. `while true; do vcgencmd measure_clock arm; vcgencmd measure_temp; sleep 10; done& stress -c 4 -t 900s`
1. Restart the server by unplugging and plugging back in. Watch the amperage on start-up.

## Improvement Ideas

### Other Colocation Options

* [webhostingtalk.com](https://www.webhostingtalk.com/forumdisplay.php?f=131)

### Other Chassis Options

* [BitScope Blade Rack](https://www.pishop.us/product/bitscope-blade-rack/)
    * Not as much room as the 1U chassis.
* [1U Raspberry Pi rack](https://www.jeffgeerling.com/blog/2021/my-6-node-1u-raspberry-pi-rack-mount-cluster)
    * No room for storage, power supply, and a switch to allow for consolidating ethernet connections to the single cable required by the colocation provider.
    * Doesn't match the usual network device form factor, and some colocation providers might not like this?
* [UCTRONICS Ultimate Rack with PoE Functionality for Raspberry Pi 4](https://www.uctronics.com/19-server-rack-mounts-for-rpi-jetson-nano/raspberry-pi-4b-rack-mount-19-inch-1u-with-poe-and-oled-screen.html)
* [iStarUSA](https://www.amazon.com/iStarUSA-Compact-Desktop-mini-ITX-D-118V2-ITX-DT/dp/B0053YKPLM)
* Dell R620
* other options on [Labgopher](https://labgopher.com/)?

### Other Single Board Computer Options
* Raspberry Pi CM4
    * Back-ordered for months at the time of writing (June 2021).
    * [TuringPi 2](https://turingpi.com/turing-pi-2-announcement/) has not been launched yet as of June 2021. 
* [RockPro64](https://pine64.com/product/rockpro64-2gb-single-board-computer/?v=0446c16e2e66)
    * 6x CPU cores
* [Quartz64 Model B](https://www.pine64.org/quartz64b/)
    * Has a built-in M.2 slot.
* [ODROID-XU4](https://www.hardkernel.com/shop/odroid-xu4-special-price/)
* [Banana Pi M4](https://www.aliexpress.com/item/33036948250.html)
    * Built-in POE
* [Mini-ITX motherboard with low-power processor](https://www.reddit.com/r/homelab/comments/kli89e/1u_poe_powered_miniitx_virtualization_server_build/)

### Other Case Options
* [Argon ONE M.2 Case for Raspberry Pi 4](https://www.amazon.com/Argon-Raspberry-Support-B-Key-Compatible/dp/B08MJ3CSW7)
    * Includes an M.2 storage adapter.

### Other Storage Options

* $44.99 - [Samsung 860 EVO SSD 250GB M.2 SATA](https://www.amazon.com/dp/B07864V6CK)
* $60 - [ORICO 128GB Mini M.2 NVME](https://www.amazon.com/dp/B081LDHS3P)
    * Fast NVMe drives might be bottlenecked by usb?
* http://pibenchmarks.com/popular/

### Other Power Options
* USB Hub
    * [Rosonway 16 Ports 100W USB 3.0 Data Hub](https://www.amazon.com/Rosonway-Aluminum-Splitter-Certified-Individual/dp/B08DKQQ6MR)
        * Allows software control with [uhubctl](https://github.com/mvp/uhubctl).
* POE (maybe there are colocation providers that provide this for you?)
    * $20 - https://www.raspberrypi.org/products/poe-plus-hat/
        * At the time of writing (June 2021), the POE+ hat has [some issues](https://www.youtube.com/watch?v=XZ08QKAbBoU).
    * POE switch
        * $110 - [Netgear GS108PP](https://www.amazon.com/NETGEAR-Unmanaged-Rackmount-Lifetime-Protection/dp/B07788WK5V) (supports POE+)
        * $https://www.amazon.com/NETGEAR-8-Port-Gigabit-Ethernet-Unmanaged/dp/B016XIU1HE

## Similar Projects
* https://epcced.github.io/wee_archlet
