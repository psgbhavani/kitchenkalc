from tkinter import *
import converter
import yo


class UI:
    def __init__(self):
        self.root = Tk()
        self.text = ''
        self.frame = None
        self.url = ''
        self.serving_size = ''
        self.url_msg = None
        self.ss_msg = None
        self.img = PhotoImage(file='actual.GIF')


    def run(self):
        self.img = PhotoImage(file='actual.GIF')
        self.root.wm_title("Kitchen Kalc")
        self.root.config(background = '#d3f7e0')
        self.root.resizable(False, False)

        self.start_screen()
    
        self.root.mainloop()


    def start_screen(self):
        Label(self.root, text='         Enter URL         ', bg='#d3f7e0', font=('times', 16, 'bold')).grid(row=0,
                                                   column=0, padx=10, pady=2)
        self.url = Entry(self.root)
        self.url.grid(row=1, column=0)
        
        Button(self.root, text='         GO         ',
               command=self._raise_infof, bg='#ba8c59').grid(row=2, column=0, padx=10, pady=2)

        Label(image = self.img).grid(row=3, column=0, padx=10, pady=2)
        Label(self.root, text='AUTHORS: Aishwarya B., Cynthia W., Grace C., Jenny C., Bhavani P.', bg='#d3f7e0').grid(row=5, column=0, padx=10, pady=2)
        
    def second_screen(self):
        t = Text(self.frame, height= 15,
                     width= 50, bg='#e9fdf0', fg='black')
        
        t.grid(row=3, column=0, padx=10, pady=2, sticky='nsew')
        t.insert(END, self.text)
        s = Scrollbar(self.frame)
        s.grid(row=3, column=1, padx=10, pady=2, sticky='nsew')
        t['yscrollcommand']=s.set

        self._make_back_button()
        self._make_ss_button()
        

    def _make_ss_button(self):
        Label(self.root, text='         Enter New Serving Size         ', bg='#d3f7e0', font=('times', 16, 'bold')).grid(
                row=0, column=0, padx=10, pady=2)
        self.serving_size = Entry(self.root)
        self.serving_size.grid(row=1, column=0)
        
        Button(self.root, text='  Get Conversion!  ',
               command=self._change_text, bg='#ba8c59').grid(row=2, column=0, padx=10, pady=2)

    def _make_back_button(self):
        Button(self.root, text='    Back    ',
               command=self.destroy_world, bg='#ba8c59').grid(row=4, column=0)

    def destroy_world(self):
        self.root.destroy()
        self.root=Tk()
        self.run()
        
    
    def _make_frame(self, color):
        self.frame = Frame(self.root, width=500, height=495,
              background = color).grid(row=3, column=0, padx=10, pady=2)
        

    def _raise_infof(self):
        try:
            url_text = ''
            url_text = self.url.get()
            print(url_text)
            if  not ('www.bettycrocker' in url_text or 'www.geniuskitchen' in url_text or 'www.foodnetwork' in url_text or 'www.marthastewart' in url_text) :
                print("1")
                raise TypeError
            
            self.text = self._temp_original(url_text)
            infof = self._make_frame('#ffccff')
            self.second_screen()
            if self.url_msg != None:
                self.url_msg.destroy()
        except TypeError:
            print("2")
            self.url_msg = Message(self.root, text='Please enter a valid URL.') 
            self.url_msg.grid(row=3, column=0)
            self.url_msg.config(bg='pink', width = 550, font=('times', 23, 'italic'),  borderwidth = 8, justify=CENTER, relief = RAISED)


    def _change_text(self):
        try:
            ss = ''
            ss = int(self.serving_size.get())
            if ss <= 0:
                raise ValueError
            self.text = self._temp_conversions(ss)
            self.second_screen()
            if self.ss_msg != None:
                self.ss_msg.destroy()
        except ValueError:
            self.ss_msg = Message(self.frame, text='Please enter a valid number.')
            self.ss_msg.grid(row=3, column=0)
            self.ss_msg.config(bg='pink', width = 550, font=('times', 23, 'italic'), borderwidth = 8, justify=CENTER, relief = RAISED)
                        
        
    def _temp_original(self, url: str):
        ''''''
        try:
            s = converter.to_str(converter.get_conversion_dict(url))
            if s == None or s == '':
                raise TypeError
            else:
                self.url = url
                return s
        except AttributeError:
            raise TypeError

    def _temp_conversions(self, ss: str):
        return converter.get_conversion(self.url, str(ss))



if __name__ =='__main__':
    UI().run()

