import os,sys
import varsList

shift = sys.argv[1]
#BDT = 'BDT'
BDT = sys.argv[2]
# varListKey = 'BigComb'

# varListKey = 'Comb61andtrij'
#varListKey = 'SepRank6j73vars2017year72top'
varListKey = sys.argv[3]
BDTconfigStr = sys.argv[4]

templateFile = '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_10/src/applicationTMVA/TTTT/TMVA/TMVAClassificationApplication_template.C'
# massList = ['Low1','Low2']
#weightFile = '/user_data/jlee/TTTT/CMSSW_9_4_6_patch1/src/TMVA/dataset/weights/'
weightFilePath = '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_10/src/TTTT/TMVA/dataset2021/weights/'

# weightFile+= BDT+'_Comb61andtrij_73vars_mDepth2_6j_year2018/TMVAClassification_'+BDT+'.weights.xml'
#BDTconfigStr = BDT+'_SepRank6j73vars2017year72top_72vars_mDepth2_6j_year2017'
weightFile = weightFilePath + BDTconfigStr + '/TMVAClassification_'+BDT+'.weights.xml'
weightFile2 = weightFilePath + BDTconfigStr + '_ttH' + '/TMVAClassification_'+BDT+'.weights.xml'
weightFile3 = weightFilePath + BDTconfigStr + '_ttbb' + '/TMVAClassification_'+BDT+'.weights.xml'

#IO directories must be full paths

relbase = '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_10/'

inputDir  = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_051321_step2'


# outputDir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_02192020_step3_61var/'+shift+'/'

# outputDir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_03192020_step3_73vars_4j/'+shift+'/'
# outputDir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_03192020_step3_73vars_6j/'+shift+'/'
# outputDir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_03192020_step3_61vars_4j/'+shift+'/'
# outputDir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_03192020_step3_61vars_6j/'+shift+'/'

# BDT_Comb61andtrij_73vars_mDepth2_4j_year2017
# BDT_Comb61andtrij_73vars_mDepth2_6j_year2017
# BDT_CombIpRank_61vars_mDepth2_4j_year2017
# BDT_CombIpRank_61vars_mDepth2_6j_year2017

outputDir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_09072021_step3_wenyu/'+BDTconfigStr+'/'+shift+'/'

# BDT_Comb61andtrij_73vars_mDepth2_6j_year2018
# BDT_CombIpRank_61vars_mDepth2_6j_year2018

inputDir += '/'+shift+'/'
runDir=os.getcwd()
varList = varsList.varList[varListKey]
condorDir=runDir+'/FWLJMET102X_1lep2017_Oct2019_4t_09072021_step3_condorLogs/Application_'+outputDir.split('/')[-3]+'/'+shift+'/'
os.system('mkdir -p '+condorDir)

f = open(templateFile, 'rU')
templateFileLines = f.readlines()
f.close()
def makeTMVAClassAppConf(thefile):
	with open(thefile,'w') as fout:
	  	vars_to_convert = ['NJetsCSV_MultiLepCalc', 'NJets_JetSubCalc','NresolvedTops1pFake','NJetsTtagged','NJetsWtagged','NJetsCSVwithSF_JetSubCalc','NJetsCSV_MultiLepCalc','NJetsCSVwithSF_MultiLepCalc']
		for line in templateFileLines:
			if line.startswith('input ='): fout.write('input = \''+rFile+'\'')
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
# 				for mass in massList: 
				fout.write('   reader->BookMVA( \"BDT_tt method\", \"'+weightFile+'\" );\n')
                                fout.write('   reader->BookMVA( \"BDT_ttH method\", \"'+weightFile2+'\" );\n')
                                fout.write('   reader->BookMVA( \"BDT_ttbb method\", \"'+weightFile3+'\" );\n')
			elif 'Float_t BDT<mass>' in line:
# 				for mass in massList: 
				fout.write('   Float_t BDT_tt;\n')
				fout.write('   TBranch *b_BDT_tt = newTree->Branch( \"BDT_tt\", &BDT_tt, \"BDT_tt/F\" );\n')
                                fout.write('   Float_t BDT_ttH;\n')
                                fout.write('   TBranch *b_BDT_ttH = newTree->Branch( \"BDT_ttH\", &BDT_ttH, \"BDT_ttH/F\" );\n')
                                fout.write('   Float_t BDT_ttbb;\n')
                                fout.write('   TBranch *b_BDT_ttbb = newTree->Branch( \"BDT_ttbb\", &BDT_ttbb, \"BDT_ttbb/F\" );\n')
			elif 'SetBranchAddress' in line:
				for i, var in enumerate(varList): 
					if var[0]=='corr_met_MultiLepCalc': 
						fout.write('   theTree->SetBranchAddress( \"'+var[0]+'\", &varD'+str(i+1)+' );\n')
					elif var[0] in vars_to_convert:
						fout.write('   theTree->SetBranchAddress( \"'+var[0]+'\", &varI'+str(i+1)+' );\n')
					else:
						fout.write('   theTree->SetBranchAddress( \"'+var[0]+'\", &var'+str(i+1)+' );\n')
			elif 'BDT<mass> = reader->EvaluateMVA' in line:
# 				for mass in massList: 
				for i, var in enumerate(varList):
					if var[0]=='corr_met_MultiLepCalc': 
						fout.write('      varF'+str(i+1)+'=(Float_t)varD'+str(i+1)+';\n')
					elif var[0] in vars_to_convert:
						fout.write('      varF'+str(i+1)+'=(Float_t)varI'+str(i+1)+';\n')

				fout.write('      BDT_tt = reader->EvaluateMVA( \"BDT_tt method\" );\n')
                                fout.write('      BDT_ttH = reader->EvaluateMVA( \"BDT_ttH method\" );\n')
                                fout.write('      BDT_ttbb = reader->EvaluateMVA( \"BDT_ttbb method\" );\n')

			else: fout.write(line)
makeTMVAClassAppConf(condorDir+'/TMVAClassificationApplication.C')

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
Executable = %(RUNDIR)s/doCondorApplication.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
Transfer_Input_Files = %(CONDORDIR)s/TMVAClassificationApplication.C
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

