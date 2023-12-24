import random
# Generate some mock data for testing
# 600 x 60 matrix of similarity scores

similarity = [[random.random() for i in range(600)] for j in range(60)]
# Write to a file
with open("similarity.txt", "w") as f:
    for i in range(60):
        for j in range(600):
            f.write(str(similarity[i][j]) + " ")
        f.write("\n")
with open("advisor.txt", "w") as f:
    for i in range(600):
        f.write(str(random.randint(0, 59)) + " ")
