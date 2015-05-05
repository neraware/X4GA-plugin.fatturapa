#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturpa_frame.py
# Copyright:    (C) 2014 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------

import wx
from xframe import XFrame
import X_wdr as wdr

ID_FATTURAPA_SETUP =  wx.NewId()
ID_FATTURAPA_GENERA = wx.NewId()
ID_FATTURAPA_FOLDER = wx.NewId()
ID_FATTURAPA_ELENCO = wx.NewId()


class _EvaCli_XFrame(XFrame):
    
    def CreateXMenuBar(self, *args, **kwargs):
        
        menubar = XFrame.CreateXMenuBar(self, *args, **kwargs)
        
        menu = wx.Menu()
        for mid, func, voce, desc in (
                    
            (ID_FATTURAPA_SETUP, self._FatturaPA_OnSetup, 
             "Configurazione",
             "Configurazione della fattura elettronica"),):
            
            if mid is None:
                menu.AppendSeparator()
            else:
                menu.Append(mid, voce, desc)
                self.Bind(wx.EVT_MENU, func, id=mid)
        
        item = menubar.FindItemById(wdr.ID_MENUSETUP)
        if item:
            menucfg = item.GetSubMenu()
            menucfg.AppendSeparator()
            menucfg.AppendMenu(ID_FATTURAPA_SETUP, "Fattura Elettronica", menu)
        
        menu = wx.Menu()
        for mid, func, voce, desc in (
            
            (ID_FATTURAPA_ELENCO, self._FatturaPA_OnElenco, 
             "Documenti trasmessi/da trasmettere",
             "Visualizza l'elenco dei documenti fattura elettronica"),
            
            (None, None, None, None),
            
            (ID_FATTURAPA_GENERA, self._FatturaPA_OnGenera, 
             "Genera file per la trasmissione\tShift-Ctrl-F",
             "Genera file da trasmettere a SDI"),
            
            (ID_FATTURAPA_FOLDER, self._FatturaPA_OnFolder, 
             "Apri cartella files generati",
             "Apre la cartella dei files generati"),
            
            ):
            
            if mid is None:
                menu.AppendSeparator()
            else:
                menu.Append(mid, voce, desc)
                self.Bind(wx.EVT_MENU, func, id=mid)
        
        item = menubar.FindItemById(wdr.ID_MAGAZZINS)
        if item:
            menumag = item.GetMenu()
            menumag.AppendMenu(wx.NewId(), "Fattura Elettronica", menu)
        
        return menubar
    
    def _FatturaPA_OnSetup(self, event):
        
        from fatturapa_cfg.cfg_fatturapa import FatturaElettronicaSetupDialog
        self.LaunchFrame(FatturaElettronicaSetupDialog)
    
    def _FatturaPA_OnGenera(self, event):
        
        from fatturapa_magazz.fatturapa import FatturaElettronicaFrame
        self.LaunchFrame(FatturaElettronicaFrame)
    
    def _FatturaPA_OnFolder(self, event):
        
        from fatturapa_magazz.fatturapa import apri_cartella_files
        apri_cartella_files()
    
    def _FatturaPA_OnElenco(self, event):
        
        from fatturapa_magazz.fatturapa import ElencoFattureElettronicheFrame
        self.LaunchFrame(ElencoFattureElettronicheFrame)

import xframe
xframe.XFrame = _EvaCli_XFrame
