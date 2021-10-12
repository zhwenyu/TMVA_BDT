#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>
 
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TH1F.h"
 
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/DataSetInfo.h"

 
using namespace TMVA;
 
void TMVAMulticlassApplication( TString myMethodList = "", TString inputFile="", TString outputFile="")
{
 
   TMVA::Tools::Instance();
 
   //---------------------------------------------------------------
   // Default MVA methods to be trained + tested
   std::map<std::string,int> Use;
   Use["MLP"]             = 0;
   Use["BDTG"]            = 1;
   Use["DL_CPU"]          = 0;
   Use["DL_GPU"]          = 0;
   Use["FDA_GA"]          = 0;
   Use["PDEFoam"]         = 0;
   //---------------------------------------------------------------
 
   std::cout << std::endl;
   std::cout << "==> Start TMVAMulticlassApp" << std::endl;
   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;
 
      std::vector<TString> mlist = gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
         std::string regMethod(mlist[i]);
 
         if (Use.find(regMethod) == Use.end()) {
            std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) std::cout << it->first << " " << std::endl;
            std::cout << std::endl;
            return;
         }
         Use[regMethod] = 1;
      }
   }
 
 
   // create the Reader object
   TMVA::Reader *reader = new TMVA::Reader( "!Color:!Silent" );
 
   // create a set of variables and declare them to the reader
   // - the variable names must corresponds in name and type to
   // those given in the weight file(s) that you use
   Float_t var<number>;
   reader->AddVariable( "<var>", &var<number>);
 
   // book the MVA methods
   reader->BookMVA( "BDTG method", weightfile );
 
   // // get dataset info, get classes 
   TMVA::DataSetInfo & datainfo = reader->DataInfo();
   std::vector<TString> class_names;   
   for (UInt_t cls = 0; cls < datainfo.GetNClasses() ; cls++) {
       // std::cout << (datainfo.GetClassInfo(cls))->GetName() << std::endl;
       class_names.push_back((datainfo.GetClassInfo(cls))->GetName());
   } 

   // input tree  
   TFile *input(0);
   if (!gSystem->AccessPathName( inputFile )){ 
      input = TFile::Open( inputFile ); // check if file in local directory exists 
   } 
   if (!input) {
      std::cout << "ERROR: could not open data file" << std::endl;
      exit(1);
   }
   std::cout << "--- TMVAMulticlassApp : Using input file: " << input->GetName() << std::endl;
 
   // prepare the tree
   // - here the variable names have to corresponds to your tree
   // - you can use the same variables as above which is slightly faster,
   //   but of course you can use different ones and copy the values inside the event loop
 
   TTree* theTree = (TTree*)input->Get("ljmet");
   std::cout << "--- Select signal sample" << std::endl;
   theTree->SetBranchAddress( "<var>", &var<number>);

   // output file and new branch 
   TFile *target  = new TFile( outputFile,"RECREATE" );
   target->cd();
   TTree *newTree = theTree->CloneTree(0);   
   Float_t BDTG; TBranch *b_BDTG = newTree->Branch("BDTG", &BDTG, "BDTG/F");
 
   std::cout << "--- Processing: " << theTree->GetEntries() << " events" << std::endl;
   TStopwatch sw;
   sw.Start();
 
   for (Long64_t ievt=0; ievt<theTree->GetEntries();ievt++) {
     // if (ievt > 10) break; // debug 

      if (ievt%1000 == 0){
         std::cout << "--- ... Processing event: " << ievt << std::endl;
      }
      theTree->GetEntry(ievt);

      BDTG = (reader->EvaluateMulticlass( "BDTG method" ))[0] ;
      std::cout << " debug --- "; 
      std::cout << (reader->EvaluateMulticlass( "BDTG method" )).size() << std::endl; // debug 
      newTree->Fill(); 

   }
 
   // get elapsed time
   sw.Stop();
   std::cout << "--- End of event loop: "; sw.Print();
 

   // write tree 
   newTree->Write(); 
   target->Close();
   std::cout << "--- Created root file: \"TMVMulticlassApp.root\" containing the MVA output histograms" << std::endl;
 
   delete reader;
 
   std::cout << "==> TMVAMulticlassApp is done!" << std::endl << std::endl;
}
 
//int main( int argc, char** argv )
//{
//   // Select methods (don't look at this code - not of interest)
//   TString methodList;
//   for (int i=1; i<argc; i++) {
//      TString regMethod(argv[i]);
//      if(regMethod=="-b" || regMethod=="--batch") continue;
//      if (!methodList.IsNull()) methodList += TString(",");
//      methodList += regMethod;
//   }
//   TMVAMulticlassApplication(methodList);
//   return 0;
//}
