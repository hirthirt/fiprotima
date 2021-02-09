import tkinter as tk
from tkinter import ttk

from datetime import datetime
from urllib.parse import urlparse

class Content(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, width=200, height=150)
        self.parent = parent
        self.dataview = None
        self.tab_control = None
        self.info = None
        self.style = None
        self.dataview_mode = "history"

        self.body()


    def body(self):
        # Treeview for main data
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        self.dataview = ttk.Treeview(self, height=20, style="mystyle.Treeview")

        self.tab_control = ttk.Notebook(self) 



        self.dataview.pack(expand=True, fill="both")
        self.tab_control.pack(side=tk.BOTTOM, expand=True, fill="both") 
        

    # On right-click load all the additional infos for the given website
    def click_column(self, a):
        for tab in self.tab_control.tabs():
            self.tab_control.forget(tab)

        item = self.dataview.item(self.dataview.focus())
        parsed_uri = urlparse(item["text"])
        split = parsed_uri.hostname.split(".")
        if len(split) > 2:
            sitename = split[1]
        else:
            sitename = split[0]
        infos = self.parent.controller.get_additional_info(sitename)

        for info in infos:
            if infos[info]:
                tab = ttk.Frame(self.tab_control)
                self.tab_control.add(tab, text=info) 
                infoview = ttk.Treeview(tab)
                headinglist = [attr.name for attr in infos[info][0].attr_list if infos[info]]
                infoview["columns"] = tuple(headinglist[1:])
                infoview.heading("#0",text=headinglist[0],anchor=tk.W)
                for heading in headinglist[1:]:
                    infoview.heading(heading, text=heading, anchor=tk.W)
                for item in infos[info]:
                    infoview.insert("", "end",  text=item.attr_list[0].value, values=tuple([attr.value for attr in item.attr_list[1:]]))
                infoview.pack(expand=True, fill="both")
            else:
                tab = ttk.Frame(self.tab_control)
                self.tab_control.add(tab, text=info)
                text = "Es konnten keine Informationen gefunden werden!"
                label = tk.Label(tab, text=text)
                label.pack(expand=True, fill="both")


    def change_data_view(self, data_view):
        if self.dataview_mode == data_view:
            return
        if data_view == "addons":
            pass
        elif data_view == "inputhistory":
            data = self.parent.controller.get_form_history()
            if data:
                self.fill_dataview(data, False)
                self.dataview_mode = data_view
        elif data_view == "history":
            data = self.parent.controller.get_history()
            print(data)
            if data:
                self.fillHistroyData(data)
                self.dataview_mode = data_view


    def fill_dataview(self, data, addi_infos):
        self.dataview.pack_forget()
        self.dataview = ttk.Treeview(self, height=20, style="mystyle.Treeview")
        self.dataview.pack(expand=True, fill="both")

        headinglist = [attr.name for attr in data[0].attr_list]
        self.dataview["columns"] = tuple(headinglist[1:])
        self.dataview.heading("#0",text=headinglist[0],anchor=tk.W)
        for heading in headinglist[1:]:
            self.dataview.heading(heading, text=heading, anchor=tk.W)
        for item in data:
            self.dataview.insert("", "end",  text=item.attr_list[0].value, values=tuple([attr.value for attr in item.attr_list[1:]]))

        if not addi_infos:
            text = "Es konnten keine Informationen gefunden werden!"
            label = tk.Label(self.tab_control, text=text)
            label.pack(expand=True, fill="both")

    # Fill the Treeview with the data from the model
    def fillHistroyData(self, history_data):
        self.dataview_mode="histroy"
        for child in self.dataview.get_children():
            self.dataview.delete(child)

        self.tab_control.pack_forget()
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(side=tk.BOTTOM, expand=True, fill="both") 
        
        self.dataview.bind('<ButtonRelease-1>', self.click_column)

        self.dataview["columns"]=("id","visit","l_visit","object")
        self.dataview["displaycolumns"] = ("visit","l_visit")
        self.dataview.column("#0", width=200, minwidth=120, stretch=tk.YES)
        self.dataview.column("visit", width=100, minwidth=60, stretch=tk.YES)
        self.dataview.column("l_visit", width=100, minwidth=60, stretch=tk.YES)
        self.dataview.heading("#0",text="URL",anchor=tk.W)
        self.dataview.heading("id", text="ID",anchor=tk.W)
        self.dataview.heading("visit", text="Besucht",anchor=tk.W)
        self.dataview.heading("l_visit", text="Letzter Besuch",anchor=tk.W)
        for entry in history_data:
            v_date = None
            lv_date = None
            for attr in entry.attr_list:
                if attr.name == "Zuletzt besucht":
                    lv_date = attr.value.strftime("%d.%m.%Y %H:%M")
                elif attr.name == "Besucht am":
                    v_date = attr.value.strftime("%d.%m.%Y %H:%M")
            parent = self.dataview.insert("", "end",  text=entry.place.url, tags=("bg"), values=(entry.id,v_date,lv_date, entry))
            if history_data[entry]:
                for sube in history_data[entry]:
                    v_date = None
                    lv_date = None
                    for attr in entry.attr_list:
                        if attr.name == "Zuletzt besucht":
                            lv_date = attr.value.strftime("%d.%m.%Y %H:%M")
                        elif attr.name == "Besucht am":
                            v_date = attr.value.strftime("%d.%m.%Y %H:%M")
                    self.dataview.insert(parent, "end",  text=sube.place.url, values=(sube.id,v_date,lv_date, sube))
        
        self.dataview.tag_configure('bg', background='#DFDFDF')