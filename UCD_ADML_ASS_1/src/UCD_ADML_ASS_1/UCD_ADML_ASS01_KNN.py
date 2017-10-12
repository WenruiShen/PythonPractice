#############################################################################################
#    Description:     Implementation of Basic Multi-class text classification 
#                     based on K-NN classifier.    
#    Author:          Wenrui Shen (University College of Dublin)
#    StudentNo:       15210671
#    E-mail:          wenrui.shen@ucdconnect.ie
#    Date:            04-Dec-2016
#############################################################################################
import os
import scipy.io as spio
from scipy.sparse import coo_matrix
from scipy import spatial
import math
import string
import numpy
import random
from networkx.algorithms.shortest_paths import unweighted
from _datetime import datetime


####################################################
#    Function Name: Cosine_Similarity_Calculator
#    Description:   Calculate the cosine similarity among two matrix.
#    Input:         sample_matrix
#                   test_array
#                   matrix_col_dimension
#    Return:        result similarity    (0:no common; 1:identical)
#    Change date:   03-Dec-2016
####################################################
def Cosine_Similarity_Calculator(sample_matrix, test_array, matrix_col_dimension):
    # numpy cosine API:
    Cosine_Similarity = 1 - spatial.distance.cosine(sample_matrix.toarray(), test_array)
    return Cosine_Similarity


####################################################
#    Function Name: unweighted_measure & weighted_measure    
#    Change date:   03-Dec-2016
####################################################
def unweighted_measure(Knn_Similarity_list, file_labels_list, k):
    # Unweighted KNN-Algorithm
    '''
    for index in range(k):
        print('    [', Knn_Similarity_list[index][0], ']:', Knn_Similarity_list[index][1])
    '''
    unweighted_labels_dic = {}
    for index in range(k):
        file_index = Knn_Similarity_list[index][0] + 1
        file_label = file_labels_list[file_index - 1]
        if file_label in unweighted_labels_dic:
            unweighted_labels_dic[file_label] += 1
        else:
            unweighted_labels_dic[file_label] = 1
    #print('    Unweighted_labels_dic', unweighted_labels_dic)
    return unweighted_labels_dic

def weighted_measure(Knn_Similarity_list, file_labels_list, k):
    # Weighted KNN-Algorithm
    weighted_labels_dic = {}
    for index in range(k):
        file_index = Knn_Similarity_list[index][0] + 1
        file_label = file_labels_list[file_index - 1]
        if file_label in weighted_labels_dic:
            weighted_labels_dic[file_label] += Knn_Similarity_list[index][1]
        else:
            weighted_labels_dic[file_label] = Knn_Similarity_list[index][1]
    #print('    Weighted_labels_dic:', weighted_labels_dic)
    return weighted_labels_dic    

####################################################
#    Function Name: Knn_Classifier
#    Description:   Basic K-NN classifier, find top k nearest data.
#    Input:         dataset_coomatrix:
#                   random_index_list:
#                   test_index:
#                   testset_startindex:
#                   testset_stopindex:  
#                   k:       number of target nearest data;
#                   m:       0:unweighted;  1:weighted;
#    Return:        weighted_labels_dic
#    Change date:   03-Dec-2016
####################################################
def Knn_Classifier(dataset_coomatrix, random_index_list, test_index, testset_startindex, 
                   testset_stopindex, k, m):
    matrix_row_dimension, matrix_col_dimension = dataset_coomatrix.get_shape()
    # Init the storage dictionary of Similarity
    Similarity_dict = {}
    testset_array = dataset_coomatrix.getrow(random_index_list[test_index]).toarray()
    train_index = 0
    while True:
        if ((train_index in range(0, testset_startindex)) or (train_index in range(testset_stopindex + 1, matrix_row_dimension))):
            Cosine_Similarity = Cosine_Similarity_Calculator(dataset_coomatrix.getrow(random_index_list[train_index]),            
                                                             testset_array, matrix_col_dimension)
            if Cosine_Similarity > 0:
                Similarity_dict[random_index_list[train_index]] = Cosine_Similarity
            train_index += 1
            if train_index >= matrix_row_dimension:
                break
        elif train_index in range(testset_startindex, testset_stopindex + 1):
            train_index += 1
        elif train_index >= matrix_row_dimension:
            break
        else:
            print('OUT train_index=', train_index)
            return
    
    # Sort the dict according to the value:similarity
    Knn_Similarity_list = sorted(Similarity_dict.items(), key=lambda d:d[1], reverse = True)
    return Knn_Similarity_list


####################################################
#    Function Name: Dataset_Load
#    Description:   Read dataset from documentation.
#    Input:         file_name
#    Return:        dataset_coomatrix
#    Change date:   02-Dec-2016
####################################################
def Dataset_Load(file_name):
    dataset_info = spio.mminfo(file_name)
    print('Load dataset_info:', dataset_info)
    dataset_coomatrix = spio.mmread(file_name)
    return dataset_coomatrix


####################################################
#    Function Name: Labels_Load
#    Description:   Read labels file from documentation.
#    Input:         file_name
#    Return:        file_labels_list
#    Change date:   03-Dec-2016
####################################################
def Labels_Load(file_name):
    file_labels_list = []
    labels_f = open(file_name, 'r')
    while 1:
        single_line = labels_f.readline()
        if single_line == '':
            break
        temp_str_list = single_line.split(',')
        #file_index = int(temp_str_list[0])
        file_labels_str = temp_str_list[1].rstrip('\n')
        file_labels_list.append(file_labels_str)
    labels_f.close()
    print('Labels loaded.')
    return file_labels_list


####################################################
#    Function Name: predict_count_init
#    Change date:   04-Dec-2016
####################################################
def predict_count_init(k):
    if k == 0:
        accuracy_num = 10
    else:
        accuracy_num = 1
    predict_correct_count = [0 for a_id in range(accuracy_num)]
    predict_wrong_count = [0 for a_id in range(accuracy_num)]
    return predict_correct_count, predict_wrong_count


####################################################
#    Function Name: Dataset_Split
#    Description:   Split dataset_coomatrix into Training set and Test set.
#    Input:         dataset_coomatrix
#                   k_fold
#                   i
#    Return:        testset_startindex
#                   testset_stopindex
#    Change date:   02-Dec-2016
####################################################
def Dataset_Split(dataset_coomatrix, k_fold, i):
    # step 1: Get the amount of different rows' values, which indicate X,
    #         the temp result dataset_coomatrix_shape is tuple.
    matrix_row_dimension, matrix_col_dimension = dataset_coomatrix.get_shape()
    
    # step 2: Split rows' dimension into k parts.
    if k_fold == 0:
        Testset_elements_amount = 0
        testset_startindex = 0
        testset_stopindex = 0
        print('No split!')
        return testset_startindex, testset_stopindex
    else:
        Testset_elements_amount = (matrix_row_dimension // k_fold)
    
    testset_startindex = Testset_elements_amount * i
    if i == k_fold - 1:
        testset_stopindex = matrix_row_dimension - 1
    else:
        testset_stopindex =  testset_startindex + Testset_elements_amount - 1
    return testset_startindex, testset_stopindex


####################################################
#    Function Name: Knn_decision_measure
#    Change date:   04-Dec-2016
####################################################
def Knn_decision_measure(Knn_Similarity_list, file_labels_list, k, m):
    predicted_labels_dic = {}
    if m == 0:
        predicted_labels_dic = unweighted_measure(Knn_Similarity_list, file_labels_list, k)
    elif m == 1:
        predicted_labels_dic = weighted_measure(Knn_Similarity_list, file_labels_list, k)
    else:
        return
    sorted_labels_list = sorted(predicted_labels_dic.items(), key=lambda d:d[1], reverse = True)
    #print('    [k=', k, ']sorted_labels_list:', sorted_labels_list)
    return sorted_labels_list


####################################################
#    Function Name: Average_accuracy_calculator
#    Change date:   04-Dec-2016
####################################################
def Average_accuracy_calculator(predict_correct_count, predict_wrong_count, k):
    if k == 0:
        accuracy_num = 10
    else:
        accuracy_num = 1
    Total_predict_count = [0 for a_id in range(accuracy_num)]
    Average_Accuracy = [0 for a_id in range(accuracy_num)]
    
    for i in range(accuracy_num):
        if k !=0:
            Average_accuracy_id = 0
        elif k == 0:
            Average_accuracy_id = i
        # Average Evaluation for the whole Knn's statistic results
        Total_predict_count[Average_accuracy_id] = predict_correct_count[Average_accuracy_id] + predict_wrong_count[Average_accuracy_id]
        if Total_predict_count[Average_accuracy_id] == 0:
            print('Error: Failed to predict!')
            return None
        else:
            Average_Accuracy[Average_accuracy_id] = predict_correct_count[Average_accuracy_id] / Total_predict_count[Average_accuracy_id]
            if k==0:
                print('The K=[', Average_accuracy_id + 1, '] Average accuracy is ', Average_Accuracy[Average_accuracy_id])
            elif k!=0:
                print('The K=[', k, '] Average accuracy is ', Average_Accuracy[Average_accuracy_id])
    return Average_Accuracy

####################################################
#    Function Name: Dynamic_accuracy_changer
#    Change date:   04-Dec-2016
####################################################
def Dynamic_accuracy_changer(sorted_labels_list, actual_label, predict_correct_count, predict_wrong_count, k, k_i):
    if k == 0:
        ave_accuracy_id = k_i-1
    elif k!=0:
        ave_accuracy_id = 0
    
    if sorted_labels_list[0][0] == actual_label:
        predict_correct_count[ave_accuracy_id] += 1
        #print('   -[k=', k_i, ']No:', predict_correct_count[ave_accuracy_id] + predict_wrong_count[ave_accuracy_id], 
        #      ',correct:', predict_correct_count[ave_accuracy_id], ',actual:', actual_label)
    else:
        predict_wrong_count[ave_accuracy_id] += 1
        #print('   -[k=', k_i, ']No:', predict_correct_count[ave_accuracy_id] + predict_wrong_count[ave_accuracy_id],
        #      ',wrong:', predict_wrong_count[ave_accuracy_id], ',actual:', actual_label)
    return


####################################################
#    Function Name: Kfold_Split_Loop_Ctl
#    Description:   Main body control
#    Input:         dataset_coomatrix
#                   file_labels_list
#                   k:       number of target nearest data: [1,10] and 0;
#                   m:       0:unweighted;  1:weighted;
#    Return:        Average_Accuracy
#    Change date:   04-Dec-2016
####################################################
def Kfold_Split_Loop_Ctl(dataset_coomatrix, file_labels_list, k, m):
    k_fold = 10
    predict_correct_count, predict_wrong_count = predict_count_init(k)
    # Create Unique Random index list for evaluation
    matrix_row_dimension = dataset_coomatrix.get_shape()[0]
    random_index_list = random.sample(range(matrix_row_dimension), matrix_row_dimension)

    # Loop_1 starting
    for i in range(0,k_fold,1):
    #for i in range(5,6,1):                                                        # Debug loop for once
        print('k_fold:', i)    
        testset_startindex, testset_stopindex = Dataset_Split(dataset_coomatrix, k_fold, i) 
        
        # Loop_2 starting, cycling for all testset's elements  
        #for test_index in range(testset_startindex, testset_startindex + 10, 1):            # Debug loop ctl
        for test_index in range(testset_startindex, testset_stopindex + 1): 
            Knn_Similarity_list = Knn_Classifier(dataset_coomatrix, random_index_list, test_index, 
                                                   testset_startindex, testset_stopindex, k, m)
            
            actual_label = file_labels_list[random_index_list[test_index]]
            if k==0:
                k_start = 1
                k_end = 11
            elif k!=0:
                k_start = k
                k_end = k+1
            else:
                return
            for k_i in range(k_start,k_end):
                # Make decision based on K-nearest data's labels
                sorted_labels_list = Knn_decision_measure(Knn_Similarity_list, file_labels_list, k_i, m)
                # Evaluating:
                Dynamic_accuracy_changer(sorted_labels_list, actual_label, predict_correct_count, predict_wrong_count, k, k_i)
            #print('--No:', test_index - testset_startindex + 1, ',test_id[', test_index, '],real_id[', random_index_list[test_index],
            #       '],k=', k , 'actual_label:', actual_label, 'sort_list:', sorted_labels_list)
        # Loop_2 Over
    # Loop_1 Over
    
    return Average_accuracy_calculator(predict_correct_count, predict_wrong_count, k)


####################################################
#    Function Name: Test_main
#    Description:   Load files, start the knn-process
#    Input:         dataset_file:str
#                   labels_file:str
#                   k:       number of target nearest data;
#                   m:       0:unweighted;  1:weighted;
#    Return:        None
#    Change date:   03-Dec-2016
####################################################
def Test_main(dataset_file, labels_file, k, m):
    start_time = datetime.now()
    dataset_coomatrix = Dataset_Load(dataset_file).tocsr()
    file_labels_list = Labels_Load(labels_file)
    if (dataset_coomatrix == None) or (file_labels_list == None):
        print('Error: Failed loading Files!!!')
        return None
    if k > 10 or k < 0:
        print('Error k input!(1-10)')
        return
    if m != 0 and m != 1:
        print('Invalid m input! (0 or 1)')
        return
    
    print('***************************************************************')
    print('*Now classify dataset_file:', dataset_file)
    print('*             labels_file :', labels_file)
    print('*             k=', k, ',m=', m)
    print('*start_time: ', start_time)
    print('***************************************************************')
    
    Kfold_Split_Loop_Ctl(dataset_coomatrix, file_labels_list, k, m)
    stop_time = datetime.now()
    print('*stop_time: ', stop_time)
    return 


####################################################
#    Function Name: Human_Interact
#    Change date:   04-Dec-2016
####################################################

def Human_Interact():
    cur_dir = os.getcwd()
    print('cur_dir:', cur_dir)
    default_set = input('* Please choose dataset(1:defaul set; 0:user input):\n\r')
    if default_set=='1':
        print('* Using Default set')
        dataset_file = cur_dir + '\\news_articles.mtx'
        labels_file = cur_dir + '\\news_articles.labels'
        k = 0
        m = 0
    elif default_set=='0':
        dataset_file = input('* Please Input test file(*.mtx only)      :\n\r')
        labels_file = input('* Please Input labels file(*.labels only) :\n\r')
        k = int(input('* Please Input k(1-10, 0:overall accuracy)  :\n\r'))
        if k > 10 or k < 0:
            print('Error k input!(1-10)')
            return
        m = int(input('* Please choose unweighted(0) or weighted(1) measurement:\n\r'))
        if m != 0 and m != 1:
            print('Invalid m input! (0 or 1)')
            return
    else:
        print('Error input')
        return
    Test_main(dataset_file, labels_file, k, m)
    return

'''   
# Operating the testing program
Test_main('D:\\File\\UCD CS\\MachineLearning\\UCD-ADML-Assignment-1\\news_articles.mtx', 
          'D:\\File\\UCD CS\\MachineLearning\\UCD-ADML-Assignment-1\\news_articles.labels', 5, 1)
'''

Human_Interact()
