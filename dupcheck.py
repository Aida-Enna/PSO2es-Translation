#!/usr/bin/env python3
# coding=utf8
import codecs
import fnmatch
import os
# import pprint
import json
import sys

# count errros
counterr = 0
bufout = "FILE: ID\n"
ENMap = dict()

# Need the json path
if len(sys.argv) < 2:
    print("Where the json folder?")
    sys.exit(os.EX_NOINPUT)


dir = sys.argv[1]

json_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_*.txt')
]

json_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_Actor_*.txt')
]

json_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_SkillRing.txt')
]

json_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_System.txt')
]

json_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Name_Actor_MagName.txt')
]

json_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Items_Leftovers.txt')
]

for files in json_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        try:
            djson = json.load(json_file)
            for rmid in djson:
                if (("tr_text" in rmid) and (rmid["tr_text"] != "")):
                    t = rmid["tr_text"]
                    tl = t.lower()
                    j = rmid["jp_text"]
                    jl = j.lower()
                    if t not in ENMap:
                        ENMap[t] = jl
                    elif ENMap[t] != jl:
                        bufout += ("{}:{} '{}'/'{}' wants the mapping of '{}'/'{}'\n".format(
                            os.path.splitext(os.path.basename(files))[0],
                            rmid["assign"], j, jl, t, tl))
                        counterr += 1
        except ValueError as e:
            counterr += 1
            print("%s: %s") % (files, e)

if counterr != 0:
    sys.exit(bufout)
