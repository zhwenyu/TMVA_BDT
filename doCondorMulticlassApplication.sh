#!/bin/sh

inDir=${1}
outDir=${2}
fileName=${3}
BDT=${4}
CONDORDIR=${5}

source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh
sleep 1
source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh

cd $outDir/


root -l -b -q $CONDORDIR/TMVAMulticlassApplication.C\(\"$BDT\",\"$inDir/$fileName\",\"$fileName\"\)

