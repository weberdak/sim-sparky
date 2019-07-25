#!/bin/bash

SIMSPARKY=/home/daniel/GitHub/sim-sparky

python $SIMSPARKY/sim_sparky.py \
       -i GB1_BMRB30088_CSV.dat \ 
       -o gb1_hsqc \
       -t csv \
       -c H N HD21 ND2 HD22 ND2 HE21 NE2 HE22 NE2 HE1 NE1 \
       -s 0 \
       --nuc1_label 1H \
       --nuc2_label 15N \
       --nuc1_freq 600.0000000 \
       --nuc2_freq 60.7639142 \
       --nuc1_center 8.30 \
       --nuc2_center 120.00 \
       --nuc1_sw 8.00 \
       --nuc2_sw 40.00 \
       --nuc1_size 1024 \
       --nuc2_size 1024
       
