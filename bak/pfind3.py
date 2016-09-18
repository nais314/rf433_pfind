import os, sys, re

import pprint

import time

import pickle


def search_distinct(thelist):
    _stat = {}
    for elem in thelist:
        if elem not in _stat:
            _stat[elem] = 1
        else:
            _stat[elem] += 1
    return _stat

def find_distinct(thelist):
    _stat = []
    for elem in thelist:
        if elem not in _stat:
            _stat.append(elem)

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
    
    for elem in _stat:
        #print(elem, elem+1)
        if elem+1 in _stat and _stat[elem+1] > _stat[elem] :
            _stat[elem+1] += _stat[elem]
            _stat[elem] = 0
            
            for item in range(0, len(thelist)-1):
                if thelist[item] == elem: thelist[item] = elem+1
                
        if elem-1 in _stat and _stat[elem-1] > _stat[elem] :
            _stat[elem-1] += _stat[elem]
            _stat[elem] = 0
            for item in range(0, len(thelist)-1):
                if thelist[item] == elem: thelist[item] = elem-1
                
        #print(thelist,'\n\n')

    
    #...................... 

    
SCATTER = 2 # magic number
def normalize_with_scatter(thelist):
    for i in range(0, len(thelist)):
        if thelist[i] == 0: thelist[i] = 1 
    
    _stat = {}
    for elem in thelist:
        if elem not in _stat:
            _stat[elem] = 1
        else:
            _stat[elem] += 1
    
    for elem in _stat:
        #print(elem, elem+1)
        for Sc in range(1,SCATTER):
            if elem+Sc in _stat and _stat[elem+Sc] > _stat[elem] :
                _stat[elem+Sc] += _stat[elem]
                _stat[elem] = 0
                
                for item in range(0, len(thelist)-1):
                    if thelist[item] == elem: thelist[item] = elem+Sc
                    
            if elem-Sc in _stat and _stat[elem-Sc] > _stat[elem] :
                _stat[elem-Sc] += _stat[elem]
                _stat[elem] = 0
                for item in range(0, len(thelist)-1):
                    if thelist[item] == elem: thelist[item] = elem-Sc
                
        #print(thelist,'\n\n')

    
    #...................... 


if __name__ == "__main__":
    if len(sys.argv) > 1: 
        filename = sys.argv[1]
    else:
        #filename = 'rf1.csv'
        #filename = "record_160201_B.txt"
        filename = "record_160201_A.txt"
        
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
           #print ("match --> reobj.group() : ", reobj.group())
           buf = str(reobj.group()).split(',')
           for x in buf: 
                if x != '': rawdata.append(int(x))
        else:
           pass
           #print ("No match!!")
           
        reobj = None
        buf = None

    #print(rawdata)
    #.......................
    
    #normalize(rawdata)
    normalize_with_scatter(rawdata)
    normalize_with_scatter(rawdata)
    
    print(rawdata)
    
    len_rawdata = len(rawdata)
    
    #exit(0)
    
    #.......................
    
    # make diff strings -------------------------------------
    
    diff = []
    dire = []
    # v1:
    #for i in range(0, len(rawdata)-1):
    #
    #    if (rawdata[i] == rawdata[i+1]
    #    or rawdata[i] == rawdata[i+1] +1
    #    or rawdata[i] == rawdata[i+1] -1) :    
    #        dire.append('=')
    #        diff.append( 0 )
    #        
    #    elif rawdata[i] < rawdata[i+1]:
    #        dire.append('<')
    #        diff.append(rawdata[i+1] - rawdata[i])
    #    elif rawdata[i] > rawdata[i+1]:
    #        dire.append('>')
    #        diff.append( (rawdata[i] - rawdata[i+1]) * -1)
    
    # v2:
    if False:
        for i in range(0, len_rawdata-1):
            if (rawdata[i] - rawdata[i+1]) in (-1,0,1):
                dire.append('=')
                #diff.append( 0 )
            elif (rawdata[i] - rawdata[i+1]) in range(-255,-160):
                dire.append('g')
            elif (rawdata[i] - rawdata[i+1]) in range(-160,-80):
                dire.append('f')
            elif (rawdata[i] - rawdata[i+1]) in range(-80,-40):
                dire.append('e')
            elif (rawdata[i] - rawdata[i+1]) in range(-40,-20):
                dire.append('d')
            elif (rawdata[i] - rawdata[i+1]) in range(-20,-10):
                dire.append('c')
            elif (rawdata[i] - rawdata[i+1]) in range(-10,-5):
                dire.append('b')
            elif (rawdata[i] - rawdata[i+1]) in range(-5,-1):
                dire.append('a')
                
            elif (rawdata[i] - rawdata[i+1]) in range(255,160):
                dire.append('7')
            elif (rawdata[i] - rawdata[i+1]) in range(160,80):
                dire.append('6')
            elif (rawdata[i] - rawdata[i+1]) in range(80,40):
                dire.append('5')
            elif (rawdata[i] - rawdata[i+1]) in range(40,20):
                dire.append('4')
            elif (rawdata[i] - rawdata[i+1]) in range(20,10):
                dire.append('3')
            elif (rawdata[i] - rawdata[i+1]) in range(10,5):
                dire.append('2')
            elif (rawdata[i] - rawdata[i+1]) in range(5,1):
                dire.append('1')            
                
        #print(dire)
        #print(diff)
        #buf = ''.join(dire[1:6])
        #print(buf)
        #input("Press Enter to continue...")
        
        
    
    
    
    
    start_time = time.time()
    # search patterns -----------------------------------------
    pattdict = {} # store items count 2+
    #for i in range(0, len(dire)-3):
    #    patt = dire[i]+dire[i+1]+dire[i+2]
    
    def gen_divider():
        iii = 1
        ii = 0
        i = 0
        while True:
            i = ii
            ii = iii
            iii = i + ii
            yield iii

    next_divider =  gen_divider()   
    
    def sample_size(sample_len, max_ssize=128, min_ssize=6):
        divider = next(next_divider)
        print('divider', divider)
        while sample_len / divider > max_ssize:
            divider = next(next_divider)
            print(divider)
            
        result = int(sample_len / divider)
        while result > min_ssize:
            result = int(sample_len / divider)
            yield result
            divider = next(next_divider)
            print ("DIVIDER:", divider, '\n')
    

 
 
    if True or not os.path.exists(filename+".dict"): # True:   # True or
        for SAMPLE_SIZE in sample_size(len_rawdata, max_ssize=96, min_ssize=12): # 75/6 good
            #build first pattern
            patt = ""
            for i in range(0, len_rawdata-SAMPLE_SIZE):
                if i % 5 == 0: print('SAMPLE_SIZE:', SAMPLE_SIZE, ' i:', i, '/', len_rawdata-SAMPLE_SIZE )
                if (i+SAMPLE_SIZE) > (len_rawdata-SAMPLE_SIZE-1): 
                    break

                patt = ''.join( str(x) for x in rawdata[i:i+SAMPLE_SIZE])
                #patt = str(rawdata[i:i+SAMPLE_SIZE])
                patt_A = rawdata[i:i+SAMPLE_SIZE]

                if patt in pattdict:
                    pattdict[patt]["count"] += 1
                    pattdict[patt]["pos"].append([i, i+SAMPLE_SIZE-1])
                    continue
                    
                for ii in range( i+SAMPLE_SIZE, len_rawdata-SAMPLE_SIZE-1): # i+1 ? or i+SS?
                    #patt2 = ""
                    #
                    #patt2 = ''.join(str(x) for x in rawdata[ii:ii+SAMPLE_SIZE])
                    #if patt == patt2:
                    if rawdata[i:i+SAMPLE_SIZE] == rawdata[ii:ii+SAMPLE_SIZE]:
                        
                        if patt in pattdict:
                            #store count and begin,end position
                            pattdict[patt]["count"] += 1
                            pattdict[patt]["pos"].append([ii, ii+SAMPLE_SIZE-1])
                            # cache:
                            if pattdict[patt]["count"] > 3: break # cache:---------------------
                        else:
                            pattdict[patt] = {}
                            pattdict[patt]["count"] = 1
                            pattdict[patt]["pos"] = []
                            pattdict[patt]["pos"].append([ii, ii+SAMPLE_SIZE-1])
                            
        print("--- %s seconds ---" % (time.time() - start_time))

                        
        #pprint.pprint(pattdict)
        for x in pattdict:
            print(x, pattdict[x]["count"])
            print( ','.join( str(x) for x in rawdata[ pattdict[x]["pos"][0][0] : pattdict[x]["pos"][0][1]+1 ]  ) )
        
        print("possible patterns:", len(pattdict))
        
        print("--- %s seconds ---" % (time.time() - start_time))
        #exit(0)
        #input('raw')
        #file = open("pattdict.dict", "wb")
        file = open(filename+".dict", "wb")
        pickle.dump(pattdict, file)
        #**************************************************************************
        
        
    if True:
        #file = open("pattdict.dict", "rb")
        file = open(filename+".dict", "rb")
        pattdict = pickle.load(file)
        
    #if True:   
        #to_remove = []
        #pattlist = []
        #for patt in pattdict:
        #    pattlist.append([patt, pattdict[patt] ])
        #    
        #
        #for i in range(len(pattlist)):
        #    for ii in range(len(pattlist)):
        #        if i == ii : continue
        #        if len(pattlist[i][0]) < len(pattlist[ii][0]):
        #            if pattlist[i][0] in pattlist[ii][0]:
        #                if i not in to_remove:
        #                    to_remove.append(i)
        #                    
        #to_remove.sort(reverse=True)
        #print(to_remove)
        ##print(pattlist)
        #for i in to_remove:
        #    del(pattlist[i])
            
        # cropped version 
    
    pattlist = []
    for patt in pattdict:
            pattlist.append([patt, pattdict[patt] ])
            
    def pattlist_clean_similars():
        global pattdict, pattlist
        to_remove = []
        for i in range(len(pattlist)):
            for ii in range(len(pattlist)):
                if i == ii : continue
                if len(pattlist[i][0]) < len(pattlist[ii][0]):
                    if (
                    (pattlist[i][0] in pattlist[ii][0]) 
                    #or (pattlist[i][0][2:-2] in pattlist[ii][0]) 
                    #or (pattlist[i][0][4:-4] in pattlist[ii][0]) 
                    or (pattlist[i][0][6:-6] in pattlist[ii][0])
                    ):
                        if i not in to_remove:
                            to_remove.append(i)
                            
        to_remove.sort(reverse=True)
        print(to_remove)
        #print(pattlist)
        for i in to_remove:
            del(pattlist[i])

            
        pattdict = {}
        for i in range(len(pattlist)):
            pattdict[pattlist[i][0]] = pattlist[i][1]
            
        for x in pattdict: print(x,'\n')
        #print(pattdict)
        print('-'*80)
        
        
        #pattlist.sort(key = lambda x: x[1]["count"])
        #for i in range(len(pattlist)-5, len(pattlist)):
        #    print(pattlist[i])
        
        #pattlist.sort(key = lambda x: len(x[0]) )
        #for i in reversed(range(len(pattlist)-10, len(pattlist))):
        #     print(pattlist[i])

        
        
        
        
    # expand patterns ----------------------------------------------------------
   
    
    if False:
        pattlist_clean_similars()
        for i in range(len(pattlist)):
            showme = False
            found = True
            c = 0
            cc = 0
            c_found = 0
            while found:
                found = False
                c += 1
                cc -= 1
                if cc < 0: cc = 0
                for apos in range( 1, len(pattlist[i][1]["pos"]) ):

                    if (
                    ( ( pattlist[i][1]["pos"][apos][1] +c) < len_rawdata ) and
                    ( ( pattlist[i][1]["pos"][0][1] +c) < len_rawdata ) and
                    ( rawdata[ pattlist[i][1]["pos"][0][1] +c  ] ==   rawdata[ pattlist[i][1]["pos"][apos][1] +c  ] )
                    ):
                        pattlist[i][0] += str(  rawdata[ pattlist[i][1]["pos"][0][1] +c ]  )
                        
                        pattlist[i][1]["pos"][0][1] += 1
                        found  = True
                        c_found += 1
                        showme = True
                        break
                        
                
                
                    if len(pattlist[i][1]["pos"]) > 2 and cc > 0:
                        for apos in range( 2, len(pattlist[i][1]["pos"]) ):
                             if ( rawdata[ pattlist[i][1]["pos"][0][1] -cc  ]
                            ==   rawdata[ pattlist[i][1]["pos"][apos][1] -cc  ] ):
                                pattlist[i][0] = str(  rawdata[ pattlist[i][1]["pos"][0][1] -cc ]  ) + pattlist[i][0] 
                                pattlist[i][1]["pos"][0][0] -= 1
                                found  = True
                                c_found += 1
                                showme = True
                                break 

                                
                    #if found and c_found > 0:  print( c_found, '\n')
                    
                    
            if showme:
                print (i,"",pattlist[i][0])
                
 
     # expand patterns  v2----------------------------------------------------------
   
    
    if True:
        pattlist_clean_similars()
        for i in range(len(pattlist)):
            showme = False
            found = True
            c = 0
            cc = 0
            c_found = 0
            for bpos in range( 0, len(pattlist[i][1]["pos"]) ):
                while found:
                    found = False
                    c += 1
                    cc -= 1
                    if cc < 0: cc = 0 # patch
                
                    for apos in range( bpos+1, len(pattlist[i][1]["pos"]) ):
                    
                        if bpos == apos : continue

                        if (
                        ( ( pattlist[i][1]["pos"][apos][1] +c) < len_rawdata ) and
                        ( ( pattlist[i][1]["pos"][bpos][1] +c) < len_rawdata ) and
                        ( rawdata[ pattlist[i][1]["pos"][bpos][1] +c  ] ==   rawdata[ pattlist[i][1]["pos"][apos][1] +c  ] )
                        ):
                            pattlist[i][0] += str(  rawdata[ pattlist[i][1]["pos"][bpos][1] +c ]  )
                            
                            pattlist[i][1]["pos"][bpos][1] += 1
                            found  = True
                            c_found += 1
                            showme = True
                            break
                            
                    
                    
                        if len(pattlist[i][1]["pos"]) > 2 and cc > 0:
                            for apos in range( 2, len(pattlist[i][1]["pos"]) ):
                                 if ( rawdata[ pattlist[i][1]["pos"][bpos][1] -cc  ]
                                ==   rawdata[ pattlist[i][1]["pos"][apos][1] -cc  ] ):
                                    pattlist[i][0] = str(  rawdata[ pattlist[i][1]["pos"][bpos][1] -cc ]  ) + pattlist[i][0] 
                                    pattlist[i][1]["pos"][bpos][0] -= 1
                                    found  = True
                                    c_found += 1
                                    showme = True
                                    break 

                                    
                        #if found and c_found > 0:  print( c_found, '\n')
                    
                    
            if showme:
                print (i,"",pattlist[i][0])   
    
    
    
    ########################################
    pattlist_clean_similars()
    ########################################

    
    
    

    #------------------------------------------------------------------------------------------------------------------
    #  search_distinct search_distinct search_distinct search_distinct search_distinct search_distinct search_distinct
    print('+'*80)    
    if True:
        volt = False
        for i in range(len(pattlist)):
            
            if len( search_distinct( rawdata[ pattlist[i][1]["pos"][0][0] : pattlist[i][1]["pos"][0][1] ] ) ) < 5:
                print(pattlist[i][0],'\n\n')
                print( rawdata[ pattlist[i][1]["pos"][0][0] : pattlist[i][1]["pos"][0][1] ] ,'\n\n')
                volt = True
        if not volt: exit(0)
    print('+'*80)
    #  search_distinct search_distinct search_distinct search_distinct search_distinct search_distinct search_distinct
    #------------------------------------------------------------------------------------------------------------------
    
    
    
    
    
    
    #------------------------------------------------------------------------------------------------------------------
    # find max index max....
    if True:
        # pattern dictionary size:
        elems = {}
        for i in range(len(pattlist)):
        
            elem = find_distinct( rawdata[ pattlist[i][1]["pos"][0][0] : pattlist[i][1]["pos"][0][1] ] )
            elem.sort()
            if str(elem) not in elems:
                elems[str(elem)] = [i]
            else:
                elems[str(elem)].append(i)
                
        print (elems) 
        
        pos_max = 0
        pos_max_elem = -1
        results = []
        for elem in elems:
            if len(elems[elem]) > 2:
                pos_max = 0
                pos_max_elem = -1
                for i in elems[elem]:
                    adat1 = rawdata[ pattlist[i][1]["pos"][0][0] : pattlist[i][1]["pos"][0][1] ]
                    maxi = max( adat1 )
                    pos1 = adat1.index(maxi)

                    if pos1 > pos_max: 
                        pos_max = pos1
                        pos_max_elem = i
                if pos_max_elem > -1:
                    results.append( rawdata[ pattlist[pos_max_elem][1]["pos"][0][0] : pattlist[pos_max_elem][1]["pos"][0][0] + pos_max+1 ]  )
                        
        #i = pos_max_elem
        #adat1 = rawdata[ pattlist[i][1]["pos"][0][0] : pattlist[i][1]["pos"][0][0] + pos_max+1 ]
        #print('#'*80)
        #print(adat1)
        #print('#'*80)
        print('#'*80)
        print(results)
        print('#'*80)
    
    
    
    # align on max, check similar #########=============----------------------------------------
    if False:
        elems = {}
        for i in range(len(pattlist)):
        
            elem = find_distinct( rawdata[ pattlist[i][1]["pos"][0][0] : pattlist[i][1]["pos"][0][1] ] )
            elem.sort()
            if str(elem) not in elems:
                elems[str(elem)] = [i]
            else:
                elems[str(elem)].append(i)
                
        print (elems)
        
        for elem in elems:
            if len(elems[elem]) > 2:
                for i in elems[elem]:
                    adat1 = rawdata[ pattlist[i][1]["pos"][0][0] : pattlist[i][1]["pos"][0][1] ]
                    maxi = max( adat1 )
                    pos1 = adat1.index(maxi)
                    pos1_last = list(reversed(adat1)).index(maxi)
                    for ii in elems[elem]:
                        if i == ii : continue
                        adat2 = rawdata[ pattlist[ii][1]["pos"][0][0] : pattlist[ii][1]["pos"][0][1] ]
                        pos2 = adat2.index(maxi)
                        pos2_last = list(reversed(adat2)).index(maxi)
                        left_align = True
                        right_align = True
                        canalign = True
                        c = 0
                        ok = False
                        while canalign:
                            c += 1
                            
                            if c < pos1 and c < pos2:
                                if adat1[pos1 - c] == adat2[pos2 - c]:
                                    ok = True
                            else: left_align = False
                            
                            if c + pos1 > len(adat1) and c + pos2 > len(adat2):
                                if adat1[pos1 + c] == adat2[pos2 + c]:
                                    ok = True
                            else: right_align = False
                            
                            if not left_align and not right_align: canalign = False
                            
                        
                        if ok:
                            if pos1 > pos2:
                                if pos1_last < pos2_last:
                                    adat3 = adat1[:pos1+1] + adat2[-pos2_last:]
                                else: adat3 = adat1
                            else:
                                if pos1_last > pos2_last:
                                    adat3 = adat2[:pos2+1] + adat1[-pos1_last:]
                                else:
                                    adat3 = adat2
                                
                            print('- '*40,'\n')
                            print(adat1,'\n',adat2,'\n\n',adat3,'\n')
                    
            
            #for i in range(len(pattlist)):
            #    maxi = max( rawdata[ pattlist[i][1]["pos"][0][0] : pattlist[i][1]["pos"][0][1] ] )
                
     
