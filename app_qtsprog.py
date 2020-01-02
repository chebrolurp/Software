from Tkinter import * 
import ScrolledText
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import os

btn_font_type = ('verdana', 10, 'normal')                       # font description
menu_font_type = ("verdana", 12, 'normal')    		# font description
text_font_type = ("Courier", 12, 'normal')    		# font description


iconpath = os.path.join('.', 'icons')				#  path for icons folder containing thumbimages for toolbar
terminal_iconfile = os.path.join(iconpath, 'terminal.png')     #  Settings iconpath
open_iconfile = os.path.join(iconpath, 'open.png')          	#  Open File iconpath
#erase_iconfile = os.path.join(iconpath, 'erase.png')          #  Detect File iconpath
auto_iconfile = os.path.join(iconpath, 'auto.png')          	#  Open File iconpath
help_iconfile = os.path.join(iconpath, 'help.png')          	#  Help iconpath
exit_iconfile = os.path.join(iconpath, 'exit.png')          	#  Exit iconpath

def app_qtsprog(root):
    oSProgGUI = SProgGUI(root)
    return oSProgGUI

class ProgressBar(Canvas):
	def __init__(self, master,fillcolor='blue',**kw):
		self.master = master
		self.width = kw['width']
		self.height = kw['height']
		self.fillcolor = fillcolor
		Canvas.__init__(self, master,**kw)
		self.textx, self.texty = self.width/2, self.height/2
		return

	def minimum(self, value):
		self.minval = value		
		return

	def maximum(self, value):
		self.maxval = value		
		return

	def mapping(self, status):
		mapval = int( ((status-self.minval)*1.0 / (self.maxval-self.minval))* self.width)
		return mapval 

	def value(self, status):
		currentwidth = self.mapping(status)
		self.refresh(currentwidth)
		return
	
	def refresh(self, currentwidth):
		self.delete(ALL)
		self.bar = self.create_rectangle(0,0,currentwidth,self.height, fill=self.fillcolor)
		percent = int( currentwidth*100 / self.width ) + 1
		self.text = self.create_text(self.textx, self.texty, anchor=CENTER, \
					text=str(percent)+ '%')
		self.master.update()
		return


class SProgGUI:
    def __init__(self, master):
	self.master = master
	self._createToolbar()
	self._createMenubar()
	self._createMainbody()
	return

    def _createMenubar(self):
	"""
	"""
	self.mainmenu = Menu(self.master, font=menu_font_type)
	self.mainmenu.config(borderwidth=1)
	self.master.config(menu=self.mainmenu)

	self.filemenu = Menu(self.mainmenu, font=menu_font_type)
	self.filemenu.config(tearoff=0)
	self.mainmenu.add_cascade(label='File', menu=self.filemenu, underline=0)
	
	self.helpmenu = Menu(self.mainmenu, font=menu_font_type)
	self.helpmenu.config(tearoff=0)
	self.mainmenu.add_cascade(label='Help', menu=self.helpmenu, underline=0)

	return

    def _createToolbar(self):
	"""
	"""
	self.FrameToolBar = Frame(self.master, borderwidth=1) #, relief=RAISED
	self.FrameToolBar.grid(row=0, column=0, sticky=W)
	self._createIcons()
	nCol = 0

	self.BtnOpenFile = Button(self.FrameToolBar,\
		image=openim, \
		font=btn_font_type,
		text=' Open ', \
		relief=FLAT, \
		overrelief=RAISED, \
		compound=TOP)
	self.BtnOpenFile.grid(row=0,column=nCol, sticky=W)
	nCol += 1

        #self.BtnErase = Button(self.FrameToolBar,\
	#	image=eraseim, \
	#	font=btn_font_type,
	#	text=' Erase ', \
	#	relief=FLAT, \
	#	overrelief=RAISED, \
	#	compound=TOP)
	#self.BtnErase.grid(row=0,column=nCol, sticky=W)
	#nCol += 1

	self.BtnAuto = Button(self.FrameToolBar,\
		image=autoim, \
		font=btn_font_type,
		text=' Prog ', \
		relief=FLAT, \
		overrelief=RAISED, \
		compound=TOP)
	self.BtnAuto.grid(row=0,column=nCol, sticky=W)
	nCol += 1


	self.BtnHelp = Button(self.FrameToolBar,\
		image=helpim, \
		font=btn_font_type,
		text=' Help ', \
		relief=FLAT, \
		overrelief=RAISED, \
		compound=TOP)
	self.BtnHelp.grid(row=0,column=nCol, sticky=W)
	nCol += 1

	self.BtnExit= Button(self.FrameToolBar,\
		image=exitim, \
		font=btn_font_type,
		text=' Exit ', \
		relief=FLAT, \
		overrelief=RAISED, \
		compound=TOP)
	self.BtnExit.grid(row=0,column=nCol, sticky=W)
	nCol += 1

        self.BtnTerminalMode = Button(self.FrameToolBar,\
		image=terminalim, \
		font=btn_font_type,
		text=' Terminal_Mode ', \
		relief=FLAT, \
		overrelief=RAISED, \
		compound=TOP)
	self.BtnTerminalMode.grid(row=0,column=nCol, sticky=W)
	return

    def _createIcons(self):
	"""
	Method : _createIcons
	    Attaches thumbnails to Toolbar buttons
	Arguments :
	    None
	Returns :
	    None
	"""
	global openim, autoim, terminalim, helpim, exitim
	openim          = ImageTk.PhotoImage(file=open_iconfile)
	#eraseim        = ImageTk.PhotoImage(file=erase_iconfile)
	terminalim      = ImageTk.PhotoImage(file=terminal_iconfile)
	autoim          = ImageTk.PhotoImage(file=auto_iconfile)
	helpim          = ImageTk.PhotoImage(file=help_iconfile)
	exitim          = ImageTk.PhotoImage(file=exit_iconfile)
	return	

    def _createMainbody(self):
	self.FrameMainboby = Frame(self.master)
	self.FrameMainboby.grid(row=1, column=0, sticky=N+W+E+S)

	self.FrameHexFileDetails = LabelFrame(self.FrameMainboby, text='IHX File Details', padx=3, pady=3)
	self.FrameHexFileDetails.grid(row=0, column=0, sticky=N+W+E+S)

	Label(self.FrameHexFileDetails, text='File Name:').grid(row=0, column=0, sticky=N+W)
	self.EntryFilename = Entry(self.FrameHexFileDetails, \
                readonlybackground='white', \
                bg='white', \
                #width=9, \
                state='readonly', \
		borderwidth=2, \
		justify=LEFT)                            
	self.EntryFilename.grid(row=1, column=0, sticky=E+W) 

	Label(self.FrameHexFileDetails, text='Code Size:').grid(row=2, column=0, sticky=N+W)
 	self.EntryCodeSize = Entry(self.FrameHexFileDetails, \
                readonlybackground='white', \
                bg='white', \
                #width=9, \
                state='readonly', \
		borderwidth=2, \
		justify=LEFT)                            
	self.EntryCodeSize.grid(row=3, column=0, sticky=E+W) 

	Label(self.FrameHexFileDetails, text='Modified Date:').grid(row=4, column=0, sticky=N+W)
 	self.EntryMdate = Entry(self.FrameHexFileDetails, \
                readonlybackground='white', \
                bg='white', \
                #width=9, \
                state='readonly', \
		borderwidth=2, \
		justify=LEFT)                            
	self.EntryMdate.grid(row=5, column=0, sticky=E+W) 


	self.FrameHexFile = LabelFrame(self.FrameMainboby, text='IHX File Contents', padx=3, pady=3)
	self.FrameHexFile.grid(row=0, column=1, sticky=N+W+E+S)

	self.TextHexFile = ScrolledText.ScrolledText(self.FrameHexFile, \
		height=20, \
		width=50, \
		font=text_font_type, \
                state=DISABLED, \
		bg='light gray')
	self.TextHexFile.grid(row=0, column=0, sticky=E+W)



if __name__ == '__main__':
    root = Tk()
    app_qtsprog(root)
    root.mainloop()
