import json


d = json.load(open('data.json'))
t = {}
for i in d:
    if t.get(i['url']) is None:
        t[i['url']] = 1
    else:
        print(d.index(i))
