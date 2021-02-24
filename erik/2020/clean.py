import os
files = 'abcdef'
scores = {c:0 for c in files}
for x in os.listdir('output'):
    for c in files:
        if x.startswith(c):
            scores[c] = max(scores[c], int(x.split('.')[0].split('_')[1]))

for x in os.listdir('output'):
    for c in files:
        if x.startswith(c):
            score = int(x.split('.')[0].split('_')[1])
            if scores[c] != score:
                os.remove(os.path.join('output',x))
                print(x)
print(sum(scores.values()))


