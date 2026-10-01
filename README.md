# Seed3 Eurorack Dev Kit

<img width="100%" height="auto" alt="seed3-eurorack-dev-kit-transparent" src="https://github.com/user-attachments/assets/1924397b-ab87-4e53-9597-504e851d0727" />


## A Eurorack Module Platform for the Daisy Seed3

The Seed3 Eurorack Dev Kit is the premier development board for building your next Eurorack module on the Daisy platform. Create powerful effects, stunning sound sources, and complex utilities, all on a single board.

The Dev Kit carries a host of hardware parameters, including 8 potentiometers, jacks for CV, gate, MIDI, and stereo audio I/O, 2 toggle switches, 2 tactile buttons, and a microSD card reader for sample playback, file generation, and data transfer. Mountable in a standard 3U Eurorack case, the Dev Kit integrates straight into your development rig so you can fully realize your next big Eurorack project.

---

## Contents

- [Features](#features)
- [Specifications](#specifications)
- [Getting Started](#getting-started)
- [Hardware Reference](#hardware-reference)
- [Resources & Support](#resources--support)
- [Open-Source Hardware](#open-source-hardware)
- [License](#license)

---

## Features

| Category | Details |
| --- | --- |
| **Format** | 3U Eurorack, 28 HP |
| **Audio** | Stereo audio input and output (AC-coupled) |
| **MIDI** | MIDI In, Out, and Thru |
| **CV & Gate** | 4 × CV inputs, 2 × gate inputs, 2 × CV outputs |
| **USB** | USB-C port |
| **Storage** | microSD slot for sample playback, file generation, and data transfer |
| **Potentiometers** | 8 × potentiometers 10 kΩ linear (B-taper) |
| **Buttons** | 2 × tactile switches |
| **Toggle Switches** | 2 × toggle switches |

## Specifications

| Parameter | Value |
| --- | --- |
| Processor module | Daisy Seed3 |
| Format | 3U Eurorack, 28 HP |
| Power | 10-pin Eurorack Power Connector |
| Current draw | firmware dependent |
| Module depth | PCB acts as front panel, can install in 3U space. 2 mm behind rails. |
| Audio codec / sample rate | TAC5242 / up to 32-bit, 192kHz |
| Audio input impedance | 100KΩ |
| Audio output impedance | 100Ω |
| Audio level | 10Vpp |
| CV input range | -5V to +5V |
| CV output range | 0V to +5V |
| Gate input threshold | +0.4V |
| MIDI connectors | In, Out, and Thru (3.5 mm TRS Type A) |

> [!WARNING]
> Check the ribbon cable orientation before powering up. The red stripe marks −12 V. Reverse power protection circuit is installed on the board.

## Getting Started

### 1. Set up the toolchain

Install the Daisy toolchain and clone the libraries by following the setup guide at [docs.daisy.audio](https://docs.daisy.audio).

- [libDaisy](https://github.com/electro-smith/libDaisy) — hardware abstraction library
- [DaisySP](https://github.com/electro-smith/DaisySP) — DSP library

### 2. Build the template

A ready-to-go starting project for the Eurorack Dev Kit lives in libDaisy at
[`examples/devkits/Eurorack-DevKit-Template`](https://github.com/daisyaudio/libDaisy/tree/master/examples/devkits/Eurorack-DevKit-Template).

```bash
git clone --recurse-submodules https://github.com/daisyaudio/libDaisy
cd libDaisy
make
cd examples/devkits/Eurorack-DevKit-Template
make
```

Copy the template folder to start your own module, then edit the audio callback. Inputs are `in[0][i]` (left) and `in[1][i]` (right), and outputs are `out[0][i]` and `out[1][i]` (see [Audio](#audio)).

### 3. Flash the Seed3

Connect the Dev Kit to your computer over USB-C, put the Seed3 into bootloader mode, then flash:

```bash
make program-dfu
```

### 4. Power up

Mount the Dev Kit in a 3U Eurorack case, connect the Eurorack power ribbon with the red stripe on −12 V, then patch in your audio, CV, gate, and MIDI connections.

## Hardware Reference

### Pinout

<img width="100%" height="auto" alt="Seed3 Eurorack Dev Kit pinout" src="https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed-3-euro/seed3-euro-dev-kit-pinout-dark.svg" />

A printable [Pinout PDF](https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed-3-euro/seed-3-euro-dev-kit-pinout.pdf) is also available.

### Audio

| Jack | Signal | Audio Callback |
| --- | --- | --- |
| Input Left | `AUDIO_IN_L` | `in[0][i]` |
| Input Right | `AUDIO_IN_R` | `in[1][i]` |
| Output Left | `AUDIO_OUT_L` | `out[0][i]` |
| Output Right | `AUDIO_OUT_R` | `out[1][i]` |

### Potentiometers (8-channel multiplexer)
 
The eight pots are read through a single ADC pin via an 8-channel analog multiplexer. Set the select lines A/B/C to choose a channel, then read `POT_MUX`.
 
| Signal | Seed3 Pin |
| --- | --- |
| `POT_MUX` (ADC) | D15 |
| `MUX_CTRL_A` | D24 |
| `MUX_CTRL_B` | D25 |
| `MUX_CTRL_C` | D26 |
 
| Pot | Mux Channel |
| --- | --- |
| VR1 | `MUX_CH_0` |
| VR2 | `MUX_CH_1` |
| VR3 | `MUX_CH_2` |
| VR4 | `MUX_CH_3` |
| VR5 | `MUX_CH_4` |
| VR6 | `MUX_CH_5` |
| VR7 | `MUX_CH_6` |
| VR8 | `MUX_CH_7` |

### CV & Gates

| Jack | Signal | Seed3 Pin |
| --- | --- | --- |
| CV In 1 | `CV_1_ADC` | D18 |
| CV In 2 | `CV_2_ADC` | D17 |
| CV In 3 | `CV_3_ADC` | D16 |
| CV In 4 | `CV_4_ADC` | D19 |
| Gate In 1 | `GPIO_GATEIN_1` | D10 |
| Gate In 2 | `GPIO_GATEIN_2` | D21 |
| CV Out 1 | `DAC_CV_1` | D22 |
| CV Out 2 | `DAC_CV_2` | D23 |

### Switches

| Switch | Signal | Seed3 Pin | Type |
| --- | --- | --- | --- |
| Tactile switch 1 | `TAC_SW1` | D0 | Momentary |
| Tactile switch 2 | `TAC_SW2` | D20 | Momentary |
| Toggle switch 1 | `TOG_2_A` / `TOG_2_B` | D27 / D7 | ON-OFF-ON (3-position, two pins) |
| Toggle switch 2 | `TOG_1` | D12 | ON-ON |

### MIDI

| Jack | Signal | Seed3 Pin | Direction |
| --- | --- | --- | --- |
| MIDI Out | `MIDI_TX` | D13 | Out |
| MIDI In | `MIDI_RX` | D14 | In |
| MIDI Thru | `MIDI_RX` | D14 | Mirrors MIDI In |

### microSD (SDMMC, 4-bit)

| Signal | Seed3 Pin |
| --- | --- |
| `SDMMC_CK` | D6 |
| `SDMMC_CMD` | D5 |
| `SDMMC_D0` | D4 |
| `SDMMC_D1` | D3 |
| `SDMMC_D2` | D2 |
| `SDMMC_D3` | D1 |

### USB-C

| Signal | Seed3 Pin |
| --- | --- |
| `USB_OTG_HS_N` | D29 |
| `USB_OTG_HS_P` | D30 |

## Resources & Support

- **Product Page:** [Seed3 Eurorack Dev Kit](https://daisy.audio/products/seed-3-eurorack-dev-kit)
- **Documentation:** [docs.daisy.audio](https://docs.daisy.audio/product/Seed3-Euro-Dev-Kit/)
- **Community Forum:** [community.daisy.audio](https://community.daisy.audio)
- **Discord:** [Daisy Discord](https://discord.gg/ByHBnMtQTR)
- **Issues:** Report bugs or hardware errata via this repository's [Issues](../../issues) tab.

### Design Files

- [Schematic (PDF)](https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed-3-euro/Seed3-DevKit-Eurorack-Rev3.pdf)
- [Bill of Materials (CSV)](https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed-3-euro/Seed3-DevKit-Eurorack_Rev3-bom.csv)
- [Pinout (PDF)](https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed-3-euro/seed-3-euro-dev-kit-pinout.pdf)
- [KiCad Design Files](https://github.com/electro-smith/ES-Seed3-DevKit-Eurorack/releases/latest)

---

## Open-Source Hardware

<img width="256px" height="auto" alt="Open Source Hardware logo" src="https://github.com/user-attachments/assets/f9264744-3509-4cf0-9f4a-981cb05eb38e" />

The Eurorack Dev Kit is open-source hardware, built to the [Open Source Hardware Definition](https://www.oshwa.org/definition/) published by the Open Source Hardware Association (OSHWA). The schematics, PCB layouts, bill of materials, and KiCad source files are published so that you can study, modify, manufacture, and sell your own designs based on them.

## License

The hardware design files in this repository are licensed under the **CERN Open Hardware Licence Version 2 – Permissive** ([CERN-OHL-P-2.0](https://ohwr.org/cern_ohl_p_v2.pdf)).

Subject to the terms of that licence, you may:

- Use, study, copy, modify, and distribute these designs and any products made from them.
- Incorporate these designs, in whole or in part, into closed-source and commercial products.

When you redistribute these designs or products made from them, you must:

- Retain all copyright, licence, and other notices contained in the source files.
- Add a notice to any modified source stating that you modified it, with the date and a brief description of the change.
- Ensure that recipients of any product made from these designs have access to the applicable notices.

These designs are provided "as is", without warranty of any kind, express or implied. See [LICENSE](https://github.com/user-attachments/files/32935889/LICENSE.txt) for the full licence text, including the disclaimer of warranty and limitation of liability.

Firmware and software, including [libDaisy](https://github.com/electro-smith/libDaisy) and [DaisySP](https://github.com/electro-smith/DaisySP), are licensed separately under the terms included in their respective repositories.

SPDX-License-Identifier: CERN-OHL-P-2.0

### Trademarks

DAISY® is a trademark of Qu-Bit Electronix, Inc., registered in the United States. CERN-OHL-P-2.0 grants a license to the copyright and related rights in these designs. It does not grant any right or license to use the DAISY name, logos, product names, or other trademarks of Qu-Bit Electronix, Inc.

Products, derivative designs, and related materials made from these designs may not:

- Use the DAISY name or logo, or any confusingly similar name or mark, in a product name, model number, brand, domain name, or marketing material.
- Reproduce the DAISY name or logo on a PCB silkscreen, front panel, enclosure, packaging, or documentation, except where needed to keep the required licence notices.
- State or imply that the product is made, endorsed, sponsored, certified, or supported by Qu-Bit Electronix, Inc.

You may make truthful, factual statements about compatibility or origin, such as "based on the Seed3 Pedal Dev Kit design" or "compatible with the Daisy Seed3", provided the statement does not suggest affiliation or endorsement. If you redistribute or sell products derived from these designs, remove the DAISY name and logo from the silkscreen and other artwork before manufacture.

For trademark licensing or permission requests, contact Qu-Bit Electronix, Inc. through [daisy.audio/pages/support](https://daisy.audio/pages/support).

© 2026 Qu-Bit Electronix, Inc. (dba Daisy)
