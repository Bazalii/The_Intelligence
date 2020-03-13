f = open('input.txt', 'r')
for i in range(2):
    f.readline()
input_data = f.readline()
input_data = list(map(float, input_data.split()))
for i in range(len(input_data)):
    print(input_data[i])