#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturapa_ver.py
# Copyright:    (C) 2014 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------

VERSION_MAJOR   = 1
VERSION_MINOR   = 12
VERSION_RELEASE = 3
VERSION_TAG     = ""

min_compat_ver = '1.1.00'
min_require_x4 = '1.5.60'

VERSION = (VERSION_MAJOR,
           VERSION_MINOR, 
           VERSION_RELEASE,
           VERSION_TAG)

version = "%s.%s.%s" % (VERSION_MAJOR, 
                        VERSION_MINOR, 
                        str(VERSION_RELEASE).zfill(2))
VERSION_STRING = version

if VERSION_TAG:
    version += ' '+VERSION_TAG

from fatturapa_verchg import plugin_history  # @UnusedImport

MODVERSION_NAME    = ""

MODVERSION_MAJOR   = 0
MODVERSION_MINOR   = 0
MODVERSION_RELEASE = 00
MODVERSION_TAG     = ""

MODVERSION = (MODVERSION_MAJOR, 
              MODVERSION_MINOR, 
              MODVERSION_RELEASE, 
              MODVERSION_TAG)

MODVERSION_STRING  = "%s.%s.%s" % (MODVERSION_MAJOR, 
                                   MODVERSION_MINOR, 
                                   str(MODVERSION_RELEASE).zfill(2))

if MODVERSION_TAG:
    MODVERSION_STRING += " %s" % MODVERSION_TAG

modversion = MODVERSION_STRING


MCOD_VERSION_NAME    = "Multi Codice"

MCOD_VERSION_MAJOR   = VERSION_MAJOR
MCOD_VERSION_MINOR   = VERSION_MINOR
MCOD_VERSION_RELEASE = VERSION_RELEASE
MCOD_VERSION_TAG     = VERSION_TAG

MCOD_VERSION = (MCOD_VERSION_MAJOR, 
                MCOD_VERSION_MINOR, 
                MCOD_VERSION_RELEASE, 
                MCOD_VERSION_TAG)

MCOD_VERSION_STRING  = "%s.%s.%s" % (MCOD_VERSION_MAJOR, 
                                     MCOD_VERSION_MINOR, 
                                     str(MCOD_VERSION_RELEASE).zfill(2))

if MCOD_VERSION_TAG:
    MCOD_VERSION_STRING += " %s" % MCOD_VERSION_TAG

mcod_version = MCOD_VERSION_STRING
