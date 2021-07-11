# Raspberry Pi 1U Server
There are server colocation providers that allow hosting a 1U server for as low as $30/month, but there's a catch: There are restrictions on power usage (1A @ 120v max, for example) because they're expecting small and power-efficient network equipment like firewalls.

This repo is about designing a server that fits within the 1U space and 1A @ 120v power constraint while maximizing computing power, storage, and value.

![raspberry pi 1u server - inside](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/finished_1_v2.jpg)
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
* [How Many More Pi's Will Fit?](#how-many-more-pis-will-fit)
* [Improvement Ideas](#improvement-ideas)
* [Similar Projects](#similar-projects)

## Colocation Providers
* $30/month - [Turnkey Internet](https://turnkeyinternet.net/colocation/)
    * 1 Amp @ 120V
    * 1 Usable IP (+10 for 5 usable IPs)
    * 10 Mbit Ethernet
    * 3 TB Monthly Transfer
* $40/month - [Nextarray](https://nextarray.com/bargain-dallas-colocation/)
    * 100Mbps Unmetered
    * 1 Amps 120V
    * 3 Usable IPs (+$13 for 11 usable IPs)
    * GigE Port
    * 1.5Tbps Protection
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
* $36.34 - [Server Rack Rails](https://www.amazon.com/NavePoint-Adjustable-Mount-Server-Shelves/dp/B0060RUVBA)
    * Depending on the colocation place, these may be provided for free.

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
* $19.99 - [NETGEAR 8-Port Gigabit Ethernet Unmanaged Switch (GS308)](https://www.amazon.com/NETGEAR-8-Port-Gigabit-Ethernet-Unmanaged/dp/B07PFYM5MZ/)
    * 12v, so can use the ATX power supply easily.
    * Using an unmanaged switch due to a limited number of IP addresses, and to make a firewall and router for a private network unnecessary.

### Single Board Computer
* 5x $35 - [Raspberry Pi 4b](https://www.canakit.com/raspberry-pi-4-2gb.html)
    * Best software support and battle-tested design.

### Raspberry Pi Case
* 5x $12.99 - [Geekworm Raspberry Pi 4 Armor Case](https://www.amazon.com/gp/product/B07VD568FB)
    * Allows access to GPIO pins, which will be necessary for the Pi wired to the relay for remote power management.
    * Uses less space than the Flirc case, which makes it difficult to close the chassis lid.
    * Reviews: [1](https://www.jeffgeerling.com/blog/2019/best-way-keep-your-cool-running-raspberry-pi-4)

### Power
* $12.99 - [ATX breakout board](https://www.amazon.com/Electronics-Salon-20-pin-Supply-Breakout-Module/dp/B01NBU2C64)
* $11.88 - [Standoffs for ATX breakout board](https://www.amazon.com/dp/B07D7828LC)
* 3x $7.99 - [USB 2.0 Female Screw Terminal Block Connector, 2-Pack](https://www.amazon.com/dp/B08Y8NKGHL) for wiring USB cables to the breakout board
* $8.90 - [Toggle switch](https://www.amazon.com/Nilight-Rocker-Toggle-Switch-Waterproof/dp/B078KBC5VH/) for powering off the server from the front panel.

### Remote Power Management
* $8.99 - [8 Channel DC 5V Relay Module](https://www.amazon.com/gp/aw/d/B00KTELP3I)
    * For power cycling most of the Pi's remotely.
* $5.98 - [One Channel Relay Module](https://www.amazon.com/HiLetgo-Channel-optocoupler-Support-Trigger/dp/B00LW15A4W/ref=sr_1_3?dchild=1&keywords=1+channel+relay&qid=1624846917&sr=8-3)
    * For power cycling the Pi that controls the 8 channel relay.

### Other Wiring
* $8.99 - [Ethernet Extension Cable w/ screws](https://www.amazon.com/gp/product/B06Y4J9MZ4)
    * For adding a single ethernet port to the back of the chassis that connects to the switch.
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
1. Install the Raspberry Pi's into their cases.

    ![install raspberry pi into geekworm case](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/install_in_case.jpg)

1. Install the M.2 drives into their enclosures.
1. Insert a SD card into each of the Pi's.
1. Add mounting tape to each of the SSDs and attach them to the top of the Raspberry Pi's.

    ![add mounting tape to ssd](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/add_ssd_sticky.jpg)

1. Add mounting tape to the bottom of the raspberry pi cases. Don't remove the bottom cover of the adhesive yet.

    ![add mounting tape to raspberry pi](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/case_sticky.jpg)

1. Add labels with numbers to the tops of the cases. These numbers will correspond to the hostnames of the Pi's in the software setup.

    ![raspberry pi numbering](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/numbered_case.jpg)

1. Cut the piece plastic that came with the chassis (for under the motherboard) to fit under the power supply breakout board.
1. Drill holes in the chassis, insert nylon standoffs, and add the plastic sheet. 

    ![installing atx breakout board 1](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/power_board_install_1.jpg)

    ![installing atx breakout board 2](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/power_board_install_2.jpg)

    ![installing atx breakout board 3](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/power_board_install_3.jpg)

    ![installing atx breakout board 4](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/power_board_install_4.jpg)

    ![installing atx breakout board 5](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/power_board_install_5.jpg)

    ![installing atx breakout board 6](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/power_board_install_6.jpg)

1. Cut 10x 6" lengths of red standed wire, strip the both ends, and install one side of the wire end in the "+" slot of the USB terminal blocks and the other side into the 5V terminal blocks of the ATX power supply breakout board. Make sure the 20 pin power supply has a corresponding wire, some wires will be missing and may not actually work on the power breakout board.

    ![cutting wire for atx breakout board](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/cutting_wire_3.jpg)

    ![add usb connectors to atx breakout board](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/2_add_connectors_to_breakout.jpg)

1. Cut and strip 10x 6" lengths of green standed wires then install one side of the wire end in the "-" slot of the USB terminal blocks and the other side into the COM terminal blocks of the ATX power supply breakout board. Again, ensure the wire exists on the 20 pin cable before using the terminal block.
1. Mount the ATX power supply breakout board and secure with nylon nuts. Insert the 20 pin ATX power supply connector into the ATX power supply breakout board.

    ![installing atx breakout board 7](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/power_board_install_7.jpg)

1. Start to lay out the Raspberry Pi's and switch in the chassis. Don't plug the power supply into the wall yet. You will probably want to try to match the layout from the finished project above, but this may change depending on how many Raspberry Pi's you have.
11. Cut the 12V barrel connector along with 12" of wire off of the power adapter for the network switch. Attach the cable with the solid white line markings to 12V on the ATX breakout board and attach the other wire a COM on the breakout board. You may want to confirm this is the correct "+" wire for your switch with an ohm meter and the diagram near the power connector the back of the switch.

    ![network switch positive negative](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/longer_solid_line_12v.jpg)

1. Cut the piece plastic that came with the chassis (for under the motherboard) to fit under the 8 channel relay board.

    ![cut piece of plastic to fit under relay](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/relay_plastic.jpg)

1. Drill holes in the chassis, insert nylon standoffs, and mount the 8 channel relay.

    ![installing relay 1](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/relay_install_1.jpg)

    ![installing relay 2](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/relay_install_2.jpg)

1. Wire the 4 of the 5 5V USB power terminal wires from the ATX breakout board to NC terminals on the 8 channel relay and wire the other side of the relay to the "+" on the terminal block for 4 of the 5 Pi's. [More relay setup instructions](https://labensky.de/raspberry-pi-relay-module-wiring/)
1. Drill holes in the chassis and insert nylon standoffs for the 1 channel relay.

    ![installing 1 ch relay part 1](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/relay_1_ch_install_1.jpg)
    ![installing 1 ch relay part 2](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/relay_1_ch_install_2.jpg)

1. Wire DC+ on the relay to a 3.3V GPIO pin from a Pi that is powered by the 8 channel relay. DC- will need to be wired to a ground GPIO pin and IN will need to be wired to GPIO pin 18. Finally, wire the 5V power from the ATX breakout board to NC and COM to the "+" on the terminal block for the Pi isn't powered by the 8 channel relay to NC and COM.

    ![installing 1 ch relay part 3](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/relay_1_ch_install_3.jpg)

1. Mount the 1 channel relay to the chassis with the nylon standoffs.

    ![installing 1 ch relay part 4](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/relay_1_ch_install_4.jpg)

1. Move the jumper on the 1 channel relay from H to L.
1. Plug one of ATX SATA power connectors into the fan controller and connect the blower fan from the chassis into the fan controller.
1. Drill a hole in the front of the case for the power switch and install the power switch.

    ![power switch installed](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/installed_power_switch.jpg)

1. Add a 290 ohm resistor inline with a 6" length of wire with a jumper connector on one side, add heatshrink, and add that wire to a 3.3V terminal on the ATX power supply breakout board. 

    ![wire front panel LED to the atx breakout board](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/white_wire_33.jpg)

1. Add another wire of the same length with a jumper connector on one side to a COM terminal on the power supply breakout board, then put the jumpers onto the pins of the LEDs on the front panel. 

    ![wire front panel LED to the atx breakout board](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/front_panel_connection.jpg)

1. Apply electrical tape over the unused header pins and terminal blocks to prevent accidental electrical shorts.

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

## How Many More Pi's Will Fit?

At least 7. (including 1 Pi Zero and a Pi 3b)

![7 raspberry pis in 1u server](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/7_pis.jpg)

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
* [SOPINE Clusterboard](https://www.pine64.org/clusterboard/)
    * Supports 7x [compute modules](https://pine64.com/product/sopine-a64-compute-module/), has a built-in switch, and can be powered by an ATX power supply.
    * Out of stock at the time of writing (June 2021).
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

Note: I tried using 2.5" SSDs with inateck enclosures and [there wasn't enough room](https://raw.githubusercontent.com/pawl/raspberry-pi-1u-server/master/pictures/2_5_ssd_not_enough_space.jpg).

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
