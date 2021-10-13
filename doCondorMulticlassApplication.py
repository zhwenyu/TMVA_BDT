import os,sys
import varsList

shift = sys.argv[1]
#BDT = sys.argv[2]
#varListKey = sys.argv[3]
#BDTconfigStr = sys.argv[4]
#shift = 'nominal'
BDT = 'BDTG' # currently only BDTG supported in multiclass  
varListKey = 'SepRank6j73vars2017Run40top' 
BDTconfigStr = 'BDTG_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2017_NJetsCSV_multi' 

templateFile = '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_10/src/applicationTMVA/TTTT/TMVA/TMVAMulticlassApplication_template.C'
weightFilePath = '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_10/src/TTTT/TMVA/dataset2021/weights/'
weightFile = weightFilePath + BDTconfigStr + '/TMVAMulticlass_'+BDT+'.weights.xml'

#IO directories must be full paths
relbase = '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_10/'
inputDir  = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_051321_step2'
outputDir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_10052021_step3_wenyu/'+BDTconfigStr+'/'+shift+'/'


inputDir += '/'+shift+'/'
runDir=os.getcwd()
varList = varsList.varList[varListKey]
condorDir=runDir+'/FWLJMET102X_1lep2017_Oct2019_4t_10052021_step3_condorLogs/Application_'+outputDir.split('/')[-3]+'/'+shift+'/'
os.system('mkdir -p '+condorDir)

f = open(templateFile, 'rU')
templateFileLines = f.readlines()
f.close()


def makeTMVAClassAppConf(thefile):

	with open(thefile,'w') as fout:
	  	vars_to_convert = ['NJetsCSV_MultiLepCalc', 'NJets_JetSubCalc', 'NresolvedTops1pFake', 'NJetsTtagged', 'NJetsWtagged', 'NJetsCSVwithSF_JetSubCalc', 'NJetsCSV_MultiLepCalc', 'NJetsCSVwithSF_MultiLepCalc']

		for line in templateFileLines:
			if line.startswith('input ='): 
				fout.write('input = \''+rFile+'\'')
			if 'Float_t var<number>' in line:
				for i, var in enumerate(varList): 
					if var[0]=='corr_met_MultiLepCalc':
						fout.write('   Float_t varF'+str(i+1)+';\n')
						fout.write('   Double_t varD'+str(i+1)+';\n')
					elif var[0] in vars_to_convert:
						fout.write('   Float_t varF'+str(i+1)+';\n')
						fout.write('   Int_t varI'+str(i+1)+';\n')
					else:
						fout.write('   Float_t var'+str(i+1)+';\n')
			elif 'AddVariable' in line:
				for i, var in enumerate(varList):
					if var[0]=='corr_met_MultiLepCalc': 
						fout.write('   reader->AddVariable( \"'+var[0]+'\", &varF'+str(i+1)+' );\n')
					elif var[0] in vars_to_convert:
						fout.write('   reader->AddVariable( \"'+var[0]+'\", &varF'+str(i+1)+' );\n')
					else:
						fout.write('   reader->AddVariable( \"'+var[0]+'\", &var'+str(i+1)+' );\n')
			elif 'BookMVA' in line:
				fout.write('   reader->BookMVA( \"BDTG method\", \"'+weightFile+'\" );\n')
			elif 'SetBranchAddress' in line:
				for i, var in enumerate(varList): 
					if var[0]=='corr_met_MultiLepCalc': 
						fout.write('   theTree->SetBranchAddress( \"'+var[0]+'\", &varD'+str(i+1)+' );\n')
					elif var[0] in vars_to_convert:
						fout.write('   theTree->SetBranchAddress( \"'+var[0]+'\", &varI'+str(i+1)+' );\n')
					else:
						fout.write('   theTree->SetBranchAddress( \"'+var[0]+'\", &var'+str(i+1)+' );\n')
			elif 'theTree->GetEntry' in line:
				fout.write(line) 
				for i, var in enumerate(varList):
					if var[0]=='corr_met_MultiLepCalc': 
						fout.write('      varF'+str(i+1)+'=(Float_t)varD'+str(i+1)+';\n')
					elif var[0] in vars_to_convert:
						fout.write('      varF'+str(i+1)+'=(Float_t)varI'+str(i+1)+';\n')

			else: fout.write(line)

makeTMVAClassAppConf(condorDir+'/TMVAMulticlassApplication.C')


rootfiles = os.popen('ls '+inputDir)
os.system('mkdir -p '+outputDir)
count=0

for file in rootfiles:
    if '.root' not in file: continue
#    if 'TTTT' not in file: continue
    rawname = file[:-6]
    print file
    count+=1
    dict={'RUNDIR':runDir,'INPUTDIR':inputDir,'FILENAME':rawname,'OUTPUTDIR':outputDir,'CONDORDIR':condorDir,'CMSSWBASE':relbase,'BDT':BDT}
    jdfName=condorDir+'/%(FILENAME)s.job'%dict
    print jdfName
    jdf=open(jdfName,'w')
    jdf.write(
"""universe = vanilla
Executable = %(RUNDIR)s/doCondorMulticlassApplication.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
Transfer_Input_Files = %(CONDORDIR)s/TMVAMulticlassApplication.C
Output = %(FILENAME)s.out
Error = %(FILENAME)s.err
Log = %(FILENAME)s.log
Notification = Never
JobBatchName = BDTstep3_wzhang
Arguments = %(INPUTDIR)s %(OUTPUTDIR)s %(FILENAME)s.root %(BDT)s %(CONDORDIR)s
Queue 1"""%dict)
    jdf.close()
    os.chdir('%s/'%(condorDir))
    print 'condor_submit %(FILENAME)s.job'%dict
    os.system('condor_submit %(FILENAME)s.job'%dict)
    os.system('sleep 1')                                
    os.chdir('%s'%(runDir))
    print count, "jobs submitted!!!"

