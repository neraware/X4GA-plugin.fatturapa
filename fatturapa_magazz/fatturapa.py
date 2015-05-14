#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturpa_magazz/fatturpa.py
# Copyright:    (C) 2014 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------

import os
def open_dir(f):
    if os.sys.platform.startswith('win'):
        f = f.replace('/', '\\')
    return os.startfile(f)  # @UndefinedVariable

import wx
import awc.controls.windows as aw
import awc.controls.dbgrid as dbglib
from awc.controls.linktable import EVT_LINKTABCHANGED

import fatturapa_magazz.fatturapa_wdr as wdr
import fatturapa_magazz.dbtables as dbfe
import fatturapa_cfg.dbtables as dbcfg

import Env
import report as rpt


_evtDOC_CHECKED = wx.NewEventType()
EVT_DOC_CHECKED = wx.PyEventBinder(_evtDOC_CHECKED)
class DocCheckedEvent(wx.PyCommandEvent):
    def __init__(self, parent):
        wx.PyCommandEvent.__init__(self, _evtDOC_CHECKED)
        self.SetEventObject(parent)
        self.SetId(parent.GetId())


FRAME_TITLE = "Documenti in formato Fattura Elettronica"

LEGEND_SELEZIONATO = 'cornflowerblue'
LEGEND_GIA_TRASMESSO = 'lightskyblue'
LEGEND_DA_TRASMETTERE = 'gray'
LEGEND_MANCA_CODICE_CIG = 'red'
LEGEND_MANCA_CODICE_CUP = 'yellow'


class ClientiMovimentatiGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbcli):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbcli,
                                 can_edit=True, can_insert=False, on_menu_select='row')
        
        cli = self.dbcli = dbcli
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        self.AddColumn(cli, 'codice', 'Cod.', col_width=40)
        self.AddColumn(cli, 'descriz', 'Ragione sociale', col_width=150, is_fittable=True)
        self.AddColumn(cli, 'id', '#pdc', col_width=1)
        
        self.CreateGrid()


class FatturaElettronicaGrid(dbglib.ADB_Grid):
    
    _canedit = True
    
    def __init__(self, parent, dbdoc):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbdoc,
                                 can_edit=True, can_insert=False, on_menu_select='row')
        
        doc = self.dbdoc = dbdoc
        tpd = doc.config
        pdc = doc.pdc
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        if self._canedit:
            self.AddColumn(doc, 'fe_sel', 'Sel.', col_width=40, col_type=self.TypeCheck())
        
        self.COL_TPDCOD = self.AddColumn(tpd, 'codice', 'Cod.', col_width=40)
        self.COL_TPDDES = self.AddColumn(tpd, 'descriz', 'Documento', col_width=150)
        self.COL_NUMDOC = self.AddColumn(doc, 'numdoc', 'Num.', col_type=self.TypeInteger(5))
        self.COL_DATDOC = self.AddColumn(doc, 'datdoc', 'Data', col_type=self.TypeDate())
        self.COL_PDCCOD = self.AddColumn(pdc, 'codice', 'Cod.', col_width=60)
        self.COL_PDCDES = self.AddColumn(pdc, 'descriz', 'Cliente', col_width=200, is_fittable=True)
        self.COL_BOLLOV = self.AddColumn(doc, 'ftel_bollovirt', 'Bollo V.', col_type=self.TypeFloat(5, 2), is_editable=self._canedit)
        self.COL_NUMORD = self.AddColumn(doc, 'ftel_ordnum', 'Ord.Acq.', col_width=80, is_editable=self._canedit)
        self.COL_DATORD = self.AddColumn(doc, 'ftel_orddat', 'Del', col_type=self.TypeDate(), is_editable=self._canedit)
        self.COL_CODCIG = self.AddColumn(doc, 'ftel_codcig', 'CIG', col_width=80, is_editable=self._canedit)
        self.COL_CODCUP = self.AddColumn(doc, 'ftel_codcup', 'CUP', col_width=110, is_editable=self._canedit)
        self.COL_RIFAMM = self.AddColumn(doc, 'ftel_rifamm', 'Rif.Amm.', col_width=120, is_editable=self._canedit)
        self.COL_NUMTRA = self.AddColumn(doc, 'ftel_numtrasm', 'N.Tras.', col_type=self.TypeInteger(5))
        self.COL_ID_DOC = self.AddColumn(doc, 'id', '#doc', col_width=1)
        self.COL_ID_PDC = self.AddColumn(pdc, 'id', '#pdc', col_width=1)
        
        self._col_sel = ci(doc, 'fe_sel')
        self._col_rfa = ci(doc, 'ftel_rifamm')
        self._col_num = ci(doc, 'ftel_numtrasm')
        self._col_oan = ci(doc, 'ftel_ordnum')
        self._col_oad = ci(doc, 'ftel_orddat')
        self._col_cig = ci(doc, 'ftel_codcig')
        self._col_cup = ci(doc, 'ftel_codcup')
        self._col_bol = ci(doc, 'ftel_bollovirt')
        self._col_tiv = ci(doc, 'totimposta')
        
        self.CreateGrid()
        
        if not self._canedit:
            self.AddTotalsRow(self.COL_PDCDES, 'Totali', (ci(doc, 'ftel_bollovirt'),))
    
    def CellEditAfterUpdate(self, row, gridcol, col, value):
        doc = self.dbdoc
        doc.MoveRow(row)
        
        if col == self._col_rfa:
            cmd = "UPDATE movmag_h SET ftel_rifamm=%%s WHERE id=%s" % doc.id
            doc._info.db.Execute(cmd, doc.ftel_rifamm[:20])
        if col == self._col_oan:
            cmd = "UPDATE movmag_h SET ftel_ordnum=%%s WHERE id=%s" % doc.id
            doc._info.db.Execute(cmd, doc.ftel_ordnum)
        elif col == self._col_oad:
            cmd = "UPDATE movmag_h SET ftel_orddat=%%s WHERE id=%s" % doc.id
            doc._info.db.Execute(cmd, doc.ftel_orddat)
        elif col == self._col_cig:
            cmd = "UPDATE movmag_h SET ftel_codcig=%%s WHERE id=%s" % doc.id
            doc._info.db.Execute(cmd, doc.ftel_codcig)
        elif col == self._col_cup:
            cmd = "UPDATE movmag_h SET ftel_codcup=%%s WHERE id=%s" % doc.id
            doc._info.db.Execute(cmd, doc.ftel_codcup)
        elif col == self._col_bol:
            cmd = "UPDATE movmag_h SET ftel_bollovirt=%%s WHERE id=%s" % doc.id
            doc._info.db.Execute(cmd, doc.ftel_bollovirt)
    
    def GetAttr(self, row, col, rscol, attr):
        attr = dbglib.ADB_Grid.GetAttr(self, row, col, rscol, attr)
        rs = self.dbdoc.GetRecordset()
        if 0 <= row < len(rs):
            r = rs[row]
            if r[self._col_sel]:
                bg = 'cornflowerblue'
            elif r[self._col_num]:
                bg = 'lightskyblue'
            else:
                bg = 'gray'
            if    (rscol == self._col_cig and not r[self._col_cig])\
               or (rscol == self._col_oan and not r[self._col_oan])\
               or (rscol == self._col_oad and not r[self._col_oad]):
                bg = 'red'
            elif rscol == self._col_cup and (r[self._col_cup] or '') == '':
                bg = 'yellow'
            elif rscol == self._col_bol and (r[self._col_tiv] or 0) == 0:
                bg = 'green'
            attr.SetBackgroundColour(bg)
        return attr
    
    def _SwapCheckValue(self, row, col):
        out = dbglib.ADB_Grid._SwapCheckValue(self, row, col)
        if col == 0:
            self.GetEventHandler().AddPendingEvent(DocCheckedEvent(self))
        return out

class FatturaElettronicaPanel(aw.Panel):
    
    GridClass = FatturaElettronicaGrid
    window_filler = wdr.EmissioneFatturaElettronicaFunc
    report_name = "Documenti fattura elettronica"
    
    def __init__(self, parent):
        
        aw.Panel.__init__(self, parent)
        self.window_filler(self)
        cn = self.FindWindowByName
        
        self.dbcli = dbfe.ClientiMovimentati()
        
        self.dbdocs = dbfe.FatturaElettronica()
        self.dbdocs.AddField('0.0', 'fe_sel')
        self.dbdocs.Reset()
        self.gridocs = self.GridClass(cn('pangridocs'), self.dbdocs)
        
        self.dbpfe = dbcfg.ProgrMagazz_FatturaElettronica()
        self.UpdateNumProgr()
        
        today = Env.Azienda.Login.dataElab
        cn('data1').SetValue(Env.DateTime.Date(today.year, today.month, 1))
        cn('data2').SetValue(today)
        c = cn('id_pdc')
        if c:
            c.SetFilter('0')
        
        for name in ('LEGEND_SELEZIONATO',
                     'LEGEND_GIA_TRASMESSO',
                     'LEGEND_DA_TRASMETTERE',
                     'LEGEND_MANCA_CODICE_CIG',
                     'LEGEND_MANCA_CODICE_CUP',):
            cn(name).SetBackgroundColour(globals()[name])
            cn(name).Refresh()
        
        def set_focus():
            self.FindWindowByName('data1').SetFocus()
        wx.CallAfter(set_focus)
        
        self.Bind(EVT_LINKTABCHANGED, self.OnUpdateData, cn('id_pdc'))
        self.Bind(wx.EVT_CHECKBOX, self.OnUpdateData, cn('includigt'))
        for name, func in (('butsrc', self.OnUpdateClienti),
                           ('butprt', self.OnPrintData),
                           ('butgen', self.OnGeneraFile),):
            c = cn(name)
            if c:
                self.Bind(wx.EVT_BUTTON, func, c)
        self.Bind(EVT_DOC_CHECKED, self.OnUpdateTotali, self.gridocs)
    
    def OnUpdateData(self, event):
        self.UpdateData()
    
    def OnUpdateClienti(self, event):
        self.UpdateClienti()
    
    def OnPrintData(self, event):
        self.PrintData()
    
    def OnGeneraFile(self, event):
        if self.Validate():
            if self.GeneraFile():
                self.UpdateData()
    
    def Validate(self):
        err = False
        for doc in self.dbdocs:
            if doc.fe_sel and not doc.totimposta and not doc.ftel_bollovirt:
                err = True
        if err:
            msg = "Sono stati selezionati documenti privi di imposta e di bollo virtuale.\nProseguire ?"
            stl = wx.ICON_QUESTION|wx.YES_NO|wx.NO_DEFAULT
            if aw.awu.MsgDialog(self, msg, style=stl) != wx.ID_YES:
                return False
        return True
    
    def UpdateNumProgr(self):
        cn = self.FindWindowByName
        self.dbpfe.Retrieve()
        cn('numprogr').SetValue((self.dbpfe.progrimp1 or 0) + 1)
    
    def _get_values(self):
        cn = self.FindWindowByName
        data1, data2, id_pdc = map(lambda x: cn(x).GetValue(), 'data1 data2 id_pdc'.split())
        if data1 is None:
            err = 'Manca la data di partenza'
        elif data2 is None:
            err = 'Manca la data di fine'
        else:
            err = None
        if err:
            aw.awu.MsgDialog(self, "Dati errati:\n%s" % err, style=wx.ICON_ERROR)
            return None
        return data1, data2, id_pdc
    
    def UpdateClienti(self):
        cn = self.FindWindowByName
        _ = self._get_values()
        if _ is None:
            return False
        data1, data2, _ = _
        clienti = self.dbdocs.get_clienti_periodo(data1, data2, cn('includigt').IsChecked())
        if clienti.IsEmpty():
            cn('id_pdc').SetFilter('0')
            cn('id_pdc').Disable()
        else:
            cn('id_pdc').SetFilter('pdc.id IN (%s)' % ','.join(map(str, [c.id for c in clienti])))
            cn('id_pdc').Enable()
        nc = clienti.RowsCount()
        cn('num_clienti').SetValue(nc)
        if nc == 1:
            cn('id_pdc').SetValue(clienti.id)
        self.gridocs.SetFocus()
    
    def UpdateData(self):
        cn = self.FindWindowByName
        self.UpdateNumProgr()
        _ = self._get_values()
        if _ is None:
            return False
        data1, data2, id_pdc = _
        
        docs = self.dbdocs
        docs.ClearFilters()
        docs.AddFilter('doc.id_pdc=%s', id_pdc)
        docs.AddFilter('doc.datdoc>=%s AND doc.datdoc<=%s', data1, data2)
        if not cn('includigt').IsChecked():
            docs.AddFilter('doc.ftel_numtrasm IS NULL')
        wx.BeginBusyCursor()
        try:
            docs.Retrieve()
        finally:
            wx.EndBusyCursor()
        err = None
        for doc in docs:
            if not doc.modpag.ftel_tippag or not doc.modpag.ftel_modpag:
                err = "Mod.pagamento non configurata su %s n. %s del %s" % (doc.config.descriz,
                                                                            doc.numdoc,
                                                                            doc.dita(doc.datdoc))
            if not err:
                for mov in doc.mov:
                    if mov.iva.id and mov.samefloat(mov.iva.perciva, 0) and not mov.iva.ftel_natura:
                        err = "Aliquota IVA %s non configurata" % mov.iva.codice
        self.gridocs.ChangeData(docs.GetRecordset())
        for name in 'butprt butgen numprogr'.split():
            cn(name).Enable(not err and not docs.IsEmpty())
        cn('warning').SetLabel(err or '')
    
    def OnUpdateTotali(self, event):
        self.UpdateTotali()
        event.Skip()
    
    def UpdateTotali(self):
        cn = self.FindWindowByName
        reg = self.dbdocs.regcon
        wx.BeginBusyCursor()
        numdoc = totdoc = 0
        try:
            for doc in self.dbdocs:
                if doc.fe_sel:
                    if reg.id != doc.id_reg:
                        reg.Get(doc.id_reg)
                    if reg.config.pasegno == "D":
                        segno = +1
                    else:
                        segno = -1
                    totdoc += (doc.totimporto*segno)
                    numdoc += 1
        finally:
            wx.EndBusyCursor()
        cn('docsel_num').SetValue(numdoc)
        cn('docsel_tot').SetValue(totdoc)
    
    def PrintData(self):
        rpt.Report(self, self.dbdocs, self.report_name)
    
    def GeneraFile(self):
        
        if not self.dbdocs.Locate(lambda r: r.fe_sel):
            aw.awu.MsgDialog(self, "Nessun documento selezionato\nper la generazione del file")
            return False
        
        msg = """Confermando, il documento sarà contrassegnato come trasmesso """\
              """ed il progressivo di trasmissione incrementerà di conseguenza.\n\n"""\
              """Confermi la generazione del file da trasmettere?\n"""
              
        if aw.awu.MsgDialog(self, msg, style=wx.ICON_QUESTION | wx.YES_NO | wx.NO_DEFAULT) == wx.ID_YES:
            
            numprogr = self.FindWindowByName('numprogr').GetValue()
            
            docids = [d.id for d in self.dbdocs if d.fe_sel]
            docs = dbfe.FatturaElettronica()
            docs.Retrieve("doc.id IN (%s)" % ','.join(map(str, docids)))
            
            wx.BeginBusyCursor()
            try:
                path, _name = docs.ftel_make_files(numprogr)
            finally:
                wx.EndBusyCursor()
            
            if len(docs.lError)>0:
                msg=''
                for r in docs.lError:
                    msg='%s\n%s' % (msg, r)
                aw.awu.MsgDialog(self, 'RILEVATI I SEGUENTI ERRORI:\n%s\nCORREGGERE PRIMA DI INVIARE' %msg, style=wx.ICON_ERROR)
            else:
                open_dir(path)
                aw.awu.MsgDialog(self, """File generato correttamente.\n"""\
                                       """Provvedere alla firma ed invio.""", style=wx.ICON_INFORMATION)
                self.UpdateData()
            
            return True
        
        return False


class FatturaElettronicaFrame(aw.Frame):
    
    Panel = FatturaElettronicaPanel
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.panel = self.Panel(self)
        self.AddSizedPanel(self.panel)


def apri_cartella_files():
    open_dir(dbfe.FatturaElettronica.ftel_get_basepath())







class ElencoFattureElettronicheGrid(FatturaElettronicaGrid):
    _canedit = False


class ElencoFattureElettronichePanel(FatturaElettronicaPanel):
    
    GridClass = ElencoFattureElettronicheGrid
    window_filler = wdr.ElencoDocumentiFunc
    
    def OnUpdateData(self, event):
        cn = self.FindWindowByName
        x = event.GetEventObject()
        if x.GetName() == 'solotrasm' and x.IsChecked():
            cn('datrasm').SetValue(False)
        elif x.GetName() == 'datrasm' and x.IsChecked():
            cn('solotrasm').SetValue(False)
        self.UpdateData()
        event.Skip()
    
    def OnUpdateClienti(self, event):
        self.UpdateData()
        event.Skip()
    
    def _get_values(self):
        cn = self.FindWindowByName
        data1, data2 = map(lambda x: cn(x).GetValue(), 'data1 data2'.split())
        id_pdc = None
        if data1 is None:
            err = 'Manca la data di partenza'
        elif data2 is None:
            err = 'Manca la data di fine'
        else:
            err = None
        if err:
            aw.awu.MsgDialog(self, "Dati errati:\n%s" % err, style=wx.ICON_ERROR)
            return None
        return data1, data2, id_pdc
    
    def UpdateData(self):
        cn = self.FindWindowByName
        _ = self._get_values()
        if _ is None:
            return False
        data1, data2, _ = _
        docs = self.dbdocs
        docs.ClearFilters()
        docs.AddFilter('doc.datdoc>=%s AND doc.datdoc<=%s', data1, data2)
        trasm, datra, bollv = map(lambda x: cn(x).IsChecked(), 'solotrasm datrasm bollovirt'.split())
        if trasm:
            docs.AddFilter('doc.ftel_numtrasm IS NOT NULL')
        elif datra:
            docs.AddFilter('doc.ftel_numtrasm IS NULL')
        if bollv:
            docs.AddFilter('(doc.ftel_bollovirt IS NOT NULL AND doc.ftel_bollovirt<>0)')
        wx.BeginBusyCursor()
        try:
            docs.SetDebug()
            docs.Retrieve()
        finally:
            wx.EndBusyCursor()
        err = None
        for doc in docs:
            if not doc.modpag.ftel_tippag or not doc.modpag.ftel_modpag:
                err = "Mod.pagamento non configurata su %s n. %s del %s" % (doc.config.descriz,
                                                                            doc.numdoc,
                                                                            doc.dita(doc.datdoc))
            if not err:
                for mov in doc.mov:
                    if mov.iva.id and mov.samefloat(mov.iva.perciva, 0) and not mov.iva.ftel_natura:
                        err = "Aliquota IVA %s non configurata" % mov.iva.codice
        self.gridocs.ChangeData(docs.GetRecordset())
        cn('butprt').Enable(not docs.IsEmpty())
    
    def UpdateNumProgr(self):
        pass


class ElencoFattureElettronicheFrame(FatturaElettronicaFrame):
    
    Panel = ElencoFattureElettronichePanel
