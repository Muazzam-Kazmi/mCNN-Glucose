"""
	@author   : Semmy Wellem Taju
	@Major    : Computer Science
	@Language : Python 3.5.3
	@Desc     : This class is used to handle basic reader file fasta and PSSM.
               Some functions will be added later.
    # Python 3.6.3 |Anaconda custom (64-bit)| (default, Nov  8 2017, 15:10:56) [MSC v.1900 64 bit (AMD64)] on win32
    
    @Link penting: http://sebastianraschka.com/Articles/2014_about_feature_scaling.html
"""

# Required Python Package
import os
import pandas as pd
import numpy as np
import time

class BasicFunctions:
    '''
        Constructor
    '''
    def __init__(self):
        print("Start your Class...");
    
    
    '''
        zscorescale
        They called standard normalization, z-score standarizat(single column)
        # Citation: 
          Singh, Bikesh Kumar, Kesari Verma, and A. S. Thoke. "Investigations on impact 
          of feature normalizattechniques on classifier's performance in breast tumor 
          classification.", International Journal of Computer Applications 116.19 (2015).
        Parameters: 
            inputs: single row of list
    '''
    def zScoreScale(self, inputs):
        meanData = np.mean(inputs);
        stdData = np.std(inputs, ddof=1);
        scores = [round(((x - meanData) / stdData), 6) for x in inputs]
            
        return scores;
    
    
    
    '''
        Softmax Scaling
        Calculate the sigmoid functfor feature scaling with inputs (array)
        # Citation: Same above
        Ex: 
            # Apply Sigmoid in list
            sigmoid_inputs = [1, 2, 3, 4]
            print("Sigmoid Function: {}".format(sigmoid(sigmoid_inputs)))
        Parameters: 
            inputs: single row of list
    '''
    def sigmoidScale(self, inputs):
        scores = [round(1 / float(1 + np.exp(- x)), 6) for x in inputs]
        
        return scores;
    
    
    '''
        Linear Scaling
        This technique normalizes data in range [0, 1].
        linear scaling to [0,1]
        Citat : Same above
        Parameters: 
            inputs: single row of list
    '''
    def linearScale(self, inputs):
        minData = np.min(inputs);
        maxData = np.max(inputs);
        scores = [round((x-minData)/(maxData-minData), 6) for x in inputs]
        
        return scores;
    
    
    '''
        Min – Max Normalization
        This technique normalize data in range [-1, 1].
        linear scaling to [-1,1]
        Citat : Same above
        Parameters: 
            inputs: single row of list
    '''
    def minMaxScale(self, inputs):
        min_new = -1;
        max_new = 1;
        minData = np.min(inputs);
        maxData = np.max(inputs);
        scores = [round((((x-minData)/(maxData-minData))*(max_new-min_new)+min_new), 6) for x in inputs]
        
        return scores;
    
    
    '''
        This functis used to read all your fasta files in dir and
        store all fasta id and seq in dataframe.
    '''
    def readFastaInDir(self, inputDir):
        fastaDir = inputDir;
        # Error handling
        try:
            # Set your time
            # start_time = time.clock()
            # Create new dataframe to store
            COLUMN_NAMES=['ID', 'sequence']
            COLLECT = pd.DataFrame(columns=COLUMN_NAMES)
            
            # Loop all files
            for root, dirs, files in os.walk(fastaDir):
                i=0;
                for file in files:
                    filePath=os.path.join(root,file)
                    #print("File {0}: {1}".format(i+1, filePath));
                    # Read file
                    f = open(filePath, "r")
                    fastaName = "";
                    fastaSeq = "";
                    count=1;
                    for line in f:
                        if count==1:
                            try:
                                start = line.index("|")+1
                                end = line.index("|", start)
                                fastaName = line[start:end]
                            except ValueError:
                                print("Error fasta name: ",filePath);
                        
                        elif count==2:
                            fastaSeq = line.replace('\n', '');
                            
                        count=count+1;
                        
                    #print(fastaName);
                    #print(fastaSeq);
                    
                    # Insert to data frame
                    COLLECT.loc[i] = [fastaName, fastaSeq]
                    
                    i=i+1;    
                    f.close
                
                # Print total file
                # print("--Time: {0} seconds, Total Fasta files: {1}--".format(round((time.clock() - start_time),4), i));
        
        except:
            print("Error message: You got an error.")

        return COLLECT;
    

    '''
        This functis used to read one pssm profile file and store it in dataframe.
        Parameters:
            inputFilePath: file path
            SeqName      : [important] Select pssm content with their sequence
            SelfStore    : Store pssm content in class and no need to return
            RETURN       : Data frame type
    '''
    def readPSSMFile(self, inputFilePath, SeqName=False, SelfStore=False):    
        # A technque to read PSSM profiles using panda
        # Start index is in col 2 to get all content only.
        # if set to 1 means select with their protein amino acid in first col.
        startCol = 2; 
        if SeqName == True:
            startCol = 1; 
        # 22 amino acid matrix, 42 means with their frequence
        endCol = 22; 
        # Set some of unuseful rows by number of row 
        setSkipRows = (0,1,2);
        # Read data
        pssmData = pd.read_csv(inputFilePath, 
                             skiprows=setSkipRows,
                             # White space delimater ignores more spaces
                             delim_whitespace=True,
                             # No header
                             header=None,
                             usecols=range(startCol, endCol)
                             )
        # Remove last 5 rows
        maxRow = (len(pssmData.index)) - 6 
        # Select only content of PSSM profiles
        pssmData = pssmData.loc[0:maxRow, :]
        
        if SelfStore == True:
            self.pssm = pssmData;
            
        else:    
            return pssmData;

    
    '''
        This functis used to generate your pssm feature set.
        Parameters: 
            inputDir: Directory path
            Scale   : Scaling data by default is false
    '''
    def pssmDefaultFeatureGenerator(self, inputDir, Scale=None):
        # Set amino acid
        AMINO_ACID = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 
                      'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'];
        # Create new dataframe to store
        COLUMN_NAMES=['Data']
        COLLECT = pd.DataFrame(columns=COLUMN_NAMES)
        
        # Set your time
        # start_time = time.clock()
            
        # Loop all files
        for root, dirs, files in os.walk(inputDir):
            i=0;
            for file in files:
                filePath=os.path.join(root,file)
                #print("File {0}: {1}".format(i+1, filePath));
                # Read file pssm profile
                self.readPSSMFile(filePath, SeqName=True, SelfStore=True);
                # Get Sequence Lenghth
                SEQ_LENGTH = len(self.pssm.index);
                #print("Sequence Length: ",SEQ_LENGTH);
                # Store
                result = []
                # By default SelfStore=True, data stored in self.pssm
                for aa in AMINO_ACID:
                    # Get for each amino acid in pssm
                    getData = self.pssm[self.pssm.iloc[:,0].isin(list([aa]))]
                    if getData.empty:
                        #print(aa,'. DataFrame is empty!')
                        result.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
                        
                    else:
                        #print(aa,'. Not empty!');
                        # Sum the same amino acid data and divided by sequence lenght
                        getNew = (getData.iloc[:,1:21].sum()/SEQ_LENGTH).tolist();
                        # Scale, Round and store
                        if Scale == "sigmoid":
                            result.append(self.sigmoidScale(getNew))
                            
                        elif Scale == "linearscale":
                            result.append(self.linearScale(getNew))
                            
                        elif Scale == "minmaxscale":
                            result.append(self.minMaxScale(getNew))
                            
                        elif Scale == "zscorescale":
                            result.append(self.zScoreScale(getNew))
                            
                        else:
                            # Without scaling data
                            result.append([round(n, 6) for n in getNew])
                            
                # convert to numpy array (list object) and than flattening the data
                newDataFormat = np.array(result, dtype=object)
                # Insert to data frame
                COLLECT.loc[i] = [newDataFormat.flatten()]
                # increase
                i=i+1;
            
            # Print total file
            # print("--Time: {0} seconds, Total PSSM files: {1}--".format(round((time.clock() - start_time),4), i));
        
        return pd.DataFrame(COLLECT['Data'].values.tolist());




    '''
        This function used to generate your pssm feature set based on the best 25 of each amino acid by summing each row
        and select best high value represent a amin acid mutatcontains with many positive value.
        Select best 25 as default: 25x20 amino acids (original sequence) = 500
                                   500x20 amino acid mutat= 10,000 features
                                   10,000 features will change to 100x100 2D as an input to CNN model
        Parameters: 
            inputDir: PSSM files Directory path
            Scale   : Selected feature scaling method
    '''
    def pssmSelectBestFeatureGenerator(self, inputDir, SelectedBest=25, Scale=None):
        # Set amino acid
        AMINO_ACID = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 
                      'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'];
        # Create new dataframe to store
        COLUMN_NAMES=['Data']
        allCOLLECT = pd.DataFrame(columns=COLUMN_NAMES)
        
        # Set your time
        # start_time = time.clock()
            
        # Loop all files
        for root, dirs, files in os.walk(inputDir):
            i=0;
            
            for file in files:
                filePath=os.path.join(root,file)
                #print("File {0}: {1}".format(i+1, filePath));
                # Read file pssm profile
                self.readPSSMFile(filePath, SeqName=True, SelfStore=True);
                # Get Sequence Lenghth
                #SEQ_LENGTH = len(self.pssm.index);
                #print("Sequence Length: ",SEQ_LENGTH);
                
                # Create new dataframe to store
                subCOLLECT = pd.DataFrame(columns=AMINO_ACID)
                
                # By default SelfStore=True, data stored in self.pssm
                for aa in AMINO_ACID:
                    # Get DataFrame for each amino acid in pssm
                    getData = self.pssm[self.pssm.iloc[:,0].isin(list([aa]))]
                    
                    # Get only content, index 0 is amino acid name
                    realPSSM = getData.iloc[:,1:21]
                    
                    # Max number of row in selected amino acid
                    maxAARow = len(realPSSM.index);
                    
                    if  maxAARow < SelectedBest:
                        getRest = SelectedBest - maxAARow;
                        # Create matrix
                        numRow = getRest;
                        numCol = 20; # This is PSSM columns i used
                        newMatrix = np.zeros((numRow, numCol))
                        # New DataFrame
                        DataFrameNew = pd.DataFrame(newMatrix, columns=AMINO_ACID)
                        
                        # Store in new dataframe variable
                        SelectRestAA = realPSSM
                        # Change column names
                        SelectRestAA.columns = AMINO_ACID
                        
                        # If empty, don't need to normilize (Evoid an error)
                        if maxAARow != 0:
                            # NormalizatData
                            if Scale == "sigmoid":
                                # Apply sigmoid functfor feature scaling in PSSM data
                                SelectRestAA = SelectRestAA.apply(lambda row: self.sigmoidScale(row), axis=1);
                                
                            elif Scale == "linearscale":
                                SelectRestAA = SelectRestAA.apply(lambda row: self.linearScale(row), axis=1);
                                
                            elif Scale == "minmaxscale":
                                SelectRestAA = SelectRestAA.apply(lambda row: self.minMaxScale(row), axis=1);
                                
                            elif Scale == "zscorescale":
                                SelectRestAA = SelectRestAA.apply(lambda row: self.zScoreScale(row), axis=1);
                        
                        # Append Zero matrix data
                        SelectRestAA = SelectRestAA.append(DataFrameNew, ignore_index=True, verify_integrity=True);
                        
                        # Append new data
                        subCOLLECT = subCOLLECT.append(SelectRestAA, ignore_index=True);
                        
                    else:
                        #print(aa,'. Not empty!');
                        # Sum multiple columns
                        realPSSM['sum'] = realPSSM.sum(axis=1)
                        
                        # Sort by column 'sum' and Decending (Big to small)
                        realPSSM = realPSSM.sort_values('sum', ascending=False)
                        
                        # Select The best by default 25
                        SelectBestAA = realPSSM.iloc[0:SelectedBest,0:20]
                        # Change column names
                        SelectBestAA.columns = AMINO_ACID
                        
                        
                        # NormalizatData
                        if Scale == "sigmoid":
                            # Apply sigmoid functfor feature scaling in PSSM data
                            SelectBestAA = SelectBestAA.apply(lambda row: self.sigmoidScale(row), axis=1);
                            
                        elif Scale == "linearscale":
                            SelectBestAA = SelectBestAA.apply(lambda row: self.linearScale(row), axis=1);
                            
                        elif Scale == "minmaxscale":
                            SelectBestAA = SelectBestAA.apply(lambda row: self.minMaxScale(row), axis=1);
                            
                        elif Scale == "zscorescale":
                            SelectBestAA = SelectBestAA.apply(lambda row: self.zScoreScale(row), axis=1);
                        
                            
                        # Append new data
                        subCOLLECT = subCOLLECT.append(SelectBestAA, ignore_index=True);
                
                # Flatten datafrome and Insert to data frame
                allCOLLECT.loc[i] = [subCOLLECT.values.flatten()]
                # increase
                i=i+1;
                
            # Print total file
            # print("--Time: {0} seconds, Total PSSM files: {1}--".format(round((time.clock() - start_time),4), i));
        
        # Seperate to many columns and Return new DataFrame
        return pd.DataFrame(allCOLLECT['Data'].values.tolist());
    
    '''
        Sliding window with checking the width shape of numpy array data
        Input: numpy array
    '''
    def slidingWindowCheckShape(self, npData, stepsize=1, setWindows=3):
        n = npData.shape[0]
        return np.hstack( npData[i:1+n+i-setWindows:stepsize] for i in range(0,setWindows) )
    
    
    '''
        Sliding window without checking the width shape of numpy array data
        Input: numpy array
    '''
    def slidingWindowWhitoutCheckShape(self, npsData, stepsize=1, setWindows=3):
        return np.hstack( npsData[i:1+i-setWindows or None:stepsize] for i in range(0,setWindows) )

    
    
    '''
        New method to generate your pssm feature set.
        Parameters: 
            inputDir: Directory path
            defaultStepSize: convolutstrides
                             None means we only need once windows
            defaultWindows: sliding windows height size
            Scale   : Scaling data by default is false
    '''
    def pssmSlidingWindowsFeatureGenerator(self, inputDir, defaultStepSize=None, defaultWindows=500, Scale=None):
        # Create new dataframe to store
        COLLECT = pd.DataFrame()
        
        # Set your time
        # start_time = time.clock()
            
        # Loop all files
        for root, dirs, files in os.walk(inputDir):
            i=0;
            for file in files:
                filePath=os.path.join(root,file)
                #print("File {0}: {1}".format(i+1, filePath));
                # Read file pssm profile
                self.readPSSMFile(filePath, SeqName=False, SelfStore=True);
                
                # NormalizatData
                if Scale == "sigmoid":
                    # Apply sigmoid functfor feature scaling in PSSM data
                    npData = self.pssm.apply(lambda row: self.sigmoidScale(row), axis=1);
                    
                elif Scale == "linearscale":
                    npData = self.pssm.apply(lambda row: self.linearScale(row), axis=1);
                    
                elif Scale == "minmaxscale":
                    npData = self.pssm.apply(lambda row: self.minMaxScale(row), axis=1);
                    
                elif Scale == "zscorescale":
                    npData = self.pssm.apply(lambda row: self.zScoreScale(row), axis=1);
                    
                else:
                    # None or without normalizatdata and convert a pandas dataframe (df) 
                    # to a numpy ndarray
                    npData = self.pssm.values 
            
                # Check if max seq length more than width
                maxLength = len(npData);
                if maxLength < defaultWindows:
                    getRest = defaultWindows - maxLength;
                    # Create matrix
                    numRow = getRest;
                    numCol = 20; # This is PSSM columns i used
                    newMatrix = np.zeros((numRow, numCol), dtype='int64')
                    # Append new data
                    npData = np.vstack([npData, newMatrix]);
                
                # Set step as high as you can. To avoid second sliding windows
                if defaultStepSize == None:
                    defaultStepSize = 10000;
                    
                # Sliding windows in numpy ndarray
                slideData = pd.DataFrame(self.slidingWindowWhitoutCheckShape(npData, stepsize=defaultStepSize, setWindows=defaultWindows));
                #print("Matrix Shape: ",slideData.shape)
                
                # Insert to data frame
                COLLECT = COLLECT.append(slideData)
                
                # increase and count file
                i=i+1;
                
            # Print total file
            # print("--Time: {0} seconds, Total PSSM files: {1}--".format(round((time.clock() - start_time),4), i));
        
        return COLLECT;
    
    
"""
Test Functions with Independent Program
Allows your program to be run by programs that import it
"""
if __name__ == '__main__':
    # Call class
    x = BasicFunctions()
    '''
    print("====================================================================");
    # Set dir, call functand read all fasta fules
    print('Read fasta files, please wait ...')
    fastaDir = "D:/test/Data/FASTA/4/neg/train/";
    dataFasta = x.readFastaInDir(fastaDir);
    
    # Find max length: get the length of the string of column in a dataframe
    dataFasta['Length'] = dataFasta['sequence'].apply(len)
    #print(dataFasta)
    # Get max length of protein sequences
    max(dataFasta['Length'].tolist())
    min(dataFasta['Length'].tolist())
    
    print("====================================================================");
    # EXAMPLE PSSM READER (Read PSSM profiles)
    pssmFileOnly = "D:/test/Data/PSSM/1/pos/1.amino_acid_Primary/test/B0R9X2.pssm_";
    
    # Parameter with SeqName=True means Amino acid name are required.
    data1 = x.readPSSMFile(pssmFileOnly, SeqName=True, SelfStore=False);
    # select only amino acid M
    strData = data1[data1.iloc[:,0].isin(list(['M']))]
    selectPSSMContent = strData.iloc[:,1:21];
    
    # Replace negative numbers in Pandas Data Frame by zero
    #NoNeg = data1[data1 < 0] = 0
    
    
    print("====================================================================");
    # EXAMPLE DATA NORMALIZATION
    print("Example normalizatdata ...");
    # Parameter with SeqName=False means we anly select the content of pssm
    data2 = x.readPSSMFile(pssmFileOnly, SeqName=False, SelfStore=True);
    
    # Apply sigmoid functfor feature scaling in PSSM data
    dataSigmoid = data2.apply(lambda row: x.sigmoidScale(row), axis=1);
    
    # Apply linear scaling in PSSM data
    dataLinear = data2.apply(lambda row: x.linearScale(row), axis=1);
    
    # Apply Min-Max scaling in PSSM data
    dataMinMax = data2.apply(lambda row: x.minMaxScale(row), axis=1);
    
    # Apply zscorescale in PSSM data
    dataZScore = data2.apply(lambda row: x.zScoreScale(row), axis=1);
    
    
    print("====================================================================");
    # DEFAULT GENERATE PSSM METHOD FROM DIRECTORY
    print('PSSM DEFAULT: Generate data from PSSM Method, please wait ...')
    pssmDir = "D:\\test\\Data\\PSSM\\1\\neg/2.electron_Primary/train/";
    pssmData = x.pssmDefaultFeatureGenerator(pssmDir, Scale=False);
    pssmData.iloc[0,:].values
    
    # Create class of data
    pssmData['class'] = 1 # Pos
    
    # Join pos and neg
    pssmData = pssmData.append(pssmData)
    
    # Save file
    output_file_name = "D:/pssm.csv";
    pssmData.to_csv(output_file_name, 
                    encoding='utf-8', 
                    sep=',',             # character, default ‘,’
                    index=False,
                    header=False
                    ) 
    '''
 
    
    print("====================================================================");
    # GENERATE Secondary PROTEIN DATA using Default PSSM Method
    print('Read paths please wait ...')
    print('Generate your PSSM Method, please wait ...')
        
    # Set paths
    WorkDir = "D:/PROJECT LAB/PAPERS/TRP-Channels/2. DATA/";
    path_test_trp = WorkDir+"1. TRAIN_TEST/2. PSSM/1.trp_channels/test/";
    path_train_trp  = WorkDir+"1. TRAIN_TEST/2. PSSM/1.trp_channels/train/";
    
    path_test_non_trp = WorkDir+"1. TRAIN_TEST/2. PSSM/2.non_trp_channels/test/";
    path_train_non_trp = WorkDir+"1. TRAIN_TEST/2. PSSM/2.non_trp_channels/train/";   
    #==========================================================================
    # NEED TO CHANGE THIS
    # Set your normalization data (linearscale, sigmoid, zscorescale, minmaxscale, noscale)
    #==========================================================================
    # setScaling = "noscale"; # None
    #setScaling = "linearscale";
    setScaling = "sigmoid";
    #setScaling = "minmaxscale";
    #setScaling = "zscorescale";
    
	# FEATURE GENERATOR
    test_ftr_trp  = x.pssmDefaultFeatureGenerator(path_test_trp, Scale=setScaling);
    train_ftr_trp  = x.pssmDefaultFeatureGenerator(path_train_trp, Scale=setScaling);
    
    test_ftr_non_trp  = x.pssmDefaultFeatureGenerator(path_test_non_trp, Scale=setScaling);
    train_ftr_non_trp  = x.pssmDefaultFeatureGenerator(path_train_non_trp, Scale=setScaling);
    
    print("STORE IN DATAFRAME ...");

    # Store SIRT 1
    traintrp = pd.DataFrame();
    traintrp = traintrp.append(train_ftr_trp)
    traintrp['class'] = 1 # 1 means positive instance
    
    testtrp = pd.DataFrame();
    testtrp = testtrp.append(test_ftr_trp)
    testtrp['class'] = 1 # 1 means positive instance
    
    # Store SIRT 2
    trainnontrp = pd.DataFrame();
    trainnontrp = trainnontrp.append(train_ftr_non_trp)
    trainnontrp['class'] = 1 # 1 means positive instance
    
    testnontrp = pd.DataFrame();
    testnontrp = testnontrp.append(test_ftr_non_trp)
    testnontrp['class'] = 1 # 1 means positive instance
    
    print("POS - NEG IN ONE FILE ...");
    
    # Class 1
    traintrp['class'] = 1  # 1 means positive instance, 0 means negative instance
    testtrp['class'] = 1 
    trainnontrp['class'] = 0
    testnontrp['class'] = 0 

    # Train
    collect_train_class1 = pd.DataFrame();
    collect_train_class1 = collect_train_class1.append(traintrp).append(trainnontrp)
    # Test
    collect_test_class1 = pd.DataFrame();
    collect_test_class1 = collect_test_class1.append(testtrp).append(testnontrp)
    
    print("FINALLY, SAVE DATA IN FILE ...");
    
    # Move class into first column
    cols = collect_train_class1.columns.tolist(); cols = cols[-1:] + cols[:-1]; 
    
    # Save file: Class 1 => sirt 1 as possitive data
    output_file = WorkDir+"3.Feature sets/16.PSSM_Features/"+"pssm_class_1_train"+".csv";
    collect_train_class1 = collect_train_class1[cols]; # Move class into first column
    collect_train_class1.to_csv(output_file, encoding='utf-8', sep=',', index=False, header=False) # character, default ‘,’
    
    output_file = WorkDir+"3.Feature sets/16.PSSM_Features/"+"pssm_class_1_test"+".csv";
    collect_test_class1 = collect_test_class1[cols]; # Move class into first column
    collect_test_class1.to_csv(output_file, encoding='utf-8', sep=',', index=False, header=False) # character, default ‘,’

   