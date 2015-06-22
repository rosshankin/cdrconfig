from Tkinter import *
import db_pbx_target
import db_pbx_misconfig

class Database(Frame):

    def __init__(self,master):
        Frame.__init__(self,master)
        self.create_widgets()
        self.grid()
        self.pbx_map = {}
        self.pbx_map2 = {}

    def create_widgets(self):
        self.ent_ip = Entry(self, width = 19)
        self.ent_ip.grid(row = 1, column = 1)
        self.bttn_ip = Button(self, text = 'Go', command = self.ip)
        self.bttn_ip.grid(row = 1, column = 2, sticky = W)
        self.lb = Listbox(self, selectmode = SINGLE,exportselection = False)
        self.lb.grid(row = 3, column = 1)
        self.lb.bind("<Double-Button-1>", self.select)
        self.lbl_enable = Label(self, text = 'Enable CDR').grid(row = 5, column = 1,sticky = W)
        self.lbl_port = Label(self, text = 'CDR Port').grid(row = 6, column = 1, sticky = W)
        self.lbl_zone = Label(self, text = 'CDR Zone').grid(row = 7, column = 1, sticky = W)
        self.ent_bool = Entry(self, width = 18)
        self.ent_bool.grid(row = 5, column =1,columnspan = 3)
        self.ent_port = Entry(self,width = 18)
        self.ent_port.grid(row = 6,column = 1,columnspan = 3)
        self.ent_zone = Entry(self,width = 18)
        self.ent_zone.grid(row = 7,column = 1,columnspan = 3)
        self.bttn_last = Button(self,text="Last Entry",command = self.last)
        self.bttn_last.grid(row=2, column = 1)
        self.lbl_key = Label(self,text = 'Key').grid(row = 9,column = 1,columnspan = 2)
        self.lb_key = Listbox(self,selectmode = SINGLE,exportselection = False)
        self.lb_key.grid(row = 10, column = 1, columnspan = 2)
        self.lb_key.bind("<Double-Button-1>",self.key_select)
        self.lbl_value = Label(self, text = 'Value').grid(row = 9, column = 3,columnspan = 2)
        self.lb_value = Listbox(self,selectmode = SINGLE, exportselection = False)
        self.lb_value.grid(row = 10, column = 3, columnspan = 2)
        self.lb_value.bind("<Double-Button-1>", self.value_select)
        self.ent_key = Entry(self,width = 22)
        self.ent_key.grid(row = 11, column = 1, columnspan = 3, sticky = W)
        self.ent_value = Entry(self,width = 20)
        self.ent_value.grid(row = 11, column = 3, columnspan = 3)
        self.bttn_reset = Button(self, text = 'Reset', command = self.reset)
        self.bttn_reset.grid(row = 1, column = 3, sticky = W)
        self.lbl_success = Label(self, text = '', fg = 'green')
        self.lbl_success.grid(row = 12, column = 3, sticky = W)

    def ip(self):
        self.lb.delete(0,END)
        if self.ent_ip.get():
            f = open('/users/rosshankin/Documents/Python/cdr/ip_pbx.txt','w')
            ip = self.ent_ip.get()
            if not ip == "":
                f.write(ip)
            engine_name = 'postgresql+pg8000://postgres:molly36@' + ip + '/ross'
            import sqlalchemy as sqla
            engine = sqla.create_engine(engine_name)
            try:
                conn = engine.connect()
            except:
                self.ent_ip.delete(0,END)
                self.ent_ip.insert(0,'Invalid')
                return
            #sf_pbx
            result = conn.execute('select server_name,enable_cdr,cdr_port,cdr_zone from sf_pbx')
            for row in result:
                self.lb.insert(END,row[0])
                self.pbx_map[row[0]] = db_pbx_target.PBX(row[0],row[1],row[2],row[3])
            self.lb.selection_set(0)
            self.select(0)
        else:
            pass

    def add_item(self):
        if self.ent_add.get():
            item = self.ent_add.get()
            self.lb.insert(END,item)
            self.ent_add.delete(0,END)
        else:
            pass
        
    def select(self,event):
        self.ent_bool.delete(0,END)
        self.ent_zone.delete(0,END)
        self.ent_port.delete(0,END)
        self.lb_key.delete(0,END)
        self.lb_value.delete(0,END)
        self.ent_key.delete(0,END)
        self.ent_value.delete(0,END)
        t = self.lb.curselection()
        index = t[0]
        text = self.lb.get(index)
        zone = self.pbx_map[text].zone
        self.ent_zone.insert(0,zone)
        port = self.pbx_map[text].port
        self.ent_port.insert(0,port)
        enable = self.pbx_map[text].enable
        if enable == 1:
            self.ent_bool.insert(0,'True')
        elif enable == 0:
            self.ent_bool.insert(0,'False')
        #sf_miconfig
        if self.ent_ip.get():
            ip = self.ent_ip.get()
            engine_name = 'postgresql+pg8000://postgres:molly36@' + ip + '/ross'
            import sqlalchemy as sqla
            engine = sqla.create_engine(engine_name)
            conn = engine.connect()
            result = conn.execute("select sf_pbx.server_name, sf_miscconfig.key,sf_miscconfig.value from public.sf_pbx, public.sf_miscconfig where sf_pbx.server_name = sf_miscconfig.section")
            res = result.fetchall()
            t = self.lb.curselection()
            index = t[0]
            text = self.lb.get(index)
            for r in res:
                server_list= []
                server_list.append(r['server_name'])
                if text in server_list:
                    self.lb_key.insert(END,r['key']+'\n')
                    self.lb_value.insert(END,r['value']+'\n')

    def last(self):
        try:
            address_list = []
            f = open('/users/rosshankin/Documents/Python/cdr/ip_pbx.txt','r')
            fr = f.readlines()
            for item in fr:
                address_list.append(item)
            f.close()
            last = address_list[-1]
            self.ent_ip.delete(0,END)
            self.ent_ip.insert(0,last)
        except:
            self.ent_ip.delete(0,END)
            self.ent_ip.insert(0,'Re-enter IP Address')

    def key_select(self,event):
        self.ent_key.delete(0,END)
        self.lbl_success['text'] = ''
        t = self.lb_key.curselection()
        index = t[0]
        text = self.lb_key.get(index)
        self.ent_key.insert(0,text)
        
    def value_select(self,event):
        self.lbl_success['text'] = ''
        t = self.lb_value.curselection()
        index = t[0]
        text = self.lb_value.get(index)
        self.ent_value.insert(0,text)
        self.bttn_val = Button(self,text = 'Go',command = self.update_value)
        self.bttn_val.grid(row = 12, column = 2, sticky = E)
        
    def update_value(self):
        if self.ent_value.get() != '' and self.ent_key.get() != '':
            t = self.lb_value.curselection()
            index = t[0]
            text = self.lb_value.get(index)
            self.lb_value.delete(index,t)
            self.lb_value.insert(t,self.ent_value.get())
            ip = self.ent_ip.get()
            engine_name = 'postgresql+pg8000://postgres:molly36@' + ip + '/ross'
            import sqlalchemy as sqla
            engine = sqla.create_engine(engine_name)
            conn = engine.connect()
            value = self.ent_value.get()
            key = self.ent_key.get()
            t2 = self.lb.curselection()
            index2 = t2[0]
            text2 = self.lb.get(index2)
            try:
                conn.execute("update sf_miscconfig set value = '"  + value + "' where section = '" + text2 + "' and key = '" + key.rstrip() + "'")
                self.ent_value.delete(0,END)
                self.ent_key.delete(0,END)
                self.lbl_success['text'] = "Success"
            except:
                self.lbl_success['fg'] = 'red'
                self.lbl_success['text'] = 'Failure'
        elif self.ent_value.get() == '' or self.ent_key.get() == '':
            self.lbl_success['fg'] = 'red'
            self.lbl_success['text'] = 'Select key and value'

    def reset(self):
        self.lb.delete(0,END)
        self.ent_ip.delete(0,END)
        self.ent_bool.delete(0,END)
        self.ent_zone.delete(0,END)
        self.ent_port.delete(0,END)
        self.lb_key.delete(0,END)
        self.lb_value.delete(0,END)
        self.ent_key.delete(0,END)
        self.ent_value.delete(0,END)
        self.lbl_success['fg'] = 'green'
        self.lbl_success['text'] = ''
        
            
            

root = Tk()
root.title('Database GUI')
root.resizable(width = True, height = True)
db = Database(root)
root.mainloop()
                            