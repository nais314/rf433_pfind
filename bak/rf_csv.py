import csv, sys


def normalize(thelist):
    _stat = {}
    for elem in thelist:
        if elem not in _stat:
            _stat[elem] = 1
        else:
            _stat[elem] += 1
    
    to_del = []        
    for elem in _stat:
        #print(elem, elem+1)
        if elem+1 in _stat and _stat[elem+1] > _stat[elem] :
            print(_stat[elem],'//',_stat[elem+1])
            _stat[elem+1] += _stat[elem]
            _stat[elem] = 0
            #to_del.append(elem)
            print(_stat[elem],'//',_stat[elem+1])
            
            for item in range(0, len(thelist)-1):
                if thelist[item] == elem: thelist[item] = elem+1
                
        if elem-1 in _stat and _stat[elem-1] > _stat[elem] :
            _stat[elem-1] += _stat[elem]
            _stat[elem] = 0
            #to_del.append(elem)
            for item in range(0, len(thelist)-1):
                if thelist[item] == elem: thelist[item] = elem-1
                
        print(thelist,'\n\n')
    
    #......................  

if __name__ == "__main__":
    hi = [];
    lo = [];
    
    if len(sys.argv) > 1: 
        filename = sys.argv[1]
    else:
        filename = 'rf1.csv'
        filename = "../433_records/vivamax_humidifier_onoff2.txt"
        
    out_filename = filename[: filename.rfind('.')  ] + '_n' + '.csv'
    
    print(out_filename)
    #exit(0)

    
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\'')
        for row in spamreader:
            if len(row) == 0: continue
            hi.append(int(row[1]))
            lo.append(int(row[0]))
            #print(row)
        
        #print(hi)
        #print(lo)
        '''hi_stat = {}
        for elem in hi:
            if elem not in hi_stat:
                hi_stat[elem] = 1
            else:
                hi_stat[elem] += 1
        
        to_del = []        
        for elem in hi_stat:
            if elem+1 in hi_stat and hi_stat[elem+1] > hi_stat[elem] :
                hi_stat[elem+1] += hi_stat[elem]
                hi_stat[elem] = 0
                #to_del.append(elem)
                for item in range(0, len(hi)-1):
                    if hi[item] == elem: hi[item] = hi_stat[elem+1]
            if elem-1 in hi_stat and hi_stat[elem-1] > hi_stat[elem] :
                hi_stat[elem-1] += hi_stat[elem]
                hi_stat[elem] = 0
                #to_del.append(elem)
                for item in range(0, len(hi)-1):
                    if hi[item] == elem: hi[item] = hi_stat[elem-1]'''
        
        #......................
        
        
        normalize(hi)
        normalize(lo)

        #......................

      

        with open(out_filename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            for i in range(0, len(hi)):
                if hi[i] == 0: hi[i] = 1
                if lo[i] == 0: lo[i] = 1
                print(hi[i], ',', lo[i])
                #spamwriter.writerow( [ hi[i] , lo[i] ] )
                spamwriter.writerow( [ lo[i] , hi[i] ] )
        
        
        out_filename = out_filename[: out_filename.rfind('.')  ] + '.list'        
        with open(out_filename, 'w') as csvfile:
            for i in range(0, len(hi)):
                #csvfile.write(str(hi[i])+','+str(lo[i])+',\n')
                csvfile.write(str(lo[i])+','+str(hi[i])+',\n')
        
        
        out_filename = out_filename[: out_filename.rfind('.')  ] + '.h'        
        with open(out_filename, 'w') as csvfile:
            csvfile.write("uint8_t {} [] = { \n".format(out_filename[: out_filename.rfind('.')  ] ) )
            for i in range(0, len(hi)-1):
                #csvfile.write(str(hi[i])+','+str(lo[i])+',\n')
                csvfile.write(str(lo[i])+','+str(hi[i])+',\n')
            csvfile.write(str(lo[len(hi)])+','+str(hi[len(hi)])+'\n')
            csvfile.write("} \n" )
        
        '''with open('rfn13.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            for i in range(0, len(hi)):
                if hi[i] == 4: hi[i] = 3
                if lo[i] == 4: lo[i] = 3
                spamwriter.writerow( [ hi[i] , lo[i] ] )'''
