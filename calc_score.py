import os
scores = {c:0 for c in 'abcde'}
for x in os.listdir('res'):
    for c in 'abcde':
        if x.startswith(c):
            scores[c] = max(scores[c], int(x.split('.')[0].split('_')[1]))
print(sum(scores.values()))
