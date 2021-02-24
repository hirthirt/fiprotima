import tkinter as tk
from tkinter import ttk

from datetime import datetime

class Content(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, width=200, height=150)
        self.parent = parent
        self.tree_frame = None
        self.tree_scroll_vertical = None
        self.tree_scroll_horizontal = None
        self.popup_menu = None
        self.dataview = None
        self.tab_control = None
        self.info = None
        self.style = None
        self.dataview_mode = "history"
        self.info_views = []

        self.body()


    def body(self):
        # Popup menu
        self.popup_menu = tk.Menu(self, tearoff=False)
        self.popup_menu.add_command(label="Ausgewählte editieren via Delta", command=lambda: self.parent.controller.edit_selected_data("delta"))
        self.popup_menu.add_command(label="Ausgewählte editieren via Datum", command=lambda: self.parent.controller.edit_selected_data("date"))
        self.popup_menu.add_command(label="Gesamte aktuelle Tablle editieren")

        # Treeview style
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        
        # Treeview in frame and scrollbars 
        self.tree_frame = tk.Frame(self)

        self.tree_scroll_vertical = tk.Scrollbar(self.tree_frame)
        self.tree_scroll_vertical.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_scroll_horizontal = tk.Scrollbar(self.tree_frame, orient="horizontal")
        self.tree_scroll_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

        self.dataview = ttk.Treeview(self.tree_frame, height=25, style="mystyle.Treeview", yscrollcommand=self.tree_scroll_vertical.set,
                                    xscrollcommand=self.tree_scroll_horizontal.set
        )
        self.dataview.pack(fill="both")
        self.tree_scroll_vertical.config(command=self.dataview.yview)
        self.tree_scroll_horizontal.config(command=self.dataview.xview)
        
        # Notebook for the additional information
        self.tab_control = ttk.Notebook(self) 

        self.tree_frame.pack(fill="both")
        self.tab_control.pack(side=tk.BOTTOM, fill="both", expand=True)

    def rebuild_treeview(self):
        self.dataview.pack_forget()
        self.tree_scroll_vertical.pack_forget()
        self.tree_scroll_horizontal.pack_forget()
        
        self.tree_scroll_vertical = tk.Scrollbar(self.tree_frame)
        self.tree_scroll_vertical.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_scroll_horizontal = tk.Scrollbar(self.tree_frame, orient="horizontal")
        self.tree_scroll_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

        self.dataview = ttk.Treeview(self.tree_frame, height=25, style="mystyle.Treeview", yscrollcommand=self.tree_scroll_vertical.set,
                                    xscrollcommand=self.tree_scroll_horizontal.set
        )
        self.dataview.pack(fill="both")
        self.tree_scroll_vertical.config(command=self.dataview.yview)
        self.tree_scroll_horizontal.config(command=self.dataview.xview)
        self.dataview.bind("<Button-3>", self.dateview_popup)

    def dateview_popup(self, e):
        self.popup_menu.tk_popup(e.x_root, e.y_root)
        
    
    # Receives additional data and builds tabs and treeviews to show it
    def fill_info_section(self, data):
        self.info_views = []
        for tab in self.tab_control.tabs():
            self.tab_control.forget(tab)

        for info in data:
                if data[info]:
                    tab = ttk.Frame(self.tab_control)
                    self.tab_control.add(tab, text=info) 
                    infoview = ttk.Treeview(tab)
                    headinglist = [attr.name for attr in data[info][0].attr_list if data[info]]
                    headinglist.append("data_name")
                    headinglist.append("id")
                    infoview["columns"] = tuple(headinglist[1:])
                    infoview["displaycolumns"] = tuple(headinglist[1:-2])
                    infoview.heading("#0",text=headinglist[0],anchor=tk.W)
                    for heading in headinglist[1:]:
                        infoview.heading(heading, text=heading, anchor=tk.W)
                    for item in data[info]:
                        values = [attr.value for attr in item.attr_list[1:]]
                        try:
                            values.append(str(item.__class__.__name__) + "Handler")
                            values.append(item.id)
                        except:
                            values.append("None")
                            values.append(0)
                        insert = infoview.insert("", "end",  text=item.attr_list[0].value, values=tuple(values))
                        if item.is_date_changed:
                            infoview.item(insert, tags=("edited"))
                    infoview.tag_configure('edited', background='green') 
                    infoview.pack(expand=True, fill="both")
                    self.info_views.append(infoview)
                else:
                    tab = ttk.Frame(self.tab_control)
                    self.tab_control.add(tab, text=info)
                    text = "Es konnten keine Informationen gefunden werden!"
                    label = tk.Label(tab, text=text)
                    label.pack(expand=True, fill="both")
        
    # Receives data and inserts it into the main treeview (dataview)
    def fill_dataview(self, data, addi_infos):
        #self.dataview.pack_forget()
        #self.dataview = ttk.Treeview(self, height=25, style="mystyle.Treeview")
        #self.dataview.pack(fill="both")
        self.rebuild_treeview()

        self.tab_control.pack_forget()
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(side=tk.BOTTOM, expand=True, fill="both")

        headinglist = [attr.name for attr in data[0].attr_list]
        headinglist.append("data_name")
        headinglist.append("id")
        self.dataview["columns"] = tuple(headinglist[1:])
        self.dataview["displaycolumns"] = tuple(headinglist[1:-2])
        self.dataview.heading("#0",text=headinglist[0],anchor=tk.W)
        for heading in headinglist[1:]:
            self.dataview.heading(heading, text=heading, anchor=tk.W)
        for item in data:
            values = [attr.value for attr in item.attr_list[1:]]
            try:
                values.append(str(item.__class__.__name__) + "Handler")
                values.append(item.id)
            except:
                values.append("None")
                values.append(0)
            insert = self.dataview.insert("", "end",  text=item.attr_list[0].value, values=tuple(values))
            if item.is_date_changed:
                self.dataview.item(insert, tags=("edited"))
        self.dataview.tag_configure('edited', background='green')
        if not addi_infos:
            text = "Zusätzliche Informationen nicht verfügbar!"
            label = tk.Label(self.tab_control, text=text)
            label.pack(expand=True, fill="both")
        else:
            self.dataview.bind('<Double-1>', self.parent.controller.load_additional_info)

    # Fill the main treeview (dataview) with history data. Extra method to load dependencies correctly
    def fillHistroyData(self, history_data):
        self.dataview_mode="history"
        for child in self.dataview.get_children():
            self.dataview.delete(child)

        self.rebuild_treeview()

        self.tab_control.pack_forget()
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(side=tk.BOTTOM, expand=True, fill="both") 
        
        if history_data == "None":
            return

        self.dataview["columns"]=("visit","l_visit", "data_name", "id")
        self.dataview["displaycolumns"] = ("visit","l_visit")
        self.dataview.column("#0", width=700, minwidth=300, stretch=tk.YES)
        self.dataview.column("visit", width=300, minwidth=100, stretch=tk.YES)
        self.dataview.column("l_visit", width=300, minwidth=100, stretch=tk.YES)
        self.dataview.heading("#0",text="URL",anchor=tk.W)
        self.dataview.heading("id", text="ID",anchor=tk.W)
        self.dataview.heading("visit", text="Besucht",anchor=tk.W)
        self.dataview.heading("l_visit", text="Letzter Besuch",anchor=tk.W)
        for entry in history_data:
            v_date = None
            lv_date = None
            for attr in entry.attr_list:
                if attr.name == "Zuletzt besucht":
                    lv_date = attr.value.strftime("%d.%m.%Y %H:%M:%S")
                elif attr.name == "Besucht am":
                    v_date = attr.value.strftime("%d.%m.%Y %H:%M:%S")
            parent = self.dataview.insert("", "end",  text=entry.place.url, tags=("bg"), values=(v_date, lv_date, str(entry.__class__.__name__) + "Handler", entry.id))
            if entry.is_date_changed:
                            self.dataview.item(parent, tags=("edited"))               
            if history_data[entry]:
                for sube in history_data[entry]:
                    v_date = None
                    lv_date = None
                    for attr in sube.attr_list:
                        if attr.name == "Zuletzt besucht":
                            lv_date = attr.value.strftime("%d.%m.%Y %H:%M:%S")
                        elif attr.name == "Besucht am":
                            v_date = attr.value.strftime("%d.%m.%Y %H:%M:%S")
                    child = self.dataview.insert(parent, "end",  text=sube.place.url, values=(v_date,lv_date, str(entry.__class__.__name__) + "Handler", sube.id))
                    if entry.is_date_changed:
                            self.dataview.item(child, tags=("edited")) 
        self.dataview.bind('<Double-1>', self.parent.controller.load_additional_info)
        self.dataview.tag_configure('bg', background='#DFDFDF')
        self.dataview.tag_configure('edited', background='green')