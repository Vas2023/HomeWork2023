#from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
#import csv
'''
with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)
'''
# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
import pandas as pd

df=pd.read_csv('phonebook_.csv')#  создаем таблицу (9x8) в панде

for i in range (len(df)):
    s = df.loc[i, 'lastname'].split(' ')
    for k in range(len(s)):
        df.loc[i, 'lastname'] =s[0]
        if len(s)>=2:df.loc[i, 'firstname'] = s[1]
        if len(s) >= 3: df.loc[i, 'surname'] = s[2]
    s_firstname=df.loc[i, 'firstname'].split(' ')
    for l in range(len(s_firstname)):
        df.loc[i, 'firstname'] = s_firstname[0]
        if len(s_firstname) >= 2: df.loc[i, 'surname'] = s_firstname[1]
df['item_lower']=df['lastname'].str.lower()


# Консолидируем строки и избавляемся от NaN значений
cons = df.groupby('item_lower').first().reset_index()
def phone_standart(ph_str):
    ph_str = re.sub('\s', '', ph_str) # удаляем пробелы
    pt_dop = r'\(доб\.(\d{4})\)'               #ищем (доб.ХХХХ) заменяем на доб.ХХХХ
    if re.search(pt_dop,ph_str) != None:
        ph_str=re.sub(pt_dop,r'доб.\1',ph_str)

    pt_7= r'7(\d{3})(\d{3})(\d{2})(\d{2})'#7XXXXXXXXXX
    if re.search(pt_7, ph_str) != None:
        ph_str =re.sub(pt_7,r'+7'+r'('+'\\1'+r')'+r'\2'+r'-'+r'\3'+r'-'+r'\4',ph_str)

    pt_8 = r'8(\()*(\d{3})(\))*([-])*(\d{3})[-](\d{2})([-])*(\d{2})' #8XXX-XXX-XXXX
    if re.search(pt_8, ph_str) != None:                           #8(XXX)-XXX-XX-XX
        ph_str =re.sub(pt_8,r'+7'+r'('+'\\2'+r')'+r'\5'+r'-'+r'\6'+r'-'+r'\8',ph_str)
    return ph_str

for index, row in cons.iterrows():
    value=row['phone']
    cons.loc[index,'phone']=phone_standart(cons.loc[index,'phone'])
# Печатаем результат
'''
print(cons['lastname'],'\n',
      cons['firstname'],'\n',
      cons['surname'],'\n',
      cons['organization'],'\n',
      cons['position'],'\n',
      cons['phone'],'\n',
      cons['email'])
'''
cons=cons.drop('item_lower',axis=1)
cons.to_csv('phonebook_new.csv', index=False)

'''

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)
'''