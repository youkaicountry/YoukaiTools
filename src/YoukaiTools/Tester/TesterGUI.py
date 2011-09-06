#Copyright (c) <2011> <Nathaniel Caldwell>

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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

