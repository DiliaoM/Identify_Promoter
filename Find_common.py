

timeseries = ["48hr_","72hr_"]
reps = ["rep1","rep2","rep3"]
labels = ["ro","g+","b."]

def overlap(chromosome,chr):
    pos = {}
    for c in chr:
        for r in chromosome.keys():
            if c not in chromosome[r].keys():
                chromosome[r][c] = []
        pos[c] = []
        i = j = k = 0
        #chromosome[0][c].sort()
        #chromosome[1][c].sort()
        #chromosome[2][c].sort()
        while i<len(chromosome[0][c]) and j < len(chromosome[1][c]) and k < len(chromosome[2][c]):
            if(chromosome[0][c][i] == chromosome[1][c][j] and chromosome[0][c][i] == chromosome[2][c][k]):
                pos[c].append(chromosome[0][c][i])
                i += 1
                j += 1
                k += 1
            else:
                m = max(chromosome[0][c][i], chromosome[1][c][j],chromosome[2][c][k])
                if(chromosome[0][c][i] != m):
                    i += 1
                if(chromosome[1][c][j] != m):
                    j += 1
                if(chromosome[2][c][k] != m):
                    k += 1
        #print(c,len(pos[c]))
    return pos

def counts_atac_seq():
    A_counts = {}
    for t in timeseries:
        chromosome = {"rep1":{},"rep2":{},"rep3":{}}
        chr = []
        for r in range(len(reps)):
            file = t+reps[r]
            f = open("./"+file+".csv")
            next(f)
            Contents = f.readlines()
            chrom = {}
            for line in Contents:
                line = line[:-1]
                line = line.split(",")
                if len(line[0])>7:
                    continue
                if line[0] not in chrom.keys():
                    chrom[line[0]] = []
                    chr.append(line[0])
                for i in range(int(line[1]),int(line[2])+1):
                    chrom[line[0]].append(i)
            chromosome[r] = chrom
        chr = list(set(chr))
        #print(t,":")
        A_counts[t] = overlap(chromosome,chr)

    return A_counts
