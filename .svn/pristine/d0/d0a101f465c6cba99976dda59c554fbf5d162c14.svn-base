from tkinter import *
import os
import operator
import serial
import time
from tkinter import filedialog as FileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import simpledialog as tkSimpleDialog
import app_qtsprog1
import subprocess
import math

HEX_BASE = 16
PACKET_SIZE = 16        #bytes
def sprogrammer (master=None):
    oAppSprog = app_qtsprog1.app_qtsprog1(master)
    oSprog = SProgrammer(oAppSprog)
    return oSprog

class SProgrammer:
    def __init__(self,oAppSprog=None):
        if oAppSprog==None:
            return
        self.oAppSprog = oAppSprog
        self.oAppSprog.master.title('QUARKit 8051 Series Flash Programmer')
        self._configureCB()
        return

    def _configureCB(self):
        self.oAppSprog.BtnOpenFile.configure(command=self.vOpenIHXCB)
        self.oAppSprog.BtnAuto.configure(command=self.vAutoCB)
        #self.oAppSprog.BtnErase.configure(command=self.vEraseCB)
        self.oAppSprog.BtnTerminalMode.configure(command=self.vTerminalModeCB)
        self.oAppSprog.BtnHelp.configure(command=self.vHelpCB)
        self.oAppSprog.BtnExit.configure(command=self.vExitCB)
        self.oAppSprog.filemenu.add_command(label='Open IHX File <Ctrl+O>', underline=0, command=self.vOpenIHXCB)
        self.oAppSprog.filemenu.add_command(label='Exit <Ctrl+Q>', underline=0, command=self.vExitCB)
        self.oAppSprog.helpmenu.add_command(label='Help <F1>', underline=0, command=self.vHelpCB)
        self.oAppSprog.helpmenu.add_command(label='About', underline=0, command=self.vAboutCB)
        self.oAppSprog.master.protocol('WM_DELETE_WINDOW',self.vExitCB)
        self.__vConfigureKBShortCuts()
        self.filename = None
        return

    def vOpenIHXCB (self, event=None):
        oFD = FileDialog.LoadFileDialog (self.oAppSprog.master, title = 'Load IHX File')
        filename = oFD.go(dir_or_file = '.', key = 'track', pattern = '*.ihx')
        if filename == None:
            return
        if self.bOpenIhxFile (filename) == False:
            tkMessageBox.showerror ('File Error !!', 'It is not a correct IHX file...')
            return
        self.vDisplayHexFile(filename)
        self.filename = filename
        return

    def vAutoCB (self, events=None):
        self.bAutoProgram ()
        return

    def vHelpCB (self, event=None):
        tkMessageBox.showinfo ('Help !!', 'Refer QUARKit Series Manual\nFlash programmer Section..')
        return

    def vExitCB (self, event=None):
        if tkMessageBox.askyesno('Exit', 'Terminate QUARKit Programmer..?'):
            self.oAppSprog.master.destroy()
    #def vEraseCB(self, event=None):
        #E = subprocess.Popen("sudo avrdude -C Modified_avrdude.conf -p ft0 -c usbasp -p AT89S52 -e",shell = True)
        #return

    def vTerminalModeCB(self, event=None):
        E = subprocess.Popen("sudo avrdude -C Modified_avrdude.conf -p ft0 -c usbasp -p AT89S52 -t",shell = True)
        return

    def vDisplayHexFile (self, filename):
        self.vFillEntries (self.oAppSprog.EntryFilename, filename.split (os.sep)[-1])
        self.vFillEntries (self.oAppSprog.EntryCodeSize, str (self.nCodeLength) +' Bytes')
        self.vFillEntries (self.oAppSprog.EntryMdate, time.ctime (os.stat(filename).st_mtime))
        self.oAppSprog.TextHexFile.configure(state=NORMAL)
        self.oAppSprog.TextHexFile.delete(1.0, END)
        for i in range (0, len (self.strTransmitArray), 2):
            if (i % (2 * PACKET_SIZE) == 0) and (i > 0):
                self.oAppSprog.TextHexFile.insert (INSERT, '\n')
            self.oAppSprog.TextHexFile.insert (INSERT, self.strTransmitArray[i]+self.strTransmitArray[i+1]+' ')
        self.oAppSprog.TextHexFile.configure(state=DISABLED)

    def vFillEntries (self, Widget, string):
        Widget.configure (state=NORMAL)
        Widget.delete (0, END)
        Widget.insert (0, string)
        Widget.configure (state='readonly')
        return

    def bAutoProgram (self, event=None):
        if self.filename == None:
            tkMessageBox.showerror('Error','No *ihx file is Choosen..!')
            return
        command = "sudo avrdude -C bin/Modified_avrdude.conf -c usbasp -p AT89S52 -e -U flash:w:"+ self.filename
        #p = subprocess.Popen("cd ", shell = True)
        #r = subprocess.Popen("gedit "+self.filename, shell = True)
        #print command
        q = subprocess.Popen(command, shell = True)
        return
    
    def bOpenIhxFile (self, ihxfile):
        """
        Returns False if the selected file is not a standard IHX file otherwise -
        Reads from a given ihx file (name is received as an argument) and stores the 
        data to be transmitted in a single stransmit array - and returns True.
        """
        fd = open(ihxfile)
        data = fd.read()
        fd.close()
        if data[0] != ':':      # A standard IHX file starts with ':'
            return False
        lines = data.split()
        dicMemMap = {}
        for line in lines[:-1]:
            byte_count = int(line[1:3], HEX_BASE)
            start_address = int(line[3:7], HEX_BASE)
            type_ = int(line[7:9], HEX_BASE)
            data = line[9:-2]
            dicMemMap[start_address] = data
            dicMemMapSorted = sorted(dicMemMap.items(), key=operator.itemgetter(0))
        #print dicMemMapSorted 
        self.strTransmitArray = ''
        for (k, v) in dicMemMapSorted:
            # Padding in between
            nBytesInString = len (self.strTransmitArray)//2
            if  nBytesInString < k:
                for i in range (k - nBytesInString):
                     self.strTransmitArray += 'FF'
            self.strTransmitArray += v
        nCodeLength = len(self.strTransmitArray) // 2
        self.nCodeLength = nCodeLength
        #self.vPrintInfo ( 'FileSize = ' + str (nCodeLength) + ' Bytes')
        #print 'Hex Array Sorted = ', self.strTransmitArray
        
        # Padding at the End
        nPackets = nCodeLength // PACKET_SIZE
        nPadSize = ((nPackets + 1) * PACKET_SIZE) - nCodeLength 
        for i in range (nPadSize):
            self.strTransmitArray += 'FF'
        return True

    def __vConfigureKBShortCuts(self):
        """
        Keyboard bindings for different functions
        """
        self.oAppSprog.master.bind('<Control-o>', self.vOpenIHXCB)
        self.oAppSprog.master.bind('<Control-p>', self.vAutoCB)
        self.oAppSprog.master.bind('<Control-q>', self.vExitCB)
        self.oAppSprog.master.bind('<F1>', self.vHelpCB)
        return

    def vAboutCB(self):
        tkMessageBox.showinfo('QUARKit Flash Programmer', \
        'A Quazar Foundations Product\nCopyright 2003 -' + time.asctime().split()[-1] +'\nwww.quazartech.com/tqf')
        return



if __name__ == '__main__':
    root = Tk() 
    sprogrammer(root)
    root.mainloop()
    
