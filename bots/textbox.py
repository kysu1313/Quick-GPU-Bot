import tkinter


class TextEntry():
    def __init__(self):

        self.top = tkinter.Tk()
        self.top.geometry("400x240")
        self.textBox = None
        self.label = tkinter.Label(self.top, text ="<==========> Enter Newegg 2FA code below: <==========>", takefocus=True)
        self.submitBtn = tkinter.Button(self.top, text="Submit", command=self.__setText)
        self.textBox = tkinter.Entry(self.top, text ="Hello", takefocus=True)
        self.result = ""

    def getTextInput(self):
        return self.result

    def __setText(self):
        self.result = self.textBox.get()
        self.top.destroy()
    
    def showField(self):
        #value = textBox.get()
        self.label.pack()
        self.textBox.pack()
        self.submitBtn.pack()
        self.top.mainloop()
    
