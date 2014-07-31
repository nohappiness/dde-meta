#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
from ConfigParser import ConfigParser
class CaseConfigParser(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)
    def optionxform(self,optionstr):
        return optionstr
    def write(self, fp):
    	if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s=%s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    key = "=".join((key, str(value).replace('\n', '\n\t')))
                fp.write("%s\n" % (key))
            fp.write("\n")

		

def get_mode(config='/usr/share/dde-misc/fix_desktop_translation.conf'):
    with open(config) as f_in:
        lines = list(line for line in (l.strip() for l in f_in) if (line and not line.startswith('#')))
        return lines

def get_sections():
    try:
        return cf.sections()
    except:
        return None

def get_value(section,key):
    try:
        return cf.get(section,key)
    except:
        return None

def set_value(section,key,value):
    try:
        cf.set(section,key,value)
    except:
        cf.add_section(section)
        cf.set(section,key,value)

desktopfilepath = '/usr/share/applications/'

for action_mode in get_mode():
    action_list = action_mode.split(',')
    app = action_list[0].replace('"','')
    action = action_list[1].replace('"','')
    section = action_list[2].replace('"','')
    try:
        key = action_list[3].replace('"','')
    except:
        key = None
    try:
        value = action_list[4].replace('"','')
    except:
        value = None

    print ("Now will %s from %s: [%s] %s -> %s" % (action, app, section, key, value))
    
    desktopfile = desktopfilepath + app + '.desktop'
    if os.path.isfile(desktopfile):
        cf = CaseConfigParser()
        cf.read(desktopfile)
        if action == 'Add' and key is not None and value is not None:
            if not get_value(section,key):
                set_value(section, key, value)
            else:
                print ("Ignore: the key:%s of section:%s already has value" % (key,section))
        elif action == 'Replace' and key is not None and value is not None:
            if get_value(section,key):
                set_value(section, key, value)
            else:
                print ("Ignore: the key:%s of section:%s does not exist" % (key,section))
        elif action == 'Delete' and key is None and value is None:
            try:
                cf.remove_section(section)
            except:
                pass
        elif action == 'Delete' and key is not None and value is None:
            try:
                cf.remove_option(section,key)
            except:
                pass
        else:
            print ("No support action yet! -> %s" % action_mode)
            exit()
            
        cf.write(open(desktopfile,"w"))
