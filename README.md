# MCU_Game_Timers
Recreation of the GamModEr foam-flinging oriented game timer, featured at https://gamemoderepository.wixsite.com/dart/koth-timer-v3

Keeps many of the core build concepts, but aims to introduce an upgrade to some of the hardware capabilities while streamlining the build.

![](https://i.imgur.com/xyAUXBF.jpg)

## Features
#### Revamped navigation and interface
The original buckets used a simple system to aim for lower complexity, relying on just the team buttons. I've decided that the increase in input complexity is a worthwhile cost to enhance the functionality of the ui. A rotary encoder is used for the majority of UI navigation with the team buttons being used solely for team selection. During a timed game mode the encoder can pause and resume the timer.

#### Consolidated construction
Core portions of the original design are maintained, such as usage of a 5gal bucket lid and a residential electrical gang box. My design aims to confine the majority of the components to inside of the electrical box "core", including even the bottoms of the team buttons. This enhances wire management and adds a layer of safety for both the integrity of the electrical connections and the person handling the timer. LED wires are the only outward-facing wires as the bucket lid inherently doesn't allow running them concealed.

#### CircuitPython vs C++/Arduino
This change is primarily due to my own coding ability, but also to make modifications, additions, and customizations easier on end-users. CircuitPython can be edited by as little as a text editor on a phone or tablet and allows for quick turnaround on changes. I've personally made changes to the code during an event and was able to add in a new mode with audio output before lunch. The basic version is currently built for a Pi Pico for cost and availability reasons, but the code is compatible with any CircuitPython capable board. The networked version is being built around ESP32-S3 boards for their proprietary ESP-NOW protocol and native USB, but should be compatible with any other CircuitPython ESP32 boards. 


## Code Versions
[Standalone Version](buckets_standalone)

This is the simplest version of the timer buckets with no networking capabilities. A good option if you're looking for a couple buckets and lower hardware costs.

[Networked Version](buckets_networked)

This version is built for multiple buckets to communicate with each other and a central hub. This version is more complex and requires more hardware, but allows for more advanced game modes and features.

---
My code and designs included in this repo are licensed under CC4.0 CC-BY-NC-SA.
Code references, libraries, and other non-original creations are under their original licenses and attributions.