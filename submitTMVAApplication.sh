#!/bin/bash

#BDTlist=("BDT")
#varListKeys=()
shiftList=("nominal" "JECup" "JECdown" "JERup" "JERdown")
#
#for ind in `seq 40 10 51`; do
#    varListKeys="${varListKeys} SepRank6j73vars2017year${ind}top"
#done

note="_6j_year2017"
mDepth=2
#for BDT in ${BDTlist[@]}; do
#    for varListKey in ${varListKeys[@]}; do
#        numVars=${varListKey: -5:2}
#        BDTconfigStr=${BDT}_${varListKey}_${numVars}vars_mDepth${mDepth}${note}
#	for sft in ${shiftList[@]}; do
#	    echo "python -u doCondorApplication.py ${sft} ${BDT} ${varListKey} ${BDTconfigStr} "
#	    python -u doCondorApplication.py ${sft} ${BDT} ${varListKey} ${BDTconfigStr}
#	    sleep 1
#	done 
#    done
#done

## only loop shift
BDT=BDT
varListKey=SepRank6j73vars2017year 
numVars=73
for sft in ${shiftList[@]}; do
    BDTconfigStr=${BDT}_${varListKey}_${numVars}vars_mDepth${mDepth}${note}
    python -u doCondorApplication.py ${sft} ${BDT} ${varListKey} ${BDTconfigStr}
done

echo "---submit DONE---"
