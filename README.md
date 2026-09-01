> [!NOTE]  
> This article is for developers who would like to create specialty output devices not already supported by MobiFlight. If you are interested in using community devices someone else has made check out [this page](https://github.com/MobiFlight/MobiFlight-Connector/wiki/Using-a-pre-build-custom-device). If you are new to MobiFlight see the [core documentation](https://docs.mobiflight.com/getting-started/)

## Quick overview
MobiFlight supports general purpose "devices". Input (buttons, encoders, potentiometers, etc) and Output (7-segment displays, LEDs, etc) running on Arduino-compatible "boards". 

Community (aka Custom) devices allow specialty output devices to be included as new devices on a user's board. A typcial use case would be creating a graphical airspeed indicator for a small LCD screen. The MobiFlight client sends the current airspeed from the sim and the Community device code draws the airspeed indicator background and positions the needle on the LCD based on the input. 

Currently, only Output devices (devices that receive information *from* the Mobiflight connector) are supported; there is no Community "Input" type. However users can add the usual input devices to a board along with a custom device (e.g. an altimiter screen with a pressure adjustment knob as a regular encoder device.)

## Prerequisites
MobiFlight firmware development uses the following free/open source tools:
*  [VSCode](https://code.visualstudio.com/) Microsoft's free IDE
*  [PlatformIO](https://platformio.org) extension to VS code
*  [Python](https://www.python.org/downloads/) as a runtime for scripts (may already be installed as part of other installs)
*  [Git client](https://git-scm.com/install/) (useful, but not strictly necessary)
  
## **Create** a new repository by using the [Community Template repository](https://github.com/MobiFlight/CommunityTemplate)
Clone the repository and open it in PlatformIO.
* Open a Windows shell
* cd to the parent directory for your project
* run ```git clone https://github.com/MobiFlight/CommunityTemplate```
* rename the new 'CommunityTemplate' directory to something appropriate for your project

## Renaming script to prepare the firmware
* cd into your new directory
* run `python renaming.py` from your terminal and answer the 2 questions (Author and Device name)
* :warning:NOTE: Do not use spaces or special characters. The script does not do any input validation!
* Best practice: Keep both entries short. E.g. use your lastname or initials for 'Author'. Use a short name for 'Device'. You can modify the longer descriptions later.
* Note: Below we will refer to these answer values as [device] and [author] 
The renaming.py script will rename classes, folders, constants, files and a directory. While it is possible to do this by hand, there are a number of places where strings must perfectly match in order for the project to work with the MobiFlight Connector software. Note that you can change values by hand, but you cannot re-run the connector software as it's looking for templated values. If you make a mistake here early in your project the best option is to re-clone the repo and start again.

## Initial Build
Now is a good point to test your changes and toolchain. The existing firmware itself will do nothing, but you can confirm that the renaming script worked correctly and that your new community board is recognized by the MF Connector software.
* From your shell window you can start VS code with ```code .``` or Start VS Code from the Windows menu and open your project directory.
* It will take VS Code a minute to update the project and get PlatformIO started. 
* Use the PlatformIO build icon (the checkmark) at the bottom to compile. If you're new to PlatformIO, documentation is [here](https://docs.platformio.org/en/latest/integration/ide/pioide.html) The checkmark compiles, while the right arrow compiles and uploads to your board. :star: Pro Tip: PIO will try to auto-detect the board. If you have more than one board connected, click on the Plug icon with the word "Auto" after it and choose the correct COM port from the drop down.
* The first compile will take a couple minutes as it pulls in the core MF Firmware repository and installs necessary libraries. Subsequent builds should go much faster. 
* Issues? Look at the compiler output. Possible issues could include spaces or special characters in the author or device name. Or missing libraries/repos. Try closing and reopening VS Code to and rebuild to re-pull libraries if first attempt failed. If you had bad characters in the name from the renaming.py script answers, it might be best to just start fresh.
* :star:PRO Tip: You can speed up your builds by only building for your current testing board. In the bottom blue PlatformIO status bar, you should see folder-with-target icon followed by "Default ([device name])" Click on that and then select your current board configuation from the top drop-down menu. E.g. "env:[author]\_[device]\_[board]" It is also safe to delete the environment sections from your [device]\_platformio.ini for boards you know will not support your Community Device.

## Test with the MF Connector Client
If your build succeeded, you can now try it with the MobiFlight Connector Client
* Copy the contents of the Community folder under your [device] folder to a new directory in the MobiFlight Community directory. By default this foler is '''%LOCALAPPDATA%\MobiFlight\MobiFlight Connector\Community'''
* Name the new folder [device] and copy the three directories: Firmware, Device, Board under that new directory.
* Start the MobiFlight client. Make sure your "bare" board is connected and there are no active Serial connections to the board.
* The example below is on Version 10 of the MF client using a new Arduino Mega with no firmware or configuration

![image](https://github.com/MobiFlight/MobiFlight-Connector/assets/3263285/7167ecb9-c254-400c-88be-fc5ef5b103b3)

In the list of available firmware there should be an entry which matches `'-DMOBIFLIGHT_TYPE="YourDevice_board"'` in `YourChangedName_platformio.ini`. This should be [author]\_[device]
Choose this entry and your new firmware will be uploaded.
You should now be able to add your custom community device to your flashed board.

![image](https://github.com/MobiFlight/MobiFlight-Connector/assets/3263285/59f292f7-cbb1-4570-b0be-c5a933958e9e)

For each `[author]\_[device].device.json` a list item with `"Type": "[author]\_[device]"` should show up. Choose one of them and check if all pins will show up. The template names these "Pin 1", "Pin 2", and "Pin 3". You will need to change the number of pins and their names to something more meaningful. If your device is hard-wired (e.g. a display/processor combo board) it is best to set these values in the code rather than require the user to enter the correct pin numbers.

![image](https://github.com/MobiFlight/MobiFlight-Connector/assets/3263285/55d15e50-39ee-4474-a251-61da51754320)

## Setup Troubleshooting
* In general, check if the issue is your board or your Community Device code by seeing if your board works with the base MF board firmware. Just flash default firmware then test to narrow down the issue.
* Make sure there are no other programs that have it's COM port open. In Windows, only one program can interact with the COM port at a time.
* Did you copy the Community files into the correct Community directory?
* In your MF Community directory is there another custom device (maybe one of your earlier attempts) with a Community directory that has errors in the files? One bad community directory can break the Mobiflight client parser.
* Are you using an unusual or clone hardware? The USB IDs could be off or may need to be added to your board.json file. Try flashing the basic MF firmware as a test.
* Does your board do something unusual (e.g. the ESP32 goes into firmware download mode) in response to a dtr signal? Change the DtrEnable setting in your board.json file to False (and check for USB vid/pid overlap with the default boards)
* Are you reusing a board? You may want to reset the board first. An old configuration could be causing an issue.
* Does your board use one of the knock-off CH340 USB/Serial driver chips? See MF documentation on installing the correct drivers.
* Did you upload bad code and the board is in a reboot loop? Connect to the board and see if there is any serial output.
* Do you have delays or Serial output in your code? These can confuse the client and cause it not to recognize the board as a MF board.
* Review the Mobiflight Connector Client debug logs to see if and how your board is detected at connection time.

# Implement your community firmware
This is where the fun starts! You've gotten past all of the pre-requisites and connection configuration and you can now write code to implement your custom device.
See configuration comments and hints in the files, especially the [device]_platformio.ini file. It is also a good idea to check how the examples are set up. The basic GNC255 community device supports an 256x128 OLED, so just one community class is supported. The community device for the FCU and EFIS display from KAV simulation supports five different classes, so it's a good example how to set up two or more supported devices.

## File organization
* All of your custom code should fall under the [device] folder of your project. 
* You will mainly be editing the [device].cpp and [device].h files after initial configuration.
* If your project will only support a single hardware type (e.g. RP2040) you may safely delete the other [env.*] sections of your [device]_platformio.ini file, all the extra board.json files, and any unnecessary files in the Community/firmware folder.
* Do NOT edit the base platformio.ini file in the root directory.
* All of the base mobiflight firmware is under the ./src/src directory. You do NOT need to edit any of them, but reading them may give you some ideas on how things work.
* :star: Pro-tip: Don't forget: Your *.json files are NOT automatically saved when you compile! Don't forget to manually save them before copying to the MF Community directory
* :star: Pro-tip: You can compile and upload to your board directly from PlatformIO. You don't need to compile, move firmware, and upload from the client! However you cannot upload from PIO if MF client is running. Close Mobiflight first. Remember: only one device can connect to a serial port at a time.

## Board Configuration (boards.json files)
Boards are the base hardware unit of MobiFlight. They are configured in the [device]/Community/boards/*.json files. 
* "Boards" are the different Arduino types. Your custom device could support one or multiple board types. The project [device]/Community/boards/*.json files define the board properties.
* If you are only supporting one particular hardware type, you may safely delete all the other board.json files (and the [env.*] sections mentioned above). 
* If you are using unusual hardware with unusual USB VID/PID, set those up in the HardwareIds of the board.
* ESP32 is not yet officially supported, but Ralf has a fork that supports it [here](https://github.com/elral/MF_CommunityTemplate/tree/ESP32_support)
* The DtrEnable setting causes MF to send your serial device a "Data Terminal Ready" command on connecting. For most arduino compatible boards this is a simple restart command. However for others this can cause your board to go into a firmware update mode. If your board always seems to lock up when the MF Client starts, this may be the reason.
* If your device uses some of the pins, remove them from the "Pins" list in the board.
* Be careful editing other named values. Many of them are linked to values in other files and if the string compare fails your project won't work.
* The "Community" section is not modified by the renaming script. Feel free to hand-update.
* The "Friendly name" can get too long. MF Client expects this to be 16 characters or less. Shorten it appropriately.
* Edit "ModuleLimits" appropriately. E.g. if you are using a hard-wired screen, you may want to limit your project to 1 "MaxCustomDevices". Similarly, remove pins from the list that the user should not use for their other devices on the same board. 

## Device Configuration (device.json files)
Devices are the base MobiFlight connectable element. (Buttons, encoders, 7-segment displays are all "devices") Your custom device(s) are configured in the [device]/Community/devices/*.json files.
* You project can have one or many different device types. The default template comes with two device types. You may safely delete the second device if you are only using one. 
* The default template uses three pins. You may add/delete/rename these. If you aren't using any user-configurable pins, you may delete them all, but leave an empty "Pins": [] section in the "Config".
* The "Label" section of "Info" can safely be edited. Keep it under 16 characters, and no special characters.
* :star: the "MessageTypes" section defines the connection between your device and the MobiFlight Connector. The id Numbers here correspond to the value passed in the `set` method of your [device] class in [device].cpp.
* MessageTypes key on the id! If you change the id value, the mobiflight connector does not update and will send the wrong values to your project.
* Stop message (`-1`) - The device should turn off on receiving this message. The message is sent by the Connector any time the MobiFlight execution stops (Stop-button) or the application is shutdown. You should not define this message in your MessageTypes. It's sent by the MF Client.
* PowerSavingMode message (`-2`) - The device should go into a power saving mode (value=1) or wake up from it again (value=0). You should not define this message in your MessageTypes. It's sent by the MF Client.
* :star: pro-tip: The order in the .json file is the order they appear in the MF Connector, not the id #. However, be careful that you don't re-use id numbers. They do not need to be consecutive, just unique.
* :star: The compile step builds a .zip file with with your community files bundled up. However this file will NOT be rebuilt at each compile. You must delete the .\_build and .\_deploy folders to rebuild the .zip

## Coding tips
* The vast majority of your custom code will go into the [device].cpp and [device].h files.
* In your [device].cpp file you will put setup code in the begin() method (similar to the "setup()" function in arduino). You react to changes in values from the sim (via the MobiFlight Connector) in the set() method. You perform periodic updates, if necessary, in the update() method (similar to the "loop()" function in arduino). You can add other methods and class variables as needed in the .h file and implement them in the .cpp file.
* In other words, you can organize your code into:
  * Setup steps: Configuring pins, displays, variables (the "begin()" class method)
  * Process data sent from MobiFlight (the switch statement in the "set()" class method)
  * Update your display with the new data (the "update()" class method)
* There are two main ways to have your device refresh/update. You can either update it when the data changes or timed refresh every n milliseconds.

To update when data changes, put the appropriate update code/method call in the set() method of your main class (the class in the [device].cpp file). E.g. for a simple altimeter, you may only want to refresh the screen when the altitude changes. In the set() method's switch() statement add a call to refresh the screen in response to a new altitude. 

However for a large gauge (e.g. an engine monitor) where several values are changing every second it would be better to just refresh the whole screen every 25ms with the then current data. So, you'd update class variables in the set() method and call the screen update in the update() method. By default, the update() method is not active. You must uncomment the -DMF_CUSTOMDEVICE_HAS_UPDATE line in the [device]\_platformio.ini file and set a -DMF_CUSTOMDEVICE_POLL_MS value. Note that if that value is set very low and your update code is extensive other MF actions may not have a chance to run and you risk losing encoder inputs or button presses. Smaller numbers mean faster refresh, but that may not be better!
* Add any necessary libraries to lib_deps in the top [env\_[device]] section of your [device]\_plaformio.ini files.* If you need the memory, you can disable device types you won't need/support in the build_unflags section of your [device]\_platformio.ini
* In the set() method you are passed two variables, the id of the variable being set (corresponding to the value in the device.json file) and a string with the value. You will decide how that string should be transformed into a floating point or an integer or be left as a string.
* In general, MobiFlight only sends values when they change. Some things never or rarely change (e.g. airplane parameters like Vs0), others change every cycle (airplane elevation to the millimeter). You can reduce load on your device by rounding values in mobiflight before sending them.
* Getting your screen to get *any* output on it is a major achievement! Wiring screens and configuring graphics libraries can be tricky. 
* Make sure you confirm that all the variables you want to use are available from your sim before you get in too deep. Nothing is more frustrating than building the perfect screen to show a value that isn't available.

## Configuration
End users can add your custom device to their configuration the usual way: Flash the board with your firmware, add devices--including your custom device--and incorporate into their cockpit. If you are shipping a pre-wired instrument and don't want your end users making a mistake in configuration you have a few options:
1. Hard code in your code. If your instrument only consists of your custom device, just remove the pin definitions, hard code them in your class, and remove the ability to add new devices in the boards.json ModuleLimits section.
2. Ship an .mfmc configuration file the user can use with their board and the MF Connector client.
3. Use the HAS_CONFIG_IN_FLASH feature. This is if you have both a custom device *and* base MobiFlight devices in your hardware. E.g. a screen with a rotary encoder and a pushbutton.
To include your board config in flash:
* Uncomment the ```-DHAS_CONFIG_IN_FLASH``` line in the [device]\_platformio.ini file
* Edit the [device]/MFCustomDevicesConfig.h file to include your complete configuration, one device per line replacing the example configuration in the template file.
* :star:The easy way to get your configuration strings is to configure your device using the MF Connector client, and then getting the necesary strings using the ```12;``` command from a serial terminal. This will give you something like: ```10,17.LC2Chrono.0|1|2|3|4|5..CC's LC2Chrono:1.6.modeBtn:14.11.7.8.9.10.2.Multiplexer:;``` From this, you would drop the leading '10,' (response type) and replace the vertical bars '|' with '.' and take out some of the extra . delimiters. So the resulting file would be:
```
const char CustomDeviceConfig[] PROGMEM =
{
  "17.0.1.2.3.4.5.CC's LC2Chrono:"
  "1.6.modeBtn:"
  "14.11.7.8.9.10.2.Multiplexer:"
}
```

* Otherwise, you can construct the strings by hand using the ids found in ./src/src/config.h with the appropriate number of arguments and the device name for each device. Arguments are separated by dots '.' and terminated with a colon ':'. The number of arguments varies by device type. E.g. an encoder is ```8.a_pin.b_pin.enc_type.name:```
* :star: NOTE: There must NOT be a conventional MobiFlight configuration on the device. If your hardware has a MobiFlight uploaded profile and an configuration in flash, the uploaded profile takes precedence. You will have to wipe your device and reupload the firmware for your flash configuration to work. You can check the profile string MobiFlight sees by using the `12;` command in a serial terminal.

# Debugging/Testing
* Many people find it easier to work out details of screen configuration and core logic in a simple "hello world" project before moving it to the MF Community template.
* You can open a serial port to directly test your device. (115200 baud) The communication protocol is CmdMessenger. The command ids are in the ./src/src/commandmessenger.h file. The general format of the command is ```command_id,command_args;``` No CR/LF.
* To send a message with id 3 with value 4.5 to your first added custom device, from a serial terminal enter: ```32,0,3,4.5;``` Note that it will not echo. Use a semi-colon, not an enter to terminate the command. Other useful comands are ```5;``` quick 'are you alive?' test. ```9;``` get info on board. ```12;``` get board config string.
* Be careful with Serial.printf() debugging. Random string output to the serial port can confuse the MF client. You can use them in combination with serial debugging described above, but you will need to disable Serial.print statements before resuming testing with the MF client.
* MF Client expects a certain response from your board when it boots. If you have long delays at startup or extraneous serial output this step may fail and your board will not be recognized.
* Instead of using Serial.printf, you can use: ```cmdMessenger.sendCmd(kDebug, F("Unexpected error! Debug message"));``` and make sure to turn up logging level in the MF Client to "debug"
* On a brand new project your custom code will NOT run until you add your new device to the board using the MF Connector. Obvious, but easy to forget, especially if you're used to debugging with the serial terminal
* You don't need to build, copy the firmware file, upload from MF with each change. You can just build and upload from VS Code and then test from a serial terminal or from the MF client, but you will need to shutdown the MF client to allow VS Code to complete the firmware update.

# Going Further, additional information

## YouTube video series
In early 2026, CACrawf recorded a six part series of screen share videos walking through setup and creation of a simple custom display device. The video playlist is [here](https://youtube.com/playlist?list=PLs8cKRa3_buI8JBxz_b9rZXPu8PL7GuUh&si=TwfioTsuSwvoiGhU)

## Discord discussion
The MobiFlight Discord server has a channel dedicated to showing off your Community devices and asking questions [here](https://discord.com/channels/608690978081210392/1202389947173052467)


### Overview how the json files are related
![image](https://github.com/MobiFlight/MobiFlight-Connector/assets/3263285/0123829b-27c1-49ad-96d2-30a751da6e25)

