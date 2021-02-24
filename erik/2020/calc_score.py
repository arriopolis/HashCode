import os
files = 'abcdef'
scores = {c:0 for c in files}
for x in os.listdir('output'):
    for c in files:
        if x.startswith(c):
            scores[c] = max(scores[c], int(x.split('.')[0].split('_')[1]))
print(sum(scores.values()))


