import tkinter as tk
import tkinter.ttk as ttk

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from tkinter import font



class pfind_gui_tk():

    def __init__(self, app):
        self.app = app

        

    def get_input_filename(self):
        return self.app.win.filename_entry.get()

    def get_minss(self):
        return int(self.app.win.v_min_ss.get())

    def get_maxss(self):
        return int(self.app.win.v_max_ss.get())
        
    def set_minss(self, x):
        self.app.win.v_min_ss.set(int(x))
        
    def set_maxss(self, x):
        self.app.win.v_max_ss.set(int(x))       

    def get_prog_v(self):
        return self.app.win.prog_v.get()
    def get_sub_prog_v(self):
        return self.app.win.sub_prog_v.get()

    def set_prog_v(self, x):
        self.app.win.prog_v.set(x)
        self.app.win.progbar.update()
    def set_sub_prog_v(self, x):
        self.app.win.sub_prog_v.set(x)
        self.app.win.sub_progbar.update()


    def set_progbar_indeterminate(self, o=True):
        if o:
            self.app.win.progbar.configure(mode="indeterminate")
            self.app.win.progbar.start()
            self.app.win.progbar.update()
        else:
            self.app.win.progbar.stop()
            self.app.win.progbar.configure(mode="determinate")
            self.app.win.prog_v.set(0)
            self.app.win.progbar.update()

    def set_state(self, state):
        self.app.win.v_curr_state.set(str(state))

    def on_run(self):
        self.maxss=self.app.win.v_max_ss.get()
        self.minss=self.app.win.v_min_ss.get()
        self.app.win.file_browse.config(state=tk.DISABLED)
        #self.app.win.go_btn.config(state=tk.DISABLED)
        self.app.win.go_btn.pack_forget()
        self.app.win.opt_btn.config(state=tk.DISABLED)
        self.app.win.cancel_btn.pack()

    def on_finish(self):
        self.app.win.file_browse.config(state=tk.NORMAL)
        #self.app.win.go_btn.config(state=tk.NORMAL)
        self.app.win.cancel_btn.pack_forget()
        self.app.win.go_btn.pack()
        self.app.win.opt_btn.config(state=tk.NORMAL)
        self.app.win.v_max_ss.set(self.maxss)
        self.app.win.v_min_ss.set(self.minss)
        self.set_sub_prog_v(0)
        
        
    #..........opt................
    
    def get_v_max_pattern_count_while_search(self):
        return int(self.app.optwin.v_max_pattern_count_while_search.get())
        
    def get_v_align_beyond_pattern_length(self):
        return int(self.app.optwin.v_align_beyond_pattern_length.get())

    def get_v_drop_small_result(self):
        return int(self.app.optwin.v_drop_small_result.get())
        
    def pattern_finder_run(self):
        global pattern_finder
        self.app.pattern_finder.run()

    def pattern_finder_cancel(self):
        global pattern_finder
        self.app.pattern_finder.CANCEL_SIGNAL = True
        
    def console_log(self, *args):
        for arg in args:
            self.app.result_win.textarea.insert(tk.INSERT, str(arg))
    def console_logln(self, *args):
        for arg in args:
            self.app.result_win.textarea.insert(tk.INSERT, str(arg))
            
        self.app.result_win.textarea.insert(tk.INSERT, '\n')


    def show_opt(self):

        self.app.optwin.deiconify()
        self.app.optwin.update()
        buf="{}x{}+{}+{}".format(
            self.app.optwin.winfo_width(), self.app.optwin.winfo_height(),
            self.app.winfo_x()+self.app.winfo_width(),    self.app.winfo_y()
        )
        self.app.optwin.geometry(buf)
        












#########################################################################
class MyFrame(tk.Toplevel):
    #self.e_fullself.filename = Entry(root)
    #self.e_fullself.filename.pack()
    #self.browse_btn = Button(self, text="Browse", command=self.load_file, width=10)

    h3_font = font.Font(size=36, weight='bold')
    h2_font = font.Font(size=26, weight='bold')





    def __init__(self, controller=None):

        tk.Toplevel.__init__(self)
        
        self.controller=controller


        self.frame1 = tk.Frame()
        self.frame1.grid(column=0, row=0, sticky=tk.E+tk.W)

        self.filename_entry = tk.Entry(master=self.frame1, bg="LightBlue3")
        #self.filename_entry.grid(column=0, row=0, sticky=tk.E+tk.W)#pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.filename_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.file_browse = tk.Button(master=self.frame1, text="Browse", command=self.ask_filename, bg="LightBlue3", bd=5)
        #self.file_browse.grid(column=1, row=0, sticky=tk.E+tk.W)
        self.file_browse.pack(side=tk.LEFT, fill=tk.X, expand=True)

        #--- row --------------

        self.frame2 = tk.Frame(bg="BurlyWood")
        self.frame2.grid(column=0, row=1, sticky=tk.E+tk.W)

        self.v_min_ss = tk.StringVar()
        self.v_min_ss.set("6")
        self.min_ss = tk.Entry(master=self.frame2, font=self.h3_font, width=3, textvariable=self.v_min_ss, justify=tk.RIGHT, bg="Khaki")
        self.min_ss.pack(side=tk.LEFT, fill=tk.X, expand=True)
        #self.min_ss.grid(column=0, row=1, sticky=tk.E+tk.W)

        self.to = tk.Label(master=self.frame2, text=" - ", font=self.h3_font, bg="BurlyWood")
        self.to.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.v_max_ss = tk.StringVar()
        self.v_max_ss.set("128")
        self.max_ss = tk.Entry(master=self.frame2, font=self.h3_font, width=3, textvariable=self.v_max_ss, justify=tk.RIGHT, bg="Khaki")
        self.max_ss.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        #self.max_ss.grid(column=1, row=1, sticky=tk.E+tk.W)




        #--- row --------------
        # 2
        self.v_curr_state = tk.StringVar()
        self.curr_state = tk.Label(text=" state ", font=self.h3_font, bg="BurlyWood", textvariable=self.v_curr_state)
        self.curr_state.grid(sticky=tk.E+tk.W)




        #--- row --------------
        # 3
        self.frame_progr = tk.Frame(bg="#330000")
        self.frame_progr.grid(row=3,column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        # - PROGRESSBAR
        self.prog_v = tk.IntVar()
        self.progbar = ttk.Progressbar(self.frame_progr, orient=tk.HORIZONTAL, mode='determinate', variable=self.prog_v)
        self.progbar.grid(row=0,column=1,columnspan=1, sticky=tk.W + tk.E)

        #self.progbar.configure(value=44)
        # - SUBPROGRESSBAR
        self.sub_prog_v = tk.IntVar()
        self.sub_progbar = ttk.Progressbar(self.frame_progr, orient=tk.HORIZONTAL, mode='determinate', variable=self.sub_prog_v)
        self.sub_progbar.grid(row=0,column=0,columnspan=1, sticky=tk.W + tk.E)

        tk.Grid.columnconfigure(self.frame_progr, 0, weight=1)
        tk.Grid.columnconfigure(self.frame_progr, 1, weight=1)
        #---


        #--- row --------------
        # 4
        self.frame_btn = tk.Frame(bg="navy")
        self.frame_btn.grid( sticky=tk.W + tk.E +tk.S+tk.N)

        self.opt_btn = tk.Button(master=self.frame_btn, text="opt", command= self.controller.show_opt)
        self.opt_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.go_btn = tk.Button(master=self.frame_btn, text="GO!", font= self.h2_font, command= self.controller.pattern_finder_run,
        bd=5, bg="#ff5c26")
        self.go_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.cancel_btn = tk.Button(master=self.frame_btn, text="CANCEL", font= self.h2_font, command= self.controller.pattern_finder_cancel)
        self.cancel_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.cancel_btn.pack_forget()

        tk.Grid.rowconfigure(self.frame_btn, 0, weight=1)

        #----------------------------------------

        #tk.Grid.columnconfigure(self, 0, weight=1)
        #for i in range(4):     tk.Grid.rowconfigure(self, i, weight=1)
        #----------------------------------------

    def ask_filename(self):
        a = askopenfilename( filetypes=(
                            ("All files", "*.*"),
                            ("Dict files", "*.dict"),
                             ("RAW files", "*.txt;*.csv")
                              ))

        if a :
            self.filename_entry.delete(0, tk.END)
            self.filename_entry.insert(tk.INSERT,a)

#**************************************************************



class result_win(tk.Toplevel):
        
    def callback(self, *args):
        self.textarea.see(tk.END)
        self.textarea.edit_modified(0)    
    
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        #text(area) with scrollbar
        self.scrollbar = tk.Scrollbar(master=self)
        self.scrollbar.pack( side=tk.RIGHT, fill=tk.Y)        
        self.textarea = tk.Text(master=self, bg="black", fg="#ffe599", yscrollcommand = self.scrollbar.set, insertbackground="#d90000",
        insertwidth=10)
        self.textarea.pack( side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.textarea.yview)
        self.textarea.bind('<<Modified>>', self.callback)

        self.textarea.insert(tk.INSERT, "READY. \n")       



