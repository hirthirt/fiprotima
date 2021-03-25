#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012, Jean-Rémy Bancel <jean-remy.bancel@telecom-paristech.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Chromagon Project nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Jean-Rémy Bancel BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Parse the Chrome Cache File
See http://www.chromium.org/developers/design-documents/network-stack/disk-cache
for design details
"""

import gzip
import os
import struct
import sys
import datetime

from Model.EdgeModel.Cache.cacheAddress import CacheAddress
from Model.EdgeModel.Cache.cacheBlock import CacheBlock
from Model.EdgeModel.Cache.cacheData import CacheData
from Model.EdgeModel.Cache.cacheEntry import CacheEntry

from Model.EdgeModel.Cache.base import (
    BaseCacheHandler,
    Caretaker
)


class CacheEntryHandler(BaseCacheHandler):

    def __init__(self, profile_path: str,):
        self.cache_path = profile_path + "/Cache"
        self.file_name = "index"
        super().__init__(self.cache_path, self.file_name)
        self.cache_entries = []

    def init(self):
        """
        Reads the whole cache and store the collected data in a table
        or find out if the given list of urls is in the cache. If yes it
        return a list of the corresponding entries.
        """
        # Verifying that the path end with / (What happen on windows?)
        path = os.path.abspath(self.cache_path) + '/'

        cacheBlock = CacheBlock(path + "index")

        # Checking type
        if cacheBlock.type != CacheBlock.INDEX:
            raise Exception("Invalid Index File")

        index = open(path + "index", 'rb')

        # Skipping Header
        index.seek(92*4)

        # If no url is specified, parse the whole cache
        for key in range(cacheBlock.tableSize):
            raw = struct.unpack('I', index.read(4))[0]
            if raw != 0:
                entry = CacheEntry(CacheAddress(raw, path=path))
                # Checking if there is a next item in the bucket because
                # such entries are not stored in the Index File so they will
                # be ignored during iterative lookup in the hash table
                while entry.next != 0:
                    self.caretakers.append(Caretaker(entry))
                    self.cache_entries.append(entry)
                    entry = CacheEntry(CacheAddress(entry.next, path=path))
                self.caretakers.append(Caretaker(entry))
                self.cache_entries.append(entry)

    def get_all_id_ordered(self):
        if not self.cache_entries:
            self.init()
        return self.cache_entries
        
    def commit(self):
        for entry in self.cache_entries:
            if entry.is_date_changed:
                block = open(entry.addr.path + entry.addr.fileSelector, "r+b")
                block.seek(8192 + entry.addr.blockNumber*entry.addr.entrySize + 24)
                block.write(struct.pack("Q", entry.creationTime))
                block.close()

        """
        This part should manipulate the http header timestamps
        Dosen´t work properly at the moment

        if entry.httpHeader:
            http = entry.httpHeader
            timestamp = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
            timestamp = bytes(timestamp, "utf-8")
            http_block = open(http.address.path + http.address.fileSelector, 'r+b')
            if http.date_start:
                print(http.date_start)
                date_start = 8192 + http.address.blockNumber*http.address.entrySize + http.date_start
                http_block.seek(date_start)
                #http_block.write(struct.pack("s", string))
                date = str(struct.unpack("200s", http_block.read(200))[0])
                print(date)
            
            if http.expires_start:
                expires_start = 8192 + http.address.blockNumber*http.address.entrySize + 16 + http.expires_start
                http_block.seek(expires_start)
                #http_block.write(struct.pack("s", timestamp))
                date = str(struct.unpack("200s", http_block.read(200))[0])
                print(date)
            
            if http.modified_start:
                modified_start = 8192 + http.address.blockNumber*http.address.entrySize + 24 + http.modified_start
                http_block.seek(modified_start)
                #http_block.write(struct.pack("s", timestamp))
                date = str(struct.unpack("200s", http_block.read(200))[0])
            

            http_block.close()
        """
        super().commit()


	
