# Desk Buddy

A small desk companion robot with an animated face, built with MicroPython on an ESP32-S3 microcontroller and a 1.3" OLED screen.

## Features
- Eyes that blink and glance around
- Expressions: neutral, happy, sleepy, surprised
- Random happy moments
- Sleepy after 23:30
- Internet clock and date (synced over Wi-Fi)
- BOOT button switches between eyes, clock and date

## Hardware
- ESP32-S3 (N16R8)
- 1.3" SH1106 OLED (I2C)
- Female-to-female jumper wires

## Wiring
| OLED | ESP32-S3 |
|------|----------|
| VCC  | 3V3      |
| GND  | GND      |
| SCK  | 9        |
| SDA  | 8        |

