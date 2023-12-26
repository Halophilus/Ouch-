# OUCH! HARDWARE README

## Introduction
![Project Overview](/Documentation/images/title.png)
This is the hardware section of the documentation for the Ouch! project. Here, I will cover the techical challenges overcame to bring the installation together.

⚠️ IMPORTANT SAFETY WARNING: HIGH RISK OF ELECTROCUTION ⚠️

READ CAREFULLY BEFORE PROCEEDING

🔴 Handling AC Electricity: This project involves working with AC (Alternating Current) electricity, which poses a significant risk of serious injury or death. AC electricity from a standard household outlet is enough to cause electrocution.

🔴 Professional Expertise Required: If you are not thoroughly trained and experienced in electrical engineering or working with high-voltage systems, DO NOT attempt this project. Incorrect handling of AC power can lead to dangerous situations, including but not limited to electric shock, fires, or fatal accidents.

🔴 Safety Precautions: Always adhere to safety guidelines and local electrical codes. Use appropriate personal protective equipment (PPE). Ensure all power is switched off and unplugged before working on any electrical component. Double-check connections and use appropriate insulation and grounding techniques.

🔴 Seek Professional Assistance: I strongly recommend consulting with or hiring a qualified electrician or electrical engineer to supervise, review, or conduct any work involving AC electricity.

🔴 Testing and Inspection: Have all electrical setups inspected by a professional for safety compliance before use.

🔴 Liability: I, the creator and distributor of this project documentation cannot be held liable for any damages, injuries, or deaths resulting from the implementation of this project. You undertake this project at your own risk.

🔴 EVERYTHING IN THIS PROJECT CAN BE ACCOMPLISHED IN SOME WAY WITHOUT DIRECTLY UTILIZING AC ELECTRICITY, PLEASE CONSIDER ALL VIABLE OPTIONS BEFORE STEPPING INTO A PROJECT LIKE THIS

## Table of Contents
1. [Introduction](#introduction)
2. [Safety Warning](#safety-warning)
3. [Hardware Components](#hardware-components)
4. [Under the Hood](#under-the-hood)
    - [PWM Fan Control](#pwm-fan-control)
    - [Fog Machine](#fog-machine)
    - [Power Supply](#power-supply)
    - [Audio Amplification Circuit](#audio-amplification-circuit)
    - [Video Output Circuit](#video-output-circuit)
    - [Power Management Circuit](#power-management-circuit)
5. [External Peripherals](#external-peripherals)
    - [CRT Housing](#crt-housing)
    - [Indicator LEDs](#indicator-leds)
    - [HDD Noise](#hdd-noise)
    - [Proximity Sensor](#proximity-sensor)
    - [Button Control Station](#button-control-station)
6. [Setup Guide](#setup-guide)
7. [Usage](#usage)
8. [License](#license)
9. [Contact](#contact)
10. [Acknowledgments](#acknowledgments)

## Hardware Components
Many of the hardware components here were harvested from existing electronics, some were purchased specifically for the project. Here is a semi-exhaustive list of those components.

| Component | Description | Notes | Quantity |
|-----------|-------------|-----------|-----------|
| RPi 3B+   | Raspberry Pi Model 3B+ | Relay GPIO signals with transistors and opto-couplers to limit current sourcing |1 |
| LM386     | Audio Amplifier Board | Adequate gain for high imp. application | 1 |
| SFF PSU   | S-Union 240W Power Supply Unit (12V, 5V, 3.3V, 5V SB, GND) | Had to be replaced twice, ultimately replaced with an external PSU. Might be worth it to invest in a higher wattage/quality. | 1 |
| CRT Display | 8.5 in. VGA Monitor SONY CRT Display Technologies CD150V-120 DB9 connector CNC OEM | Every antiquated CRT has its quirks, this one needed replaced pots. | 1 |
| DB9 M to F | Cable for 9 pin VGA protocol | Has one-to-one pin connections for DB15 protocol | 1 |
| DB9 to DB15 Patch | Screw terminal adapter for converting DB15 to DB19 | When installed, the construction is extremely durable to vibration and movement | 1 |
| SSR Relay | SSR-25DA 25A /250V 3-32V DC Input 24-380VAC Output solid state relay | Logic level relay can be triggered by GPIO | 1 |
| HC-SR04 | Ultrasonic proximity sensor | May be glitchy when RPi is managing multiple high-power peripherals. Voltage step-down is needed as this module returns a 5V signal. | 1 |
| Audio headset | High impedance military HAM radio earpiece | Do not glue something like this shut! The wire terminals can bend loose and become totally unserviceable. Mine was a one-of-a-kind antique and now I need to dremel it apart to fix it. | 1 |
| 3.5mm audio adapter | Mono male to 2-pin screw terminal female AUX | Effective and reusable. | 1 |
| Blower fan | 80mm exhaust fan facing out of the case | These are less common these days but can be harvested from older electronics, like much of this project. | 1 |
| ULN2803 | Darlington transistor array for driving motor activity | Works to relay a PWM signal to higher voltages, notable 12V. | 1 |
| Small fan | 50mm intake fan | Came with the original IBM 2011 | 1 |
| Hard drive | Quantum Fireball(TM) 3.5 Series 1280MB IDE Disk Drive | The original plan was to write a script that caused the hard drive to seek. This proved overly complicated for this application. The effect was simulated by disabling and enabling the molex power to the HDD itself, which triggered spooling and seeking sounds on demand | 1 |
| USB to IDE cable | USB interface for accessing old hard drives | Ultimately deprecated from the final product, but could be added back with some refactoring | 1 |
| Button control station | NEMA3R dust-proof garage door control station with three buttons and a turnkey | While aesthetically pleasing, the nature of the button contacts in this control station caused phantom pressing and unpredictable bouncing at this operating voltage. This required software fixes that limited the desired functionality of the project. For future reference, use a different control station or embed low voltage momentaries into the station | 1 |
| RGB LED | Three-tone LED with a light guide for external visibility and an in-line resistor | Different LED colors operate at different save current loads, so each individual LED within this piece has to be given a different in-line resistance | 1 |
| Yellow LED | ibid. | A good low power option for an activity light. When installing, keep in mind that the posts are very brittle and will break if bent enought times. To ensure a long-lasting configuration, use marine heatshrink and some silicone adhesive to keep the rigid components in place | 1 |
| Supercapacitor | 5.4V 250F Serial Capacitor array | This is capable of intensely high and abrupt current loads so it is to be handled with care. However, it can be safely discharged across low resistances and operates at a low voltage, so risk of electrical shock is low. | 2 |
| Power resistor | 10ohm 50W current limiting power resistor | This is to limit the charging current passed from the PSU to the supercaps, which needs to be high wattage to deal with the power necessary to charge a 250F array. This also prevents the the PSU from sourcing too much current when the capacitors themselves are discharged | 1 |
| MOSFET | IRLB3034 power MOSFET | Can safely handle loads up to 60A. In parallel, that limit becomes 120A. A 3D housing mount was modeled to separate the MOSFETs from touching each other or short circuiting, as their back panels connect to drain | 2 |
| MOSFET Heatsink | M3 mount finned aluminum heatsink | Dissipates heat of MOSFETS under heavy load. Probably not totally necessary for this application, but when dealing with such high currents it is best to play it safe. | 1 |
| Thermal paste | Any will do | Facilitates transfer of heat from MOSFETs to heatsink | 10g |
| Resistance wire | Nichrome 80 resistance wire for heating | Rapidly generates fog as long as enough polyethylene glycol is added to the device. When building the coil, be careful that it only touches the live and ground post in the mount as it can easily short circuit if done improperly | 10 ft. |
| Heating element | 510 mounted four-post wire heating element with replaceable coils | This can be repurposed from your average roadside vape, although for safety it is best to buy a well machined one | 1 |
| PNP Transistors | P2222 transistors | Useful for switching higher voltages without sourcing to much current from the RPi, although not suitable for high power applications. | 15 |
| Opto-couplers | Optoisolation module for transmitting a signal between disparate circuits | Helpful when trying to distance high voltages from the sensitive RPi, although it does consume more power than a transistor switch | 5 |
| Piezoelectric speaker | A surface mount passive beeper | Can be triggered by GPIO. Doesn't need an entire section because the circuit consists of one component | 1 |
| IBM 2011 | Retro computer chassis, virtually any will do | When mapping out a project like this, take measurements ahead of time rather than assuming it will all fit. I did the latter and had to undergo complicated retrofitting to make everything work. There was considerable overflow, but luckily there was space to store additional peripherals in the monitor housing. | 1 |
| Safety capacitors | X and Y ceramic capacitors | These are necessary for the AC applications in this project. Work at your own risk. | 3 |
| External Cables | DB9 VGA, C14 power | These are the only external cables that aren't just wires and serve some insitutional purpose | 2 |
| Wire | 16awg speaker wire, 22awg solid-core wire, 12awg copper wire | The speaker wire is surprisingly brittle so position it where it will be bent the least. The solid-core wire is flexible and reusable but be sure to measure it carefully before cutting lengths of it, as excessive strain can pull it loose from contacts in breadboard and other circuits (get a set with several colors to differentiate different circuit paths), the solid copper wire is great for high current applications, but is not shielded and should be utilized conservatively. | 3 |
| Decorative cables | Misc. | These can be attached to the back of the PC which serve no practical purpose other than appearance. In this project, cables were scorched and scoured to look like they've gone through a war. Be careful when doing this if this step is included. | x |
| Breadboard | Prototyping pinhole breadboard | This is useful for prototyping, but became an embedded part of the project that made altering or adding circuity much easier | 2 |
| Adapters | Right-angle / pivot USB and HDMI adapters | There is a certain economy of space that is required for designing a project like this. While the original goal was to minimize USB peripherals, debugging demands the use of a mouse and keyboard, especially when working over networks where SSH is blocked. These will make it easier to route the necessary USB cables around existing peripherals | 4-5 |
| Silicone adhesive | Vibration-resistant electronic insulating adhesive | When fixing wires that were meant to flex in place, rigid adhesives will work against you. A flexible, insulating adhesive kept fragile fixtures in place, and even allowed me to fix items in the breadboard | 2 |
| Hot glue | High strength/temperature hot glue gun | Sometimes a rigid fixative is necessary, especially when adding in the 3D printed components | Countless sticks, 1 gun |
| Heatshrink tubing | Ideally marine heatshrink with inbuilt adhesives | For a project with this many wires, it would be reckless to rely on electrical tape. | Large set |
| Resistors | A variety pack of different impedance resistors | All of the circuits here are RC, and only some have capacitance: a great variety of resistors is needed | One set |

## Under the Hood
Most of the hardware was contained within the IBM 2011 chassis. Below is an image of the inside of that chassis with notable peripherals highlighted and colorized. Only the largest components from each category were numbered, but all components from each category are given the same color. 
![Colorized component map](/Documentation/images/under-the-hood.png)

1. [PWM Fan Control](#pwm-fan-control)
2. [Fog Machine](#fog-machine)
3. [Power supply](#power-supply)
4. [Audio Amplification Circuit](#audio-amplification-circuit)
5. [Video Output Circuit](#video-output-circuit)
6. [Power Management Circuit](#power-management-circuit)
---
### PWM Fan Control
This circuit utilizes a ULN2803 Darlington transistor array to control a motor using a PWM signal from a GPIO pin. 

![ULN2803 Darlington Transistor Motor Control](/Documentation/images/pwm-fan-control/circuit.png)

- **PWM Signal Generation:**
    - A GPIO pin on the RPi generates a PWM (Pulse Width Modulation) signal. The duty cycle of this PWM signal will determine the average voltage applied to the motor, which in turn controls the motor speed.

- **Current Limiting Resistor (R1):**
    - The GPIO pin is connected to the base of an NPN transistor (Q1) through a current-limiting resistor (R1). This resistor protects the GPIO from sourcing too much current and also sets the base current for Q1.

- **ULN2803 Darlington Pairs (Q1, Q2):**
    - The Darlington pairs in the ULN2803 are driven by the amplified signal from Q1. In your setup, multiple pairs are bridged in parallel to handle greater current. Bridging pairs is a common technique to allow more current to flow to the motor by combining the current capacity of multiple outputs.

- **Motor Connection:**
    - The motor is connected to the common output (COM) of the ULN2803 and the power supply. The COM pin also connects to a diode (D3), which provides a path for the inductive kickback from the motor's coil inductance (L) when the transistors switch off.

- **Free-wheeling Diodes (Built into ULN2803):**
        Each Darlington pair inside the ULN2803 has a built-in flyback diode (like D1) to handle the inductive kickback from the motor when the transistor turns off, preventing damage to the transistor.

- **Motor's Coil Inductance, Resistance, and Back EMF:**
    - The motor is modeled by three components: inductance (L), resistance (I), and back EMF (H). The inductance and back EMF represent the motor's inductive properties, and the resistance represents the actual resistance of the motor windings.

- **Operation:**
    - When the GPIO outputs a high signal, Q1 turns on, which in turn activates the Darlington pairs in the ULN2803, allowing current to flow through the motor, causing it to turn.
    - The speed of the motor is controlled by the PWM signal. A higher duty cycle means the motor receives more power and runs faster, while a lower duty cycle means less power and slower speed.

- **Power Supply Unit (PSU):**
    - The 12V PSU rail is used to provide the necessary voltage and current for the motor. This is separate from the logic level voltages provided by the microcontroller.


![Fan control components](/Documentation/images/pwm-fan-control/Implements.png)

The exhaust fan on the front of the case had a custom vent hood 3D printed for it so that all of the exhaust is exiting the case (50mm fan vent v1.STL). This feature plays into the functionality of the fog machine.

![Vent 3D model](/Documentation/images/pwm-fan-control/vent.png)

---
### Fog machine
This circuit is designed to discharge a pair of serial supercapacitors through a heating element to generate fog for theatrical effect at the end of the sequence.

![Circuit for fog machine](/Documentation/images/fog-machine/circuit.png)

- **ATX 5V Supply:**
    - The 5V rail on the PSU, used to passively charge the supercapacitors. 

- **SW1:**
    - This switch controls whether the supercapacitors are connected to the power supply for charging or isolated for discharge. This is controlled by activating and deactivating the PSU via the RPi.

- **C2 (250 F):**
    - Two 2.7V 500F supercapacitors connected in series, which would give a combined capacitance of 250F at 5.4V. This series connection allows the capacitors to be charged to a higher voltage, suitable for the 5V ATX power supply without requiring a step-down converter.

- **Current Limiting Resistor for Charging:**
    - In the charging path from the ATX power supply to the supercapacitors, there's a 10ohm resistor not shown in the diagram, which is used to limit the charging current to prevent strain on the power supply.

- **R2 (200 mΩ):**
    - This low impedance resistor acts as a heating element made from nichrome 80 wire. Its purpose is to generate fog by heating polyethylene glycol. Due to the low resistance, it can rapidly heat up when a high current passes through it.

- **M1 (IRLB3034 MOSFETs):** 
    - These MOSFETs are connected in parallel, each with a heatsink to handle the high current discharge from the supercapacitors. They act as electronic switches to control the discharge of the supercapacitors through R2. The parallel connection allows for current sharing between the MOSFETs, thus managing the abrupt high current without overheating.

- **R3 (15 kΩ):**
    - A pull-down resistor to ensure that M1's gate is at a known low potential when not actively driven by the RPi, preventing accidental activation of the MOSFETs.

- **ULN2003:**
    - This Darlington transistor array is used to interface the low-power GPIO signal from the RPi to the higher power required to switch the IRLB3034 MOSFETs, similar to how it was used for PWM. 

- **R4 (220 Ω):** 
    - This limits the base current going into the ULN2003 from the GPIO. This is not necessary due to the in-line resistor within the ULN2803, but was included in the original circuit design

- **RPi GPIO:** 
    - The Raspberry Pi controls the operation of the circuit. By outputting a signal, the RPi can precisely control the duration and timing of the discharge through the MOSFETs.

- **Supercapacitor Housing:** 
    - The supercapacitors are housed in a 3D-printed ATX case, which provides a safe enclosure and active cooling.

In operation, the supercapacitors charge when SW1 is closed. Once fully charged, SW1 is opened, and the RPi can initiate discharge by sending a signal to the ULN2003, which in turn activates the MOSFETs. The supercapacitors then discharge through R2, the heating element, creating a burst of high current that rapidly generates fog from the polyethylene glycol. The high capacity and swift discharge ability of supercapacitors make them excellent for applications requiring immediate energy release, which would not be safe or feasible for regular power supplies over such a low resistance load. The design must ensure that the supercapacitors and MOSFETs are adequately rated for the high discharge currents and that the heating element (R2) can withstand the thermal stress of rapid heating.

![Fog machine components](/Documentation/images/fog-machine/components.png)
These are the individual components involved in the fog machine. Originally, there was another circuit that discharged the capacitors only when the PSU was off and a discharge signal was being sent from the RPi. Later versions used the ULN2803.

![Atomizer support](/Documentation/images/fog-machine/atomizer.png)

This elevates the heating element away from wires and the base of the case where a short could occur (Atomizer Mount v1.STL). This also elevates the heating element so that generated fog is more readily carried by the fan current within the case.

![MOSFET Castle](/Documentation/images/fog-machine/castle.png)

This elevates the individual MOSFETs and fixes them in place to avoid shorts between them (Mosfet Castle v2.STL).

![MOSFET Castle Demo](/Documentation/images/fog-machine/fog.png)

What the MOSFET castle looks like fully installed. The red and black wires correspond to the source and drain ends of the gate respectively. The green wire acts as the trigger for the gate pin.

---
### Power Supply
The power supply is a modified SSF power supply in a custom housing that allows it to fit within the IBM 2011 and accommodate the supercaps in the fog machine circuit (PSU_Chassis.STL, PSU_Lid.STL)

![PSU Chassis](/Documentation/images/psu/model.png)

- There are five posts for five ATX rails (12V, 5V, 3.3V, 5VSB, GND).
- There are two holes on the bottom left of the PSU housing to accommodate wires for the power management circuit and the SSR.
- The back has a hole for an exit cable to power the CRT monitor.
- The female C14 outlet is glued into place on the lid
- There is also a spot for a power LED secondary to the PSU.
- The large circular hole on the same end as the fan exhaust is for peripherals not taking power directly from the rails, such as the supercap charging circuit.
- The fan for the power supply mounts directly to the far end of the case
- The lid itself is loose and easy to remove to access the interior until the top of the IBM 2011 chassis secures it in place
- This is a dangerous high AC voltage aspect to the project and not altogether necessary. An external PSU can supply all of these things and be isolated.

![PSU Chassis 2](/Documentation/images/psu/model2.png)

![Early installation for PSU](/Documentation/images/psu/installation.png)

---

### Audio Amplification Circuit
The audio output from the Raspberry Pi (RPi) is amplified using an LM386 op-amp board to drive a high-impedance HAM radio headset.

![LM386 Circuit Design courtesy of Marlin P. Jones & Assoc, Inc](/Documentation/images/audio/circuit.png)

note: The above circuit diagram was provided courtsey of Marlin P. Jones & Assoc, Inc, the manufacturers of the board used in this project. This is NOT an original circuit design.
- **LM386 Op-Amp Board:**
    - The board is built around the LM386 audio amplifier chip, which is known for its low voltage operation and ability to drive headphones and small speakers.
    - It provides a fixed gain of 200 times the input signal, which is suitable for amplifying the low-voltage audio output from the RPi.
    - The board includes a screw terminal for easy connection to a speaker or, in this case, the headset.
    - An onboard 10K variable resistor (potentiometer) allows for adjusting the volume. Turning the potentiometer clockwise increases the volume.
    - The board accepts an audio input signal directly through the chip pin leads, which makes it convenient for interfacing with the RPi analogue
    - It operates within a voltage range of 5-12V DC, and in this setup, it is powered by the 12V rail from the PSU to ensure enough power to drive the high-impedance headset.

- **Audio Connection:**
    - The audio signal from the RPi is routed to the op-amp board through a 3.5mm TS Mono Male to 2 Pin Screw Terminal Female AUX adapter. This adapter is a solderless balun converter that facilitates a reliable connection without the need for soldering, ideal for quick setups or prototyping.

- **HAM Radio Headset:**
    - The headset in use is an antique HAM radio set with an impedance of 846 ohms, which is considerably higher than modern headphones. High-impedance headphones require more voltage to achieve the same loudness as low-impedance ones.
    - The LM386's gain is sufficient to amplify the RPi's audio output (typically 0.5-1V) to a level that is audible through the high-impedance headset.

- **Power Supply:**
    - The LM386 board is powered by the ATX PSU's 12V supply. This voltage is at the upper end of the LM386's operating range, providing maximum headroom for the amplifier and ensuring that the headset is driven with enough power.

- **Volume and Distortion Control:**
    - The onboard volume control allows for real-time adjustment of the audio output level to the headset.
    - Additionally, the board features an adjustable potentiometer for distortion control, giving the user the option to fine-tune the audio quality and minimize any unwanted distortion.

![Components for the audio circuit](/Documentation/images/audio/components.png)

### Video Output Circuit
To facilitate a connection between the Raspberry Pi (RPi) and an older CRT monitor that accepts a DB9 VGA input, an adapter chain is used to convert the RPi's HDMI output to a VGA signal, and then adapt that VGA signal from a DB15 connector to a DB9 connector. Here's a technical description of this process, with a focus on the pin mapping from DB15 to DB9 for video signals:

![VGA Patch Detail](/Documentation/images/video/detail.png)

- **HDMI to VGA Conversion:**
    - The RPi outputs digital video signals through its HDMI port. A male HDMI to female VGA adapter is used to convert these digital signals into analog VGA signals. This adapter typically includes a DAC (Digital-to-Analog Converter) to handle the signal conversion.

- **DB15 VGA Breakout:**
    - The female VGA end of the adapter connects to a DB15 breakout board. The DB15 connector carries analog red, green, and blue video signals on pins 1, 2, and 3 respectively, along with other pins for horizontal and vertical sync signals, ground connections, and possibly additional signals for display data channel (DDC) information.

- **DB15 to DB9 Bridging:**
    - The analog VGA signals from the DB15 breakout are then bridged to a DB9 breakout board. The DB9 connector does not natively support VGA, as it was originally used for serial connections, so the following pins are repurposed for VGA signals:

    | Signal | 9-Pin | 15-Pin |
    |--------|-------|--------|
    | Red Video | 1 | 1 |
    | Green Video | 2 | 2 |
    | Blue Video | 3 | 3 |
    | Horizontal Sync | 4 | 13 |
    | Vertical Sync | 5 | 14 |
    | Red GND | 6 | 6 |
    | Green GND | 7 | 7 |
    | Blue GND | 8 | 8 |
    | Sync GND | 9 | 10 + 11 |

    - The remaining pins on the DB15 patch are  not connected, as DB9 does not accommodate all the signals present on a DB15 VGA connector.

- **DB9 VGA Cable Connection:**
    - The DB9 breakout board is then connected to the CRT monitor using a standard 9-pin VGA cable. The CRT monitor, an 8.5" VGA Monitor SONY CRT Display Technologies CD150V-120 with a DB9 connector, is designed to accept these repurposed VGA signals.

- **Power Circuit Control:**
    - The power to the CRT is controlled by the previously described power circuit, allowing the RPi to turn the monitor on or off as needed.

The DB9-out visible on the outside of the IBM 2011 was made flush with the existing I/O panel on the back. In order to support the DB9 board, staging was 3D printed to hold it up (VGA Stage v4.STL).

![Other angle of patch circuit](/Documentation/images/video/detail3.png)

![DB9 Support Staging](/Documentation/images/video/stage.png)

---

### Power Management Circuit
The RPi needs to manage power for a CRT monitor and an ATX Power Supply Unit (PSU) and controlling it using a Solid State Relay (SSR) and simple transistors.

![Power management circuit design](/Documentation/images/power/circuit.png)

- **RPi GPIO and ATX PSU Control:**
    - The RPi uses one of its GPIO pins (GPIO1) to control the power state of the ATX PSU. This is achieved through a transistor (N2222), which bridges the PS_ON pin to ground when activated. The PS_ON pin is a feature of ATX PSUs that allows for remote activation; pulling it to ground turns the PSU on. This configuration allows the RPi to switch the ATX PSU on or off as needed, ensuring power is provided only when required.

- **Solid State Relay (SSR) Activation:**
    - Another GPIO pin (GPIO2) on the RPi provides a control signal to the SSR-25DA. This SSR is rated for a substantial load of 25A at 250V AC, with a control voltage range of 3-32V DC, which is compatible with the RPi's GPIO output levels. When GPIO2 is high, the SSR is activated, allowing current to flow to the CRT, thus turning it on.

- **Safety Capacitors (CX and CY):**
    - Class X and Class Y safety capacitors are employed in the circuit to enhance safety and suppress electrical noise. CX, a Class X capacitor, is connected across the live and neutral lines to mitigate differential mode interference, while CY, a Class Y capacitor, bridges the live line to ground to filter common mode noise and protect against transient voltages.

- **Shared Ground:**
    - The RPi and the ATX PSU share a common ground, which is necessary for the proper operation of the transistor switching the PS_ON line and for the SSR that switches the CRT. This shared ground reference ensures that the control signals from the RPi have a return path and are referenced correctly to the PSU's and SSR's ground.

- **Fuses for Overcurrent Protection:**
    - The circuit includes a 10A fuse in series with the live wire going to the CRT. This fuse acts as a safeguard against overcurrent conditions which could potentially damage the CRT or create a fire hazard. Another fuse is assumed to be on the primary side of the ATX PSU to protect against overcurrent drawn from the mains.

- **CRT Power Management:**
    - The positioning of the SSR on the live wire going to the CRT is deliberate. When the SSR is off, the CRT is disconnected from the live supply and can discharge any residual voltage into the neutral line, preventing the accumulation of dangerous charge within the monitor.

In practice, the RPi can run scripts or programs that determine when the CRT should be powered on or off, possibly based on user input, a preset schedule, or sensor data. The use of solid-state switching and safety components ensures reliability and safety in operation, while the inclusion of fuses provides an essential layer of overcurrent protection.

The power management circuit started with an unsheathed PSU, an SSR, a transistor and a series of wires

![Power Circuit Components](/Documentation/images/power/components.png)

Because the SSR is controlling a high voltage, the entire apparatus needs to be heavily shielded. A sheath for the SSR was printed, isolating the contacts from any conductors (SSR Stage v6.STL). Sheathed leads eliminate the possibility of a short circuit.

![SSR Stage](/Documentation/images/power/stage.png)

![SSR](/Documentation/images/power/ssr.png)

- An aluminum heatsink was added to the SSR to dissipate heat associated with high voltage switching. 
- Due to the infrequency of switching, this was probably unnecessary, but I included it anyway.

---
## External Peripherals

The IBM 2011 was not accommodating enough for all of the features that needed to be packed into this installation. For that reason, some of the peripherals were packed into the CRT housing or otherwise hosted externally.

---

### CRT Housing
    
The CRT hardware originally arrived without a chassis, so a 3D model was generated that could present the monitor in the style of a machine terminal.

![CRT Housing Model](/Documentation/images/crt/model.png)

- The model was designed in three parts, bespoke for the dimensions of the Sony hardware.
    - The outer shell, forming the frame around the front screen and covering the length of the monitor (Monitor_Front.STL).
    - The back plate, which has an access port in the bottom for cables that can be attached to the back of the hardware (Monitor_Back.STL).
    - The bottom tray, which served to vault the monitor off of the base and provide some storage space for peripherals (Monitor_Bottom.STL).
        - Holes were drilled into the bottom tray and the top of the IBM 2011 to pass peripheral wires out of the case in a discreet fashion
        - Holes were also drilled so that bolts could be screwed into nuts that were adhered to the inside of the IBM 2011 as a stator to prevent slipping or theft.

---

### Indicator LEDs

To fully encapsulate the PC experience, power and randomly flickering activity lights were placed on the front panel of the IBM 2011.

![Front panel](/Documentation/images/led/panel.png)

- **Activity light**, left
    - Single yellow LED, powered by GPIO
    - Flickers at random intervals, with the frequency increasing with each successive sequence in the film.
    - Takes 220ohm limiting resistor

- **Power light**, right
    - Common cathode RGB LED with three diodes each associated with a primary color
    - Powered by 3.3V PSU rail to supply additional current, signals controlled with switching transistors
    - GPIO pins must be pulled low to trigger the light due to common cathode setup
    - G and B pins take 100ohm of limiting resistance, R gets 150ohm.
    - Different colors illuminate depending on the sequence being played.

---

### HDD Noise

Seeking and tracking sounds associated with hard drive activity were also a must for this retro computer experience.

![HDD and cables](/Documentation/images/hdd/hdd.png)

- Originally, the plan was to trigger seeking sounds using low-level IOCTL commands.
- The final setup simply deactivated and reactivated molex power (5V, 12V) to the HDD.
- Upon startup, the HDD seeks for a few minutes before shutting off.
- By power cycling the HDD rapidly, you can get audible differences in seeking behavior.
- This is likely damaging the HDD, which is fine because its only purpose for this application is a noisemaker.

---

### Proximity Sensor

One of the most engaging aspects of this installation was the instant activation upon approach. This was accomplished with an HC-SR04 module mounted to the front of the monitor casing. When an object is detected within a certain threshold, it initiates the wakeup protocol and waits for a key turn on the button panel.

![Front-facing proximity sensor](/Documentation/images/prox/prox.png)

- A voltage divider was used to pull down the return voltage from the module to the logic level of the RPi (~3.3V)
- This feature was disabled during demo screenings so the overall sequence was easier to control.
- The power control circuit was affected by input from the proximity sensor, so if someone walks away during the sequence the screen turns off.

### Button Control Station 
    
A button interface is necessary for user interaction. I used an industrial-looking button control station which has three buttons and a turnkey throw.

![NEMA3R Button Interface](/Documentation/images/button/closed.png)

- Upon initial startup, the device becomes primed to start the first sequence.
- The first sequence initializes when the user turns the key labelled 'ACCESS'
- At the terminus of the first sequence, a waiting sequence loops until the black 'SELECT' button is pressed.
- The same occurs for the next sequence, this time priming the yellow 'A-35' button.
- At the end of the final sequence, pressing the red 'THE RIGHT DECISION' button initiates the credits sequence.
- At the end of the credits sequence, finally turning the key back to its original position initiates shutdown and resets the device.

![Open panel button interface](/Documentation/images/button/open.png)

- The control panel was designed for voltages beyond logic level (3.3-5V).
- Button bouncing and phantom presses were very common for this application.
- This was dealt with on the software end, but it still posed issues.
- If I were to revisit this project, I would modify the button pressing mechanic.
- 4 cables are connected to GPIO pins, and all buttons share a common ground.
- A limiting resistor is added in the event of accidental discharge across the switch circuit as to protect the GPIO pins.

---

## Setup Guide

I've given enough material here for anyone to more-or-less be able to replicate the hardware component of this project. If anyone has any desire to create an engine like the one described to host their own unique material, I invite you to do so. 

## Usage
A machine terminal simulacrum can be used to display all manner of media beyond an interactive film. The hardware elements in here could be tied into any variety of user-facing interactive applications. 

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE.txt) file for details.

The GNU General Public License v3.0 is a free, copyleft license for software and other kinds of works, ensuring that all modified versions of the project are also free. This license guarantees your freedom to share and change all versions of a project to make sure it remains free software for all its users. For more information, please visit [GNU GPL v3.0's webpage](https://www.gnu.org/licenses/gpl-3.0.html).

## Contact
Reach me on my Git profile, Halophilus, or email me at benshaw@halophil.us if you have any questions.

## Acknowledgments
Credits to Ethan McCue for writing the looping_video.py script. All of these mechanics would be for naught had he not contributed.
