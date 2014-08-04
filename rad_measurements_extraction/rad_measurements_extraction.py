#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# rad_measurements_extraction.py
# python script to extract radiation measurements reports
# from small text strings such as tweets

# by Antonin Segault <antonin.segault@edu.univ-fcomte.fr>
# ELLIADD lab, Université de Franche-Comté, France
# written during Digital Methods Initiative's Summer School 2014
# see also https://wiki.digitalmethods.net/Dmi/DmiSummer2014MappingTheJDArchive
# shared under Creative Commons CC-BY-SA 3.0 France
# http://creativecommons.org/licenses/by-sa/3.0/fr/


########## Use ########## 

# input : a text file with a tweet (only the text content) per line
# output : three files, one for each unit (Gray, Sivert, CPM)
# on each line, the tweet and the amount extracted, tab separated

# if several measurements are found in one tweet, several lines
# will appear in the output files, with the same tweet and
# the different measurements


########## configuration ##########

# the file containing the tweets to be processed
input_file = 'rad_measurements_tweets.csv'
# the output files for each unit
output_cpm = 'rad_measurements_cpm.csv'
output_gy = 'rad_measurements_gy.csv'
output_sv = 'rad_measurements_sv.csv'


########## initialisation ##########

import re
# a regular expression matching measurements
exp = re.compile(u'((?![,.])[0-9\uff10-\uff19]+([,.][0-9\uff10-\uff19]+)? ?([nμµum]?([Ss][Vv]|[Gg][Yy])/[Hh]|[Cc][Pp][Mm]))', re.U)
# a regular expression matching measurement amounts
exp_num = re.compile(u'([0-9\uff10-\uff19]+([,.][0-9\uff10-\uff19]+)?)', re.U)
# the number of rows processed
num_row = 0
# the number of measurements found
num_rad = 0


########## data processing ##########

with open(input_file) as tab :
	# processing each tweet
	for tweet in tab :
		# finding matching parts of the tweet
		items = exp.findall(tweet)
		# processing each tweet fragment
		for i in items :
			item = i[0]
			# uncomment the next line for debugging outputs
			# print item
			num = exp_num.match(item)
			if num is not None :
				# for the matching unit, the amount is converted 
				# and then written on the output file
				num = num.group().replace(',', '.')
				num = float(num)
				low = item.lower()
				
				########## CPM measurements ########## 
				
				if low.find('cpm') >= 0 :
					out_cpm = open(output_cpm, 'a')
					out_cpm.write(tweet[:-1] +  '\t' + "%.1f" % num + '\n')
					out_cpm.close()
					
				########## Gray measurements ########## 
				
				elif low.find('gy') >= 0 :
					if low.find('ngy') >= 0 :
						num = 0.000000001 * num
					elif low.find('ugy')  >= 0 or low.find('μgy')  >= 0 or low.find('µgy') >= 0  :
						# there is a trick on the previous line : in UTF-8,
						# there are two "µ" characters, the greek letter and
						# the mathematical symbol. They look exactly the same
						# but have different UTF codes
						num = 0.000001 * num
					elif low.find('mgy')  >= 0 :
						num = 0.001 * num
					out_gy = open(output_gy, 'a')
					out_gy.write(tweet[:-1] +  '\t' + "%.9f" % num + '\n')
					out_gy.close()
					
				########## Sievert measurements ########## 
				
				elif low.find('sv') >= 0 :
					if low.find('nsv') >= 0 :
						num = 0.000000001 * num
					elif low.find('usv')  >= 0 or low.find('μsv') >= 0  or low.find('µsv') >= 0  :
						num = 0.000001 * num
					elif low.find('msv')  >= 0 :
						num = 0.001 * num
					out_sv = open(output_sv, 'a')
					out_sv.write(tweet[:-1] +  '\t' + "%.9f" % num + '\n')
					out_sv.close()
					
				num_rad = num_rad + 1
		num_row = num_row + 1

# displaying basic stats when the program ends
print str(num_row) + " rows processed"
print str(num_rad) + " measurements found"
