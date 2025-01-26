> [!NOTE]  
> This article is for developers who would like to create their own community device implementation. If you are interested in simply using community devices, check out [this page](https://github.com/MobiFlight/MobiFlight-Connector/wiki/Using-a-pre-build-custom-device)

## Prerequisites
* MobiFlight firmware development is done with [VSCode](https://code.visualstudio.com/) and the [PlatformIO](https://platformio.org) extension. 
Make sure to install both.
* **Create** a new reposority by using the [Community Template repository](https://github.com/MobiFlight/CommunityTemplate)*
* Clone this reposority and open it in PlatformIO. Cloning could be directly done within PlatformIO,

Follow the next steps carefully!

## Preparing the firmware
* Open a terminal window within PlatformIO if it's not already opened

![image](https://github.com/user-attachments/assets/871652b5-eab5-4709-af93-2338cd526e75)
* type `python renaming.py` into the terminal window and answer the 2 questions

![image](https://github.com/user-attachments/assets/bc9e553f-f55e-48cd-8374-fb27e9f1ba43)

All required files and folders get renamed according your naming.

### Testing
Now it's a good point to test everything you have set up.

The existing firmware itself will do nothing, but you can check if your new community board will show up under the Mobiflight Modules dialog if flashing the firmware to your new board. Additionally you can check if your community device could be choosed and gets uploaded to your board.
A new Mega w/o firmware is connected:

![image](https://github.com/MobiFlight/MobiFlight-Connector/assets/3263285/7167ecb9-c254-400c-88be-fc5ef5b103b3)

In the list of firmwares there should be an entry which matches `'-DMOBIFLIGHT_TYPE="YourDevice_board"'` from `YourChangedName_platformio.ini`.
Choose this entry and your firmware gets uploaded.
After this step you should be able to add a community device.

![image](https://github.com/MobiFlight/MobiFlight-Connector/assets/3263285/59f292f7-cbb1-4570-b0be-c5a933958e9e)

For each `YourName.YourDevice.device.json` a list item with `"Type": "YourName_YourDevice"` should show up. Choose one of them and check if all pins will show up. If you have more than one community device defined test this with all of them.

![image](https://github.com/MobiFlight/MobiFlight-Connector/assets/3263285/55d15e50-39ee-4474-a251-61da51754320)


## Implement your community firmware
See all hints in the files. It is also a good idea to check how the examples are set up. The basic GNC255 community device supports an 256x128 OLED, so just one community class is supported. The community device for the FCU and EFIS display from KAV simulation supports five different classes, so it's a good example how to set up two ore more supported devices.

## Further information

### Special message
There are some special messages with their respective IDs defined:
* Stop message (`-1`) - The device should turn off on receiving this message. The message is sent by the Connector any time the MobiFlight execution stops (Stop-button) or the application is shutdown.
* PowerSavingMode message (`-2`) - The device should go into a power saving mode (value=1) or wake up from it again (value=0).

### Overview how the json files are related
![image](https://github.com/MobiFlight/MobiFlight-Connector/assets/3263285/0123829b-27c1-49ad-96d2-30a751da6e25)

