#!/usr/bin/env python
# encoding: utf-8

from detie.settings import DATA_DIR
import os
import cPickle
from lxml import etree 

class BaseData(object):
    """A base data class to define a protocol for iterate all the data records/entries"""

    def __init__(self, filename, encoding='utf8'):
        self._filename = filename
        self._encoding = encoding

    def __iter__(self):
        return self.texts
        
    @property
    def absolute_file_path(self):
        return os.path.join(DATA_DIR, self._filename)

    @property
    def exists(self):
        return os.path.isfile(self.absolute_file_path)

    @property
    def records(self):
        return self._records()

    @property
    def texts(self):
        return self._texts()

    def block_groups(self, count, line_count=1000):
        groups = []
        texts = self.texts
        while True:
            for i in range(count):
                lines = [l for n,l in enumerate(texts) if n<1000]
                if lines:
                    groups.append(lines)
                elif groups:
                    yield groups
                else:
                    return
            yield groups

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
    def _decode(self, text):
        try:
            return text.decode(self._encoding)
        except Exception, e:
            return ''

    def _texts(self):
        with open(self.absolute_file_path) as f:
            while True:
                line = f.readline()
                if line:
                    l = self._decode(line).strip()
                    if len(l)==1: continue
                    else: yield l
                else: break

    def write(self, list_):
        str_ = u'\n'.join(list_)
        with open(self.absolute_file_path, 'w') as f:
            f.write(str_.encode('utf8'))

class SetData(BaseData):
    def __init__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        with open(self.absolute_file_path) as f:
            self._chars =set([c.strip().decode('utf8') for c in f.read().split('\n')])

    def __contains__(self, char):
        return char in self._chars

    def to_regexp(self):
        return ur"[%s]" % (u''.join(self._chars))

class PickleData(BaseData):
    def read(self):
        with open(self.absolute_file_path) as f:
            return cPickle.load(f)

    def write(self, obj):
        with open(self.absolute_file_path, 'wb') as f:
            return cPickle.dump(obj, f)
