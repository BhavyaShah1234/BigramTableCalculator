import numpy as np
import pandas as pd

smoothing = True

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

print(f'WORD COUNT: {total_count}')

v = 0
for i in total_count:
    v += total_count[i]
print(f'V: {v}')

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
print(f'COUNT MATRIX:\n{matrix}')

if smoothing:
    smooth_matrix = np.zeros_like(matrix)
    smooth_matrix = pd.DataFrame(smooth_matrix, columns=unique, index=unique)
    for i in unique:
        for j in unique:
            if matrix[i][j] == 0:
                smooth_matrix[i][j] = (matrix[i][j] + 1) / (total_count[j] + v)
            else:
                smooth_matrix[i][j] = matrix[i][j] / total_count[j]
    print(f'SMOOTHING:\n{smooth_matrix}')
    smooth_matrix.to_csv('bigram_probability_table_with_smoothing.csv')

non_smooth_matrix = np.zeros_like(matrix)
non_smooth_matrix = pd.DataFrame(non_smooth_matrix, columns=unique, index=unique)
for i in unique:
    for j in unique:
        non_smooth_matrix[i][j] = matrix[i][j] / total_count[j]
print(f'WITHOUT SMOOTHING:\n{non_smooth_matrix}')

non_smooth_matrix.to_csv('bigram_probability_table_without_smoothing.csv')
