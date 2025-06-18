# FLOAT CODE

## Firmware 

1) Uncomment the `#define TRIAL` line in the `float.h` file in the `firmware_float` folder of the firmware before the trial 

```cpp
// Uncomment this line to enable motor control for trial runs
//#define TRIAL 1
```

2) First add the correct IP for your laptop in `float.h` file in the `firmware_float` folder of the firmware.


Run this command in your terminal to know ur laptop's IP:

```bash
ipconfig
```

**expect the following output:**

``` yaml
Wireless LAN adapter Wi-Fi:

Connection-specific DNS Suffix  . : home
IPv6 Address. . . . . . . . . . . : fd8c:d76:375e:1b00:cb8c:c0c8:7abb:18ed
Temporary IPv6 Address. . . . . . : fd8c:d76:375e:1b00:91ff:9d15:e368:daa2
Link-local IPv6 Address . . . . . : fe80::baec:9687:f239:3a79%11
IPv4 Address. . . . . . . . . . . : 192.168.1.5   <---- Change to your laptop IP in the float.h         
Subnet Mask . . . . . . . . . . . : 255.255.255.0
Default Gateway . . . . . . . . . : 192.168.1.1
```

3) Callibrate the Time for going down and going up in the `float.h` file in the `firmware_float` folder of the firmware.

``` cpp
// Time constants for diving
#define TIME_FOR_GOING_DOWN 5000  // Time to go down in milliseconds
#define TIME_FOR_GOING_UP 5000    // Time to go up in milliseconds