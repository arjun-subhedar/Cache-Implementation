from prettytable import PrettyTable
import time
start = time.time()
def split_address(address):
    global count
    tag = address[0:13]
    index = address[13:30]
    offset = address[30:32]
    count += 1
    return ([index,tag,count])
def cash():
    global count,h,lines,evictions
    for i in lines:
        l = split_address(i)
        if l[0] in cache.keys() and cache[l[0]][0][2] == 1:
            hits= 0
            for i in cache[l[0]]:
                if (i[0] == l[1]):
                    hits+=1
                    i[1] = count
                    h+=1
                    break
            if hits == 0:
                if ([None,None,0] in cache[l[0]]):
                    index = cache[l[0]].index([None,None,0])
                    cache[l[0]][index] = [l[1],l[2],1]

                else:
                    evictions += 1
                    ways = cache[l[0]]
                    min_count = ways[0][1]
                    for i in cache[l[0]]:
                        if i[1] == min_count:
                            i[1]=count
                            i[0]=l[1]
        else:
            cache[l[0]] = [[l[1],l[2],1]]
h=0
count=0
evictions = 0
cache = {}
nones = 0
namelist=['gcc','swim','twolf','mcf','gzip']
result_table = PrettyTable(["FILE NAME","HITS", "EVICTIONS", "ROWS", "EMPTY", "INSTRUCTIONS COUNT", "HITRATE"])
for trace in namelist:
    fh = open('{}.trace'.format(trace),'r')
    lines=[]
    lr= fh.readlines()
    for i in lr:
        res = "{0:08b}".format(int(i[4:12], 16))
        lines.append(str(res.zfill(32)))
    fh.close()
    cash()
    cache_table = PrettyTable(["INDEX", "WAY1(Valid)", "WAY1(Tag)"])
    for i in cache.keys():
        valids = [cache[i][0][2]]
        nones = nones + valids.count(0)
        cache_table.add_row([i, cache[i][0][2], cache[i][0][0:2]])

    with open('1waySA_512kb_{}_trace.txt'.format(trace),'w') as w:
        w.write(str(cache_table))
    len_trace = len(cache) + evictions - nones + h
    result_table.add_row([trace, h, evictions, len(cache), nones, len_trace, round((h/len_trace)*100,4)])
    rows=count=h=evictions=nones=0
    cache={}
    cache_table=[]
print(result_table)
end = time.time()
print("Program execution time = {} s".format(round(end-start,2)))


