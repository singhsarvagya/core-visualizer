from tkinter import *


class TerminalGUI:

    '''
        text:   Used to store Text object form tkinter library. Constitutes a text board on the GUI
                that is helpful in displaying important information about the graph
    '''
    text = None

    def __init__(self, root):
        '''
            textFrame:  frame alotted on the GUI to display this text board
            scrollbar: To add scroll feature to the text board
        '''
        self.textFrame = Frame(root, borderwidth=4, relief=GROOVE, width=700, height=300)
        self.textFrame.pack_propagate(False)
        scrollbar = Scrollbar(self.textFrame)

        TerminalGUI.text = Text(self.textFrame, wrap=WORD, yscrollcommand=scrollbar.set, state=DISABLED, height=500)
        TerminalGUI.text.pack(fill=X)

    '''
        This function is used to pack the Terminal into the GUI.
        It also clear the text widget for the new project.
    '''
    # TODO work on packing of the terminal GUI 
    def pack(self):
        TerminalGUI.text.config(state=NORMAL)
        TerminalGUI.text.delete('1.0', END)
        TerminalGUI.text.config(state=DISABLED)
        self.textFrame.pack(side=BOTTOM)

    '''
        To remove the text frame from the GUI
    '''
    def pack_forget(self):
        self.textFrame.grid_forget()

    '''
        static function; can be used without creating an object
        acts as a print statement for the text board on GUI. Any kind of writing is disabled
        on the text board which is only enabled when printing something and then is
        immediately closed. Also, the text board is automatically scrolled to the end
        when something is printed on it.
    '''
    @staticmethod
    def print_func(string):
        TerminalGUI.text.config(state=NORMAL)
        TerminalGUI.text.insert(END, string+"\n")
        TerminalGUI.text.insert(END, "------------------------------------------------\n")
        TerminalGUI.text.yview(END)
        TerminalGUI.text.config(state=DISABLED)