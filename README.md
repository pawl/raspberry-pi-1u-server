# Raspberry Pi 1U Server
There are server colocation providers that allow hosting a 1U server for as low as $30/month, but there's a catch: There are restrictions on power usage (1A @ 120v max, for example) because they're expecting small and power-efficient network equipment like firewalls.

This repo is about designing a server that fits within the 1U space and 1A @ 120v power constraint while maximizing computing power, storage, and value.

![raspberry pi 1u server - inside](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/finished_1.jpg)
![raspberry pi 1u server - front](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/finished_2.jpg)
![raspberry pi 1u server - back](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/finished_3.jpg)

TODO: Cost and performance comparison with AWS/DigitalOcean/Vultr

TODO: calculate time to pay off vs R620

## Table of contents

* [Colocation Providers](#colocation-providers)
* [Parts](#parts)
    * [Specs Summary](#specs-summary)
    * [1U Chassis](#1u-chassis)
    * [Storage](#storage)
    * [Storage Enclosure](#storage-enclosure)
    * [Switch](#switch)
    * [Single Board Computer](#single-board-computer)
    * [Raspberry Pi Case](#raspberry-pi-case)
    * [Power](#power)
    * [Remote Power Management](#remote-power-management)
    * [Other Wiring](#other-wiring)
* [Power Usage](#power-usage)
* [Software Setup](#software-setup)
* [Hardware Setup](#hardware-setup)
* [Remote Power Management Software Setup](#remote-power-management-software-setup)
* [Measuring Amperage](#measuring-amperage)
* [Single Points Of Failure](#single-points-of-failure)
* [Improvement Ideas](#improvement-ideas)
* [Similar Projects](#similar-projects)

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

### Specs Summary

* 20x 1.5GHz CPUs
* 16GB LPDDR4-3200 SDRAM
* 1.2TB SSD Storage
* Gigabit Ethernet

Total cost: `~$800`

### 1U Chassis
* $85 - [Supermicro SuperChassis 1U Rackmount Server Case CSE-512L-200B](https://www.ebay.com/sch/i.html?_from=R40&_nkw=Supermicro+512&_sacat=0)
    * Comes with ATX power supply and blower fan.
    * Recommendations: [1](https://www.reddit.com/r/HomeServer/comments/k7i03n/best_1u_chassis/), [2](https://www.reddit.com/r/homelab/comments/7fyren/1u_chassis_for_pfsense_build/dqfb7wh/)

### Storage
* 5x $34.99 - [Kingston A400 240G Internal SSD M.2](https://www.amazon.com/gp/product/B07P22RK1G?th=1)
    * Need to use M.2 drives to save space.
* 1x $31.50 - [5-Pack of SAMSUNG 32GB Evo Plus Micro SD Cards](https://www.amazon.com/Samsung-Class-Micro-Adapter-MB-MC32GA/dp/B07NP96DX5/ref=mp_s_a_1_4?dchild=1&keywords=5+pack+evo+sd&qid=1624215476&sr=8-4)
    * For failover storage in case the SSD fails.

### Storage Enclosure
*  5x $15.99 - [UGREEN M.2 Enclosure for SATA NGFF SSD Aluminum USB 3.1](https://www.amazon.com/dp/B07NPG5H83)
    * Recommendations: [1](https://jamesachambers.com/best-ssd-storage-adapters-for-raspberry-pi-4-400/)
    * Supports UART ([important](https://www.jeffgeerling.com/blog/2020/uasp-makes-raspberry-pi-4-disk-io-50-faster))

### Switch 
* $25.99 - [NETGEAR 8-Port Gigabit Ethernet Plus Switch (GS308E)](https://www.amazon.com/NETGEAR-8-Port-Gigabit-Ethernet-Managed/dp/B07PLFCQVK/)
    * 12v, so can use the ATX power supply easily.

### Single Board Computer
* 5x $35 - [Raspberry Pi 4b](https://www.canakit.com/raspberry-pi-4-2gb.html)
    * Best software support and battle-tested design.

### Raspberry Pi Case
* 4x $15.95 - [Flirc case](https://www.amazon.com/Flirc-Raspberry-Pi-Case-Silver/dp/B07WG4DW52)
    * It's a big heatsink and [improves cooling dramatically](https://www.jeffgeerling.com/blog/2019/best-way-keep-your-cool-running-raspberry-pi-4).
* 1x $12.99 - [Geekworm Raspberry Pi 4 Armor Case](https://www.amazon.com/gp/product/B07VD568FB)
    * Allows access to GPIO pins, which will be necessary for the Pi wired to the relay for remote power management.

### Power
* $12.99 - [ATX breakout board](https://www.amazon.com/Electronics-Salon-20-pin-Supply-Breakout-Module/dp/B01NBU2C64)
* $11.88 - [Standoffs for ATX breakout board](https://www.amazon.com/dp/B07D7828LC)
* 3x $7.99 - [USB 2.0 Female Screw Terminal Block Connector, 2-Pack](https://www.amazon.com/dp/B08Y8NKGHL) for wiring USB cables to breakout board
* Power switch for ATX power supply
    * $8.90 - [toggle switch](https://www.amazon.com/Nilight-Rocker-Toggle-Switch-Waterproof/dp/B078KBC5VH/)

### Remote Power Management
* $8.99 - [8 Channel DC 5V Relay Module](https://www.amazon.com/gp/aw/d/B00KTELP3I)

### Other Wiring
* $8.99 - [Ethernet Extension Cable w/ screws](https://www.amazon.com/gp/product/B06Y4J9MZ4)
* $26.99 - [Kill A Watt Electricity Usage Monitor](https://www.amazon.com/gp/product/B00009MDBU)
    * For measuring amperage and ensuring it's below the max.
* $20.95 - [Noctua NA-FC1, 4-Pin PWM Fan Controller](https://www.amazon.com/dp/B072M2HKSN)
    * For controlling PWM fan without a motherboard.
* 2x $6.99 - [2-pack of 1ft USB C Cables](https://www.amazon.com/dp/B08933P982)
* $14.99 - [USB C Cables w/ right angle connectors, 6-pack](https://www.amazon.com/dp/B085ZVMZ9P)
    * The right angle connector is key, this saves a ton of space.
* 4x $2.09 - [1 Foot Long Slim Ethernet cables](https://www.amazon.com/dp/B01C68CX9O)
* 1x $2.09 - [0.5 Foot Long Slim Ethernet cables](https://www.amazon.com/dp/B0195XY6F2)
* $8.99 - [Zip Tie Mounts](https://www.amazon.com/gp/product/B08F77YVYB)
* $10.99 - [Mounting tape](https://www.amazon.com/gp/aw/d/B07VNSXY31/)
* $5.28 - [22 AWG Stranded Copper Wire](https://www.amazon.com/BNTECHGO-Silicone-Flexible-Strands-Stranded/dp/B01MFEV8SG)

## Power Usage

* Raspberry Pi 4 + SSD:
    * idle: 0.44A @ 5V (0.018A @ 120v)
    * load: 0.84A @ 5V (0.035A @ 120v)
* Total w/ blower fan on low setting: 
    * idle: 0.30-32A @ 120V
    * load: 0.36A 
* Total w/ blower fan on high setting:
    * idle: 0.4A @ 120V

## Software Setup
You will need to do this for each of the Raspberry Pi's:
1. [Flash an SD card with Raspbian Lite](https://www.raspberrypi.org/documentation/installation/installing-images/) (under "Raspberry Pi OS (other)" in the Raspberry Pi Imager) and enable SSH with:
    1. `cd /Volumes/boot/`
    1. `touch shh`
1. Insert the SD card into the Pi, power on, and ssh into the Pi with `ssh pi@<ip address>` and the password "raspberry".
1. Update the hostname to correspond to the number on the case:
    1. `sudo raspi-config`
    1. `1 System Options` -> `S4 Hostname` -> Update hostname -> Finish -> Reboot
1. Update the firmware on the Pi to allow booting from USB:
    1. `sudo apt-get update && sudo apt full-upgrade -y`
    1. `sudo rpi-update` (only do this once on each Pi)
1. [Disable wifi and bluetooth](https://chrisapproved.com/blog/raspberry-pi-hardening.html#disable-wireless-interfaces):
    1. `sudo bash -c 'echo -e "dtoverlay=pi3-disable-wifi" >> /boot/config.txt'`
    1. `sudo bash -c 'echo -e "dtoverlay=pi3-disable-bt" >> /boot/config.txt'`
    1. `sudo reboot`
1. [Add your public key](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md) (while disconnected from the pi, with `cat ~/.ssh/id_rsa.pub | ssh pi@<IP-ADDRESS> 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'`)
1. Make sure the SSD into one of the blue USB 3 ports.
1. SSH into the Pi again and [Disable password authentication](https://gist.github.com/brpaz/10243211f3f7cd06cc11#file-deploy_user-sh-L14-L17):
    1. `sudo sed -i '/^#*PubkeyAuthentication /c PubkeyAuthentication yes' /etc/ssh/sshd_config`
    1. `sudo sed -i '/^#*ChallengeResponseAuthentication /c ChallengeResponseAuthentication no' /etc/ssh/sshd_config`
    1. `sudo sed -i '/^#*PasswordAuthentication /c PasswordAuthentication no' /etc/ssh/sshd_config`
    1. `sudo sed -i '/^#*UsePAM /c UsePAM no' /etc/ssh/sshd_config`
1. Configure the Pi to [prioritize booting from the SSD](https://docs.nextcloudpi.com/en/rpi4-chnage-boot-order/):
    1. `sudo raspi-config`
    1. `6 Advanced Options` -> `A6 Boot Order` -> `B2 USB Boot` -> Finish -> Reboot
    1. If you see an "No EEPROM bin file found" error, you may need to run `sudo -E rpi-eeprom-config --edit` and add `[all] BOOT_ORDER=0xf14`.
1. Repeat the steps above (without `sudo rpi-update`) with the new OS on the SSD. SSH'ing into the new OS on the SSD may require clearing out the line with the corresponding IP in your `~/.ssh/known_hosts` file.

## Hardware Setup

1. Install the Raspberry Pi's in their Flirc Cases. Make sure you put the bottom on the case before adding the screws.
1. Add labels with numbers to the tops of the cases. 
1. Cut 8x 6" lengths of standed wire, strip the ends, 
1. Start to lay out the Raspberry Pi's, switch, and power supply breakout board in the chassis. Don't plug the power supply into the wall yet.
1. https://labensky.de/raspberry-pi-relay-module-wiring/

TODO

## Remote Power Management Software
Only do this on the power management Paspberry Pi connected to the relay:
1. `curl -o relay_control.py https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/main/relay_control.py`
1. Test the script: `python relay_control.py`

You should see the light on the SSD flash off and on for the Pi whose relay's GPIO pin you entered.

## Measuring Amperage
1. Plug the server into the Kill-A-Watt.
1. Press the button on the Kill-A-Watt for "amps".
1. `sudo apt-get install stress`
1. `while true; do vcgencmd measure_clock arm; vcgencmd measure_temp; sleep 10; done& stress -c 4 -t 900s`
1. Restart the server by unplugging and plugging back in. Watch the amperage on start-up.

## Single Points Of Failure
* Switch 
* Relay 
* Power Supply 
* Electrical Short (from loose terminal or pinched wire?)
* The Management Pi Dies (and can't powercycle the other Pi's)

## Improvement Ideas

### Other Colocation Options

* [webhostingtalk.com](https://www.webhostingtalk.com/forumdisplay.php?f=131)

### Other Chassis Options

* [BitScope Blade Rack](https://www.pishop.us/product/bitscope-blade-rack/)
    * Doesn't have as much room as the 1U chassis.
* [1U Raspberry Pi rack](https://www.jeffgeerling.com/blog/2021/my-6-node-1u-raspberry-pi-rack-mount-cluster)
    * No room for storage, power supply, and a switch to allow for consolidating ethernet connections to the single cable required by the colocation provider.
    * Doesn't match the usual server form factor, and some colocation providers might not like this?
* [UCTRONICS Ultimate Rack with PoE Functionality for Raspberry Pi 4](https://www.uctronics.com/19-server-rack-mounts-for-rpi-jetson-nano/raspberry-pi-4b-rack-mount-19-inch-1u-with-poe-and-oled-screen.html)
* [iStarUSA](https://www.amazon.com/iStarUSA-Compact-Desktop-mini-ITX-D-118V2-ITX-DT/dp/B0053YKPLM)
* Dell R620
* Other options on [Labgopher](https://labgopher.com/)?

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
* No case, drill holes for stand-offs, and mount to the chassis.
    * More work, but would probably work fine and small heatsinks would be cheap.
* [Argon ONE M.2 Case for Raspberry Pi 4](https://www.amazon.com/Argon-Raspberry-Support-B-Key-Compatible/dp/B08MJ3CSW7)
    * Includes an M.2 storage adapter.

### Other Storage Options

* $44.99 - [Samsung 860 EVO SSD 250GB M.2 SATA](https://www.amazon.com/dp/B07864V6CK)
* $60 - [ORICO 128GB Mini M.2 NVME](https://www.amazon.com/dp/B081LDHS3P)
    * Fast NVMe drives might be bottlenecked by usb?
* http://pibenchmarks.com/popular/

Note: I tried using 2.5" SSDs with inateck enclosures and there wasn't enough room.

### Other Power Options
* USB Hub
    * [Rosonway 16 Ports 100W USB 3.0 Data Hub](https://www.amazon.com/Rosonway-Aluminum-Splitter-Certified-Individual/dp/B08DKQQ6MR)
        * Allows software control with [uhubctl](https://github.com/mvp/uhubctl).
* POE (maybe there are colocation providers that provide this for you?)
    * $20 - (PoE+ HAT)[https://www.raspberrypi.org/products/poe-plus-hat/]
        * At the time of writing (June 2021), the POE+ hat has [some issues](https://www.youtube.com/watch?v=XZ08QKAbBoU).
    * POE switch
        * $110 - [Netgear GS108PP](https://www.amazon.com/NETGEAR-Unmanaged-Rackmount-Lifetime-Protection/dp/B07788WK5V) (supports POE+)
        * $69.99 - [NETGEAR 8-Port Gigabit Ethernet Unmanaged PoE Switch (GS308P)](https://www.amazon.com/NETGEAR-8-Port-Gigabit-Ethernet-Unmanaged/dp/B016XIU1HE) (no POE+, only 53W)

## Similar Projects
* https://epcced.github.io/wee_archlet
