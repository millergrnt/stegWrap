import tkinter as tk
import tkinter.filedialog
import subprocess
from subprocess import PIPE,STDOUT
import string
import os
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()



class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.mode = True    # True if hiding files
        
        self.label = tk.Label(self, text="Mode: Hiding Files", anchor='w')
        self.label.place(x=160, y=30, w=180, h=25)

        self.modeHideButton  = tk.Button(self, command=self.modeHide, text="Hide", bg="#0d0", activebackground="#0f0")
        self.modeHideButton.place(x=20, y=30, w=70, h=25)

        self.modeRecoverButton  = tk.Button(self, command=self.modeRecover, text="Recover", bg="#d00", activebackground="#f00")
        self.modeRecoverButton.place(x=90, y=30, w=70, h=25)

        self.submitButton = tk.Button(self, command=self.startStego, text="Submit")
        self.submitButton.place(x=20, y=70, w=120, h=25)


        
        self.getInputImage = tk.Button(self, command=self.getInputImageF, text="Input Image")
        self.getInputImage.place(x=160, y=70, w=120, h=25)
        self.getInputImageTxt = tk.Label(self, text="", anchor='e', relief="sunken")
        self.getInputImageTxt.place(x=280, y=70, w=200, h=25)
        self.InputImageTxt = ""

        self.passwordLabel =tk.Label(self, text="Password:", anchor='w')
        self.passwordLabel.place(x=20+280+200, y=70, w=70, h=25)
        self.passwordTxt = tk.Text(self, relief="sunken")
        self.passwordTxt.place(x=580, y=70, w=140, h=25)



        self.getInputFile = tk.Button(self, command=self.getInputFileF, text="Input File")
        self.getInputFile.place(x=160, y=100, w=120, h=25)
        self.getInputFileTxt = tk.Label(self, text="", anchor='e', relief="sunken")
        self.getInputFileTxt.place(x=280, y=100, w=200, h=25)
        self.InputFileTxt = ""

        self.nameOutputFile =tk.Label(self, text="Output Filename:", anchor='w')
        self.nameOutputFile.place(x=160, y=130, w=120, h=25)
        self.nameOutputFileTxt = tk.Text(self, relief="sunken")
        self.nameOutputFileTxt.place(x=280, y=130, w=200, h=25)
        

        #stegFile = tk.Label(self, text="Pure Image").pack(side="bottom")


        self.text = tk.Text(self)
        self.text.place(x=0, y=369, w=800, h=200)

    def modeHide(self):
        self.mode = True
        self.modeHideButton.config(bg="#0d0", activebackground="#0f0")
        self.modeRecoverButton.config(bg="#d00", activebackground="#f00")
        self.label.config(text="Mode: Hiding Files")

        self.getInputFile.config(state="active")
        self.getInputFileTxt.config(state="active")
        # global buttonframe
        # global container
        # self.getInputImage.lift(self)
    
    def modeRecover(self):
        self.mode = False
        self.modeHideButton.config(bg="#d00", activebackground="#f00")
        self.modeRecoverButton.config(bg="#0d0", activebackground="#0f0")
        self.label.config(text="Mode: Recovering Files")

        self.getInputFile.config(state="disabled")
        self.getInputFileTxt.config(state="disabled")
        # global buttonframe
        # global container
        # self.getInputImage.lower(self)




    def getInputImageF(self):
        self.InputImageTxt = tk.filedialog.askopenfilename()
        self.getInputImageTxt.config(text=self.InputImageTxt)
    
    def getInputFileF(self):
        self.InputFileTxt = tk.filedialog.askopenfilename()
        self.getInputFileTxt.config(text=self.InputFileTxt)
        
    
    def startStego(self):
        self.text.delete(0.0, tk.END)
        if self.mode:   # Hiding data
            self.text.insert(tk.END, "We are hiding data\n")
            extension = self.InputImageTxt
            if len(extension) < 4:
                extension = -1
                self.text.insert(tk.END, "Error! Invalid Filename! Too short.\n")
                return
            elif extension[-4] == '.' or extension[-5] == '.':
                if   ".jpg"  in extension:
                    extension = ".jpg"
                elif ".jpeg" in extension:
                    extension = ".jpeg"
                elif ".bmp"  in extension:
                    extension = ".bmp"
                elif ".au"   in extension:
                    extension = ".au"
                elif ".wav"  in extension:
                    extension = ".wav"
            else:
                extension = -1
                self.text.insert(tk.END, "Error! Invalid File Extension! Valid Extensions are\n")
                self.text.insert(tk.END, " .AU audio files")
                self.text.insert(tk.END, " .WAV audio files")
                self.text.insert(tk.END, " .BMP bitmap photos")
                self.text.insert(tk.END, " .JPEG compressed photos")
                return
            ###
            if len(self.InputFileTxt) > 1:
                pass
            else:
                self.text.insert(tk.END, "Input File Filename too short!")
                return

            password = ""
            if len(self.passwordTxt.get(0.0, tk.END)) > 2 :
                password = self.passwordTxt.get(0.0, tk.END)[:-1]
            if len(password) < 65:
                pass
            else:
                self.text.insert(tk.END, "Input Password must be of length 0..64 characters")
                return
            passwordtemp = "".join(c for c in password if c in valid_chars)
            if password == passwordtemp:
                pass
            else:
                self.text.insert(tk.END, "Input Password must only contain '{}'".format(valid_chars))
                return

            filename = self.nameOutputFileTxt.get(0.0, tk.END)
            fileOut = "".join(c for c in filename if c in valid_chars)
            if len(fileOut) == 0:
                fileOut = "stegWrap{}".format(extension)
            self.text.insert(tk.END, "Filename = '{}'\n".format(fileOut))

            self.text.insert(tk.END, "{}\n".format(self.InputImageTxt))
            self.text.insert(tk.END, "{}\n".format(self.InputFileTxt))
            self.text.insert(tk.END, "{}\n".format(password))
            exists = os.path.isfile(fileOut)
            if exists:
                os.remove(fileOut)
                self.text.insert(tk.END, "Old {} removed!\n".format(fileOut))
            

            self.text.see("end")
            process = subprocess.Popen(["steghide", "--embed", "-v", "-cf", self.InputImageTxt, "-sf", fileOut, "-ef", self.InputFileTxt, "-p", password], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
            out = (process.communicate()[0]).decode()
            
            self.text.insert(tk.END, out)
            
            
            print("the commandline is {}".format(process.args))
            print(out)

            self.text.see("end")

            
        #################################
        else:           # Recovering data
            extension = self.InputImageTxt
            if len(extension) < 4:
                extension = -1
                self.text.insert(tk.END, "Error! Invalid Filename! Too short.\n")
                return
            elif extension[-4] == '.':
                extension = extension[-3:]

            elif extension[-5] == '.':
                extension = extension[-4:]
            else:
                extension = -1
                self.text.insert(tk.END, "Error! Invalid File Extension! Valid Extensions are\n")
                self.text.insert(tk.END, " .AU audio files")
                self.text.insert(tk.END, " .WAV audio files")
                self.text.insert(tk.END, " .BMP bitmap photos")
                self.text.insert(tk.END, " .JPEG compressed photos")
                return
            ###
            self.text.insert(tk.END, "Valid Input Filename")

            password = ""
            if len(self.passwordTxt.get(0.0, tk.END)) > 2 :
                password = self.passwordTxt.get(0.0, tk.END)[:-1]
            if len(password) < 65:
                pass
            else:
                self.text.insert(tk.END, "Input Password must be of length 0..64 characters")
                return
            passwordtemp = "".join(c for c in password if c in valid_chars)
            if password == passwordtemp:
                pass
            else:
                self.text.insert(tk.END, "Input Password must only contain '{}'".format(valid_chars))
                return


            self.text.see("end")
            process = subprocess.Popen(["steghide", "--extract", "-v", "-sf", self.InputImageTxt, "-p", password], stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
            out = (process.communicate()[0]).decode()

        
        
            filename = self.nameOutputFileTxt.get(0.0, tk.END)
            fileOut = "".join(c for c in filename if c in valid_chars)
            if len(fileOut) == 0:
                fileOut = "stegWrap.{}".format(extension)
            print("Filename = '{}'".format(fileOut))

            self.text.see("end")
        
        # p = sub.Popen('steghide',stdout=sub.PIPE,stderr=sub.PIPE)
        # output, errors = p.communicate()
        # self.text.delete(0.0, tk.END)
        # self.text.insert(tk.END, output)
        
        




class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is page 2")
        label.pack(side="top", fill="both", expand=True)

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)

class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is page 4")
        label.pack(side="top", fill="both", expand=True)

buttonframe = ""
container = ""

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)

        global buttonframe
        global container

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="File Processing", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Steghide Options", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Page 3", command=p3.lift)
        b4 = tk.Button(buttonframe, text="Page 4", command=p4.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x600")
    root.title("Stegwrap")
    root.resizable(False, False)
    root.mainloop()