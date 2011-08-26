from Tkinter import *

class TesterGUI:
   def __init__(self, tester, master):
      self.m = master
      self.t = tester
      
      #FRAMES
      self.frm_list = Frame(master, borderwidth=5)
      self.frm_list.pack(side=LEFT, fill=BOTH)
      
      self.frm_desc = Frame(master, borderwidth = 5)
      self.frm_desc.pack(side=LEFT, fill=BOTH)
      
      #LIST FRAME STUFF
      self.lbl_tests = Label(self.frm_list, text="Tests:", justify=CENTER)
      self.lbl_tests.pack(side=TOP)
      
      self.lb_stacklist = Listbox(self.frm_list, width=64, height=16)
      self.lb_stacklist.pack(side=TOP)
      
      self.btn_alltests = Button(self.frm_list, text="Do All Tests", command=self.btnpress_alltests, width=12)
      self.btn_alltests.pack(side=TOP)
      
      self.btn_selectedtest = Button(self.frm_list, text="Do Selected Test", command=self.btnpress_selectedtest, width=12)
      self.btn_selectedtest.pack(side=TOP)
      
      #DESCRIPTION FRAME STUFF
      self.lbl_description = Label(self.frm_desc, text="Description:", justify=CENTER)
      self.lbl_description.pack(side=TOP)
      
      self.txt_description = Text(self.frm_desc, width=32, height=4)
      self.txt_description.pack(side=TOP)
      
      self.lbl_message = Label(self.frm_desc, text="Run Message:", justify=CENTER)
      self.lbl_message.pack(side=TOP)
      
      #BUTTON HANDLERS
   def btnpress_alltests(self):
      return
      
   def btnpress_selectedtest(self):
      return
      
def makeGUI(tester):
   root = Tk()
   root.title("Tester GUI")
   
   p = TesterGUI(tester, root)
   
   root.mainloop()
   return

