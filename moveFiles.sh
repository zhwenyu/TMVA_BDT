#!/bin/bash

PATH_ORIGIN=/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2021_TTbb_4t_10202021_step3_wenyu/BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2018_NJetsCSV/ 
PATH_DEST=/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_10202021_step3_wenyu/BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2018_NJetsCSV/ 

SHIFTS=(JECdown JECup JERdown JERup nominal)

for s in ${SHIFTS[@]}; do 
    echo "copying shift ${s}"
    cp ${PATH_ORIGIN}/${s}/*.root ${PATH_DEST}/${s}/.
done


