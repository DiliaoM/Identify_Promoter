from Find_common import counts_atac_seq
import pandas as pd
import matplotlib.pyplot as plt

timeseries = ["48hr_","72hr_"]
reps = ["rep1","rep2","rep3"]



# Find the peak values in ATAC-seq data
def get_peakvalue():
    peak = {}
    for t in timeseries:
        chromosome = {"rep1": {}, "rep2": {}, "rep3": {}}
        chr = []
        for r in reps:
            file = t + r
            f = open("./" + file + ".csv")
            next(f)
            Contents = f.readlines()
            chrom = {}
            f.close()
            for line in Contents:
                line = line[:-1]
                line = line.split(",")
                if len(line[0]) > 7:
                    continue
                if line[0] not in chrom.keys():
                    chrom[line[0]] = {"pos": [], "value": []}
                    chr.append(line[0])
                chrom[line[0]]["pos"].append([int(line[1]),int(line[2])])
                chrom[line[0]]["value"].append(float(line[4]))
            chromosome[r] = chrom
        peak[t] = chromosome
        chr = list(set(chr))
    return peak



## Find the peak value of each position in ATAC-seq data
def find_value(positions,peak_values):
    res = []
    i = 0
    j = 0
    positions.sort()
    while(i<len(positions)):
        while(peak_values["pos"][j][1]<positions[i]):
            j += 1
        res.append(peak_values["value"][j])
        i += 1
    return res


datalist = counts_atac_seq()
peak_values = get_peakvalue()
for t in datalist.keys():
    chrom = []
    positions = []
    rep1 = []
    rep2 = []
    rep3 = []
    for chr in datalist[t].keys():

        for pos in datalist[t][chr]:
            chrom.append(chr)
            positions.append(pos)
        if chr in peak_values[t]["rep1"].keys():
            rep1 += find_value(datalist[t][chr], peak_values[t]["rep1"][chr])
        if chr in peak_values[t]["rep2"].keys():
            rep2 += find_value(datalist[t][chr], peak_values[t]["rep2"][chr])
        if chr in peak_values[t]["rep3"].keys():
            rep3 += find_value(datalist[t][chr], peak_values[t]["rep3"][chr])
    dataframe = pd.DataFrame({"Chrom":chrom,"pos":positions,"rep1_value":rep1,"rep2_value":rep2,"rep3_value":rep3})
    df2 = dataframe.sort_values(by=["Chrom","pos"],ascending=(True,True))
    df2.to_csv(t+"ATAC_seq_peaks.csv",index=False,sep=",")
