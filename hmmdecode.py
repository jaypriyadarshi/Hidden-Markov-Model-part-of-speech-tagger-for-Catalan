import sys
import operator
import math


filename = sys.argv[1]
o = open('hmmmodel.txt','r')
f = open(filename,'r')
f1 = open('hmmoutput.txt','w')

c = o.readlines()
c[0] = c[0][:-1]
transistion_mat = eval(c[0])
c[1] = c[1][:-1]
emission_mat = eval(c[1])
tag_dict = eval(c[2])

content = f.readlines()

states = transistion_mat.keys()
states.remove('q0')

for data in content:
	data =  data[:-1]
	probability_mat = {}
	backpointer_mat = {}
	word_tags = {}
	prev_states = {}
	tokens = data.split(" ")
	sent_length = len(tokens)
	probability_mat[0] = {}
	backpointer_mat[0] = {}
	for i in states:
		if tokens[0] in emission_mat[i]:
			probability_mat[0][i] = math.log(transistion_mat['q0'][i])+math.log(emission_mat[i][tokens[0]])
		else:
			probability_mat[0][i] = -10000000
		backpointer_mat[0][i] = 'q0'
	prev_states[0] = states
	for t in xrange(1,sent_length):
		probability_mat[t] = {}
		backpointer_mat[t] = {}
		#print probability_mat[1]
		if tokens[t] in tag_dict:
			lis = tag_dict[tokens[t]]
			for q in lis:
				probability_mat[t][q] = max(probability_mat[t-1][q1]+math.log(transistion_mat[q1][q])+math.log(emission_mat[q][tokens[t]]) for q1 in prev_states[t-1])
				backpointer_mat[t][q] = max((probability_mat[t-1][q1]+math.log(transistion_mat[q1][q]),q1) for q1 in prev_states[t-1])[1]
			prev_states[t] = lis 
		else:
			for q in states:
				probability_mat[t][q] = -10000000
				backpointer_mat[t][q] = max((probability_mat[t-1][q1]+math.log(transistion_mat[q1][q]),q1) for q1 in prev_states[t-1])[1]
			prev_states[t] = states
			
	max_p = max((probability_mat[sent_length-1][q1],q1) for q1 in prev_states[sent_length-1])[1]
	j = sent_length-2
	opt = [max_p]
	while j>=0:
		max_p = backpointer_mat[j+1][max_p]
		opt.insert(0,max_p)
		j = j-1
	
	for i in xrange(sent_length):
		f1.write(tokens[i]+"/"+opt[i])
		if i!=sent_length-1:
			f1.write(" ")
	f1.write("\n")
