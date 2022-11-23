![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg)

# Project Description
This project is a rather simplified 4-bit ALU inspired by the 2022 Supercon Badge.
The challenge was to do this within the constraints of the Tiny Tapeout submission.

A typical 4-bit ALU needs 12 pins just to handle the two input ports and an output port.
Additional pins would be needed for control. It might also have outputs for a carry-out
and a zero-detect. So it's easy to imagine a need for at least 10 inputs (assuming 2 input pins to control the ALU mode)
and 6 outputs (assuming an ALU result, carry-out, and a zero-detect).

Tiny Tapeout (TT02) is limited to 8 inputs and 8 outputs!

To work around these constraints, we surround the ALU with some registers.
There is an A register and a B register for the A and B inputs of the ALU.
There is also a Mode register to set the ALU mode (i.e. add or subtract).
We then add a state machine to allow selectively loading those registers.
However, the output of the ALU goes directly to the chip-designated outputs.

Currently, only two ALU operations are supported, ADD and SUB.

That's it!

=====

# What is Tiny Tapeout?

TinyTapeout is an educational project that aims to make it easier and cheaper than ever to get your digital designs manufactured on a real chip!

Go to https://tinytapeout.com for instructions!

## How to change the Wokwi project

Edit the [info.yaml](info.yaml) and change the wokwi_id to match your project.

## How to enable the GitHub actions to build the ASIC files

Please see the instructions for:

* [Enabling GitHub Actions](https://tinytapeout.com/faq/#when-i-commit-my-change-the-gds-action-isnt-running)
* [Enabling GitHub Pages](https://tinytapeout.com/faq/#my-github-action-is-failing-on-the-pages-part)

## How does it work?

When you edit the info.yaml to choose a different ID, the [GitHub Action](.github/workflows/gds.yaml) will fetch the digital netlist of your design from Wokwi.

After that, the action uses the open source ASIC tool called [OpenLane](https://www.zerotoasiccourse.com/terminology/openlane/) to build the files needed to fabricate an ASIC.

## Resources

* [FAQ](https://tinytapeout.com/faq/)
* [Digital design lessons](https://tinytapeout.com/digital_design/)
* [Join the community](https://discord.gg/rPK2nSjxy8)

## What next?

* Share your GDS on Twitter, tag it [#tinytapeout](https://twitter.com/hashtag/tinytapeout?src=hashtag_click) and [link me](https://twitter.com/matthewvenn)!
