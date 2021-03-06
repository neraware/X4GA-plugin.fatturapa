﻿#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturapa_plugin.py
# Copyright:    (C) 2014 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------

title = """Fattura Elettronica per la Pubblica Amministrazione"""

description = title

author = 'Fabio Cassini <fc@f4b10.org>'

from fatturapa_ver import *  # @UnusedWildImport
from fatturapa_env import TabStru # @UnusedImport

import fatturapa_frame  # @UnusedImport
import fatturapa_cfg.ftdif  # @UnusedImport
import fatturapa_cfg.azisetup  # @UnusedImport
import fatturapa_magazz.ftdif  # @UnusedImport
import fatturapa_magazz.dbftd  # @UnusedImport
