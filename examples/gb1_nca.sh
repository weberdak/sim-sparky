#!/bin/bash

SIMSPARKY=/home/daniel/GitHub/sim-sparky

python3 $SIMSPARKY/sim_sparky.py \
       -i GB1_BMRB30088_CSV.dat \
       -o gb1_nca \
       -t csv \
       -c CA N \
       -s 0 \
       --nuc1_label 13C \
       --nuc2_label 15N \
       --nuc1_freq 150.903 \
       --nuc2_freq 60.834 \
       --nuc1_center 57.50 \
       --nuc2_center 120.00 \
       --nuc1_sw 40.00 \
       --nuc2_sw 40.00 \
       --nuc1_size 1024 \
       --nuc2_size 1024
       
