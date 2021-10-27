# TMVA BDT
TMVA BDT for fourtops

## Classfication
-- signal vs background \
-- classficiation input - step2 files
1. Edit configs in TMVAClassification.py, doCondorClassification.py, varsList.py
* check sample list, input vars, cuts, weights, directories...
2. submit by 
``` 
python doCondorClassification.py 
```

## Application (for Classification)
-- input: step2 files and BDT output xml files 
1. Edit configs doCondorApplication.py, submitTMVAApplication.sh \
By default, doCondorApplication.py takes ``` TMVAClassificationApplication_template.C ```, 
if one needs to apply over one BDT xml inputs, check doCondorApplication_3trainingInputs.py
2. submit by 
```
./submitTMVAApplication.sh
```

### make AUC plots
Edit computeAUC.py to read BDT output root files 
```
python computeAUC.py
```
###

## Multiclass 
* multiple classes, defined in TMVAmulticlass.py. TMVA multiclass only supports BDTG method. \
Note: currently AddTree() does not support TCut() \
* Application takes ``` TMVAMulticlassApplication_template.C```. This template is for BDTG method only. 
* use following scripts \
doCondorMulticlass.py, TMVAmulticlass.py, varsList_multiclass.py \
doCondorMulticlassApplication.py

