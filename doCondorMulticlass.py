import os,sys
import varsList

nTrees = '100'
BDTlist = ['BDTG']
varListKeys = [ #'SepRank6j73vars2017Run' 
#'CombIpRank',
#'Comb20top'
]
for ind in range(40, 42, 10):
  varListKeys.append('SepRank6j73vars2017Run'+str(ind)+ 'top')

runDir=os.getcwd()
condorDir=runDir+'/condor_log/'
os.system('mkdir -p '+condorDir)
note='_6j_year2018_NJetsCSV_multi'
count=0
for method in BDTlist:
    for vListKey in varListKeys:
        for mDepth in ['2']:
            count+=1
            fileName = method+'_'+vListKey+'_'+str(len(varsList.varList[vListKey]))+'vars_mDepth'+mDepth+note
            dict={'RUNDIR':runDir,'FILENAME':fileName,'METHOD':method,'vListKey':vListKey,'mDepth':mDepth,'nTrees':nTrees}
            jdfName=condorDir+'/%(FILENAME)s.job'%dict
            print jdfName
            jdf=open(jdfName,'w')
            jdf.write(
"""universe = vanilla
Executable = %(RUNDIR)s/doCondorMulticlass.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
Output = %(FILENAME)s.out
Error = %(FILENAME)s.err
Log = %(FILENAME)s.log
Notification = Never
Arguments = %(RUNDIR)s %(FILENAME)s %(METHOD)s %(vListKey)s %(nTrees)s %(mDepth)s
Queue 1"""%dict)
            jdf.close()
            os.chdir('%s/'%(condorDir))
            os.system('condor_submit %(FILENAME)s.job'%dict)
            os.system('sleep 0.5')                                
            os.chdir('%s'%(runDir))
            print count, "jobs submitted!!!"

