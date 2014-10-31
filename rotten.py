from __future__ import division
from collections import Counter
import random 
import os 
import re 


# training dataset and a testing dataset
# function to loop over training dataset and hoepfully do the following things
# function returns word count in each phrase
# function returns a dictionary: key is the class, values is also a dictionary (key as words, values is wordcount)
# return the count of total words in each class 
# function returns a dictionary with words as keys and P(w/c) for each class
# function looks up values in prob_count() function and assign probabilities to unknown words


# randomly select the phrases 
# a dictionary with class as a key and value is another dictionary with keys like phrase id and content 

os.chdir('/Users/bearkid/Downloads')

stopWords = set(['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also',
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
	     'you', 'your'])

def split_tab(list_of_phrase):
	return [i.split('\t') for i in list_of_phrase]

def read_in(filepath,filename):
	open_file = open(filepath+filename,'r')
	data = open_file.read()
	# break it in a list 
	list_phrase = data.split('\n')
	# remove the header
	dataset = list_phrase[1:]
	return split_tab(dataset)

def split_str(string):
	# remove spaces/tabs/...
	remove_space = re.sub("[\s]+"," ",string)
	# split by space 
	list_words = remove_space.split(' ')
	# remove stop words and convert to lower case 
	return [i.lower() for i in list_words if i not in stopWords]

def turn_list_into_dict(list_of_phrase):
	big_dict = {}
	for i in list_of_phrase:
		small_dict = {}
		# some missing sentence_id
		try:
			small_dict["sentence_id"]=i[1]
		except IndexError:
			continue 
		small_dict["phrase"]=split_str(i[2])
		small_dict["sentiment"]=i[3]
		phrase_id=i[0]
		big_dict[phrase_id]=small_dict
	return big_dict 

def get_nrow(list_of_phrase):
	return len(list_of_phrase)

def generate_random(num, percent):
	return random.sample(range(1,num+1),int(percent*num))


def build_training(dictionary,select_ID):
	# create an empty list to append dictionaries 
	training_list={}
	for i in select_ID:
		if dictionary.has_key(i):
			value_i = dictionary[i]
			sentiment = value_i["sentiment"]
			value_i["phrase_id"] = i 
			if sentiment not in training_list:
				training_list[sentiment] = []
				training_list[sentiment].append(value_i)
			else:
				training_list[sentiment].append(value_i)
	return training_list


def build_testing(dictionary,select_ID):
	# create an empty list to append dictionaries 
	testing_list=[]
	for i in select_ID:
		if dictionary.has_key(i):
			testing_list.append(dictionary[i])
	return testing_list 

if __name__=="__main__":
	list_read = read_in('/Users/bearkid/Downloads/','train.tsv')
	nrow = get_nrow(list_read)
	dict_test = turn_list_into_dict(list_read)
	# dict_test.items()[0]
	# select id for training and turn them in str 
	select_id_training = [str(j) for j in generate_random(nrow, 0.7)]
	#print select_id_training[:10]
	total_id = [str(i) for i in range(1,nrow+1)]
	#print total_id[:10]
	training_set = build_training(dict_test,select_id_training)
	# the remaining id goes for testing turn them in str 
	select_id_testing = list(set(total_id)-set(select_id_training))
	testing_set = build_testing(dict_test,select_id_testing)
	print testing_set[:2]






	


	

	




	
















