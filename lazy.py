def word_gen(file):
    for line in file:
        for word in line.split():
            print ('\"'+ str(word).lower()+'\"', end=", ")

with open('test.txt') as f:
    word_gen(f)