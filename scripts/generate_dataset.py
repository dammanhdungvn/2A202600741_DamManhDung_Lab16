import json
with open('data/hotpot_mini.json') as f:
    mini = json.load(f)

res = []
for i in range(15):
    for item in mini:
        new_item = dict(item)
        new_item['qid'] = f"{item['qid']}_{i}"
        res.append(new_item)

with open('data/evaluation_100.json', 'w') as f:
    json.dump(res, f, indent=2)

