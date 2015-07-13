#!/bin/sh


TRAIN=50
declare -a algos=("FHMM" "CO" "Hart")
num_algos=${#algos[@]}
for ((N_STATES=2; N_STATES<5; N_STATES+=1))
    do
    for ((K=3;K<7;K+=1))
        do
        for((ii=0;ii<$num_algos;ii+=1))
            do
            algo=${algos[$ii]}
            OFILE=../../../results/hvac/sweep_results/N${N_STATES}_K${K}_T${TRAIN}_"$algo".out
            EFILE=../../../results/hvac/sweep_results/N${N_STATES}_K${K}_T${TRAIN}_"$algo".err

            SLURM_SCRIPT=N${N_STATES}_K${K}_T${TRAIN}.pbs
            python ../../hvac/disaggregate_hvac.py ~/wikienergy-2013.h5 '$N_STATES' '$K' '$TRAIN' '$algo' >$OFILE 2>&1 &

            done
        done
    done




