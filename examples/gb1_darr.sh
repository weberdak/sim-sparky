#!/bin/bash

SIMSPARKY=/home/daniel/GitHub/sim-sparky

python $SIMSPARKY/sim_sparky.py \
       -i GB1_BMRB30088_CSV.dat \
       -o gb1_darr \
       -t csv \
       -c C CA C CB CA CB CA C CB C CB CA C C CA CA CB CB \
       -s 0 \
       --nuc1_label 13C \
       --nuc2_label 13C \
       --nuc1_freq 150.903 \
       --nuc2_freq 150.903 \
       --nuc1_center 100.00 \
       --nuc2_center 100.00 \
       --nuc1_sw 200.00 \
       --nuc2_sw 200.00 \
       --nuc1_size 1024 \
       --nuc2_size 1024
       
