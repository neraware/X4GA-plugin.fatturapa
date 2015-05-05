# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturapa_magazz/ftdif.py
# Copyright:    (C) 2015 Marcello Montaldo <m.montaldo@astra-srl.com>
# ------------------------------------------------------------------------------


import wx
import awc.controls.windows as aw
import magazz.ftdif as mag


class _FatturaPA_MagazzFtDifPanel(mag.FtDifPanel):
    
    def test(self):
        lEsito=True
        lError=[]
        for d in self.ftd.docgen:
            nIvaNormale=0
            nIvaSplit  =0
            for m in self.ftd.movgen:
                if m.id_doc==-d.numdoc:
                    if not  m.id_aliqiva==None:
                        #if m.iva.perciva>0:
                        if m.iva.tipo=='S':
                            nIvaSplit += 1
                        else:
                            nIvaNormale += 1
            if nIvaSplit>0 and nIvaNormale>0:
                lError.append('%s - Doc.n.%s' % (d.pdc.descriz, d.numdoc))
        if len(lError)>0:
            lEsito=False
            msg="I seguenti documenti se generati conterranno\naliquote Iva di tipo promiscuo."
            for e in lError:
                msg='%s\n%s' % (msg, e)
            msg='%s\n%s' % (msg, "Continuare nella generazione?")
            
            if aw.awu.MsgDialog(self, msg,
                                style=wx.ICON_QUESTION|\
                                wx.YES_NO|wx.NO_DEFAULT) == wx.ID_YES:
                lEsito=True
        return lEsito
    
    def OnGenera(self, event):
        if self.test():
            if self.Genera():
                event.Skip()

mag.FtDifPanel = _FatturaPA_MagazzFtDifPanel
