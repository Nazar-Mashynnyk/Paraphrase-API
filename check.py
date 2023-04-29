import requests
import json


ip='http://127.0.0.1:8000'
tree='(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS restaurants) ) ) ) ) ) ) )'
limit=20
url = ip+"/paraphrase?tree="+tree+"&limit="+str(limit)

response = requests.get(url)

if response.status_code == 200:
    paraphrases = response.json()
    js=json.dumps(paraphrases,indent=2)
    with open('result.json','w', encoding="utf-8") as f:
        f.write(js)
else:
	print('Some error happened')