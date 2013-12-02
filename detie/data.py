#!/usr/bin/env python
# encoding: utf-8

from detie.settings import DATA_DIR
import os
from lxml import etree 

class BaseData(object):
    """A base data class to define a protocol for iterate all the data records/entries"""

    def __init__(self, filename):
        self._filename = filename

    def __iter__(self):
        return self.texts
        
    @property
    def absolute_file_path(self):
        return os.path.join(DATA_DIR, self._filename)

    @property
    def records(self):
        return self._records()

    @property
    def texts(self):
        return self._texts()

    def _records(self):
        raise NotImplementedError()

    def _texts(self):
        raise NotImplementedError()

class NLPIRXMLData(BaseData):
    """Class to handle NLPIR data in xml format"""

    def __iter__(self):
        return self.records

    def _records(self):
        itertree = etree.iterparse(self.absolute_file_path)
        latest_id = ''
        latest_article = ''
        latest_time = ''
        for event, elem in itertree:
            if event != 'end': continue

            if elem.tag == 'id':
                latest_id = elem.text
            elif elem.tag == 'article':
                latest_article = elem.text
            elif elem.tag == 'time':
                latest_time = elem.text
            if elem.tag == 'RECORD':
                record = {
                        'id':latest_id,
                        'texts':latest_article,
                        'datetime':latest_time}
                yield record

    def _texts(self):
        itertree = etree.iterparse(self.absolute_file_path)
        for event, elem in itertree:
            if event != 'end': continue
            
            if elem.tag == 'article':
                yield elem.text


class DictData(BaseData):
    def _texts(self):
        with open(self.absolute_file_path) as f:
            while True:
                line = f.readline()
                if line:
                    l = line.decode('gbk').strip()
                    if len(l)==1: continue
                    else: yield l
                else: break

class SetData(BaseData):
    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        with open(self.absolute_file_path) as f:
            self._chars =set([c.strip().decode('utf8') for c in f.read().split('\n')])

    def __contains__(self, char):
        return char in self._chars
