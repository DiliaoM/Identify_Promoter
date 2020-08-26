import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def seperate(chrom,chromaver,signalValue,file):
    dict = {}
    for i in range(2):
        for j in range(len(chrom[i])):
            if chrom[i][j] not in dict.keys():
                dict[chrom[i][j]] = {"pos":[],"value":[]}
                for _ in range(2):
                    dict[chrom[i][j]]["pos"].append([])
                    dict[chrom[i][j]]["value"].append([])

    for i in range(len(chromaver[0])):
        dict[chrom[0][i]]["pos"][0].append(chromaver[0][i]) # 48hr
        dict[chrom[1][i]]["pos"][1].append(chromaver[1][i]) # 72hr
        dict[chrom[0][i]]["value"][0].append(signalValue[0][i]) #48hr
        dict[chrom[1][i]]["value"][1].append(signalValue[1][i]) #72hr

    for it in dict.keys():
        if len(it)>7 or len(dict[it]["pos"][1])==0:
            continue
        print(it,len(dict[it]["pos"][0]),len(dict[it]["pos"][1]))
        plotpeak(dict[it]["pos"],dict[it]["value"],file+"("+it+")")


def plotpeak(chromaver,signalValue,file):
    l1 = plt.plot(chromaver[0],signalValue[0],'ro',label = "48hrs")
    l2 = plt.plot(chromaver[1], signalValue[1], 'g+', label="72hrs")
    plt.plot(chromaver[0],signalValue[0], 'ro', chromaver[1], signalValue[1],'g+')
    plt.title('Measurement of average enrichment for the region'+"("+file+")")
    plt.xlabel('position')
    plt.ylabel('values')
    plt.legend()
    plt.show()


# Where my files are:
path = "/Users/miranda/Documents/Courses/lab/Bioinfomatics/Drosophila/ATAC-seq"

timeseries = ["48hr_","72hr_"]
reps = ["rep1","rep2","rep3"]


for r in reps:
    chromosome = []
    aver = []
    value = []
    for t in timeseries:
        file = t+r
        f = open(path+"/"+file+"/sample.narrowPeak","r")
        Contents = f.readlines()
        c = 0
        chrom = []
        chromStart  = []
        chromEnd = []
        chromaver = []
        signalValue = []
        for line in Contents:
            line = line[:-1]
            line = line.split(" ")
            line = line[0].split('\t')
            #print(line)
            chrom.append(line[0])
            chromStart.append(int(line[1]))
            chromEnd.append(int(line[2]))
            chromaver.append((int(line[1])+int(line[2]))/2)
            signalValue.append(float(line[6]))
        dataframe = pd.DataFrame({"chrom":chrom,"chromStart":chromStart,"chromEnd":chromEnd,"chromaver":chromaver,"signalValue":signalValue})
        dataframe.to_csv(file+".csv",index = False,sep=',')
        # Sorting by position in ascending order
        #df2 = dataframe.sort_values(by=["chromStart","chromEnd","chromaver","signalValue"],ascending=(True,True,True ,True))
        #df2.to_csv(file+".csv",index = False,sep=',')
        f.close()
        chromosome.append(chrom)
        aver.append(chromaver)
        value.append(signalValue)
    seperate(chromosome,aver,value,r)
    print(" ")

