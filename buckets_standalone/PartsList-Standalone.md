# Preliminary Parts List - Standalone Version
Parts are listed on a per-timer basis. Prices are tax and shipping exclusive.
Current price breakdown gives about $64 per bucket.

#### Raspberry Pi Pico W - 1x $6 - https://www.adafruit.com/product/5526 or https://www.microcenter.com/product/650108/raspberry-pi-pico-w
>The heart of the build. Can be supplemented with a regular Pi Pico if you have no need for wireless/bluetooth, and can also be orderered in the "WH" version with header pins pre-soldered onto it. Other CircuitPython-compatible controllers could be used, but would require pinout configuration and additional setup.

#### 1602/16x2 LCD Display - 1x $5 | .25x $15 - https://www.microcenter.com/product/632704/inland-1602-i2c-lcd-display-module or https://www.amazon.com/gp/product/B09W8TTZ1D
>Core of the basic build. **Most** of these types of screens are close enough to work as long as they have the little "backpack" portion that has 4 pins out. Some fancier ones have the 4 pins on their own and don't need the backpack; I'd like to move to using those eventually.

#### 5V Addressable RGB Strip - .2x $23 - https://www.amazon.com/gp/product/B0BNN2NVLR
>There's plenty of options for RGB strip, this is just one I found super convenient. The key details are 5V power, 3-pin addressable, and you need just under 1m per bucket lid. Many options are 5m lengths, so enough for 5 buckets with a little left.

#### 100mm Arcade Buttons - 2x $10 - https://www.adafruit.com/product/1185
>Nice, fairly rugged buttons for players to slap. The built-in LEDs may be a little dim, so on mine I replaced the inline resistors with 1ohm ones. Can easily be substituted with other button options, but the code is expecting 2 switch pins and 2 LED pins.

#### EC11 Rotary Encoder - .1x $11 - https://www.amazon.com/DIYhz-Rotary-Encoder-Digital-Potentiometer/dp/B07D3D64X7
>For menu navigation and game setup. Should be able to substitute pretty easily so long as it's "EC11" on the listing.

#### 5V Step Down Regulator - .5x $14 - https://www.amazon.com/gp/product/B09VY3WQ93
>The controller doesn't need much current, but the LEDs can pull a surprising amount of power, so this type of regulator is enough overhead to even have room for future expansion. In addition, this will take any voltage up to 24v/6s and down to at least 7v/2s, so it gives a lot of flexibility in powering the timer. This brand is a pack of 2, but there's plenty around in single packs.

#### 4-Gang Old Work Box - 1x $11.50 - https://www.homedepot.com/p/Carlon-4-Gang-71-cu-in-PVC-Old-Work-Electrical-Switch-and-Outlet-Box-B468R/202077406
>This mounts down into the bucket lid and keeps all your electronics nice and contained and away from unaware fingies. It's important to get the "old work" style with the little flappy bits as those are what lets it just mount into the bucket lid. Originally went with 4-gang to be able to fit our existing batts, but also found it's large enough to even mount the arcade buttons to have their wiring extend down into it. A 3-gang or even 2-gang box is a viable option if you don't intend to mount the buttons inside of it. 

#### 5gal Bucket Lid + 5gal bucket - 1x $3 + $4 - https://www.homedepot.com/p/Leaktite-5-gal-Black-Paint-Bucket-Lid-6GLDBLK30/202264045 and https://www.homedepot.com/p/The-Home-Depot-5-Gallon-Orange-Homer-Bucket-05GLHD2/100087613
>All of our components mount either into the lid or sit inside something that does. I like this particular lid for needing less force to pop off after it's been in the sun all day. Bucket type is completely substitutable, just included for completeness.

#### XT60E-M - .1x $10 - https://www.amazon.com/SoloGood-XT60E-M-Mountable-Connector-Multicopter/dp/B07YJMCDC3
>Good ole XT60 to plug in whatever power source you desire. Probably plenty of listings for cheaper, I picked this one because it comes with the M2.5 screws that are uncommon to have on hand. Could be cheeky and find some with wires presoldered to run direct to the regulator.Panel mount because the intent is have it face **out** of the electronics box and into the bucket where the battery will stay. Saves space inside the box and is a good layer of battery safety. 

#### Power Switch - 1x $2 - https://www.microcenter.com/product/501707/nte-electronics-rocker-micro-snap-in-nylon-spst-6a-125vac-switch-black
>Goes between your battery input and the power regulator to have some control other than unplugging the battery. A flexible option, I previously impulse-bought the tiniest rocker switch I've ever seen and wanted somewhere to use it. Ideally you should match the switch rating to the regulator max draw.

### Assorted Hardware Needs
---

 - Wire - I like 22ga silicone that you can get multi-packs of for pretty cheap
 - Header wires - https://www.microcenter.com/product/613879/inland-dupont-jumper-wire-20cm-3-pack - Can do most hookup aside from power with just a pack of these if you wanted.
 - Some screws - The printed panel I use screws directly into the electrical box. I put some M3 heatsets in there for ease, but any close-enough screw should work. 

### Future Hardware Additions
---

#### Low Voltage Cutoff Module - .33x $14 - https://www.amazon.com/dp/B0B6BP6J2D/
>Rather than rely on alarms alone for LiPo, this is an extra level of safety for them that I'd like to be an auto-include in future builds.