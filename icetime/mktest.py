#!/usr/bin/env python3

import sys, os, shutil
import numpy as np

pins = np.random.permutation("""
    1 2 3 4 7 8 9 10 11 12 19 22 23 24 25 26 28 29 31 32 33 34
    37 38 41 42 43 44 45 47 48 52 56 58 60 61 62 63 64
    73 74 75 76 78 79 80 81 87 88 90 91 95 96 97 98 101 102 104 105 106 107
    112 113 114 115 116 117 118 119 120 121 122 134 135 136 137 138 139 141 142 143 144
""".split())

io_names = None
mode = "test0" # sys.argv[1]

with open("%s.v" % sys.argv[1], "w") as f:
    if mode == "test0":
        io_names = [ "clk", "i0", "o0", "o1", "o2" ]
        print("module top(input clk, i0, output o0, o1, o2);", file=f)
        print("  reg [31:0] state;", file=f)
        print("  always @(posedge clk) state <= ((state << 5) + state) ^ i0;", file=f)
        print("  assign o0 = ^state, o1 = |state, o2 = state[31:16] + state[15:0];", file=f)
        print("endmodule", file=f)
    if mode == "test1":
        io_names = [ "clk", "i0", "i1", "i2", "i3", "o0", "o1", "o2", "o3" ]
        print("module top(input clk, i0, i1, i2, i3, output o0, o1, o2, o3);", file=f)
        print("  reg [15:0] din, dout;", file=f)
        print("  always @(posedge clk) din <= {din, i3, i2, i1, i0};", file=f)
        print("  always @(posedge clk) dout <= din + {din[7:0], din[15:8]};", file=f)
        print("  assign {o3, o2, o1, o0} = dout >> din;", file=f)
        print("endmodule", file=f)

with open("%s.pcf" % sys.argv[1], "w") as f:
    for i, name in enumerate(io_names):
        print("set_io %s %s" % (name, pins[i]), file=f)

with open("%s.ys" % sys.argv[1], "w") as f:
    print("echo on", file=f)
    print("read_verilog -lib cells.v", file=f)
    print("read_verilog %s_ref.v" % sys.argv[1], file=f)
    print("read_verilog %s_out.v" % sys.argv[1], file=f)
    print("prep", file=f)
    print("equiv_make top chip equiv", file=f)
    print("check -assert", file=f)
    print("cd equiv", file=f)
    print("script %s.lc" % sys.argv[1], file=f)
    print("rename -hide w:N_*", file=f)
    print("equiv_struct", file=f)
    print("opt_clean -purge", file=f)
    print("write_ilang %s.il" % sys.argv[1], file=f)
    print("equiv_status -assert", file=f)

assert os.system("bash ../icefuzz/icecube.sh %s.v" % sys.argv[1]) == 0
os.rename("%s.v" % sys.argv[1], "%s_in.v" % sys.argv[1])

with open("%s_ref.v" % sys.argv[1], "w") as f:
    for line in open("%s.vsb" % sys.argv[1], "r"):
        zspan_hack = False

        line = line.replace(" Span4Mux_s0_h ",   " Span4Mux_h0 "  if zspan_hack else " Span4Mux_h0 ")
        line = line.replace(" Span4Mux_s1_h ",   " Span4Mux_h0 "  if zspan_hack else " Span4Mux_h1 ")
        line = line.replace(" Span4Mux_s2_h ",   " Span4Mux_h0 "  if zspan_hack else " Span4Mux_h2 ")
        line = line.replace(" Span4Mux_s3_h ",   " Span4Mux_h0 "  if zspan_hack else " Span4Mux_h3 ")
        line = line.replace(" Span4Mux_h ",      " Span4Mux_h0 "  if zspan_hack else " Span4Mux_h4 ")

        line = line.replace(" Span4Mux_s0_v ",   " Span4Mux_v0 "  if zspan_hack else " Span4Mux_v0 ")
        line = line.replace(" Span4Mux_s1_v ",   " Span4Mux_v0 "  if zspan_hack else " Span4Mux_v1 ")
        line = line.replace(" Span4Mux_s2_v ",   " Span4Mux_v0 "  if zspan_hack else " Span4Mux_v2 ")
        line = line.replace(" Span4Mux_s3_v ",   " Span4Mux_v0 "  if zspan_hack else " Span4Mux_v3 ")
        line = line.replace(" Span4Mux_v ",      " Span4Mux_v0 "  if zspan_hack else " Span4Mux_v4 ")
        line = line.replace(" Span4Mux ",        " Span4Mux_v0 "  if zspan_hack else " Span4Mux_v4 ")

        line = line.replace(" Span12Mux_s0_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h0 ")
        line = line.replace(" Span12Mux_s1_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h1 ")
        line = line.replace(" Span12Mux_s2_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h2 ")
        line = line.replace(" Span12Mux_s3_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h3 ")
        line = line.replace(" Span12Mux_s4_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h4 ")
        line = line.replace(" Span12Mux_s5_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h5 ")
        line = line.replace(" Span12Mux_s6_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h6 ")
        line = line.replace(" Span12Mux_s7_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h7 ")
        line = line.replace(" Span12Mux_s8_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h8 ")
        line = line.replace(" Span12Mux_s9_h ",  " Span12Mux_h0 " if zspan_hack else " Span12Mux_h9 ")
        line = line.replace(" Span12Mux_s10_h ", " Span12Mux_h0 " if zspan_hack else " Span12Mux_h10 ")
        line = line.replace(" Span12Mux_s11_h ", " Span12Mux_h0 " if zspan_hack else " Span12Mux_h11 ")
        line = line.replace(" Span12Mux ",       " Span12Mux_h0 " if zspan_hack else " Span12Mux_h12 ")

        line = line.replace(" Span12Mux_s0_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v0 ")
        line = line.replace(" Span12Mux_s1_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v1 ")
        line = line.replace(" Span12Mux_s2_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v2 ")
        line = line.replace(" Span12Mux_s3_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v3 ")
        line = line.replace(" Span12Mux_s4_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v4 ")
        line = line.replace(" Span12Mux_s5_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v5 ")
        line = line.replace(" Span12Mux_s6_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v6 ")
        line = line.replace(" Span12Mux_s7_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v7 ")
        line = line.replace(" Span12Mux_s8_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v8 ")
        line = line.replace(" Span12Mux_s9_v ",  " Span12Mux_v0 " if zspan_hack else " Span12Mux_v9 ")
        line = line.replace(" Span12Mux_s10_v ", " Span12Mux_v0 " if zspan_hack else " Span12Mux_v10 ")
        line = line.replace(" Span12Mux_s11_v ", " Span12Mux_v0 " if zspan_hack else " Span12Mux_v11 ")
        line = line.replace(" Span12Mux_v ",     " Span12Mux_v0 " if zspan_hack else " Span12Mux_v12 ")

        f.write(line)

assert os.system("yosys -qp 'select -write %s.lc t:LogicCell40' %s_ref.v" % (sys.argv[1], sys.argv[1])) == 0
assert os.system(r"sed -i -r 's,.*/(.*)LC_(.*),equiv_add -cell \1LC_\2_gold lc40_\2_gate,' %s.lc" % sys.argv[1]) == 0

os.remove("%s.bin" % sys.argv[1])
os.remove("%s.vsb" % sys.argv[1])
os.remove("%s.glb" % sys.argv[1])
os.remove("%s.psb" % sys.argv[1])
os.remove("%s.sdf" % sys.argv[1])
shutil.rmtree("%s.tmp" % sys.argv[1])

