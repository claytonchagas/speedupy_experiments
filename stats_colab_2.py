import statistics
import sys

#data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def main(_x=4,_y=5):
    o = sys.argv[1]
    f = open(o, "r")
    data = []
    for x in f.readlines()[_x::_y]:
    #for x in f.read().splitlines()[1::2]:
    #for i in range(0, len(f1)):
        data.append(float(x))
    f.close()
    print(data)
    print("Max:", max(data))
    print("Min:", min(data))
    print("Mean:", statistics.mean(data))
    print("Median:", statistics.median(data))
    print("Standard deviation:", statistics.stdev(data))
    print("Variance:", statistics.variance(data))

    

    # for i in range(0, len(data)):
    #     if(i % 2 != 0):
    #         print(data[i])
    
    # for i in range(1, len(data), 2):
    #     print(data[i])

    # for i in data[::2]:
    #     print(data[i])


if __name__=="__main__":
    try:
        main(int(sys.argv[2]),int(sys.argv[3]))
    except IndexError:
        main()
