import sys

filename = sys.argv[1]
o = open('hmmmodel.txt','w')
f = open(filename,'r')

content = f.readlines()

transistion_mat = {}
emission_mat = {}
total_tags = {}
tag_dict = {}

tag_names = []

for data in content:
	data = data[:-1]
	tokens = data.split(" ")
	sent_length = len(tokens)
	for i in range(sent_length):
		if i == 0:
			first = tokens[i].split("/")
			tag1 = first[-1]

			if tag1 not in tag_names:
				tag_names.append(tag1)

			if 'q0' not in transistion_mat:
				transistion_mat['q0'] = {}
			
			if tag1 in transistion_mat['q0']:
				transistion_mat['q0'][tag1] += 1
			else:
				transistion_mat['q0'][tag1] = 1

		if i!=sent_length-1:
			
			first = tokens[i].split("/")
			second = tokens[i+1].split("/")
			tag1 = first[-1]
			tag2 = second[-1]
			if tag1 not in tag_names:
				tag_names.append(tag1)
			if tag2 not in tag_names:
				tag_names.append(tag2)
			
			if tag1 not in transistion_mat:
					transistion_mat[tag1] = {}

			if tag2 in transistion_mat[tag1]:
				transistion_mat[tag1][tag2] += 1
			else:
				transistion_mat[tag1][tag2] = 1

		first_term = tokens[i].split("/")
		word = first_term[:-1]
		if len(word)>1:
			word = '/'.join(word)
		else:
			word = word[0]
		#word = word.lower()
		tag = first_term[-1]

		if word in tag_dict:
			if tag not in tag_dict[word]:
				tag_dict[word].append(tag)
		else:
			tag_dict[word] = [tag]

		if tag not in emission_mat:
			emission_mat[tag] = {}
		if word in emission_mat[tag]:
			emission_mat[tag][word] += 1
		else:
			emission_mat[tag][word] = 1

		if tag in total_tags:
				total_tags[tag] += 1
		else:
				total_tags[tag] = 1



for i in transistion_mat.iterkeys():
	temp = tag_names[:]
	total = 0

	for j in transistion_mat[i].iterkeys():
		temp.remove(j)
		#transistion_mat[i][j] += 1
	for j in temp:
		transistion_mat[i][j] = 0

	#for j in transistion_mat[i].iterkeys():
	total = sum(transistion_mat[i].values())

	for j in transistion_mat[i].iterkeys():
		transistion_mat[i][j] = float(transistion_mat[i][j]+1)/(total+len(transistion_mat[i]))
for i in emission_mat.iterkeys():
	for j in emission_mat[i].iterkeys():
		emission_mat[i][j] = float(emission_mat[i][j])/total_tags[i]

s = str(transistion_mat)+"\n"+str(emission_mat)+"\n"+str(tag_dict)
o.write(s)

o.close()
f.close()
		
			
