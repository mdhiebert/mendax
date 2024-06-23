# Mendax

Mendax (latin for "liar") is a disposable, efficient signal-replicator for operational use.

## Table of Contents

1. [Table of Contents](#table-of-contents])
2. [Quickstart](#quickstart])
    - [Setting up the HackRF](#setting-up-the-hackrf)
        - [Installing HackRF Software](#installing-hackrf-software)
        - [Updating HackRF Firmware](#updating-hackrf-firmware)
        - [Verifying Successful HackRF Setup](#verifying-successful-hackrf-setup)
3. [Resources](#resources)

## Quickstart

### Setting up the HackRF

If your HackRF is already configured, skip to [Verifying Successful HackRF Setup](#verifying-successful-hackrf-setup)

#### Installing HackRF Software

Follow the instructions for your OS at [this link](https://hackrf.readthedocs.io/en/latest/installing_hackrf_software.html).

For a generic Raspberry Pi:

```sh
sudo apt-get install hackrf
```
#### Updating HackRF Firmware

Instructions below pulled from [this link](https://hackrf.readthedocs.io/en/latest/updating_firmware.html#updating-firmware).

_"To update the firmware on a working HackRF One, use the hackrf_spiflash program:_

```sh
hackrf_spiflash -w hackrf_one_usb.bin
```
_You can find the firmware binary (hackrf_one_usb.bin) in the firmware-bin directory of the latest [release package](https://github.com/greatscottgadgets/hackrf/releases/latest) or you can compile your own from the [source](https://github.com/greatscottgadgets/hackrf/tree/master/firmware). For Jawbreaker, use hackrf_jawbreaker_usb.bin. If you compile from source, the file will be called hackrf_usb.bin._

_The hackrf_spiflash program is part of hackrf-tools._

_When writing a firmware image to SPI flash, be sure to select firmware with a filename ending in “.bin”._

_After writing the firmware to SPI flash, you may need to reset the HackRF device by pressing the RESET button or by unplugging it and plugging it back in._

_If you get an error that mentions HACKRF_ERROR_NOT_FOUND, it is often a permissions problem on your OS._"

#### Verifying Successful HackRF Setup

**TODO**: make a script to validate the hackrf commands

## Resources

- [Princeton's Labs](https://www.cs.princeton.edu/courses/archive/spring18/cos463/labs/Lab%201%20preview.html)
- [GSG Tutorials](https://greatscottgadgets.com/sdr/11/)