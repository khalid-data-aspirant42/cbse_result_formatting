### Libraries
import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
import re
### Functions

def line_to_list(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        columns = [line.strip().split(' ') for line in lines]
        return columns

def remove_empty_elements(lst):
    new_lst = [elem for elem in lst if elem not in ['',[], None]]
    return new_lst

def extract_elements(lst):
    new_lst = [elem for elem in lst if lst[0][0][0]=='2' or lst[0][0][0]=='0' or lst[0]=='AB']
    return new_lst

def add_last_few_strings(lst,n):
    # Get the last 'n' elements of the list and join them into one string
    string = " ".join(lst[n:])
    
    # Remove the last 'n' elements from the original list and add the new string to the end
    lst = lst[:n]
    lst.append(string)
    
    # Return the updated list
    return lst

# ------------ main part ---------
filename = str(input('Enter the txt filename kept in the same folder'))
lines = line_to_list(filename)
new_list2 = [remove_empty_elements(elem2) for elem2 in lines]
my_new_lst = [extract_elements(elem) for elem in new_list2]
my_new_lst2 = remove_empty_elements(my_new_lst)  # this is the main result

for elem in my_new_lst2[::2]:
    if bool(re.search(r"\d+",elem[3]))==True:
        n=2
        elem[n] = elem[n]
    elif bool(re.search(r"\d+",elem[4]))==True:
        n=2
        elem[n] += ' ' + elem[n+1]
        del elem[n+1]
    elif bool(re.search(r"\d+",elem[5]))==True:
        n=2
        elem[n] += ' ' + elem[n+1]
        del elem[n+1]
        elem[n] += ' ' + elem[n+1]
        del elem[n+1]
    
student_final = []
for elem in my_new_lst2[::2]:
    student_final.append(elem[0:3])
student_df = pd.DataFrame(student_final, columns=['roll_no','gender','full_name'])

my_new_lst3 = my_new_lst2.copy()
for elem in my_new_lst3[::2]:
    del elem[0:3]

# -----------
import copy

my_new_lst4 = copy.deepcopy(my_new_lst3)

if bool(re.search(r"\d+",my_new_lst3[2][5][0]))==False:
    n1=8
    n2=5
else:
    n1=6 
    n2=6   
for elem in my_new_lst4[::2]:
    if 'ESSENTIAL' in elem:
        elem[n1] += ' ' + elem[n1+1]
        del elem[n1+1]
    else:
        pass

if bool(re.search(r"\d+",my_new_lst3[2][5][0]))==False:
    extra_grade = []
    for elem in my_new_lst4[::2]:
        extra_grade.append(elem[5:8])
        del elem[5:8]
    extra_grade_df = pd.DataFrame(extra_grade, columns=['Grade1','Grade2','Grade3'])
else:
    pass


compart = []
for elem in my_new_lst4[::2]:
    if elem[n2]!='COMP':
        compart.append('')
    else:
        compart.append(' '.join(elem[n2+1:])) 
        del elem[n2+1:]

# -----------

result = []
for elem in my_new_lst4[::2]:
    result.append(elem[-1])
    del elem[-1]

marks1 = []
for elem in my_new_lst4[1::2]:
    new_list = []
    for i in range(0, len(elem)-1,2):
        new_list.append(elem[i] + " " + elem[i+1])  
    marks1.append(new_list)

marks = []
for elem1 in marks1:
    list1 = []
    for elem in elem1:
        list1.append(elem.split(' ')[0])
    marks.append(list1)

grades = []
for elem1 in marks1:
    list1 = []
    for elem in elem1:
        list1.append(elem.split(' ')[1])
    grades.append(list1)


sub_code = []
for elem in my_new_lst4[::2]:
    sub_code.append(elem)

# -------------

standard_marks = []
for i in range(len(sub_code)):
    if bool(re.search(r"\d+",my_new_lst3[2][5][0]))==False:
        temp_dict1 = {sub_code[i][n]: marks[i][n] for n in range(5)}
    else:
        temp_dict1 = {sub_code[i][n]: marks[i][n] for n in range(6)} 
    standard_marks.append(temp_dict1)

graded_marks = []
for i in range(len(sub_code)):
    if bool(re.search(r"\d+",my_new_lst3[2][5][0]))==False:
        temp_dict2 = {sub_code[i][n]: grades[i][n] for n in range(5)}
    else:
        temp_dict2 = {sub_code[i][n]: grades[i][n] for n in range(6)}
    graded_marks.append(temp_dict2)

both_type_marks = []
for i in range(len(sub_code)):
    if bool(re.search(r"\d+",my_new_lst3[2][5][0]))==False:
        temp_dict3 = {sub_code[i][n]: marks1[i][n] for n in range(5)}
    else:
        temp_dict3 = {sub_code[i][n]: marks1[i][n] for n in range(6)}
    both_type_marks.append(temp_dict3)

# -------------

df1 = pd.DataFrame(standard_marks)
df2 = pd.DataFrame(graded_marks)
df3 = pd.DataFrame(both_type_marks)
# extra_grade_df
df_result = pd.Series(result, name='result')
df_compart = pd.Series(compart, name='compart')

if bool(re.search(r"\d+",my_new_lst3[2][5][0]))==False:
    cbse_result = pd.concat([student_df,df3,extra_grade_df,df_result,df_compart], axis=1)
else:
    cbse_result = pd.concat([student_df,df3,df_result,df_compart], axis=1)

print(cbse_result)
import os
if bool(re.search(r"\d+",my_new_lst3[2][5][0]))==False:
    filename = "class_12.xlsx"
    counter = 1
    while os.path.exists(filename):
        filename = f"class_12_{counter}.xlsx"
        counter += 1
    cbse_result.to_excel(filename, index=False)
else:
    filename = "class_10.xlsx"
    counter = 1
    while os.path.exists(filename):
        filename = f"class_10_{counter}.xlsx"
        counter += 1
    cbse_result.to_excel(filename, index=False)




