`default_nettype none
`timescale 1ns/1ps

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

module tb (
    // testbench is controlled by test.py
    input clk,
    input rst,
    input ctl,
    input [3:0] datain,
    output [3:0] alu,
    output cout
   );

    // this part dumps the trace to a vcd file that can be viewed with GTKWave
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    // wire up the inputs and outputs
    //wire [7:0] inputs = {datain[3:0], 1'b0, ctl, rst, clk};
    wire [7:0] inputs = {clk, rst, ctl, 1'b0, datain[3:0]};
    wire [7:0] outputs;

    assign alu = outputs[3:0];
    assign cout = outputs[4];

    // instantiate the DUT
    rolfmobile99_alu_fsm_top alu_fsm_top(
        .io_in  (inputs),
        .io_out (outputs)
        );

endmodule
