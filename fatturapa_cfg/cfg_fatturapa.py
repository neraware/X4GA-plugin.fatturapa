#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturpa_cfg/fatturpa.py
# Copyright:    (C) 2014 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------

import wx
import awc.controls.windows as aw
import awc.controls.dbgrid as dbglib

import fatturapa_cfg.cfg_fatturapa_wdr as wdr
import fatturapa_cfg.dbtables as dbcfg


FRAME_TITLE = "Setup Fattura Elettronica"


class TipoDocumentoPanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.TipoDocumentoFunc(self)
        cn = self.FindWindowByName
        def set_focus():
            cn('tipodocumento').SetFocus()
        wx.CallAfter(set_focus)
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butsave'))
    
    def OnSaveData(self, event):
        if self.ValidateData():
            event.Skip()
    
    def ValidateData(self):
        return True

class TipoDocumentoDialog(aw.Dialog):
    
    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Tipo documento'
        aw.Dialog.__init__(self, *args, **kwargs)
        self.panel = TipoDocumentoPanel(self)
        self.AddSizedPanel(self.panel)
        cn = self.FindWindowByName
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butsave'))
    
    def OnSaveData(self, event):
        self.EndModal(wx.ID_OK)
    
    def SetData(self, tpd):
        cn = self.FindWindowByName
        if tpd.ftel_tipdoc:
            value = int(tpd.ftel_tipdoc[2:])
        else:
            value = 0
        cn('tipodocumento').SetSelection(value)
        cn('toolprint').SetValue(tpd.ftel_layout)
        if tpd.ftel_flgddt==None:
            cn('isddt').SetValue(False)
        else:
            cn('isddt').SetValue(tpd.ftel_flgddt)
    
    def GetData(self):
        cn = self.FindWindowByName
        sel = cn('tipodocumento').GetSelection()
        if sel == 0:
            value = None
        else:
            value = 'TD%s' % str(sel).zfill(2)
        return value, cn('toolprint').GetValue(), cn('isddt').GetValue()


class ModPagamentoPanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.DatiModPagamentoFunc(self)
        cn = self.FindWindowByName
        def set_focus():
            cn('modpagamento').SetFocus()
        wx.CallAfter(set_focus)
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butsave'))
    
    def OnSaveData(self, event):
        if self.ValidateData():
            event.Skip()
    
    def ValidateData(self):
        return True


class ModPagamentoDialog(aw.Dialog):
    
    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Mod.Pagamento'
        aw.Dialog.__init__(self, *args, **kwargs)
        self.panel = ModPagamentoPanel(self)
        self.AddSizedPanel(self.panel)
        cn = self.FindWindowByName
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butsave'))
    
    def OnSaveData(self, event):
        self.EndModal(wx.ID_OK)
    
    def SetData(self, mpa):
        cn = self.FindWindowByName
        for name, col in (('tiporate',     'ftel_tippag'),
                          ('modpagamento', 'ftel_modpag'),):
            info = getattr(mpa, col)
            if info:
                value = int(info[2:])-1
            else:
                value = 0
            cn(name).SetSelection(value)
    
    def GetData(self):
        cn = self.FindWindowByName
        seltip = cn('tiporate').GetSelection()
        selmod = cn('modpagamento').GetSelection()
        valtip = 'TP%s' % str(seltip+1).zfill(2)
        valmod = 'MP%s' % str(selmod+1).zfill(2)
        return valtip, valmod


class AliqIvaPanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.DatiAliqIvaFunc(self)
        cn = self.FindWindowByName
        def set_focus():
            cn('naturaliqiva').SetFocus()
        wx.CallAfter(set_focus)
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butsave'))
    
    def OnSaveData(self, event):
        if self.ValidateData():
            event.Skip()
    
    def ValidateData(self):
        return True


class AliqIvaDialog(aw.Dialog):
    
    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Aliquote IVA'
        aw.Dialog.__init__(self, *args, **kwargs)
        self.panel = AliqIvaPanel(self)
        self.AddSizedPanel(self.panel)
        cn = self.FindWindowByName
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butsave'))
    
    def OnSaveData(self, event):
        self.EndModal(wx.ID_OK)
    
    def SetData(self, iva):
        cn = self.FindWindowByName
        natura = iva.ftel_natura
        if natura:
            value = int(natura[1:])
        else:
            value = 0
        cn('naturaliqiva').SetSelection(value)
    
    def GetData(self):
        cn = self.FindWindowByName
        natura = cn('naturaliqiva').GetSelection()
        if natura == 0:
            valnat = ''
        else:
            valnat = 'N%s' % str(natura).zfill(1)
        return valnat


class DatiClientePanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.DatiClienteFunc(self)
        cn = self.FindWindowByName
        def set_focus():
            cn('ftel_codice').SetFocus()
        wx.CallAfter(set_focus)
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butsave'))
    
    def OnSaveData(self, event):
        if self.ValidateData():
            event.Skip()
    
    def ValidateData(self):
        return True

class DatiClienteDialog(aw.Dialog):
    
    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Codice destinatario'
        aw.Dialog.__init__(self, *args, **kwargs)
        self.panel = DatiClientePanel(self)
        self.AddSizedPanel(self.panel)
        cn = self.FindWindowByName
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butsave'))
    
    def OnSaveData(self, event):
        self.EndModal(wx.ID_OK)
    
    def SetData(self, pdc):
        cn = self.FindWindowByName
        cn('codice').SetValue(pdc.codice)
        cn('descriz').SetValue(pdc.descriz)
        cn('ftel_codice').SetValue(pdc.ftel_codice)
    
    def GetData(self):
        cn = self.FindWindowByName
        return cn('ftel_codice').GetValue()


class FatturaElettronicaCausaliGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbtpd):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbtpd, 
                                 can_edit=False, can_insert=False, on_menu_select='row')
        
        tpd = self.dbtpd = dbtpd
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        self.AddColumn(tpd, 'codice',      'Cod.', col_width=40)
        self.AddColumn(tpd, 'descriz',     'Documento', col_width=200, is_fittable=True)
        self.AddColumn(tpd, 'ftel_tipdoc', 'TDxx', col_width=60)
        self.AddColumn(tpd, 'ftel_layout', 'Layout', col_width=90)
        self.AddColumn(tpd, 'ftel_flgddt', 'ddt', col_width=30, col_type=self.TypeCheck())
        self.AddColumn(tpd, 'id',          '#tpd', col_width=1)
        
        self.CreateGrid()


class FatturaElettronicaModPagGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbmpa):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbmpa, 
                                 can_edit=False, can_insert=False, on_menu_select='row')
        
        mpa = self.dbmpa = dbmpa
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        self.AddColumn(mpa, 'codice',      'Cod.', col_width=40)
        self.AddColumn(mpa, 'descriz',     'Mod.Pagamento', col_width=200, is_fittable=True)
        self.AddColumn(mpa, 'ftel_tippag', 'TPxx', col_width=60)
        self.AddColumn(mpa, 'ftel_modpag', 'MPxx', col_width=60)
        self.AddColumn(mpa, 'id',          '#mpa', col_width=1)
        
        self.CreateGrid()


class FatturaElettronicaAliqIvaGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbiva):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbiva, 
                                 can_edit=False, can_insert=False, on_menu_select='row')
        
        iva = self.dbiva = dbiva
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        self.AddColumn(iva, 'codice',      'Cod.', col_width=40)
        self.AddColumn(iva, 'descriz',     'Aliquota Iva', col_width=200, is_fittable=True)
        self.AddColumn(iva, 'ftel_natura', 'Nx', col_width=60)
        self.AddColumn(iva, 'id',          '#iva', col_width=1)
        
        self.CreateGrid()


class FatturaElettronicaClientiGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbpdc):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbpdc, 
                                 can_edit=False, can_insert=False, on_menu_select='row')
        
        pdc = self.dbpdc = dbpdc
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        self.AddColumn(pdc, 'codice',      'Cod.', col_width=40)
        self.AddColumn(pdc, 'descriz',     'Documento', col_width=200, is_fittable=True)
        self.AddColumn(pdc, 'ftel_codice', 'CodicePA', col_width=100)
        self.AddColumn(pdc, 'id',          '#pdc', col_width=1)
        
        self.CreateGrid()


class FatturaElettronicaSetupPanel(aw.Panel):
    
    def __init__(self, *args, **kwargs):
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.FatturaElettronicaFunc(self)
        cn = self.FindWindowByName
        
        import magazz.dbtables as dbm
        self.dbcfg = dbm.adb.DbTable('cfgsetup', 'setup')        
        
        
        
        self.dbpfe = dbcfg.ProgrMagazz_FatturaElettronica()
        self.dbcli = dbcfg.FatturaElettronica_Clienti()
        self.dbmpa = dbcfg.FatturaElettronica_ModPagamento()
        self.dbiva = dbcfg.FatturaElettronica_AliqIva()
        self.dbtpd = dbcfg.FatturaElettronica_Causali()
        self.gridcli = FatturaElettronicaClientiGrid(cn('pangridcli'), self.dbcli)
        self.gridmpa = FatturaElettronicaModPagGrid(cn('pangridmpa'), self.dbmpa)
        self.gridiva = FatturaElettronicaAliqIvaGrid(cn('pangridiva'), self.dbiva)
        self.gridtpd = FatturaElettronicaCausaliGrid(cn('pangridtpd'), self.dbtpd)
        for grid, func in ((self.gridcli, self.OnGridClientiData),
                           (self.gridmpa, self.OnGridModPagData),
                           (self.gridiva, self.OnGridAliqIvaData),
                           (self.gridtpd, self.OnGridTipDocData),):
            self.Bind(dbglib.gridlib.EVT_GRID_CELL_LEFT_DCLICK, func, grid)
        self.LoadData()
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butupd'))
    
    def OnGridClientiData(self, event):
        cli = self.dbcli
        cli.MoveRow(event.GetRow())
        dlg = DatiClienteDialog(self)
        dlg.SetData(cli)
        do = (dlg.ShowModal() == wx.ID_OK)
        dlg.Destroy()
        if do:
            cli.MoveRow(event.GetRow())
            cli.ftel_codice = dlg.GetData()
            self.Refresh()
        event.Skip()
    
    def OnGridModPagData(self, event):
        mpa = self.dbmpa
        mpa.MoveRow(event.GetRow())
        dlg = ModPagamentoDialog(self)
        dlg.SetData(mpa)
        do = (dlg.ShowModal() == wx.ID_OK)
        dlg.Destroy()
        if do:
            mpa.MoveRow(event.GetRow())
            mpa.ftel_tippag, mpa.ftel_modpag = dlg.GetData()
            self.Refresh()
        event.Skip()
    
    def OnGridAliqIvaData(self, event):
        iva = self.dbiva
        iva.MoveRow(event.GetRow())
        dlg = AliqIvaDialog(self)
        dlg.SetData(iva)
        do = (dlg.ShowModal() == wx.ID_OK)
        dlg.Destroy()
        if do:
            iva.MoveRow(event.GetRow())
            iva.ftel_natura = dlg.GetData()
            self.Refresh()
        event.Skip()
    
    def OnGridTipDocData(self, event):
        tpd = self.dbtpd
        tpd.MoveRow(event.GetRow())
        dlg = TipoDocumentoDialog(self)
        dlg.SetData(tpd)
        do = (dlg.ShowModal() == wx.ID_OK)
        dlg.Destroy()
        if do:
            tpd.MoveRow(event.GetRow())
            tpd.ftel_tipdoc, tpd.ftel_layout, tpd.ftel_flgddt = dlg.GetData()
            self.Refresh()
        event.Skip()
    
    def LoadData(self):
        wx.BeginBusyCursor()
        try:
            self.dbcfg.Retrieve('setup.chiave=%s', 'azienda_ftel_flagdescriz')
            if self.dbcfg.OneRow():
                self.FindWindowByName('flagdescriz').SetValue(int(self.dbcfg.flag)==1)
                
            
            cfg = self.dbpfe
            cfg.Retrieve()
            self.FindWindowByName('ftel_numprogr').SetValue(cfg.progrimp1 or 0)
            for table, grid in ((self.dbcli, self.gridcli),
                                (self.dbmpa, self.gridmpa),
                                (self.dbiva, self.gridiva),
                                (self.dbtpd, self.gridtpd),):
                table.Retrieve()
                grid.ChangeData(table.GetRecordset())
        finally:
            wx.EndBusyCursor()
    
    def ValidateData(self):
        return True
    
    def SaveData(self):
        self.dbcfg.Retrieve('setup.chiave=%s', 'azienda_ftel_flagdescriz')
        if self.dbcfg.RowsCount()==0:
            self.dbcfg.CreateNewRow()
            self.dbcfg.chiave='azienda_ftel_flagdescriz'
        self.dbcfg.flag=self.FindWindowByName('flagdescriz').IsChecked()
        self.dbcfg.Save()
        
        
        cfg = self.dbpfe
        key = 'ftel_numprogr'
        cfg.Retrieve('progr.codice=%s', key)
        if cfg.IsEmpty():
            cfg.CreateNewRow()
        cfg.progrimp1 = self.FindWindowByName(key).GetValue()
        written = cfg.Save()
        if written:
            self.dbcli.Save()
            self.dbmpa.Save()
            self.dbiva.Save()
            self.dbtpd.Save()
        else:
            aw.awu.MsgDialog(self, repr(cfg.GetError()), style=wx.ICON_ERROR)
        return written
    
    def OnSaveData(self, event):
        if self.ValidateData():
            if self.SaveData():
                event.Skip()


class FatturaElettronicaSetupDialog(aw.Dialog):
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_TITLE
        aw.Dialog.__init__(self, *args, **kwargs)
        self.panel = FatturaElettronicaSetupPanel(self)
        self.AddSizedPanel(self.panel)
        cn = self.FindWindowByName
        def set_focus():
            cn('ftel_numprogr').SetFocus()
        wx.CallAfter(set_focus)
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, cn('butupd'))
    
    def Show(self):
        return self.ShowModal()
    
    def OnSaveData(self, event):
        self.EndModal(wx.ID_OK)
