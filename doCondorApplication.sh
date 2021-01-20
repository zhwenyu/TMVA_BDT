#!/bin/sh

inDir=${1}
outDir=${2}
fileName=${3}
BDT=${4}
CONDORDIR=${5}

sleep 5
source /cvmfs/cms.cern.ch/cmsset_default.sh
sleep 5
# # cd /user_data/jlee/TTTT/CMSSW_9_4_6_patch1/src/TMVA
# export SCRAM_ARCH="slc7_amd64_gcc700"
# cd /home/eusai/4t/CMSSW_10_2_16_UL/src/
# eval `scramv1 runtime -sh`
# cd /home/eusai/4t/TTTT/TMVA
source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh
sleep 5
source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh

cd $outDir/

# source /cvmfs/sft.cern.ch/lcg/contrib/gcc/7.3.0/x86_64-centos7-gcc7-opt/setup.sh
# source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.16.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh

root -l -b -q $CONDORDIR/TMVAClassificationApplication.C\(\"$BDT\",\"$inDir/$fileName\",\"$fileName\"\)

# cp $fileName $outDir/
# rm $fileName 
