import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

# simple test - cycle through states S1 to S4, back to S1
datain_values = [  0, 0x7, 0x8, 0x1, 0x0 ]
alu_values =    [  0,   0, 0x7, 0xf, 0xf ]

# DUT requires the following inputs:
#   - clk
#   - reset
#   - ctl
#
# and outputs:
#   - alu (4 bits)
#   - cout
#

@cocotb.test()
async def test_alu_fsm(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.fork(clock.start())
    
    dut._log.info("reset")
    dut.reset.value = 1
    await ClockCycles(dut.clk, 10)
    dut.reset.value = 0
    dut.ctl.value = 1       # alters state machine on each clk cycle

    dut._log.info("check alu output values")
    for i in range(5):
        dut._log.info("check alu for cycle {}".format(i))
        await ClockCycles(dut.clk, 1)
        if i == 3:
            dut.ctl.value = 0       # on S4, want to go back to S1 (set ctl = 0)

        assert int(dut.alu.value) == alu_values[i]
