import os

d = {}
for filename in os.listdir('res'):
    problem, score = filename.split('/')[-1].split('.')[0].split('_')
    if problem not in d: d[problem] = 0
    d[problem] = max(d[problem], int(score))
print(sum(d.values()))
