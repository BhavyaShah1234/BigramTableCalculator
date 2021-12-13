import numpy as np
import pandas as pd

n = int(input('ENTER NUMBER OF SENTENCES IN CORPUS: '))
sentences = []

for i in range(n):
    sentence = input(f'ENTER SENTENCE {i+1}(WITHOUT <s> AND </s>): ')
    sentence = '<s> ' + sentence + ' </s>'
    sentence = sentence.split(' ')
    sentences.append(sentence)

unique = []
for i in range(n):
    unique.extend(sentences[i])
unique = list(set(unique))
unique.sort()

total_count = {}
for i in unique:
    total_count[i] = 0

for i in range(len(unique)):
    for j in range(n):
        for k in range(len(sentences[j])):
            if sentences[j][k] == unique[i]:
                total_count[unique[i]] += 1

print(total_count)

matrix = np.zeros(shape=(len(unique), len(unique)))

for i in range(len(unique)):
    for j in range(len(unique)):
        present = unique[i]
        future = unique[j]
        for k in range(n):
            for l in range(len(sentences[k]) - 1):
                if sentences[k][l] == present and sentences[k][l+1] == future:
                    matrix[i][j] += 1

matrix = pd.DataFrame(matrix, columns=unique, index=unique)

for i in unique:
    for j in unique:
        matrix[i][j] = matrix[i][j] / total_count[j]

matrix.to_csv('bigram_probability_table.csv')
