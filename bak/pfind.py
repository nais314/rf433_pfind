import os, sys, re

import pprint


def search_distinct(thelist):
    _stat = {}
    for elem in thelist:
        if elem not in _stat:
            _stat[elem] = 1
        else:
            _stat[elem] += 1
    return _stat


def normalize(thelist):
    for i in range(0, len(thelist)):
        if thelist[i] == 0: thelist[i] = 1 
    
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
            #print(_stat[elem],'//',_stat[elem+1])
            _stat[elem+1] += _stat[elem]
            _stat[elem] = 0
            #to_del.append(elem)
            #print(_stat[elem],'//',_stat[elem+1])
            
            for item in range(0, len(thelist)-1):
                if thelist[item] == elem: thelist[item] = elem+1
                
        if elem-1 in _stat and _stat[elem-1] > _stat[elem] :
            _stat[elem-1] += _stat[elem]
            _stat[elem] = 0
            #to_del.append(elem)
            for item in range(0, len(thelist)-1):
                if thelist[item] == elem: thelist[item] = elem-1
                
        #print(thelist,'\n\n')

    
    #......................  




if __name__ == "__main__":
    if len(sys.argv) > 1: 
        filename = sys.argv[1]
    else:
        #filename = 'rf1.csv'
        filename = "record_160201_B.txt"
        
    out_filename_diff = filename[: filename.rfind('.')  ] + '_n' + '.diff'
    out_filename_dire = filename[: filename.rfind('.')  ] + '_n' + '.dire'
    
    print(out_filename_dire, out_filename_diff)
    #exit(0)
    
    
    # read file into variable ----------------------------------
    
    file = open(filename, "r")
    #line = file.readline()
    rawdata = []
    for line in file:
        reobj = re.match("^\d*,\d*", line, flags=0)
        if reobj:
           print ("match --> reobj.group() : ", reobj.group())
           buf = str(reobj.group()).split(',')
           for x in buf: rawdata.append(int(x))
        else:
           print ("No match!!")
           
        reobj = None
        buf = None

    print(rawdata)
    #.......................
    
    normalize(rawdata)
    
    print(rawdata)
    
    exit(0)
    
    #.......................
    
    # make diff strings -------------------------------------
    
    diff = []
    dire = []
    #for i in range(0, len(rawdata)-1):
    #    if rawdata[i] < rawdata[i+1]:
    #        dire.append('<')
    #        diff.append(rawdata[i+1] - rawdata[i])
    #    elif rawdata[i] > rawdata[i+1]:
    #        dire.append('>')
    #        diff.append( (rawdata[i] - rawdata[i+1]) * -1)
    #    elif rawdata[i] == rawdata[i+1]:
    #        dire.append('=')
    #        diff.append( 0 )
    for i in range(0, len(rawdata)-1):

        if (rawdata[i] == rawdata[i+1]
        or rawdata[i] == rawdata[i+1] +1
        or rawdata[i] == rawdata[i+1] -1) :    
            dire.append('=')
            diff.append( 0 )
        if rawdata[i] < rawdata[i+1]:
            dire.append('<')
            diff.append(rawdata[i+1] - rawdata[i])
        elif rawdata[i] > rawdata[i+1]:
            dire.append('>')
            diff.append( (rawdata[i] - rawdata[i+1]) * -1)
                    
    #print(dire)
    #print(diff)
    
    
    
    
    
    
    
    
    # search patterns -----------------------------------------
    pattdict = {} # store items count 2+
    for i in range(0, len(dire)-3):
        patt = dire[i]+dire[i+1]+dire[i+2]
        #print(patt)
        #exit(0)
        if patt in pattdict:
            pattdict[patt]["count"] += 1
            pattdict[patt]["pos"].append([i, i+2])
            continue
        for ii in range( i+1, len(dire)-3):
            if patt == dire[ii]+dire[ii+1]+dire[ii+2]:
                if patt in pattdict:
                    #store count and begin,end position
                    pattdict[patt]["count"] += 1
                    pattdict[patt]["pos"].append([ii, ii+2])
                else:
                    pattdict[patt] = {}
                    pattdict[patt]["count"] = 1
                    pattdict[patt]["pos"] = []
                    pattdict[patt]["pos"].append([ii, ii+2])
                    
    #pprint.pprint(pattdict)
    for x in pattdict:
        print(x, pattdict[x]["count"])
    
    print("possible patterns:", len(pattdict))
    #exit(0)
    #............................
    
    raw_patterns = []
    
    len_dire = len(dire)
    for patt in pattdict:
        newpatt = patt
        n = 0
        #retrieve patt from raw:
        o_patt = []
        o_patt.append( rawdata[pattdict[patt]["pos"][0][0]]  )
        o_patt.append( rawdata[pattdict[patt]["pos"][0][0]+1]  )
        o_patt.append( rawdata[pattdict[patt]["pos"][0][0]+2]  )
        o_last = None
        
        while True:
            n += 1 # like a for loop
            hasmatch = False
            
            # cancel if reached next pattern
            if pattdict[patt]["pos"][0][0] + n == pattdict[patt]["pos"][1][0]: 
                break

            firstrun = True
            # for every patt occurance in list:
            for poses in pattdict[patt]["pos"]:
                
                if firstrun :
                    if poses[1]+n >= len_dire: continue # range check
                    if poses[0]-n < 0: continue # range check
                    nextchar = dire[  poses[1]+n  ]
                    prevchar = dire[  poses[0]-n  ]
                    firstrun = False
                    continue
                if poses[1]+n < len_dire: # range check
                    if dire[  poses[1]+n  ] == nextchar:
                        
                        if hasmatch == False: 
                            newpatt += nextchar
                            # build pattern from rawdata too
                            o_patt.append( rawdata[pattdict[patt]["pos"][0][0]+n]  )
                            #o_last = rawdata[pattdict[patt]["pos"][0][0]+n+1]
                        hasmatch = True
                #if poses[0]-n > 0:
                #    if dire[  poses[0]-n  ] == prevchar:
                #        hasmatch = True
                #        newpatt = prevchar + newpatt
            if hasmatch == False: break
        #if n > 1: o_patt.append( o_last )
            
        print(newpatt,"\n")
        #print(o_patt,"\n")
        
        raw_patterns.append(o_patt)
        



        
            



        
    # remove unhomogen patterns **************************************
    if True:
        for i in reversed(range(0,len(raw_patterns))):
            normalize(raw_patterns[i])
            # opt: get homogenity of pattern
            x = len(search_distinct(raw_patterns[i]))
            if x < 5:
                print("distincts: ", x,  "len: ", len(raw_patterns[i]), '\n')
                print(raw_patterns[i], '\n', '-------------------------------------\n')
            else: del(raw_patterns[i])


    #****************************************************************
    for x in raw_patterns:
        print(x,'\n\n')



    # if rp in rp?--------------------------------------------------
    if False:
        matches = []
        for i in range(0, len(raw_patterns)):
            match = False
            for ii in range(0, len(raw_patterns)):
                if ii != i and (len(raw_patterns[i]) <= len(raw_patterns[ii]) ):
                    # compare
                    for iii in range(0, len(raw_patterns[i])):
                        if raw_patterns[i][iii] == raw_patterns[ii][iii]:
                            match = True
                        else:
                            match = False
                if match: 
                    #print('Match Found ! #: {} len: {} \n'.format(i,len(raw_patterns[i])))
                    if i not in matches: matches.append(i)
                    #if ii not in matches: matches.append(ii)
                
        matches.sort(reverse=True)
        print(matches)
        print("#patt before ",len(raw_patterns))
        for x in matches: del(raw_patterns[x])
        print("#patt after  ",len(raw_patterns), '\n', '*'*80,'\n')
        
        for i in range(0, len(raw_patterns)):
            print(raw_patterns[i], '\n\n')









    # partial matches, similarities---------------------------------
    if False:
        print('*'*80)
        tolerance = 0
        #matches = []
        diffies = []
        for i in range(0, len(raw_patterns)):
            
            tolerance = int( len(raw_patterns[i]) /  5 ) # change tolerance here
            print('tolerance: ', tolerance, '.'*70)
            for ii in range(0, len(raw_patterns)):
                difference = 0
                
                
                if (ii != i) and (len(raw_patterns[i]) <= len(raw_patterns[ii]) ):
                    # compare
                    # align
                    # diffie = []
                    a = raw_patterns[i]
                    b = raw_patterns[ii]
                    len_a = len(raw_patterns[i])
                    len_rpi = len(raw_patterns[i])
                    state = "run original" #"run left crop" "run right crop" "run mid crop" "fin"
                    while True:
                        print (state)
                        diffie = []
                        alignment = len(b) - len_a 
                        for align in range(0, alignment):
                            difference = 0
                            #matches = 0
                            for iii in range(0, len_a):
                                if a[iii] == b[iii+align]:
                                    #matches += 1
                                    pass #difference = True
                                else:
                                    difference += 1
                            diffie.append([difference, tolerance, align, ii, i])
                            
                        # remove all except least diff
                        diffie.sort(key=lambda x: x[0])
                        del(diffie[1:])
                        #if difference < tolerance
                        #print(diffie)
                        if len(diffie) > 0 and diffie[0][0] < diffie[0][1]:
                            #print(alignment,'\n', raw_patterns[diffie[0][4]], '\n', raw_patterns[diffie[0][3]], '\n\n')
                            diffies.append(diffie[0])
                            
                        if len_rpi >=5:
                            if state == "run original":
                                a = raw_patterns[i][int(len_rpi / 5):]
                                state = "run right crop"
                            elif state == "run right crop":
                                a = raw_patterns[i][:len_rpi - int(len_rpi / 5)]
                                state = "run left crop"
                            elif state == "run left crop":
                                a = raw_patterns[i][int(len_rpi / 5):len_rpi - int(len_rpi / 5)]
                                state = "run mid crop"
                            elif state == "run mid crop":
                                state = "fin"
                        else: break
                            
                        if state == "run original" or state == "fin" : break
                        
                        len_a = len(a)

                        
                #else: print('wrong length \n')
                
                
        print('\n','*'*80,'\n')
        print(len(diffies))
        if len(diffies) > 1 : 
            diffies.sort(key = lambda x: x[0])
            print(diffies)
            for x in diffies:
                print('\n', raw_patterns[x[4]], '\n', raw_patterns[x[3]], '\n\n')
        
        
        
        
        #print("#patt before ",len(raw_patterns))
        #for x in matches: del(raw_patterns[x])
        print("#patt after  ",len(raw_patterns), '\n', '*'*80,'\n')
        
        for i in range(0, len(raw_patterns)):
            print(raw_patterns[i], '\n\n')
    
    #repeat same with crop left right
