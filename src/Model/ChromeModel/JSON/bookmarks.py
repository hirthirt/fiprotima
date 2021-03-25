import json
import random
import hashlib

from Model.util import log_message
from Model.ChromeModel.JSON.base import (
    BaseJSONHandler,
    BaseJSONClass,
    BaseAttribute,
    Caretaker,
    OTHER,
    DT_SEC,
    DT_SIMPLE_STRING,
    DT_WEBKIT,
    DT_WEBKIT_SEC,
    DT_SEC_DOT_MICRO
)

NAME = "Name"
TYP = "Typ"
DATEADDED = "Hinzugefügt am"
DATEMODIFIED = "Bearbeitet am"




class Bookmark(BaseJSONClass):
    def __init__(self, id, name, typ, date_added, date_modified=None):
        self.id = id
        self.name = name
        self.typ = typ
        self.date_added = date_added
        self.date_modified = date_modified

        

        self.init()

    def init(self):
        self.is_date_changed = False
        self.attr_list = []
        self.attr_list.append(BaseAttribute(NAME, OTHER, self.name))
        self.attr_list.append(BaseAttribute(TYP, OTHER, self.typ))
        self.attr_list.append(BaseAttribute(DATEADDED, DT_WEBKIT, self.date_added))
        if self.typ == "folder":
            self.attr_list.append(BaseAttribute(DATEMODIFIED, DT_WEBKIT, self.date_modified))
        else:
            self.attr_list.append(BaseAttribute("None", OTHER, self.date_modified))

        


    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Lesezeichen", "error")
            return
        for attr in self.attr_list:
            if attr.name == DATEADDED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.date_added = attr.timestamp
                except:
                    log_message("Fehler bei Update in Lesezeichen für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == DATEMODIFIED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.date_modified = attr.timestamp
                except:
                    log_message("Fehler bei Update in Lesezeichen für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class BookmarkHandler(BaseJSONHandler):
    name = "Bookmark"

    def __init__(
        self, profile_path: str, file_name: str = "Bookmarks"
    ):
        self.bookmarks = {}
        super().__init__(profile_path, file_name)

    def get_all_id_ordered(self):
        if self.bookmarks:
            return self.bookmarks

        
        self.open_file()
        self.json_all = json.loads(self.read_file())
        self.close()

        root = self.json_all["roots"]
        for elem in root:
            if root[elem]["type"] == "folder":
                id = int(root[elem]["id"])
                name = root[elem]["name"]
                typ = root[elem]["type"]
                date_added = root[elem]["date_added"]
                date_modified = root[elem]["date_modified"]
                bookmark = Bookmark(id, name, typ, date_added, date_modified)
                self.bookmarks[id] = bookmark
                self.caretakers.append(Caretaker(bookmark))
                if root[elem]["children"]:
                    self.get_bookmarks_recursiv(root[elem]["children"])
            else:
                id = int(root[elem]["id"])
                name = root[elem]["name"]
                typ = root[elem]["type"]
                date_added = root[elem]["date_added"]
                bookmark = Bookmark(id, name, typ, date_added)
                self.bookmarks[id] = bookmark
                self.caretakers.append(Caretaker(bookmark))

        
        return [self.bookmarks[key] for key in self.bookmarks]
    
    def get_bookmarks_recursiv(self, root):
        for elem in root:
            if elem["type"] == "folder":
                id = int(elem["id"])
                name = elem["name"]
                typ = elem["type"]
                date_added = elem["date_added"]
                date_modified = elem["date_modified"]
                bookmark = Bookmark(id, name, typ, date_added, date_modified)
                self.bookmarks[id] = bookmark
                self.caretakers.append(Caretaker(bookmark))
                if elem["children"]:
                    self.get_bookmarks_recursiv(elem["children"])
            else:
                id = int(elem["id"])
                name = elem["name"]
                typ = elem["type"]
                date_added = elem["date_added"]
                bookmark = Bookmark(id, name, typ, date_added)
                self.bookmarks[id] = bookmark
                self.caretakers.append(Caretaker(bookmark))

    def set_bookmarks_recursiv(self,root):
        for elem in root:
            if elem["type"] == "folder":
                elem["date_added"] = self.bookmarks[int(elem["id"])].date_added
                elem["date_modified"] = self.bookmarks[int(elem["id"])].date_modified
                if elem["children"]:
                    children = self.set_bookmarks_recursiv(elem["children"])
                    elem["children"] = children        
            else:
                 elem["date_added"] = self.bookmarks[int(elem["id"])].date_added
        return root

    def checksum_bookmarks(self, bookmarks):
        roots = ['bookmark_bar', 'other', 'synced']
        md5 = hashlib.md5()

        def checksum_node(node):
            md5.update(node['id'].encode())
            md5.update(node['name'].encode('utf-16le'))
            if node['type'] == 'url':
                md5.update(b'url')
                md5.update(node['url'].encode())
            else:
                md5.update(b'folder')
                if 'children' in node:
                    for c in node['children']:
                        checksum_node(c)

        for root in roots:
            checksum_node(bookmarks['roots'][root])
        return md5.hexdigest()

    def commit(self):
        
        root = self.json_all["roots"]
        for elem in root:
            if root[elem]["type"] == "folder":
                root[elem]["date_added"] = str(self.bookmarks[int(root[elem]["id"])].date_added)
                root[elem]["date_modified"] = str(self.bookmarks[int(root[elem]["id"])].date_modified)
                if root[elem]["children"]:
                    children = self.set_bookmarks_recursiv(root[elem]["children"])
                    root[elem]["children"] = children
            else:
                root[elem]["date_added"] = self.bookmarks[int(root[elem]["id"])].date_added
        
        self.json_all["roots"] = root

        checksum = self.checksum_bookmarks(self.json_all)
        self.json_all["checksum"] = str(checksum)

        self.write_file()

        super().commit()
