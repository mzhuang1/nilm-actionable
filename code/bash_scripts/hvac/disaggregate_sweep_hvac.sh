#!/bin/sh


source ~/.bashrc
TRAIN=50
declare -a algos=("FHMM")
#declare -a algos=("FHMM" "CO" "Hart")
num_algos=${#algos[@]}
for ((N_STATES=2; N_STATES<5; N_STATES+=1))
    do
    for ((K=3;K<7;K+=1))
        do
        for((ii=0;ii<$num_algos;ii+=1))
            do
            for((group=0;group<21;group+=1))
                algo=${algos[$ii]}
                OFILE=../../../results/hvac/sweep_results/N${N_STATES}_K${K}_T${TRAIN}_"$algo"_G${group}.out
                EFILE=../../../results/hvac/sweep_results/N${N_STATES}_K${K}_T${TRAIN}_"$algo"_G${group}.err

                SLURM_SCRIPT=N${N_STATES}_K${K}_T${TRAIN}.pbs
                CMD='python ../../hvac/disaggregate_hvac.py ~/wikienergy-2013.h5 '$N_STATES' '$K' '$TRAIN' '$algo' '$group''
                echo $CMD

                #rm ${SLURM_SCRIPT}
                echo "#!/bin/sh" > ${SLURM_SCRIPT}
                #echo $pwd > ${SLURM_SCRIPT}
                echo '#SBATCH --time=1-02:0:00' >> ${SLURM_SCRIPT}
                echo '#SBATCH --mem=16' >> ${SLURM_SCRIPT}
                echo '#SBATCH -o "./'${OFILE}'"' >> ${SLURM_SCRIPT}
                echo '#SBATCH -e "./'${EFILE}'"' >> ${SLURM_SCRIPT}
                #echo 'cd $SLURM_SUBMIT_DIR' >> ${SLURM_SCRIPT}
                echo ${CMD} >> ${SLURM_SCRIPT}

                #cat ${SLURM_SCRIPT}
                sbatch ${SLURM_SCRIPT}
            done
        done
    done




