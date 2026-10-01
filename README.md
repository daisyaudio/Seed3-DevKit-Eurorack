# Seed3 Eurorack Dev Kit

<img width="100%" height="auto" alt="Seed3 Eurorack Dev Kit" src="https://github.com/user-attachments/assets/1924397b-ab87-4e53-9597-504e851d0727" />

## A Eurorack Module Platform for the Daisy Seed3

The Seed3 Eurorack Dev Kit is the premier development board for building your next Eurorack module on the Daisy platform. Create powerful effects, stunning sound sources, and complex utilities, all on a single board.

The Dev Kit carries a host of hardware parameters, including 8 potentiometers, jacks for CV, gate, MIDI, and stereo audio I/O, 2 toggle switches, 2 tactile buttons, and a microSD card reader for sample playback, file generation, and data transfer. Mountable in a standard 3U Eurorack case, the Dev Kit integrates straight into your development rig so you can fully realize your next big Eurorack project.

---

## Contents

- [Features](#features)
- [Specifications](#specifications)
- [Getting Started](#getting-started)
- [Making Your Own Project](#making-your-own-project)
- [Hardware Reference](#hardware-reference)
- [Resources & Support](#resources--support)
- [Open-Source Hardware](#open-source-hardware)
- [License](#license)

---

## Features

| Category | Details |
| --- | --- |
| **Format** | 3U Eurorack, 28HP |
| **Audio** | Stereo audio input and output (AC-coupled) |
| **MIDI** | 3.5mm TRS MIDI In, Out, and Thru |
| **CV & Gate** | 4 × CV inputs, 2 × gate inputs, 2 × CV outputs |
| **USB** | USB-C port connected to the Seed3's USB High Speed peripheral, for USB features in your firmware |
| **Storage** | microSD slot for sample playback, file generation, and data transfer |
| **Potentiometers** | 8 × 10kΩ linear (B-taper) |
| **Buttons** | 2 × tactile switches |
| **Toggle Switches** | 2 × toggle switches (1 × ON-OFF-ON, 1 × ON-ON) |
| **LEDs** | 1 × RGB LED, 1 × single-color LED |

## Specifications

| Parameter | Value |
| --- | --- |
| Processor module | Daisy Seed3 |
| Format | 3U Eurorack, 28HP |
| Power | 10-pin Eurorack power header (+12V / -12V) |
| Current draw | Firmware dependent |
| Reverse polarity protection | Yes |
| Module depth | PCB acts as front panel, can install in 3U space. 2mm behind rails. |
| Audio codec / sample rate | TAC5242 / up to 32-bit, 192kHz |
| Audio input impedance | 100kΩ |
| Audio output impedance | 100Ω |
| Audio level | 10Vpp nominal (Eurorack standard), with headroom up to about 20Vpp |
| CV input range | -5V to +5V |
| CV output range | 0V to +5V |
| Gate input threshold | +0.4V |
| MIDI connectors | 3 × 3.5mm TRS Type A (In, Out, Thru) |

> [!WARNING]
> Check the ribbon cable orientation before powering up. The red stripe marks -12V. Reverse power protection circuit is installed on the board.

## Getting Started

> [!IMPORTANT]
> This kit has two USB-C ports: one on the **Dev Kit board** (J7) and one on the **Seed3 module** itself. Program the template and read its serial output through the **Seed3's** USB-C port.

### 1. Install the toolchain

Follow the Daisy [C++ Getting Started guide](https://docs.daisy.audio/tutorials/cpp-dev-env/). It installs the toolchain and clones [DaisyExamples](https://github.com/daisyaudio/DaisyExamples), which includes [libDaisy](https://github.com/daisyaudio/libDaisy) (hardware library) and [DaisySP](https://github.com/daisyaudio/DaisySP) (DSP library).

### 2. Update libDaisy

The Eurorack Dev Kit template and board support are newer than the copy of libDaisy that DaisyExamples includes. From your `DaisyExamples` folder, update libDaisy to the latest version and rebuild it:

```bash
git submodule update --remote libDaisy
cd libDaisy
make
```

### 3. Build the template

The starting project for this kit is [`examples/devkits/Eurorack-DevKit-Template`](https://github.com/daisyaudio/libDaisy/tree/master/examples/devkits/Eurorack-DevKit-Template). From the `libDaisy` folder:

```bash
cd examples/devkits/Eurorack-DevKit-Template
make
```

This creates `Eurorack-DevKit-Template.bin` in the template's `build/` folder.

### 4. Flash the Seed3

1. Connect a USB-C cable from your computer to the USB-C port on the **Seed3 module**. The Seed3 is powered over USB while you flash, so the module doesn't need to be in a powered case.
2. Hold **BOOT**, press and release **RESET**, then release **BOOT**.
3. From the template folder, run:

   ```bash
   make program-dfu
   ```

   Or, in the [Daisy Web Programmer](https://flash.daisy.audio/), upload the `Eurorack-DevKit-Template.bin` file from the `build/` folder.

### 5. Power up and try it out

Mount the Dev Kit in a 3U Eurorack case and connect the Eurorack power ribbon to the power header (P1) with the red stripe on -12V. You can leave the Seed3's USB cable connected so you can watch the serial output.

The template:

- Passes audio from the inputs straight to the outputs.
- Cycles the colors of the RGB LED (LED1) and blinks LED2.
- Outputs a slow rising ramp on CV Out 1 and a falling ramp on CV Out 2 (about a 2.5-second period).
- Echoes MIDI notes received on MIDI In to MIDI Out.
- Prints the state of every control over USB serial on the Seed3's USB-C port. Open any serial monitor to see it.

## Making Your Own Project

Edits only take effect on the module after you rebuild and reflash, so start your own project from a copy of the template.

1. Copy the `Eurorack-DevKit-Template` folder into your `DaisyExamples` folder and rename it, for example `DaisyExamples/MyModule`.
2. In the copied `Makefile`:
   - Set `TARGET` to your project name, for example `TARGET = MyModule`.
   - Change `LIBDAISY_DIR` to point to libDaisy from the new location: `LIBDAISY_DIR = ../libDaisy`.
   - To use DaisySP, uncomment the DaisySP line and set `DAISYSP_DIR = ../DaisySP`.
3. Write your module in `src/main.cpp`. Audio is processed in `AudioCallback()`: inputs are `in[0][i]` (left) and `in[1][i]` (right), and outputs are `out[0][i]` and `out[1][i]` (see [Audio](#audio)).
4. Rebuild and flash after every change:

   ```bash
   make
   make program-dfu
   ```

   Put the Seed3 into BOOT mode (step 4 above) before each `make program-dfu`.

> [!TIP]
> The template builds with debugging enabled (`DEBUG = 1`, `OPT = -Og`). For release builds, set `DEBUG = 0` and `OPT = -O3` in the Makefile. If your program grows too large for the Seed3's internal flash, see the [Daisy Bootloader guide](https://docs.daisy.audio/tutorials/_a7_Getting-Started-Daisy-Bootloader/).

## Hardware Reference

The **Ref** column lists each part's reference designator, as printed on the board's silkscreen.

### Pinout

<img width="100%" height="auto" alt="Seed3 Eurorack Dev Kit pinout" src="https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed-3-euro/seed3-euro-dev-kit-pinout-dark.svg" />

A printable [Pinout PDF](https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed-3-euro/seed-3-euro-dev-kit-pinout.pdf) is also available.

### Audio

| Jack | Ref | Signal | Audio Callback |
| --- | --- | --- | --- |
| Input Left | J_AUDIO_IN_L1 | `AUDIO_IN_L` | `in[0][i]` |
| Input Right | J_AUDIO_IN_R1 | `AUDIO_IN_R` | `in[1][i]` |
| Output Left | J_AUDIO_OUT_L1 | `AUDIO_OUT_L` | `out[0][i]` |
| Output Right | J_AUDIO_OUT_R1 | `AUDIO_OUT_R` | `out[1][i]` |

> [!NOTE]
> Input Right is normalled to Input Left. With nothing patched into Input Right, a signal patched into Input Left feeds both channels.

### Potentiometers (8-channel multiplexer)

The eight pots are read through a single ADC pin via an 8-channel analog multiplexer (U12). Set the select lines A/B/C to choose a channel, then read `POT_MUX`.

| Signal | Seed3 Pin |
| --- | --- |
| `POT_MUX` (ADC) | D15 |
| `MUX_CTRL_A` | D24 |
| `MUX_CTRL_B` | D25 |
| `MUX_CTRL_C` | D26 |

| Pot | Ref | Mux Channel |
| --- | --- | --- |
| Potentiometer 1 | VR1 | `MUX_CH_0` |
| Potentiometer 2 | VR2 | `MUX_CH_1` |
| Potentiometer 3 | VR3 | `MUX_CH_2` |
| Potentiometer 4 | VR4 | `MUX_CH_3` |
| Potentiometer 5 | VR5 | `MUX_CH_4` |
| Potentiometer 6 | VR6 | `MUX_CH_5` |
| Potentiometer 7 | VR7 | `MUX_CH_6` |
| Potentiometer 8 | VR8 | `MUX_CH_7` |

### CV & Gates

| Jack | Ref | Signal | Seed3 Pin |
| --- | --- | --- | --- |
| CV In 1 | J_CV_IN_1 | `CV_1_ADC` | D18 |
| CV In 2 | J_CV_IN_2 | `CV_2_ADC` | D17 |
| CV In 3 | J_CV_IN_3 | `CV_3_ADC` | D16 |
| CV In 4 | J_CV_IN_4 | `CV_4_ADC` | D19 |
| Gate In 1 | J_GATE_IN_1 | `GPIO_GATEIN_1` | D10 |
| Gate In 2 | J_GATE_IN_2 | `GPIO_GATEIN_2` | D21 |
| CV Out 1 | J_CV_OUT_1 | `DAC_CV_1` | D23 (DAC channel 1) |
| CV Out 2 | J_CV_OUT_2 | `DAC_CV_2` | D22 (DAC channel 2) |

### Switches

| Switch | Ref | Signal | Seed3 Pin | Type |
| --- | --- | --- | --- | --- |
| Tactile switch 1 | SW1 | `TAC_SW1` | D0 | Momentary |
| Tactile switch 2 | SW2 | `TAC_SW2` | D20 | Momentary |
| Toggle switch 1 | SW3 | `TOG_2_A` / `TOG_2_B` | D27 / D7 | ON-OFF-ON (3-position, two pins) |
| Toggle switch 2 | SW4 | `TOG_1` | D12 | ON-ON |

### LEDs

| LED | Ref | Signal | Seed3 Pin |
| --- | --- | --- | --- |
| RGB LED — Red | LED1 | `LED_R` | D9 |
| RGB LED — Green | LED1 | `LED_G` | D28 |
| RGB LED — Blue | LED1 | `LED_B` | D8 |
| Single-color LED | LED2 | `LED_MONO_1` | D11 |

### MIDI

| Jack | Ref | Signal | Seed3 Pin | Direction |
| --- | --- | --- | --- | --- |
| MIDI Out | J_MIDI_OUT1 | `MIDI_TX` | D13 | Out |
| MIDI In | J_MIDI_IN1 | `MIDI_RX` | D14 | In |
| MIDI Thru | J_MIDI_THRU1 | `MIDI_RX` | D14 | Mirrors MIDI In |

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

The Dev Kit's USB-C port (J7) connects to the Seed3's USB High Speed peripheral. It is separate from the USB-C port on the Seed3 module, which is used for programming and for the template's serial output. The module is powered from the Eurorack power header (P1), not from USB.

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
- [KiCad Design Files](https://github.com/daisyaudio/ES-Seed3-DevKit-Eurorack/releases/latest)

---

## Open-Source Hardware

<img width="256px" height="auto" alt="Open Source Hardware logo" src="https://github.com/user-attachments/assets/f9264744-3509-4cf0-9f4a-981cb05eb38e" />

The Eurorack Dev Kit is open-source hardware, built to the [Open Source Hardware Definition](https://www.oshwa.org/definition/) published by the Open Source Hardware Association (OSHWA). The schematics, PCB layouts, bill of materials, and KiCad source files are published so that you can study, modify, manufacture, and sell your own designs based on them.

## License

Copyright © 2026 Qu-Bit Electronix, Inc. (dba Daisy)

The hardware design files in this repository are licensed under the **CERN Open Hardware Licence Version 2 – Permissive** ([CERN-OHL-P-2.0](https://ohwr.org/cern_ohl_p_v2.pdf)).

Subject to the terms of that licence, you may:

- Use, study, copy, modify, and distribute these designs and any products made from them.
- Incorporate these designs, in whole or in part, into closed-source and commercial products.

When you redistribute these designs or products made from them, you must:

- Retain all copyright, licence, and other notices contained in the source files.
- Add a notice to any modified source stating that you modified it, with the date and a brief description of the change.
- Ensure that recipients of any product made from these designs have access to the applicable notices.

These designs are provided "as is", without warranty of any kind, express or implied. See [LICENSE](LICENSE.txt) for the full licence text, including the disclaimer of warranty and limitation of liability.

Firmware and software, including [libDaisy](https://github.com/daisyaudio/libDaisy) and [DaisySP](https://github.com/daisyaudio/DaisySP), are licensed separately under the terms included in their respective repositories.

SPDX-License-Identifier: CERN-OHL-P-2.0

### Trademarks

DAISY® is a trademark of Qu-Bit Electronix, Inc., registered in the United States. CERN-OHL-P-2.0 grants a license to the copyright and related rights in these designs. It does not grant any right or license to use the DAISY name, logos, product names, or other trademarks of Qu-Bit Electronix, Inc.

Products, derivative designs, and related materials made from these designs may not:

- Use the DAISY name or logo, or any confusingly similar name or mark, in a product name, model number, brand, domain name, or marketing material.
- Reproduce the DAISY name or logo on a PCB silkscreen, front panel, enclosure, packaging, or documentation, except where needed to keep the required licence notices.
- State or imply that the product is made, endorsed, sponsored, certified, or supported by Qu-Bit Electronix, Inc.

You may make truthful, factual statements about compatibility or origin, such as "based on the Seed3 Eurorack Dev Kit design" or "compatible with the Daisy Seed3", provided the statement does not suggest affiliation or endorsement. If you redistribute or sell products derived from these designs, remove the DAISY name and logo from the silkscreen and other artwork before manufacture.

For trademark licensing or permission requests, contact Qu-Bit Electronix, Inc. through [daisy.audio/pages/support](https://daisy.audio/pages/support).
