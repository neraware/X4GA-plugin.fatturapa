# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturapa_cfg/ftdif.py
# Copyright:    (C) 2015 Marcello Montaldo <m.montaldo@astra-srl.com>
# ------------------------------------------------------------------------------


import wx

import stormdb as adb

import awc.controls.windows as aw
import cfg.ftdif_wdr as wdr

from Env import Azienda
bt = Azienda.BaseTab

    
from cfg.ftdif import FtDifPanel

class _FatturaPA_FtDifPanel(FtDifPanel):
    """
    Frame impostazione fatturazione differita
    """

    def InitAnagCard(self, parent):
        ci = lambda x: self.FindWindowById(x)
        p = wx.Panel( parent, -1)
        main_sizer = wdr.FtDifCardFunc( p, True )
        
        from awc.controls.radiobox import RadioBox
        item=RadioBox( p, wx.NewId(), "Considera ", wx.DefaultPosition, wx.DefaultSize, ["Tutte le Anagrafiche","Solo Soggetti a Fatturaz.Elettronica","Escludi Soggetti a Fatturaz.Elettronica"] , 1, wx.RA_SPECIFY_ROWS )
        item.SetName("f_tipopdc")
        main_sizer.Add(item, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        px, py = p.GetSize()
        _itemx, itemy = item.GetSize()
        self.SetMinSize((px+100, py + itemy + 100))
        
        self.FindWindowByName('descriz').ForceUpperCase(False)
        for cbi, name in ((wdr.ID_SEPALL,   'f_sepall'),
                          (wdr.ID_SEPMP,    'f_sepmp'),
                          (wdr.ID_SEPDEST,  'f_sepdest'),
                          (wdr.ID_SOLOSTA,  'f_solosta'),
                          (wdr.ID_SETACQ,   'f_setacq'),
                          (wdr.ID_SETANN,   'f_setann'),
                          (wdr.ID_SETGEN,   'f_setgen'),
                          (wdr.ID_NODESRIF, 'f_nodesrif'),):
            ci(cbi).SetDataLink(name, {True: 1, False: 0})
        item.SetDataLink(values=['T','E','A'])
            
        ci(wdr.ID_F_CHGMAG).SetDataLink(values=[0,1])
        docs = adb.DbTable(bt.TABNAME_CFGMAGDOC, writable=False)
        docs.AddOrder('descriz')
        if docs.Retrieve():
            l = ci(wdr.ID_DOCS)
            for d in docs:
                l.Append(d.descriz)
                self.docs.append(d.id)
            self.Bind(wx.EVT_CHECKLISTBOX, self.OnDdrModif, l)
        self.Bind(wx.EVT_RADIOBOX, self.OnChgMag, ci(wdr.ID_F_CHGMAG))
        return p

import cfg.ftdif as ftdif
ftdif.FtDifPanel = _FatturaPA_FtDifPanel
