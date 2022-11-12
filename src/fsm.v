`default_nettype none

//
// fsm.sv - state machine (controller) for ALU logic and registers
//
// note: reset, clk included.
//

module alu_fsm(ctl, curstate, rst_out, enA, enB, enM, enC, selC, reset, clk);

  input wire ctl;
  output [2:0] curstate; // expose fsm state for debug only
  output reg rst_out;
  output reg enA, enB, enM, enC;
  output reg selC;

  input wire reset;
  input wire clk;
  
  localparam S0 = 3'b000;
  localparam S1 = 3'b001;
  localparam S2 = 3'b010;
  localparam S3 = 3'b011;
  localparam S4 = 3'b100;
  localparam S5 = 3'b101;
  
  reg [2:0] state, nextstate;	// our state bits
  
  assign curstate = state;	// output current state bits
  
    
  // comb. logic for state machine
  always @(state, ctl) begin

	// defaults
    rst_out = 0;  // normal operation
    enA = 0;
    enB = 0;
	enM = 0;
    enC = 0;

    case (state)
      
      S0: begin
        rst_out = 1;  // in state S0, reset all regs

        if (ctl)
          nextstate = S1;
        else
          nextstate = S0;
      end

      S1: begin		// alu op

        if (ctl)
          nextstate = S2;
        else
          nextstate = S0;
      end

      S2: begin		// load A
		enA = 1;

        if (ctl)
          nextstate = S3;
        else
          nextstate = S1;
      end

      S3: begin		// load B
		enB = 1;
 
        if (ctl)
          nextstate = S4;
        else
          nextstate = S1;
      end

      S4: begin		// load M
		enM = 1;

        if (ctl)
          nextstate = S5;
        else
          nextstate = S1;
      end

      S5: begin		// load C
		enC = 1;
      	nextstate = S1;	// always back to S1
      end

    endcase
  end
  
  // 3-bit state machine

  always @(posedge clk or posedge reset) begin
    if (reset) begin
      state <= S0;		// reset state
    
    end else begin
      state <= nextstate;

    end

  end

endmodule


// 4-bit ALU inspired by Supercon.6 badge
//
// inputs:
//	op - alu operation
//	a, b - 4-bit ALU inputs
//	out - 4-bit ALU output
//	z - zero status (set if zero detected)
//	cout - carry out (set if overflow)
//	outEn - enable output (tristate otherwise)
//
// outputs:
// sel(decides if a branch should happen)
//
// notes:
//	- this has no state, just "gates"
//
module alu_4(op, a, b, cin, out, z, cout, outEn);
  
  input op;			// op=0 add, op=1 sub
  input [3:0] a, b;
  input cin;
  output [3:0] out;
  output z;
  output cout;			// carry out
  input outEn;		// set to enable output

  wire [3:0] f;		// alu result
  wire co;
  
  assign {co,f} = (op == 1)? a - b : a + b;

  assign z = ~(|f);	// zero flag: "or" all bits of f

  assign cout = co;	// carry out flag

  assign out = (outEn)? f : 4'bz;
  
endmodule


//
//  a simple 4-bit register, 
//	which can be connected to a bus.
//  note: this has a cEn pin to allow selective clocking
//
module flop_4(
  input [3:0] dd,		// in
  output tri [3:0] qq,	// out
  input qEn,			// output en
  input reset,			// reset (async)
  input cEn,            // clk enable
  input clk				// clk
  );

  reg [3:0] mem;	// our state bits
  
  assign qq = (qEn) ? mem : 4'bz;	// allows tristate output
  
  // this is an 4-bit "d" flip flop

  always @(posedge clk or posedge reset) begin
    if (reset)
      mem <= 4'b0000;		// clear on reset
    else begin
      if (cEn) begin
        mem <= dd;
        //$display("** %g flop_4: latched 0x%h", $time, dd);
      end
    end
  end

endmodule


// borrowed from tiny tapeout cell library (mux_cell)
module mux_1 (
    input wire a,
    input wire b,
    input wire sel,
    output wire out
    );

    assign out = sel ? b : a;
endmodule
