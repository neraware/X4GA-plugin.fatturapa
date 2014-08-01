#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturapa_cfg/azisetup.py
#               (C) 2014 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------

import wx

from cfg.azisetup import AziendaSetupPanel

import fatturapa_cfg.azisetup_wdr as wdr

class _FatturaPA_AziendaSetupPanel(AziendaSetupPanel):
    
    def __init__(self, *args, **kwargs):
        
        AziendaSetupPanel.__init__(self, *args, **kwargs)
        
        for x in self.GetChildren():
            if isinstance(x, wx.Notebook):
                nb = x
                break
        self.panel_fatturapa = wx.Panel(nb)
        wdr.FatturaElettronicaFiller(self.panel_fatturapa)
        
        nb.InsertPage(1, self.panel_fatturapa, "Fattura PA")
        
        self.SetupRead()

import cfg.azisetup as azisetup
azisetup.AziendaSetupPanel = _FatturaPA_AziendaSetupPanel
