### Libraries
import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
import re
import openpyxl
import tabulate
### Functions

def line_to_list(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        columns = [line.strip().split(' ') for line in lines]
        return columns

def remove_empty_elements(lst):
    new_lst = [elem for elem in lst if elem not in ['',[], None]]
    return new_lst

def extract_elements(lst, length):
    new_lst = [elem for elem in lst if lst[0][0][0]=='2' or lst[0][0][0]=='0']
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
input1 = str(input('Enter Filename in txt format'))
lines = line_to_list(input1)
new_list2 = [remove_empty_elements(elem2) for elem2 in lines]
my_new_lst = [extract_elements(elem, 7) for elem in new_list2]
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
    
student_final = [elem[0:3] for elem in my_new_lst2[::2]]
student_df = pd.DataFrame(student_final, columns=['roll_no','gender','full_name'])

my_new_lst3 = my_new_lst2.copy()
for elem in my_new_lst3[::2]:
    del elem[0:3]

n=6
for elem in my_new_lst3[::2]:
    if 'ESSENTIAL' in elem:
        elem[n] += ' ' + elem[n+1]
        del elem[n+1]
    else:
        pass

compart = []
for elem in my_new_lst3[::2]:
    if elem[6]!='COMP':
        compart.append('None')
    else:
        compart.append(' '.join(elem[7:])) 
        del elem[7:]

result = []
for elem in my_new_lst3[::2]:
    result.append(elem[-1])
    del elem[-1]

marks1 = []
for elem in my_new_lst3[1::2]:
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
for elem in my_new_lst3[::2]:
    sub_code.append(elem)

both_type_marks = []
for elem1 in sub_code:
    for elem2 in marks1:
        if sub_code.index(elem1) == marks1.index(elem2):
            zipped = zip(elem1,elem2)
            both_type_marks.append(dict(zipped))

standard_marks = []
for elem1 in sub_code:
    for elem2 in marks:
        if sub_code.index(elem1) == marks.index(elem2):
            zipped = zip(elem1,elem2)
            standard_marks.append(dict(zipped))

graded_marks = []
for elem1 in sub_code:
    for elem2 in grades:
        if sub_code.index(elem1) == grades.index(elem2):
            zipped = zip(elem1,elem2)
            graded_marks.append(dict(zipped))

df1 = pd.DataFrame(standard_marks)
df2 = pd.DataFrame(graded_marks)
df3 = pd.DataFrame(both_type_marks)

df_result = pd.Series(result, name='result')
df_compart = pd.Series(compart, name='compart')

input2 = str(input('Do you want standard marks,graded marks or both type'))

if input2 =='standard marks':
    cbse_result = pd.concat([student_df,df1,df_result,df_compart], axis=1)
elif input2 =='graded marks':
    cbse_result = pd.concat([student_df,df2,df_result,df_compart], axis=1)
elif input2 =='both type':
    cbse_result = pd.concat([student_df,df3,df_result,df_compart], axis=1)

print(cbse_result)

input3 = str(input('Type the resultant format you want:csv,excel,json,html,latex'))
# Get you file in all essential formats:
if input3=='csv':
      # csv format
    cbse_result.to_csv('cbse_result.csv',index=False)
elif input3=='excel':
    # Excel format
    cbse_result.to_excel('my_data.xlsx', index=False)   
elif input3=='json':
    # JSON format
    cbse_result.to_json('my_data.json', orient='records')   
elif input3=='html':
    # HTML format
    cbse_result.to_html('my_data.html', index=False)   
elif input3=='latex':
    # LaTeX format
    cbse_result.to_latex('my_data.tex', index=False)   

print('Your file has been exported')



