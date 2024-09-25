# Preliminary Parts List - Networked Version
Parts are listed on a per-timer basis.  
Prices are tax and shipping exclusive.  
Current price breakdown can be as low as $48/bucket if buying enough parts for multiple. 
https://www.aliexpress.com/p/wishlist/shareReflux.html?groupId=wIt%2Bhup2qP6fPVAMoLEBz7bzxX8L0D9rNX4JnENpSFI%3D - AliExpress wishlist with most of the parts

#### ESP32-S3 - 1x $5-$6 - https://www.aliexpress.us/item/3256807091398627.html , many other sources
>The heart of the build. S3 has native USB so it's easier to deal with the CircuitPython programming, but other supported versions like C3 or S2 can be used through Web Workflow. Versions with an external antenna are recommended for better range; the linked version requires soldering a super small 0Ω resistor to enable the external antenna port, so I recommend shopping around if you're not confident in doing that.

#### U.FL to RP-SMA Pigtail - .2x ~$4 - https://www.aliexpress.us/item/3256803636448232.html
>Needed to connect the external antenna to the ESP32. The linked one is a 15cm right-angle cable, but you can find them in various lengths so long as they match both your ESP32 port (U.FL or sometimes W.FL) and your antenna (mostly RP-SMA). I like this style with the better protected cable for not being as easy to pinch.

#### 2.4GHz Antenna - .25x ~$4 - https://www.aliexpress.us/item/3256807417930585.html
>Helps provide way better ranges than relying on onboard antenna inside the enclosure. Should look for any like this that mention 2.4ghz and RP-SMA. Too many options to really say one is ideal, but I do like any that can bend or flex to help prevent accidental damage to or from players.

#### 1602/16x2 LCD Display - 1x $5 | 1x ~$2 - https://www.microcenter.com/product/632704/inland-1602-i2c-lcd-display-module or https://www.aliexpress.us/item/3256805831794547.html
>Integral to the basic build. **Most** of these types of screens are close enough to work as long as they have the little "backpack" portion that has 4 pins out. Some fancier ones have the 4 pins on their own and don't need the backpack; I'd like to move to using those eventually.

#### 5V Addressable RGB Strip - .2x $23 | .2x $13- https://www.amazon.com/gp/product/B0BNN2NVLR or https://www.aliexpress.us/item/3256805637835340.html
>There's plenty of options for RGB strip, this is just one I found super convenient. The key details are 5V power, 3-pin addressable, 60/m, and you need around 1m per bucket lid. Many options are 5m lengths, so enough for 5 buckets with a little left.

#### 100mm Arcade Buttons - 2x $10 | 2x ~$5 - https://www.adafruit.com/product/1185 or https://www.aliexpress.us/item/3256805889389320.html
>Nice, fairly rugged buttons for players to slap. The built-in LEDs may be a little dim, so on mine I replaced the inline resistors with 1ohm ones. Can easily be substituted with other button options, but the code is expecting 2 switch pins and 2 LED pins.

#### EC11 Rotary Encoder - .1x $11 | .2x ~$2.5 - https://www.amazon.com/DIYhz-Rotary-Encoder-Digital-Potentiometer/dp/B07D3D64X7 or https://www.aliexpress.us/item/3256805796819763.html
>For menu navigation and game setup. Should be able to substitute pretty easily so long as it's "EC11" on the listing.

#### 5V Step Down Regulator - .5x $14 | 1x ~$6 - https://www.amazon.com/gp/product/B09VY3WQ93 or https://www.aliexpress.us/item/3256804842995283.html
>The controller doesn't need much current, but the LEDs can pull a surprising amount of power, so this type of regulator is enough overhead to even have room for future expansion. In addition, this will take any voltage up to 24v/6s and down to at least 7v/2s, so it gives a lot of flexibility in powering the timer. This brand is a pack of 2, but there's plenty around in single packs.

#### XT60E-M - .1x $10 | .1x ~$5.5 - https://www.amazon.com/SoloGood-XT60E-M-Mountable-Connector-Multicopter/dp/B07YJMCDC3 or https://www.aliexpress.us/item/3256805624001851.html
>Good ole XT60 to plug in whatever power source you desire. Probably plenty of listings for cheaper, I picked this one because it comes with the M2.5 screws that are uncommon to have on hand. Could be cheeky and find some with wires presoldered to run direct to the regulator.Panel mount because the intent is have it face **out** of the electronics box and into the bucket where the battery will stay. Saves space inside the box and is a good layer of battery safety. 

#### Power Switch - 1/12x $6 | .1x ~$2 https://www.amazon.com/gp/product/B018FHB0H6/ or https://www.aliexpress.com/i/2255799836658047.html
>Goes between your battery input and the power regulator to have some control other than unplugging the battery. A flexible option, I like these little rockers for being able to be on the top of the timer but not be easy for players to hit by accident. 

#### 4-Gang Old Work Box - 1x $11.50 - https://www.homedepot.com/p/Carlon-4-Gang-71-cu-in-PVC-Old-Work-Electrical-Switch-and-Outlet-Box-B468R/202077406
>This mounts down into the bucket lid and keeps all your electronics nice and contained and away from unaware fingies. It's important to get the "old work" style with the little flappy bits as those are what lets it just mount into the bucket lid. Originally went with 4-gang to be able to fit our existing batts, but also found it's large enough to even mount the arcade buttons to have their wiring extend down into it. A 3-gang or even 2-gang box is a viable option if you don't intend to mount the buttons inside of it. 

#### 5gal Bucket Lid + 5gal bucket - 1x $3 + $4 - https://www.homedepot.com/p/Leaktite-5-gal-Black-Paint-Bucket-Lid-6GLDBLK30/202264045 and https://www.homedepot.com/p/The-Home-Depot-5-Gallon-Orange-Homer-Bucket-05GLHD2/100087613
>All of our components mount either into the lid or sit inside something that does. I like this particular lid for needing less force to pop off after it's been in the sun all day. Bucket type is completely substitutable, just included for completeness. I have come to like any buckets with the flexible plastic handle as it doesn't get caught on the LED strips around the lid.

### Assorted Hardware Needs
---

 - Wire - I like 22ga silicone that you can get multi-packs of for pretty cheap
 - Heatshrink - For any soldered connections
 - Header wires - https://www.microcenter.com/product/613879/inland-dupont-jumper-wire-20cm-3-pack - Can do most hookup aside from power with just a pack of these if you wanted.
 - Some screws - The printed panel I use screws directly into the electrical box. I put some M3 heatsets in there for ease, but any close-enough screw should work. 

### Future Hardware Additions
---

#### Low Voltage Cutoff Module - .33x $14 - https://www.amazon.com/dp/B0B6BP6J2D/
>Rather than rely on alarms alone for LiPo, this is an extra level of safety for them that I'd like to be an auto-include in future builds.