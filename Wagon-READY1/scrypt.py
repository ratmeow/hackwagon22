import re
import pandas
from russian_number import *
import sys
import os
from collections import Counter

list_all = []
list_keywords = ['завод', 'год', 'номер', 'запись', 'начало']
list_comable = ["гайка", "шайба", "шайба без буксы", "гайка без буксы", "брак"]




def create_dict(list_all, name, number, year ,fact, comm):
    my_dict = {'наименование': name, 'номер': number, 'год': year, 'завод': fact, 'комментарий': comm}
    list_all.append(my_dict)


def create_text(audio):
    text = ""
    f = open(f'{audio}'+'.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        opt = re.sub(r'[^\w\s]', '', line.strip())
        text += opt + " "
    # закрываем файл
    f.close
    return text.lower()

def create_name(str):
    name=''
    i = 0
    while not str[i].isalpha() or str[i] in list_keywords:
        i += 1
        if i > (len(str) -1):
            return name
    while not str[i].isdigit() and not str[i] in list_keywords:
        name += str[i] + " "
        i += 1
        if i > (len(str) -1):
            break
    return name

def create_number(str):
    numbers=''
    i=0

    for elem in range(len(str)):
        if str[elem]=='номер' and elem!=(len(str)-1) and str[elem+1].isdigit():
            i=elem
        else:
            continue

    if i!=0:
        str = str[i+1:]

    for elem in range(len(str)):
        if str[elem].isdigit():
            numbers+=str[elem]
            if len(str[elem])>3 or (len(str[elem])<=3 and str[elem+1].isalpha()) and elem!=(len(str)-1):
                return str[elem], str[elem+1:]
            else:
                if elem!=(len(str)-2):
                    return str[elem]+str[elem+1], str[elem+2:]
        else:
            continue

def create_year(str):
    for elem in range(len(str)):
        if str[elem]=='год' and elem!=len(str)-1 and str[elem+1].isdigit():
            return str[elem+1]
        if str[elem]=='год' and str[elem-1].isdigit():
            return str[elem-1]
        elif str[elem]=='год' and elem!=len(str)-1:
            mypred=RussianNumber.text_to_number(str[elem-1])
            mynext=RussianNumber.text_to_number(str[elem+1])
            if mypred!=-1:
                return mypred
            elif mynext!=-1:
                return mynext
            else:
                continue
        else:
            continue

def create_factory(str):
    if "китай" in str:
        return "китай"
    for elem in range(len(str)):
        if str[elem]=='завод' and elem!=len(str)-1 and str[elem+1].isdigit():
            return str[elem+1]
        if str[elem]=='завод' and str[elem-1].isdigit():
            return str[elem-1]
        elif str[elem]=='завод' and elem!=len(str)-1:
            mypred=RussianNumber.text_to_number(str[elem-1])
            mynext=RussianNumber.text_to_number(str[elem+1])
            if mypred!=-1:
                return mypred
            elif mynext!=-1:
                return mynext
            else:
                continue
        else:
            continue

def extend_year(year):
    if year!=None:
        year=int(year)
        if year>=2000:
            return year
        elif year>22:
            return 1900 + year
        else:
            return 2000+year
    else:
        return None


def create_com(str):
    com = ""
    str = " ".join(str)
    for comable in list_comable:
        if comable in str:
            com=comable
    return com

def interpol(list):
    names = []
    for elem in list:
        for k, v in elem.items():
            if k == 'name':
                names.append(v)
    c = Counter(names)
    dover = 0.05
    common_value = []
    common_name = []
    for k, v in c.items():
        if v >= dover * len(names):
            common_name.append(k)
            common_value.append(v)

    for i in range(len(names)):
        if names[i] not in common_name and i != 0 and i != (len(names) - 1):
            pred = names[i-1]
            sled = names[i+1]
            pred_value, sled_value = 0, 0
            if pred in common_name:
                pred_value = common_value[common_name.index(pred)]
            if sled in common_name:
                sled_value = common_value[common_name.index(sled)]
            sum = pred_value + sled_value
            pred_prob, sled_prob = (pred_value / sum), (sled_value / sum)
            if pred_prob > sled_prob:
                names[i] = names[i-1]
            else:
                names[i] = names[i+1]
    i = 0
    for elem in list:
        for k, v in elem.items():
            if k == 'name':
                elem[k] = names[i]
                i += 1
    return list

###### MAIN


def solution(audio):
    os.system(f"whisper {audio} --language ru --model medium") # Строка для распознавания речи из файла

    #print(audio)
    temp = create_text(audio)

    text = ""
    for word in temp.split():
        if "следующ" in word:
            text+="следующий "
        elif "рам" in word:
            text+="рама "
        elif "-й" in word:
            text+=word[:-2] + " "
        elif "боков" in word:
            text+="боковая "
        elif "запис" in word:
            text += "запись "
        elif "бухсы" in word or "букса" in word:
            text += "буксы "
        elif "первый" in word or "один" in word:
            text += "1 "
        elif "второй" in word or "два" in word:
            text += "2 "
        elif "третий" in word or "три" in word:
            text += "3 "
        elif "четвертый" in word or "четыре" in word:
            text += "4 "
        elif "пятый" in word or "пять" in word:
            text += "5 "
        elif "шестой" in word or "шесть" in word:
            text += "6 "
        elif "седьмой" in word or "семь" in word:
            text += "7 "
        elif "восьмой" in word or "восемь" in word:
            text += "8 "
        elif "девятый" in word or "девять" in word:
            text += "9 "
        else:
            text+=word + " "

    #print(text)
    #substring = text[text.index("слудующий"):text.index("слудующий")]
    #print(*text.split("следующий"), sep="\n")
    mysplit = text.split("следующий")
    mysplit = [x for x in mysplit if x!=" "]
    #print(*mysplit, sep="\n")
    #print()
    #print()
    #print(len(mysplit))

    for info in mysplit:
        if ("год" in info) and ("завод" in info):
            info = info.split()
            print(info)
            name = create_name(info)
            print(name)
            if name==None or name=='' or info==None:
                continue
            checdig=False
            for elem in info:
                if elem.isdigit():
                    checdig = True
            if checdig==False:
                continue
            number, info = create_number(info)
            year = extend_year(create_year(info))
            factory = create_factory(info)
            com = create_com(info)
            #print(info)
            #print(com)

            create_dict(list_all, name.strip(), number, year, factory, com)
    #print(*list_all, sep="\n")
    result = []
    [result.append(x) for x in list_all if x not in result]
    print(*result, sep="\n")

    # УДАЛЕНИЕ ОСТАТОЧНЫХ ФАЙЛОВ
    if os.path.isfile(audio+".txt"):
        os.remove(audio + ".txt")
        os.remove(audio + ".vtt")
        os.remove(audio + ".srt")
        #os.remove(audio)
    else:
         print('Path is not a file')

    tmp=interpol(result)


    data_frame = pandas.DataFrame(tmp)
    data_frame.to_csv('wagonapp/DEMO.csv', index=False)

