############  get the info of promoters in bed files.
def getpromoter():
    file = "/Users/miranda/Documents/Courses/lab/Bioinfomatics/Drosophila/RNA-seq/Dm_EPDnew.bed"
    f = open(file)
    lines = f.readlines()
    promoter = {}
    for line in lines:
        line = line[:-1]
        line = line.split(' ')
        #print(line)
        if line[0] not in promoter:
            promoter[line[0]] = {}
        """
        if line[3][:-2] not in promoter[line[0]]:
            promoter[line[0]][line[3][:-2]] = [int(line[1]),int(line[2]),line[5]]
        else:
            promoter[line[0]][line[3][:-2]][0] = min(promoter[line[0]][line[3][:-2]][0],int(line[1])) 
        """
        promoter[line[0]][line[3]] = [int(line[1]),int(line[2]),line[5]]
        #print(promoter[line[0]][line[3]])
    #for k in promoter.keys():
        #print(len(promoter[k]))
    return promoter
