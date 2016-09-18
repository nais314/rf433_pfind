import pdb
import tkinter as tk
import tkinter.ttk as ttk
#from tkinter import *

app = tk.Tk()
app.LIVE = False
app.VERSION = 0.3

#--------------------------------------






import os, sys, re, os.path

import pprint

import time

import pickle




from pfind_tk_opt import OptionWindow

from pfind_gui_tk import *

####################################################################










####################################################################
class pfind3():


    def __init__(self):

        self.CANCEL_SIGNAL = False

        #self.MAX_PATT_COUNT = 3 # stop pattern search after N found
        self.MAX_PATT_COUNT = pfind3_gui.get_v_max_pattern_count_while_search()
        self.SCATTER = 2 # magic number
        self.MIN_SIGNAL_LEN = 6 #TODO not yet in options

        self.sample_size_list = []

        #self.filename
        #self.rawdata
        #self.pattdict = {}


    def run(self, file_in=""):
        self.CANCEL_SIGNAL = False
        pfind3_gui.set_state("starting")
        pfind3_gui.set_prog_v(5)
        pfind3_gui.on_run()

        self.start_time = time.time()

        if len(file_in) > 1: # not empty, maybe command line argument
            self.filename = file_in
        else:
            self.filename = pfind3_gui.get_input_filename() # else GUI launched action

        if self.filename == "":
            pfind3_gui.set_state("ERR: no file")
            pfind3_gui.set_prog_v(0)
            pfind3_gui.on_finish()
            return False


        # read file into variable ----------------------------------

        try:
            file = open(self.filename, "r")
        except(e):
            file = open(self.filename, "r", encoding="utf8")

        self.rawdata = [] #<-@VAR

        for line in file:
            reobj = re.match("^\d*,\d*", line, flags=0)
            if reobj:
               #print ("match --> reobj.group() : ", reobj.group())
               buf = str(reobj.group()).split(',')
               for x in buf:
                    if x != '': self.rawdata.append(int(x))
            else:
               pass
               #print ("No match!!")

            reobj = None
            buf = None

        #print(self.rawdata)
        pfind3_gui.set_prog_v(10)
        #----------------------------------------------------------




        # NORMALIZE RAW DATA --------------------------------------
        pfind3_gui.set_state("normalizing")
        #self.normalize(self.rawdata)
        self.normalize_with_scatter(self.rawdata)

        self.len_rawdata = len(self.rawdata)

        #exit(0)
        pfind3_gui.set_prog_v(15)
        #----------------------------------------------------------




        # FIND PATTERNS, STORE THEM IN PATTDICT -------------------
        pfind3_gui.set_state("create pattdict")
        #self.next_divider = self.gen_divider()

        self.pattdict = {} # store items count 2+

        if os.path.isfile(self.filename+".dict") and app.optwin.v_load_dicts_if_exists.get() == 1:
            self.load_pattdict()
        else:
            self.find_patterns() #<<<<<####

            # save pattdict:
            file = open(self.filename+".dict", "wb")
            pickle.dump(self.pattdict, file)

        pfind3_gui.set_prog_v(50)



        # copy pattdict into a sortable LIST.......
        pfind3_gui.set_state("create gen_pattlist")
        self.gen_pattlist()
        pfind3_gui.set_prog_v(55)
        #..........................
        pfind3_gui.set_state("pattlist_clean_similars")
        self.pattlist_clean_similars()
        pfind3_gui.set_prog_v(60)
        #..........................................
        #----------------------------------------------------------

        pfind3_gui.set_state("expand patterns v2")
        self.expand_patterns()
        pfind3_gui.set_prog_v(65)
        #..........................

        pfind3_gui.set_state("pattlist_clean_similars")
        self.pattlist_clean_similars()
        pfind3_gui.set_prog_v(60)
        #..........................................

        pfind3_gui.set_state("rf code crop")
        self.find_max_index_max()
        pfind3_gui.set_prog_v(70)

        pfind3_gui.set_progbar_indeterminate(False)

        if self.CANCEL_SIGNAL == False:
            pfind3_gui.set_state("finished")
        else:
            pfind3_gui.set_state("state")

        pfind3_gui.set_prog_v(100)
        pfind3_gui.on_finish()


    def cancel(self):
        self.CANCEL_SIGNAL = True

    # search patterns =======================================================
    #
    # search patterns =======================================================
    #
    # search patterns =======================================================




    def stat_dict(self, thelist):
        _stat = {}
        for elem in thelist:
            if elem not in _stat:
                _stat[elem] = 1
            else:
                _stat[elem] += 1
        return _stat

    def find_distinct(self, thelist):
        _stat = []
        for elem in thelist:
            if elem not in _stat:
                _stat.append(elem)

        return _stat



    def normalize(self, thelist):
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



    def normalize_with_scatter(self, thelist):
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
            for Sc in range(1,self.SCATTER):
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





    def gen_divider(self): #Fibonacci generator ....................................
        iii = 1
        ii = 0
        i = 0
        while True:
            i = ii
            ii = iii
            iii = i + ii
            yield iii



    def sample_size(self, sample_len, max_ssize=128, min_ssize=6):#.......................
        self.next_divider = self.gen_divider()
        divider = next(self.next_divider)
        pfind3_gui.console_logln('Initializing DIVIDER: "while sample_len / divider > max_ssize"')

        #increase divider, until: filesize/divider > max_sample_size
        while sample_len / divider > max_ssize:
            divider = next(self.next_divider)
            #print(divider)

        #yield a sample size, while ss>min_ss
        result = int(sample_len / divider)
        while result > min_ssize:
            result = int(sample_len / divider)
            yield result
            divider = next(self.next_divider)
            pfind3_gui.console_logln ("Sample size: ", str( int(sample_len / divider) ))

    def gen_sample_size_list(self, sample_len, max_ssize=128, min_ssize=6):
        self.next_divider = self.gen_divider()
        divider = next(self.next_divider)
        pfind3_gui.console_logln('Initializing DIVIDER: "while sample_len / divider > max_ssize"')

        #increase divider, until: filesize/divider > max_sample_size
        while sample_len / divider > max_ssize:
            divider = next(self.next_divider)

        result = int(sample_len / divider)
        while result > min_ssize:
            result = int(sample_len / divider)
            self.sample_size_list.append( result )
            divider = next(self.next_divider)






    def find_patterns(self): #.....................................................
        #global win, app
        #if True or not os.path.exists(self.filename+".dict"): # True:   # True or
        max_ssize = pfind3_gui.get_maxss()
        min_ssize = pfind3_gui.get_minss()

        self.gen_sample_size_list(self.len_rawdata, max_ssize=max_ssize, min_ssize=min_ssize)
        for SAMPLE_SIZE in self.sample_size_list:#self.sample_size(self.len_rawdata, max_ssize=max_ssize, min_ssize=min_ssize):
            #pfind3_gui.set_minss(SAMPLE_SIZE)
            pfind3_gui.set_maxss(SAMPLE_SIZE)

            if self.CANCEL_SIGNAL :  break #return False #      <<<< break <<<<

            #pfind3_gui.set_sub_prog_v(2)
            pfind3_gui.set_progbar_indeterminate(True)

            #build first pattern
            patt = ""
            for i in range(0, self.len_rawdata-SAMPLE_SIZE):
                if self.CANCEL_SIGNAL :  break # return False #      <<<< break <<<<

                if i % 5 == 0:
                    #print('SAMPLE_SIZE:', SAMPLE_SIZE, ' i:', i, '/', self.len_rawdata-SAMPLE_SIZE )
                    #print(  int(100 / (self.len_rawdata / (i+1)) )  )
                    #self.sub_prog_v = 100 / self.len_rawdata / SAMPLE_SIZE
                    pfind3_gui.set_sub_prog_v(   int(100 / (self.len_rawdata / (i+1)) )   )
                if (i+SAMPLE_SIZE) > (self.len_rawdata-SAMPLE_SIZE-1):
                    break

                patt = ''.join( str(x) for x in self.rawdata[i:i+SAMPLE_SIZE])

                if patt in self.pattdict:
                    self.pattdict[patt]["count"] += 1
                    self.pattdict[patt]["pos"].append([i, i+SAMPLE_SIZE-1])
                    continue

                #search for patterns occurances
                for ii in range( i+SAMPLE_SIZE, self.len_rawdata-SAMPLE_SIZE-1): # i+1 ? or i+SS?
                    if self.CANCEL_SIGNAL : break #return False #      <<<< break <<<<

                    if self.rawdata[i:i+SAMPLE_SIZE] == self.rawdata[ii:ii+SAMPLE_SIZE]:

                        if patt in self.pattdict:
                            #store count and begin,end position
                            self.pattdict[patt]["count"] += 1 # count maybe obsolete
                            self.pattdict[patt]["pos"].append([ii, ii+SAMPLE_SIZE-1])
                            # cache:
                            if self.MAX_PATT_COUNT > 0: # see opt window
                                if self.pattdict[patt]["count"] >= self.MAX_PATT_COUNT: break # cache:---------------------
                        else:
                            self.pattdict[patt] = {}
                            self.pattdict[patt]["count"] = 1
                            self.pattdict[patt]["pos"] = []
                            self.pattdict[patt]["pos"].append([ii, ii+SAMPLE_SIZE-1])

        #print("--- %s seconds ---" % (time.time() - start_time))
        #RESTORE GUI and VARIABLES
        pfind3_gui.set_progbar_indeterminate(False)
        #pprint.pprint(self.pattdict)
        #pfind3_gui.console_logln("PATTERN DICTIONARY ITEMS:")
        #for x in self.pattdict:
        #    #print(x, self.pattdict[x]["count"])
        #    pfind3_gui.console_logln(x, self.pattdict[x]["count"])
        #    #print( ','.join( str(x) for x in self.rawdata[ self.pattdict[x]["pos"][0][0] : self.pattdict[x]["pos"][0][1]+1 ]  ) )
        #


        pfind3_gui.console_logln("possible patterns:", len(self.pattdict))

        pfind3_gui.console_logln("--- elapsed: %s seconds ---" % (time.time() - self.start_time))


        #**************************************************************************




    def load_pattdict(self):
        #file = open("self.pattdict.dict", "rb")
        file = open(self.filename+".dict", "rb")
        self.pattdict = pickle.load(file)



    def gen_pattlist(self):
        self.pattlist = []
        for patt in self.pattdict:
                self.pattlist.append([patt, self.pattdict[patt] ])



    def pattlist_clean_similars(self):
        #global self.pattdict, self.pattlist
        to_remove = []
        for i in range(len(self.pattlist)):
            if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
            for ii in range(len(self.pattlist)):
                if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
                if i == ii : continue
                if len(self.pattlist[i][0]) < len(self.pattlist[ii][0]):
                    if (
                    (self.pattlist[i][0] in self.pattlist[ii][0])
                    #or (self.pattlist[i][0][2:-2] in self.pattlist[ii][0])
                    #or (self.pattlist[i][0][4:-4] in self.pattlist[ii][0])
                    or (    ( len(self.pattlist[i][0]) > 2 ) 
                        and (pfind3_gui.get_v_align_beyond_pattern_length == 1) 
                        and (self.pattlist[i][0][2:-2] in self.pattlist[ii][0]) )
                    or (    ( len(self.pattlist[i][0]) > 4 ) 
                        and (pfind3_gui.get_v_align_beyond_pattern_length == 1) 
                        and (self.pattlist[i][0][4:-4] in self.pattlist[ii][0]) )
                    or (    ( len(self.pattlist[i][0]) > 6 ) 
                        and (pfind3_gui.get_v_align_beyond_pattern_length == 1) 
                        and (self.pattlist[i][0][6:-6] in self.pattlist[ii][0]) )
                    ):
                        if i not in to_remove:
                            to_remove.append(i)

        to_remove.sort(reverse=True) # delete from list from top to bottom -:)
        #print(to_remove)
        #print(self.pattlist)
        for i in to_remove:
            del(self.pattlist[i])


        self.pattdict = {}
        for i in range(len(self.pattlist)):
            self.pattdict[self.pattlist[i][0]] = self.pattlist[i][1]

        #for x in self.pattdict: print(x,'\n')
        #print(self.pattdict)
        pfind3_gui.console_logln('-'*80)






    # expand patterns  v2----------------------------------------------------------

    def expand_patterns(self): #  v2:
        self.pattlist_clean_similars()
        for i in range(len(self.pattlist)):
            if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
            showme = False
            found = True
            c = 0
            cc = 0
            c_found = 0
            for bpos in range( 0, len(self.pattlist[i][1]["pos"]) ):
                if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
                while found:
                    if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
                    found = False
                    c += 1
                    cc -= 1
                    if cc < 0: cc = 0 # patch

                    for apos in range( bpos+1, len(self.pattlist[i][1]["pos"]) ):
                        if self.CANCEL_SIGNAL : return False #      <<<< break <<<<

                        if bpos == apos : continue

                        if (
                        ( ( self.pattlist[i][1]["pos"][apos][1] +c) < self.len_rawdata ) and
                        ( ( self.pattlist[i][1]["pos"][bpos][1] +c) < self.len_rawdata ) and
                        ( self.rawdata[ self.pattlist[i][1]["pos"][bpos][1] +c  ] ==   self.rawdata[ self.pattlist[i][1]["pos"][apos][1] +c  ] )
                        ):
                            self.pattlist[i][0] += str(  self.rawdata[ self.pattlist[i][1]["pos"][bpos][1] +c ]  )

                            self.pattlist[i][1]["pos"][bpos][1] += 1
                            found  = True
                            c_found += 1
                            showme = True
                            break



                        if len(self.pattlist[i][1]["pos"]) > 2 and cc > 0:
                            for apos in range( 2, len(self.pattlist[i][1]["pos"]) ):
                                if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
                                
                                if ( self.rawdata[ self.pattlist[i][1]["pos"][bpos][1] -cc  ]
                                ==   self.rawdata[ self.pattlist[i][1]["pos"][apos][1] -cc  ] ):
                                    self.pattlist[i][0] = str(  self.rawdata[ self.pattlist[i][1]["pos"][bpos][1] -cc ]  ) + self.pattlist[i][0]
                                    self.pattlist[i][1]["pos"][bpos][0] -= 1
                                    found  = True
                                    c_found += 1
                                    showme = True
                                    break


                        #if found and c_found > 0:  print( c_found, '\n')


            if showme:
                pfind3_gui.console_log(i,": ",self.pattlist[i][0],"\n")



    ########################################
    #self.pattlist_clean_similars()
    ########################################





    #------------------------------------------------------------------------------------------------------------------

    #print('+'*80)
    def search_distinct(self):
        if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
        volt = False
        result = []

        for i in range(len(self.pattlist)):

            if len( self.stat_dict( self.rawdata[ self.pattlist[i][1]["pos"][0][0] : self.pattlist[i][1]["pos"][0][1] ] ) ) < 5:
                #print(self.pattlist[i][0],'\n\n')
                #print( self.rawdata[ self.pattlist[i][1]["pos"][0][0] : self.pattlist[i][1]["pos"][0][1] ] ,'\n\n')
                volt = True
                result.append(self.rawdata[ self.pattlist[i][1]["pos"][0][0] : self.pattlist[i][1]["pos"][0][1] ])
        #if not volt: exit(0)
        #print('+'*80)
        return result

    #------------------------------------------------------------------------------------------------------------------






    #------------------------------------------------------------------------------------------------------------------
    # find max index max....
    def find_max_index_max(self):
        if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
        # pattern dictionary size:
        elems = {}
        for i in range(len(self.pattlist)):
            if self.CANCEL_SIGNAL : return False #      <<<< break <<<<

            elem = self.find_distinct( self.rawdata[ self.pattlist[i][1]["pos"][0][0] : self.pattlist[i][1]["pos"][0][1] ] )
            elem.sort()
            if str(elem) not in elems:
                elems[str(elem)] = [i]
            else:
                elems[str(elem)].append(i)

        #print (elems)

        #___________________________________________________________
        # extract a typical rf signal, ending with a long sync signal
        pos_max = 0
        pos_max_elem = -1
        results = []
        for elem in elems:
            if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
            if len(elems[elem]) > 2:
                pos_max = 0
                pos_max_elem = -1
                for i in elems[elem]:
                    adat1 = self.rawdata[ self.pattlist[i][1]["pos"][0][0] : self.pattlist[i][1]["pos"][0][1] ]
                    maxi = max( adat1 )
                    pos1 = adat1.index(maxi)

                    if pos1 > pos_max:
                        pos_max = pos1
                        pos_max_elem = i

                if pos_max_elem > -1:
                    results.append( self.rawdata[ self.pattlist[pos_max_elem][1]["pos"][0][0] : self.pattlist[pos_max_elem][1]["pos"][0][0] + pos_max+1 ]  )

        #i = pos_max_elem
        #adat1 = self.rawdata[ self.pattlist[i][1]["pos"][0][0] : self.pattlist[i][1]["pos"][0][0] + pos_max+1 ]
        #print('#'*80)
        #print(adat1)
        #print('#'*80)
        #file = open( self.filename[: self.filename.rfind('.')  ] + '_results' + '.txt'  , "w")
        #pfind3_gui.console_logln('#'*80)
        #pfind3_gui.console_logln("Possible signals:")
        #for signal in results:
        #    if pfind3_gui.get_v_drop_small_result() == 1 and len(signal) < self.MIN_SIGNAL_LEN : continue
        #    pfind3_gui.console_logln(signal )
        #    file.write(str(signal)+'\n\n')
        #pfind3_gui.console_logln('#'*80)
        #file.close()
        
        #AFTERMATH
        #TODO: to options
        file = open( self.filename[: self.filename.rfind('.')  ] + '_results' + '.txt'  , "w")
        pfind3_gui.set_state("after-counting")
        pfind3_gui.set_progbar_indeterminate(True)
        pfind3_gui.console_logln('#'*80)
        pfind3_gui.console_logln("Possible Signals + count:")
        for signal in results:
            if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
            if pfind3_gui.get_v_drop_small_result() == 1 and len(signal) < self.MIN_SIGNAL_LEN : continue
            count = 0
            for i in range(len(self.rawdata)-len(signal)):
                if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
                if self.rawdata[i: i+len(signal)] == signal:
                    count +=1
            pfind3_gui.console_logln("count: ", str(count), '\n', signal, '\n')
            file.write("count: "+ str(count)+ '\n'+ str(signal)+ '\n\n')
        pfind3_gui.set_progbar_indeterminate(False)
        file.close()
        pfind3_gui.console_logln('#'*80)
        





    # align on max, check similar #########=============----------------------------------------
    def align_on_max__check_similar(): # @EXPERIMENTAL
        if self.CANCEL_SIGNAL : return False #      <<<< break <<<<
        #if False:
        elems = {}
        for i in range(len(self.pattlist)):

            elem = self.find_distinct( self.rawdata[ self.pattlist[i][1]["pos"][0][0] : self.pattlist[i][1]["pos"][0][1] ] )
            elem.sort()
            if str(elem) not in elems:
                elems[str(elem)] = [i]
            else:
                elems[str(elem)].append(i)

        print (elems)

        for elem in elems:
            if len(elems[elem]) > 2:
                for i in elems[elem]:
                    adat1 = self.rawdata[ self.pattlist[i][1]["pos"][0][0] : self.pattlist[i][1]["pos"][0][1] ]
                    maxi = max( adat1 )
                    pos1 = adat1.index(maxi)
                    pos1_last = list(reversed(adat1)).index(maxi)
                    for ii in elems[elem]:
                        if i == ii : continue
                        adat2 = self.rawdata[ self.pattlist[ii][1]["pos"][0][0] : self.pattlist[ii][1]["pos"][0][1] ]
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


            #for i in range(len(self.pattlist)):
            #    maxi = max( self.rawdata[ self.pattlist[i][1]["pos"][0][0] : self.pattlist[i][1]["pos"][0][1] ] )





#########################################################################





def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(a) for a in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))











#**************************************************************
if __name__ == "__main__":

    app.geometry("300x300+100+100")
    app.optwin = OptionWindow()

    pfind3_gui = pfind_gui_tk(app)
    app.pattern_finder = pfind3()

    win = MyFrame(pfind3_gui)
    
    app.win = win
    
    pfind3_gui.show_opt()
    
    
    #tk.Grid.columnconfigure(app, 0, weight=1)
    #tk.Grid.rowconfigure(app, 0, weight=1)
    #tk.Grid.rowconfigure(app, 1, weight=1)
    app.columnconfigure( 0, weight=1)
    app.rowconfigure( 4, weight=1)
    #app.rowconfigure( 1, weight=1)
    #win.columnconfigure( 0, weight=1)
    #win.rowconfigure( 0, weight=1)
    #win.pack(expand=True, fill=tk.BOTH)
    app.update()







    #app.optwin.update()
    #buf="{}x{}+{}+{}".format(
    #    app.optwin.winfo_width(), app.optwin.winfo_height(),
    #    app.winfo_x()+app.winfo_width(),    app.winfo_y()
    #)
    #app.optwin.geometry(buf)
    #app.optwin.iconify()


    #pfind3_gui = pfind3_gui_tk(app)

    app.result_win = result_win()
    app.result_win.update()
    buf="{}x{}+{}+{}".format(
        app.result_win.winfo_width(), app.result_win.winfo_height(),
        app.winfo_x()+app.winfo_width(),    app.winfo_y()
    )
    app.result_win.geometry(buf)



    if len(sys.argv) > 1:
        #filename = sys.argv[1]
        pattern_finder.run(sys.argv[1])
    else: #GUI will launch
        pass


    #********************
    app.mainloop()
    #********************
