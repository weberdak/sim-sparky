#!/bin/bash

SIMSPARKY=/home/daniel/GitHub/sim-sparky

python $SIMSPARKY/sim_sparky.py \
       -i GB1_BMRB30088_CSV.dat \
       -o gb1_darr_allIntra \
       -t csv \
       -c C CA CA C CA CB CB CA CB CG CG CB CB CG1 CG1 CB CB CG2 CG2 CB CG CD1 CD1 CG CG CD2 CD2 CG CG CD CD CG CG1 CD CD CG1 CD1 CE1 CE1 CD1 CD2 CE2 CE2 CD2 CD CE CE CD C C CA CA CB CB CG CG CG1 CG1 CG2 CG2 CD CD CD1 CD1 CD2 CD2 CE CE CE1 CE1 CE2 CE2 \
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
       
