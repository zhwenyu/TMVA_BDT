import ROOT as r, math as m #needs 6.14 or greater
import ROOT
r.gROOT.SetBatch()

import numpy as np

intcolor=[r.TColor.GetColor(i) for i in ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]]
def compare(name,file_list,name_list,legend_list,normalize=False,drawoption='hE',xtitle='',ytitle='',minx=0,maxx=0,rebin=1,miny=0,maxy=0,textsizefactor=1,logy=False):
  c=r.TCanvas(name,'',600,600)
  c.SetLeftMargin(0.15)#
  c.SetRightMargin(0.05)#
  c.SetBottomMargin(0.11)
  c.SetTopMargin(0.25)
  legend=r.TLegend(0.0,0.76,0.99,1.04)
  legend.SetHeader('')
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  histo_list=[]
  the_maxy=0
  for i in range(len(name_list)):
    histo_list.append(file_list[i].Get(name_list[i]).Clone(name_list[i]+'_'+str(i)))
    if normalize:
      histo_list[-1].Scale(1.0/(histo_list[-1].Integral()+0.00000001))
    histo_list[-1].SetStats(0)
    histo_list[-1].SetLineWidth(3)
    histo_list[-1].SetLineColor(intcolor[i])
    histo_list[-1].SetTitle('')
    if rebin!=1:
      histo_list[-1].Rebin(rebin)
    the_maxy=max(the_maxy,histo_list[-1].GetBinContent(histo_list[-1].GetMaximumBin())*1.05)
    legend.AddEntry(histo_list[-1],legend_list[i],'l')
  for i in range(len(name_list)):
    if i==0:
      if miny!=0 or maxy!=0:
        histo_list[i].SetMaximum(maxy)
        histo_list[i].SetMinimum(miny)
      else:
        histo_list[i].SetMaximum(the_maxy)
        #histo_list[i].SetMinimum(0.0001)
      histo_list[i].Draw(drawoption)
      charsize=0.05*textsizefactor
      histo_list[i].GetYaxis().SetLabelSize(charsize)
      histo_list[i].GetYaxis().SetTitleSize(charsize)
      histo_list[i].GetYaxis().SetTitleOffset(1.6)
      histo_list[i].GetXaxis().SetLabelSize(charsize)
      histo_list[i].GetXaxis().SetTitleSize(charsize)
      histo_list[i].GetXaxis().SetTitleOffset(0.95)
      if xtitle!='':
        histo_list[i].GetXaxis().SetTitle(xtitle)
      if ytitle!='':  
        histo_list[i].GetYaxis().SetTitle(ytitle)
      if maxx!=0 or minx!=0:
        histo_list[i].GetXaxis().SetRangeUser(minx,maxx)
    else:
      histo_list[i].Draw(drawoption+'SAME')
  if logy:
    c.SetLogy()
  legend.Draw()
  c.SaveAs('pdf/'+name+'.pdf')

def compare2(name,file_list, file_list2, name_list, legend_list, legend_list2, normalize=False,drawoption='hE',xtitle='',ytitle='',minx=0,maxx=0,rebin=1,miny=0,maxy=0,textsizefactor=1,logy=False):
  c=r.TCanvas(name,'',600,600)
  c.SetLeftMargin(0.)#
  c.SetRightMargin(0.0)#
  c.SetBottomMargin(0.0)
  c.SetTopMargin(0.0)
  c.cd()

  legend=r.TLegend(0.7,0.76,0.99,1.04)
  legend.SetHeader('')
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  histo_list=[]
  the_maxy=0

  for i in range(len(name_list)):
      histo_list.append(file_list[i].Get(name_list[i]).Clone(name_list[i]+'_'+str(i)))
      if normalize:
        histo_list[-1].Scale(1.0/(histo_list[-1].Integral()+0.00000001))
      histo_list[-1].SetStats(0)
      histo_list[-1].SetLineWidth(3)
      histo_list[-1].SetLineColor(intcolor[i])
      histo_list[-1].SetTitle('')
      if rebin!=1:
        histo_list[-1].Rebin(rebin)
      the_maxy=max(the_maxy,histo_list[-1].GetBinContent(histo_list[-1].GetMaximumBin())*1.05)
      legend.AddEntry(histo_list[-1],legend_list[i],'l')
  for i in range(len(name_list)):
      histo_list.append(file_list2[i].Get(name_list[i]).Clone(name_list[i]+'_2_'+str(i)))
      if normalize:
        histo_list[-1].Scale(1.0/(histo_list[-1].Integral()+0.00000001))
      histo_list[-1].SetStats(0)
      histo_list[-1].SetLineWidth(3)
      histo_list[-1].SetLineColor(intcolor[i] + len(file_list))
      histo_list[-1].SetTitle('')
      if rebin!=1:
        histo_list[-1].Rebin(rebin)
      the_maxy=max(the_maxy,histo_list[-1].GetBinContent(histo_list[-1].GetMaximumBin())*1.05)
      legend.AddEntry(histo_list[-1],legend_list2[i],'l')

  p1=ROOT.TPad('p1','p1',0.0,0.3,1.0,1.0)
  p1.SetRightMargin(0.05)
  p1.SetLeftMargin(0.12)
  p1.SetTopMargin(0.01)
  p1.SetBottomMargin(0.01)
  p1.Draw()
  p1.SetGridx(False)
  p1.SetGridy(False)
  p1.cd()
  for i in range(len(name_list)):
    if i==0:
      if miny!=0 or maxy!=0:
        histo_list[i].SetMaximum(maxy)
        histo_list[i].SetMinimum(miny)
      else:
        histo_list[i].SetMaximum(the_maxy)
        #histo_list[i].SetMinimum(0.0001)
      histo_list[i].Draw(drawoption)
      charsize=0.05*textsizefactor
      histo_list[i].GetYaxis().SetLabelSize(charsize)
      histo_list[i].GetYaxis().SetTitleSize(charsize)
      histo_list[i].GetYaxis().SetTitleOffset(1.6)
      histo_list[i].GetXaxis().SetLabelSize(charsize)
      histo_list[i].GetXaxis().SetTitleSize(charsize)
      histo_list[i].GetXaxis().SetTitleOffset(0.95)
      if xtitle!='':
        histo_list[i].GetXaxis().SetTitle(xtitle)
      if ytitle!='':  
        histo_list[i].GetYaxis().SetTitle(ytitle)
      if maxx!=0 or minx!=0:
        histo_list[i].GetXaxis().SetRangeUser(minx,maxx)
    else:
      histo_list[i].Draw(drawoption+'SAME')
  if logy:
    c.SetLogy()
  legend.Draw()

  c.cd()
  p2 = ROOT.TPad('p2','p2',0.0,0.0,1.0,0.3)
  p2.Draw()
  p2.SetBottomMargin(0.15)
  p2.SetRightMargin(0.05)
  p2.SetLeftMargin(0.12)
  p2.SetTopMargin(0.01)
  p2.SetGridx(False)
  p2.SetGridy(True)
  p2.cd()
  ratios = [None]*2
  for i in range(len(histo_list)//2):
      ratios[i] = histo_list[i].Clone('ratio'+str(i))
      ratios[i].Divide(histo_list[i+2])  # 73/40 
      ratios[i].SetLineColor(intcolor[i])
      ratios[i].Draw('lX') 
      ratios[i].GetYaxis().SetLabelSize(0.1)
      ratios[i].GetYaxis().SetTitleSize(0.1)
      ratios[i].GetYaxis().SetTitleOffset(0.3)
      ratios[i].GetYaxis().SetTitle('ratio')
      ratios[i].GetXaxis().SetTitle(histo_list[i].GetXaxis().GetTitle())
      ratios[i].GetXaxis().SetLabelSize(0.1)
      ratios[i].GetXaxis().SetTitleSize(0.1)
      #break 

  c.SaveAs('pdf/'+name+'_ratio.pdf')




filenames={

#'40v_4j_y17' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2017_NJetsCSV_v1.root',
#'40v_4j_y18' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2018_NJetsCSV_v1.root',
#'40v_6j_y17' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year40top_40vars_mDepth2_6j_year2017_NJetsCSV_v1.root',

#'50v_4j_y18' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year50top_50vars_mDepth2_4j_year2018_NJetsCSV_v1.root',
#'50v_6j_y17' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year50top_50vars_mDepth2_6j_year2017_NJetsCSV_v1.root',
#'50v_6j_y18' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year50top_50vars_mDepth2_6j_year2018_NJetsCSV_v1.root',
#'40v_4j_y17' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2017_NJetsCSV_v1.root',
#'40v_4j_y16' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2016_NJetsCSV_v1.root',
#'40v_6j_y16' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year40top_40vars_mDepth2_6j_year2016_NJetsCSV_v1.root',
#'50v_4j_y16' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year50top_50vars_mDepth2_4j_year2016_NJetsCSV_v1.root',
#'50v_6j_y16' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017year50top_50vars_mDepth2_6j_year2016_NJetsCSV_v1.root',

#'40v_6j_y16_ttH' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2016_NJetsCSV_ttH.root',
#'40v_6j_y17_ttH' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2017_NJetsCSV_ttH.root',
#'40v_6j_y18_ttH' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2018_NJetsCSV_ttH.root',
#'40v_6j_y16_ttbb' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2016_NJetsCSV_ttbb.root',
#'40v_6j_y17_ttbb' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2017_NJetsCSV_ttbb.root',
#'40v_6j_y18_ttbb' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2018_NJetsCSV_ttbb.root',

'73v_6j_y16_ttH' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run_73vars_mDepth2_6j_year2016_NJetsCSV_ttH.root',
'73v_6j_y17_ttH' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run_73vars_mDepth2_6j_year2017_NJetsCSV_ttH.root',
'73v_6j_y18_ttH' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run_73vars_mDepth2_6j_year2018_NJetsCSV_ttH.root',
'73v_6j_y16_ttbb' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run_73vars_mDepth2_6j_year2016_NJetsCSV_ttbb.root', 
'73v_6j_y17_ttbb' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run_73vars_mDepth2_6j_year2017_NJetsCSV_ttbb.root',
'73v_6j_y18_ttbb' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run_73vars_mDepth2_6j_year2018_NJetsCSV_ttbb.root',
}

filenames2 = {
'73v_6j_y18_ttH' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2018_NJetsCSV_ttH.root',
'73v_6j_y16_ttH' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2016_NJetsCSV_ttH.root',
'73v_6j_y17_ttH' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2017_NJetsCSV_ttH.root',
'73v_6j_y16_ttbb' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2016_NJetsCSV_ttbb.root',
'73v_6j_y17_ttbb' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2017_NJetsCSV_ttbb.root',
'73v_6j_y18_ttbb' : 'dataset2021/weights/TMVA_BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2018_NJetsCSV_ttbb.root',

}
files={}
files2= {}
for key in filenames:
    files[key]=r.TFile(filenames[key],'r')
    files2[key]=r.TFile(filenames2[key],'r')

plots={

#'effS' : 'dataset2021/Method_BDT/BDT/MVA_BDT_effS',
#'effB' : 'dataset2021/Method_BDT/BDT/MVA_BDT_effB',
#'effBvsS' : 'dataset2021/Method_BDT/BDT/MVA_BDT_effBvsS',
'rejBvsS' : 'dataset2021/Method_BDT/BDT/MVA_BDT_rejBvsS',
#'invBeffvsSeff' : 'dataset2021/Method_BDT/BDT/MVA_BDT_invBeffvsSeff',
'trainingRejBvsS' : 'dataset2021/Method_BDT/BDT/MVA_BDT_trainingRejBvsS',
#'trainingEffS' : 'dataset2021/Method_BDT/BDT/MVA_BDT_trainingEffS',
#'trainingEffB' : 'dataset2021/Method_BDT/BDT/MVA_BDT_trainingEffB',
#'trainingEffBvsS' : 'dataset2021/Method_BDT/BDT/MVA_BDT_trainingEffBvsS',

}

U='_'
C=','
R='\n'

for key in files:
#	compare(key+U+'TestVsTrain',textsizefactor=0.7,
#		normalize= False,
#		file_list=[files[key],files[key]],legend_list=['Test','Training'],name_list=[plots['rejBvsS'],plots['trainingRejBvsS']],
#		drawoption= '')
    compare2(key+U+'TestVsTrain',textsizefactor=0.7,
        normalize= False,
        file_list=[files[key],files[key]], file_list2=[files2[key],files2[key]], legend_list=['Test_73v','Training_73v'], legend_list2=['Test_40v','Training_40v'], name_list=[plots['rejBvsS'],plots['trainingRejBvsS']],
        drawoption= '')


print 'training'+C+"AUC"

keys=[k for k in files]
keys.sort()

for key in keys:
	tmp=files[key].Get(plots['rejBvsS']).Clone()
	print key+' (validation)'+C+str(tmp.Integral())
	tmp=files[key].Get(plots['trainingRejBvsS']).Clone()
	print key+' (training)'+C+str(tmp.Integral())

