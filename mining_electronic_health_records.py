# Nabih El-helou
# 260766611
import json


# Question 1 reading ICD-9 definitions
def process_icd9_file(filename):
    """
    args:
        filename: Name of file containing ICD-9 definition
    returns:
        dictionary of dictionaries
        level 1 dictionary: icd9 group name as key
        level 2 dictionary: icd9 code as key and icd9 names as values
    """
    icd9_encyclopedia={}    
    f = open(filename, 'r')

    # YOUR CODE HERE
    group_name=""
    disease_code={}
    for line in f:
        line = line.rstrip()
        if line[1].isnumeric() is not True :
            group_name = line
            disease_code={}
            icd9_encyclopedia[group_name] = disease_code 
        else:
            if line[0] == "E":
                 disease_code[line[0:4]] = line[5:]
            else:
                disease_code[line[0:3]] = line[4:]
        
    f.close()
    
    return icd9_encyclopedia



# Question 2 process patient data to read in 5000 patients
def process_patient_data(filename, max_patients=5000):
    """
    args:
        filename: "DIAGNOSES_ICD.txt"
        max_patients: optional argument for maximum number of patients to store
        in the dictionary
    returns:
        a dictionary with patient ID as key and a set of ICD-9 code as values
        NOTE: the ICD-9 code from DIAGNOSES_ICD.txt is not directly compatible
        with the ICD9_encyclopedia from function process_icd9_file()
        This function will parse the ICD-9 code as follows.
        If the ICD-9 code is numeric or starts with "V", the first 3 characters
        of each ICD-9 code is stored as the values in the ICD-9 list; 
        If the ICD-9 code starts with "E", the first 4 characters of the ICD-9
        code is stored as the values in the ICD-9 list
    """
    f = open(filename, 'r')    
    patient_records = {}

    
    # YOUR CODE HERE
    patient_count = 0
    subject_ID=""
    icd9_code = set()
    for line in f:
        if line[0].isnumeric():
            line =line.split(',')
            if patient_count > 4999:
                break
            if subject_ID != line[0]:    
                subject_ID = line[0]
                icd9_code = set()
                patient_count += 1
            patient_records[subject_ID] = icd9_code
            if line[2][0] == "V" or line[2][0].isnumeric():
                icd9_code.add(line[2][0:3])
            if line[2][0] == "E":
                icd9_code.add(line[2][0:4])
            
    f.close()

    return patient_records





# Question 3
def average_patient_icd9code(patient_records):
    """
    args:
        patient_records obtained from process_patient_data("DIAGNOSES_ICD.txt")
    returns:
        average number of patient observed per ICD-9 code
    """
    
    icd9avg = 0
    
    # YOUR CODE HERE
    icd9_code = set()
    count = 0
    for patient, diseases in patient_records.items():
        
        for code in diseases:
            if code in icd9_code:
                count +=1
            else:    
                icd9_code.add(code)
                count +=1
    icd9avg = count/len(icd9_code)
    return icd9avg


# Question 4 group patient icd9 code by icd9 categories
# Question 4 part 1
def process_icd9_encyclopedia(icd9_encyclopedia):
    """
    args:
        icd9_encyclopedia obtained from process_icd9_info("icd9_info.txt")
    returns:
        icd9_encyclopedia_reverseIndex: dictionary with key as icd-9 code and value
        as the corresponding disease group names
    """

    icd9_encyclopedia_reverseIndex = {}

    # YOUR CODE HERE
    for group_name, diseases in icd9_encyclopedia.items():
        for code in diseases:
            if code[0].isnumeric() or code[0] == "V" :
                icd9_encyclopedia_reverseIndex[code[0:3]]= group_name
            if code[0] == "E" :
                icd9_encyclopedia_reverseIndex[code[0:4]]= group_name

    return icd9_encyclopedia_reverseIndex


# Question 4 part 2
def summarize_patient_records(patient_records, icd9_encyclopedia_reverseIndex):
    """
    args:
        patient_records obtained from process_patient_data("DIAGNOSES_ICD.txt")
        icd9_encyclopedia_reverseIndex from process_icd9_encyclopedia(icd9_encyclopedia)
    returns:
        patient_records_summary: a dictionary with patient ID as key and a list of 
        disease group names as value
    """

    patient_records_summary = {}

    # YOUR CODE HERE
    # disease_groups = set()
    for patient, icd9_codes in patient_records.items():
        disease_groups = set()
       
        for code in icd9_codes:
            disease_groups.add(icd9_encyclopedia_reverseIndex[code])
        patient_records_summary[patient] = disease_groups    
    return patient_records_summary






# Question 5 find similar patients
def getKey1(item): return item[1]

def get_patients_similarity(query_patient_records, patient_records_summary, icd9_encyclopedia_reverseIndex):
    """
    args:
        query_patient_records: same compound type as patient_records but for a test set of patients
        patient_records_summary: dictionary obtained from 
        summarize_patient_records(patient_records, icd9_encyclopedia_reverseIndex)
        icd9_encyclopedia_reverseIndex from process_icd9_encyclopedia(icd9_encyclopedia)
    returns:
        patient_similarity: a dictionary with key as test patient ID and value as a list of 2-value tuples
        The first value in the tuple is the neighbor patient ID and the second value in the tuple is the 
        similarity score between the neighbor patient and the test patient
        NOTE: the list must *not* contain the query patient ID and the similarity with the query patient themselves
    """    
    
    query_patient_records_summary = summarize_patient_records(query_patient_records, icd9_encyclopedia_reverseIndex)
    
    patient_similarity = {}
    
    # YOUR CODE HERE
    for patient, diseases in query_patient_records_summary.items():
        A= set(diseases)
        similar_list = []
        
        for neighbor, neighbor_disease in patient_records_summary.items() :
            
            if patient != neighbor:
                B = set(neighbor_disease)
                
                similarity = len(A.intersection(B)) - len(A.difference(B)) - \
                    len(B.difference(A))
                
                similar_list.append((neighbor , similarity))
        
        similar_list.sort(key=getKey1, reverse=True)
        patient_similarity[patient] = similar_list
            
            
        

    return patient_similarity




# TEST YOUR CODE BELOW THIS CONDITIONAL
if __name__ == '__main__':
    
    # Question 1
    icd9_encyclopedia = process_icd9_file("icd9_info.txt")
        
    # check
    count = 0
    print("\n\n**** output from q1 ****")
    for k,x in icd9_encyclopedia.items():
        print('group name', k, sep='\t')
        for k1,x1 in x.items():
            print(k1, x1, sep='\t')
            count+=1
        if count > 10:
            break


    # Your can load this file to compare the correctness of your outputs
    # icd9_encyclopedia_json = "icd9_encyclopedia.json"    
    # f = open(icd9_encyclopedia_json, "r")
    # x = json.load(f)
    # f.close()
            
    # Question 2
    patient_records = process_patient_data("DIAGNOSES_ICD.txt")
    
    # check
    count = 0
    print("\n\n**** output from q2 ****")
    for k,x in patient_records.items():
        print(k, x ,sep='\t')
        count += 1
        if count > 10:
            break

    # Your can load this file to compare the correctness of your outputs
    # patient_records_json = "patient_records.json"
    # f = open(patient_records_json, "r")
    # patient_records = json.load(f)
    # for k,x in patient_records.items():
    #     patient_records[k] = set(x)        
    # f.close()    
        
    
    # Question 3
    print("\n\n**** output from q3 ****")
    print(f"Average patient count {average_patient_icd9code(patient_records):.2f}")
    # Expected output: 57.28
    
    
    # Question 4
    # check
    print("\n\n**** output from q4 ****")
    icd9_encyclopedia_reverseIndex = process_icd9_encyclopedia(icd9_encyclopedia)
    count = 0
    for k,x in icd9_encyclopedia_reverseIndex.items():
        print(k, x)
        if count > 10:
            break
        count += 1
    
    patient_records_summary = summarize_patient_records(patient_records, icd9_encyclopedia_reverseIndex)
    
    # check
    print("\n\n**** output from q4 ****")
    for patId, summary in patient_records_summary.items():
        if patId in ['34','35']:
            print(patId, summary)
    # Expected output:
    # 34 {'Disorders of thyroid gland (240-246)', ...}
    # 35 {'Disorders of thyroid gland (240-246)', ...}    

    
    # Question 5
    # Choose 3 patients with # schizo, parkinson, copd ICD code
    icd9group_examples = [[295], [332], [491]] # schizo, parkinson, copd
    example_disorders_all = set([])
    for i in icd9group_examples:
        for j in i:
            example_disorders_all.add(str(j))
    
    query_patient_records = {}
    for i in icd9group_examples:
        example_disorders = set([])
        for j in i:
            example_disorders.add(str(j))
        for patId,icd9list in patient_records.items():
            if len(icd9list & example_disorders) > 0 and \
            len(icd9list & (example_disorders_all-example_disorders)) == 0:
                query_patient_records[patId] = icd9list            
                break
    
    print(query_patient_records.keys()) # dict_keys(['71', '85', '111'])
    
    patient_similarity = get_patients_similarity(query_patient_records, 
                                                 patient_records_summary, 
                                                 icd9_encyclopedia_reverseIndex)
    
    # check
    print("\n\n**** output from q5 ****")
    for k,x in patient_similarity.items():
        print(k, x[0:5])
    
    # Expected outut:
    # 71 [('2247', 1), ('1438', 0), ('2183', 0), ('4596', 0), ('750', -1)]
    # 85 [('5166', 0), ('2061', -1), ('5107', -1), ('4577', -2), ('4676', -2)]
    # 111 [('4453', 9), ('1598', 6), ('3122', 6), ('5077', 6), ('1038', 5)]
    
    
    # Your can load this file to compare the correctness of your outputs    
    # patient_similarity_json = "patient_similarity.json"
    # f = open(patient_similarity_json, "r")
    # patient_similarity = json.load(f)
    # f.close()
    
    # show 10 patients
    # for k,x in patient_similarity.items():
    #    print(k, x[0:10])
    
        
    
        








    






    






    






    






    




