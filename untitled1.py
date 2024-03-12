

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
    all_lines = f.readlines()
    family = ""
    diseases = {}
    for line in all_lines:

        if not line[1].isnumeric():

            if diseases != {}:
                icd9_encyclopedia[family] = diseases
                diseases = {}
            family = line.rstrip()


        else:
            diseases[line[0:4].rstrip()]=line[4:len(line.rstrip())]

    print(icd9_encyclopedia)

    f.close()

    return icd9_encyclopedia
process_icd9_file(icd9_info.txt)

# Question 1
    # icd9_encyclopedia = process_icd9_file("icd9_info.txt")

    # # check
    # count = 0
    # print("\n\n output from q1 ")
    # for k,x in icd9_encyclopedia.items():
    #     print('group name', k, sep='\t')
    #     for k1,x1 in x.items():
    #         print(k1, x1, sep='\t')
    #         count+=1
    #     if count > 10:
    #         break


    # Your can load this file to compare the correctness of your outputs
    # icd9_encyclopedia_json = "icd9_encyclopedia.json"
    # f = open(icd9_encyclopedia_json, "r")
    # x = json.load(f)
    # f.close()