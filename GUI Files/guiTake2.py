import tkinter as tk
import tkinter.filedialog
import subprocess as sub
from HoverInfo import HoverInfo

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()



class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is page 1")
        label.place(x=160, y=20, w=120, h=25)

        self.submitButton = tk.Button(self, command=self.startStego, text="Submit")
        self.submitButton.place(x=20, y=50, w=120, h=25)
        self.hover = HoverInfo(self.submitButton, " Hide Input File in Input Image")
        
        self.getInputimage = tk.Button(self, command=self.getInputimageF, text="Input Image")
        self.getInputimage.place(x=160, y=50, w=160, h=25)
        self.hoverGIi = HoverInfo(self.getInputimage, " Select image to hide data inside of")

        getInputfile = tk.Button(self, command=self.getInputfile, text="Input File")
        getInputfile.place(x=330, y=50, w=160, h=25)
        

        stegFile = tk.Label(self, text="Pure Image").pack(side="bottom")


        self.text = tk.Text(self)
        self.text.place(x=560, y=20, w=240, h=180)

    def getInputimageF(self):
        self.inputImagef = tk.filedialog.askopenfilename()
    
    def getInputfile(self):
        self.inputFile = tk.filedialog.askopenfilename()
        
    
    def startStego(self):
        p = sub.Popen('steghide',stdout=sub.PIPE,stderr=sub.PIPE)
        output, errors = p.communicate()
        #self.text.delete(0.0, tk.END)
        self.text.insert(tk.END, output)
        
        




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

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)

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