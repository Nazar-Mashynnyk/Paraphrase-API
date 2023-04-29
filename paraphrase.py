from nltk.tree import *
from itertools import permutations,product
from fastapi import FastAPI

app = FastAPI()

@app.get("/paraphrase")
def paraphrase(tree, limit=20):
	tree = ParentedTree.fromstring(tree)
	validNPS=[]
	for st in tree.subtrees():
		nothingElse=True
		count=0
		if st.label()=='NP':
			for sst in st.subtrees():
				if (len(sst.treeposition())-len(st.treeposition()))==1 and (sst.label() not in ['NP','CC',',']):
					nothingElse=False
				if (len(sst.treeposition())-len(st.treeposition()))==1 and sst.label()=='NP':
					count+=1	
		if count>1 and nothingElse:
			validNPS.append(st)
	nps=[]
	for i in range(len(validNPS)):
		nps.append([])
		for st in validNPS[i].subtrees():
			if (len(st.treeposition())-len(validNPS[i].treeposition()))==1 and st.label()=='NP':
				nps[i].append(str(st))
	newNPS=[]
	for i in range(len(nps)):
		newNPS.append([])
		newNPS[i].append(list(permutations(nps[i])))
	precombinations=list(product(*newNPS))
	combinations=[]
	count=0
	for i in precombinations:
		for j in i:
			combinations.append([])
			for k in j:
				combinations[count].append(k)
			count+=1
	combinations=list(product(*combinations))
	results=[]
	for i in range(len(combinations)):
		newtree=str(tree)
		to=nps
		for j in range(len(combinations[i])):
			for k in range(len(combinations[i][j])):
					newtree=newtree.replace(to[j][k],combinations[i][j][k][:len(combinations[i][j][k])//2]+'0_0_0'+combinations[i][j][k][len(combinations[i][j][k])//2:])
		newtree=newtree.replace('0_0_0','')
		newtree=newtree.replace('    ',' ')
		results.append(newtree)
	formatted=[{"tree":r} for r in results]
	return {"paraphrases":formatted}

