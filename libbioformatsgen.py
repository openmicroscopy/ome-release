#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from utils import RSYNC_PATH, get_version, get_tag
from doc_generator import find_pkg, repl_all


def usage():
    print "bfcppgen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

# Read major and minor version from input version
major_version, minor_version = get_version(version)

repl["@TAG_URL@"] = get_tag("bioformats", version)
repl["@DOC_URL@"] = (
    "http://www.openmicroscopy.org/site/support/bio-formats%s.%s"
    % (major_version, minor_version))

PREFIX = os.environ.get('PREFIX', 'libbioformats')
BF_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("DOC", "artifacts/Bio-Formats-@VERSION@.pdf"),
        ("DOXYGEN", "artifacts/bio-formats-javadocs.zip"),
        ("SOURCE_CODE", "artifacts/bioformats-@VERSION@.zip"),
        ("CPP_OSX108", "artifacts/bioformats-cpp-@VERSION@-MacOSX10.8.zip"),
        ("CPP_CENTOS65",
         "artifacts/bioformats-cpp-@VERSION@-CentOS6.5-x86_64.zip"),
        ):

    find_pkg(repl, BF_RSYNC_PATH, x, y)


for line in fileinput.input(["libbioformats_downloads.html"]):
    print repl_all(repl, line, check_http=True),
