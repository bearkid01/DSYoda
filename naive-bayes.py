from __future__ import division
import os
import random
import re
import sys
from collections import Counter 
import math


# add stop words
stopWords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also',
             'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be',
	     'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear',
	     'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for',
	     'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers',
	     'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is',
	     'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may',
	     'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor',
	     'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our',
	     'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since',
	     'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then',
	     'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us',
	     've', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
	     'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet',
	     'you', 'your']


# function creates a dictionary to store all the files names for "pos" and "neg" classes
def get_file_book(pathspec):
    global fullpath 
    fullpath=os.path.abspath(pathspec)
    file_book={}
    for i in ['pos','neg']:
	file_book[i]=[]
	for j in os.listdir(fullpath+'/'+i):
	    file_book[i].append(j)
    return file_book 

# function randomly selects 1/3 of the "pos" data set as testing and the rest as training 
# does the same thing for "neg" data set 
def subset_files(file_book):
    training={}
    testing={}
    testing['pos']=random.sample(file_book['pos'],int(len(file_book['pos'])/3))
    training['pos']=[i for i in file_book['pos'] if i not in testing['pos']]
    testing['neg']=random.sample(file_book['neg'],int(len(file_book['neg'])/3))
    training['neg']=[i for i in file_book['neg'] if i not in testing['neg']]
    return training, testing

# function takes a filename and a classname and then fetches the text from the file 
# also removes the stop words and splits the text into words 
def get_words(filename,classname):
    filepath=fullpath+"/"+classname+"/"+filename
    f=open(filepath,"r")
    s=f.read()
    d=re.sub("[\s]+"," ",s)
    #for c in string.punctuation:
        #d.replace(c,"")
    words=d.split(" ")
    stopWord=set(stopWords)
    words=[t for t in words if t not in stopWord] 
    return words

# function returns word count in each document 
def word_count_in_doc(filename,classname):
    words=get_words(filename,classname) 
    wc_in_doc=Counter(words)
    return wc_in_doc
 
# function takes a dataset,i.e. training and returns a dictionary of words as keys and counts as values for each class
def word_count(dataset):
    dic={}
    for i in dataset:
        dic[i]=[]
        for j in dataset[i]:
            words=get_words(j,i)
            dic[i]+=words
        dic[i]=Counter(dic[i])
    return dic

# function returns the count of unique words from "neg" and "pos" class combined
def unique_count(dictionary):
    count=set()
    for i in dictionary:
        count|=set(dictionary[i].keys())
    return len(count)

# function returns a dictionary with words as keys and P(w/c) as values for each class
def prob_count(dic,unique_word):
    for i in dic:
        count_c=word_count_class(i,dic)
        for j in dic[i]:
            dic[i][j]=(dic[i][j]+1)/(count_c+unique_word+1)
    return dic

# function returns the count of total words in a class, i.e. "pos" or "neg" 
def word_count_class(classname,dic):
    return sum(dic[classname].values())

# function looks up value in prob_count() function and assigns probabilities to unknown words 
def prob_cal(word,prob,unique_w,c_count,classname):
    if word in prob[classname]:
        return prob[classname][word]
    else:
        return 1/(1+c_count+unique_w)

# main() function basically conducts three tests on the unigram model and calculates the average accuracy
def main():
    # use sys.argv function to get the name of the directory containing "pos" and "neg" text files 
    pathspec=sys.argv[-1]
    three_iter_result=[]
    file_book=get_file_book(pathspec)
    for t in range(3):
	#randomly selects 1/3 data as testing data set and the rest goes to training data set 
        training,testing=subset_files(file_book)
 	#p_cp is the P(c) value for the "pos" class and p_cn is the P(c) value for the "neg" class 
	p_cp=len(training['pos'])/(len(training['pos'])+len(training['neg']))
	p_cn=len(training['neg'])/(len(training['pos'])+len(training['neg']))
        dic=word_count(training)
        count_uw=unique_count(dic)
        prob_training=prob_count(dic,count_uw)
        pos_wc=word_count_class("pos",dic)
        neg_wc=word_count_class("neg",dic)
	#result is a dictionary of two keys, "pos" and "neg" and values are the count of how many of each are classified as "pos"
        result={}
        for i in testing:
            result[i]=0
            for k in testing[i]: #k represents each document 
                word_list_in_doc=word_count_in_doc(k,i)
	        #here initializes p,q to compute the P(c/d) values for each document 
                p=0
		q=0
                for j in word_list_in_doc:
                    word_freq=word_list_in_doc[j]
                    p+=math.log(prob_cal(j,prob_training,count_uw,pos_wc,"pos"))*word_freq
                    q+=math.log(prob_cal(j,prob_training,count_uw,neg_wc,"neg"))*word_freq 
                p=p+math.log(p_cp)
		q=q+math.log(p_cn)
		#predict the class c* based on the P(c/d) values calculated above 
	        #if p>q, then classify this document as "pos" and count increases by 1;
		#if p<q, then classify this document as "neg" and count doesn't change 
		if p>q:
                    result[i]+=1        
	correct_neg=len(testing['neg'])-result['neg']
        correct_pos=result['pos']
	num_test_neg=len(testing['neg'])
	num_test_pos=len(testing['pos'])
	accuracy=(correct_neg+correct_pos)/(num_test_neg+num_test_pos)
	print 'iteration %d:' % (t+1)
	print 'num_pos_test_docs: %d' % num_test_pos
	print 'num_pos_training_docs: %d' % len(training['pos'])
        print 'num_pos_correct_docs: %d' % correct_pos
	print 'num_neg_test_docs: %d' % num_test_neg
	print 'num_neg_training_docs: %d' % len(training['neg'])
	print 'num_neg_correct_docs: %d' % correct_neg
        print 'accuracy: %.0f'% (accuracy*100)+'%'

        three_iter_result.append(accuracy)
    print 'ave_accuracy: %.1f' % ((sum(three_iter_result)/3)*100)+'%'


if __name__=="__main__":
    main()
    

        

                
        
        
    
    
    

    


        
        
        
        
        
        

    
    







            
            
        
