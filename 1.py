


#！/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import os
import jieba
import nltk
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords






def labeled_words(path_s):
    switcher = {
        '环境200': '环境',
        '计算机200': '计算机',
        '交通214': '交通',
        '教育220': '教育',
        '经济325': '经济',
        '军事249': '军事',
        '体育450': '体育',
        '医药204': '医药',
        '艺术248': '艺术',
        '政治505': '政治',
    }
    return switcher.get(path_s, "nothing")  #此段代码类似于switch.case中的输入路径，返回对应：后的内容，无对应则默认输出nothing
words_list=[]
i=1
label = 'err'
def eachFile(filepath):
    global i   #python想在函数内修改全局变量，须用此关键字引用
    global label
    pathDir = os.listdir(filepath)      #获取当前路径下的文件名，返回List
    for s in pathDir:
        if i==1:   #用i的值来控制，只在访问文件夹时贴标签，当递归进入文件夹访问文档时，i==2，不再进行贴标签
            #print(s)
            label = labeled_words(s)
           # print(label)
        newDir=os.path.join(filepath,s)     #将文件命加入到当前文件路径后面
        if os.path.isfile(newDir) :

            if os.path.splitext(newDir)[1] == ".txt" or os.path.splitext(newDir)[1] == ".TXT":  # 判断是否是txt
                with open(newDir, 'r',errors='ignore') as f:
                    s = f.read()
                    p = s.find("【 正  文 】")
                    if p > -1:
                        p += len("【 正  文 】")
                        s = s[p:]
                    else:
                        p1 = s.find("发信站")
                        if p1 > -1:
                            p1 = s.find("\n", p1)
                            p1 += len("\n")
                            endPos = s.find("※ 来源")
                            s = s[p1 + 1:endPos]
                s="".join(s)


                seg_list = jieba.cut(s,cut_all=False)
                result=[]
                stopwords = stopwordslist("D:/stop_word.txt")
                for word in seg_list:
                    if word not in stopwords:
                     if word != '\n' and word != ' ':
                      result.append(word)




                word_str = " ".join(result)
                word_list = word_str.split(' ')

                word_dict = {}  # 空字典
                for item in word_list:
                    if item not in word_dict:
                        word_dict[item] = 1
                    else:
                        word_dict[item] += 1

                words_list.append((word_dict, label))



        else:
            i=2
            eachFile(newDir)
            i=1

eachFile("C:/Users/岑兮归无意/Documents/Tencent Files/2684581045/FileRecv/文本分类语料库/文本分类语料库")
print( words_list)
random.shuffle(words_list)
train_set,test_set=words_list[563:],words_list[:563]
classifier=nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)