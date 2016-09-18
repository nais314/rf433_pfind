import tkinter as tk
import tkinter.ttk as ttk

 

class OptionWindow(tk.Toplevel):

    def gen_col(self):
        c = 1
        while True:
            if c == 0:  c = 1
            else:       c = 0
            yield c


    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        
        self.title="OptionWindow"
        
        self.nextcol = self.gen_col()
        
        #self.attributes("-toolwindow",1) #BUG
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        
        #.................................
        row=0
        self.v_load_dicts_if_exists = tk.IntVar()
        self.v_load_dicts_if_exists.set(1)
        
        self.lab_load_dicts_if_exists = tk.Label(master=self, text="load_dicts_if_exists")
        self.lab_load_dicts_if_exists.grid(column= 1, row=row )
        
        self.chk_load_dicts_if_exists = tk.Checkbutton ( master=self, variable = self.v_load_dicts_if_exists )
        self.chk_load_dicts_if_exists.grid(column= 0, row=row)
        #.................................
        row=1
        self.v_max_pattern_count_while_search  = tk.StringVar()
        self.v_max_pattern_count_while_search.set("2")
        
        self.lab_max_pattern_count_while_search = tk.Label(master=self, text="max_pattern_count_while_search")
        self.lab_max_pattern_count_while_search.grid(column= 1, row=row )
        
        self.ent_max_pattern_count_while_search = tk.Entry(master=self, width=3, textvariable=self.v_max_pattern_count_while_search)
        self.ent_max_pattern_count_while_search.grid(column= 0, row=row)
        #.................................
        row=2
        self.v_align_beyond_pattern_length = tk.IntVar()
        self.v_align_beyond_pattern_length.set(1)
        
        self.lab_align_beyond_pattern_length = tk.Label(master=self, text="align_beyond_pattern_length")
        self.lab_align_beyond_pattern_length.grid(column= 1, row=row )
        
        self.chk_align_beyond_pattern_length = tk.Checkbutton ( master=self, variable = self.v_align_beyond_pattern_length )
        self.chk_align_beyond_pattern_length.grid(column= 0, row=row)
        #.................................
        row=3
        self.v_drop_small_result = tk.IntVar()
        self.v_drop_small_result.set(1)
        
        self.lab_drop_small_result = tk.Label(master=self, text="drop_small_result")
        self.lab_drop_small_result.grid(column= 1, row=row )
        
        self.chk_drop_small_result = tk.Checkbutton ( master=self, variable = self.v_drop_small_result )
        self.chk_drop_small_result.grid(column= 0, row=row)

