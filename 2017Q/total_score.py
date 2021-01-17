import os
total_score = 0
scores = {}
for file in os.listdir('output'):
    assert file.endswith('.out')
    *name,score = file[:-4].split('_')
    name = '_'.join(name)
    if name == 'example': continue
    if name not in scores: scores[name] = 0
    scores[name] = max(scores[name],int(score))
print(sum(scores.values()))
