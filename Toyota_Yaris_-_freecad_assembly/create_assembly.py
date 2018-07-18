# -*- coding: utf-8 -*-

"""
Script to create Assembly Structure inside FreeCAD from filesystem hierarchy.

Usage:
Open Script with FreeCAD and provide absolute path of the root folder.

Example:
freecad `readlink -f create_assembly.py` /home/peter.friedrich/workspace/freecad_git_tryout/Toyota_Yaris_-_freecad_assembly/body_in_white___________________________PID0
"""


import json
import freecad.asm3.assembly
import FreeCAD
import sys
import fnmatch
import os


def main():
    basedir = sys.argv[3]
    s = Structure(basedir)
    s.create()
    s.export_to_json(os.path.join(os.path.split(basedir)[0], 'structure.json'))
    asm = FreeCADAssembly(s._groups, s._parts, os.path.split(s._basedir)[0])
    asm.start()


class Structure(object):

    def __init__(self, basedir):
        self._basedir = basedir
        self._groups = []
        self._parts = []

    def create(self):
        matches = []
        for root, dirnames, filenames in os.walk(self._basedir):
            for filename in fnmatch.filter(filenames, '*.fcstd'):
                matches.append(os.path.join(root, filename))
        parts = []
        groups = []
        for m in matches:
            m = os.path.relpath(m, os.path.split(self._basedir)[0])
            p, g = Structure.extract_path(m)
            parts.append(p)
            groups += g
        groupdict = {g['name']: g for g in groups}
        self._groups = [v for _, v in groupdict.items()]
        self._parts  = parts

    @staticmethod
    def parse_name(name):
        """Parse name like 'body_in_white___________________________PID_1' into name and label"""
        split = name.split('_')
        pid = name[name.find('PID'):]
        label = '_'.join(s for s in split[:-1] if s)
        if name.endswith('.fcstd'):
            pid = pid[:-6]
        return pid, label

    @staticmethod
    def extract_path(filename):
        """Extract Group Path from"""
        groups = []
        parent = ''
        for element in filename.split(os.path.sep)[:-1]:
            if element == '.':
                continue
            name, label = Structure.parse_name(element)
            groups.append({'name': name, 'label': label, 'parent': parent})
            parent = name

        p = os.path.split(filename)[1]
        name, label = Structure.parse_name(p)
        part = {'name': name, 'label': label, 'parent': parent, 'filename': filename}
        return part, groups

    def export_to_json(self, filename):
        _dict = {}
        _dict['parts'] = self._parts
        _dict['groups'] = self._groups

        with open(filename, 'w') as f:
            json.dump(_dict, f, indent=4)


class Assembly(object):

    def __init__(self, groups, parts, basedir):
        super(Assembly, self).__init__()
        self._groups = groups
        self._parts = parts
        self._basedir = basedir

    @classmethod
    def from_json(cls, filename):
        with open(filename, 'r') as f:
            _dict = json.load(f)
        groups = _dict.get('groups', [])
        parts = _dict.get('parts', [])
        basedir = os.path.dirname(filename)
        return cls(groups, parts, basedir)

    def abspath(self, path):
        return os.path.join(self._basedir, path)


class FreeCADAssembly(Assembly):

    def __init__(self, groups, parts, basedir, *args, **kwargs):
        super(FreeCADAssembly, self).__init__(groups, parts, basedir, *args, **kwargs)

    @property
    def document_name(self):
        return "assembly"

    def start(self):
        self.create_document()
        self.create_groups()
        for p in self._parts:
            self.create_part(p)

        App.setActiveDocument(self.document_name)

    def create_document(self):
        App.newDocument(self.document_name)
        App.setActiveDocument(self.document_name)
        App.ActiveDocument=App.getDocument(self.document_name)
        Gui.ActiveDocument=Gui.getDocument(self.document_name)

        doc = App.getDocument(self.document_name)
        doc.saveAs(self.abspath('assembly.fcstd'))

    def create_groups(self):
        doc = App.getDocument(self.document_name)

        for g in self._groups:
            obj = doc.addObject('App::Part', g['name'])
            obj.Label = g['label']

        for g in self._groups:
            if g['parent'] != '':
                obj = doc.getObject(g['name'])
                doc.getObject(g['parent']).addObject(obj)

    def create_part(self, part):
        doc = App.getDocument(self.document_name)

        newdoc = FreeCAD.open(self.abspath(part['filename']))

        if len(newdoc.RootObjects) > 1:
            print("More than one root object!")

        obj = newdoc.RootObjects[0]
        label, name = obj.Label, obj.Name
        doc.addObject('App::Link', part['name']).setLink(obj)
        doc.getObject(part['name']).Label = part['label']
        doc.getObject(part['parent']).addObject(doc.getObject(part['name']))



if __name__ == '__main__':
    main()
