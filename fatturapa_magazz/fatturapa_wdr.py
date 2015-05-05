# -*- coding: UTF-8 -*-

#-----------------------------------------------------------------------------
# Python source generated by wxDesigner from file: fatturapa.wdr
# Do not modify this file, all changes will be lost!
#-----------------------------------------------------------------------------

# Include wxPython modules
import wx
import wx.grid
import wx.animate

# Custom source
from awc.controls.datectrl import DateCtrl
from awc.controls.numctrl import NumCtrl
import anag.lib as alib


# Window functions

ID_TEXT = 10000
ID_DATA1 = 10001
ID_DATA2 = 10002
ID_CHECKBOX = 10003
ID_BUTSRC = 10004
ID_NUMCLI = 10005
ID_FOREIGN = 10006
ID_DOCSEL_NUM = 10007
ID_DOCSEL_TOT = 10008
ID_LINE = 10009
ID_NUMPROGR = 10010
ID_BUTGEN = 10011
ID_PANGRIDOCS = 10012
ID_LEGEND_GIA_TRASMESSO = 10013
ID_LEGEND_DA_TRASMETTERE = 10014
ID_LEGEND_MANCA_CODICE_CIG = 10015
ID_LEGEND_MANCA_CODICE_CUP = 10016
ID_LEGEND_SELEZIONATO = 10017
ID_BUTPRT = 10018

def EmissioneFatturaElettronicaFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item3 = wx.StaticBox( parent, -1, "Ricerca documenti" )
    item2 = wx.StaticBoxSizer( item3, wx.VERTICAL )
    
    item4 = wx.FlexGridSizer( 0, 4, 0, 0 )
    
    item5 = wx.StaticText( parent, ID_TEXT, "Ricerca documenti dal:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item4.Add( item5, 0, wx.ALIGN_CENTER|wx.LEFT|wx.BOTTOM, 5 )

    item6 = DateCtrl( parent, ID_DATA1, "", wx.DefaultPosition, [80,-1], 0 )
    item6.SetName( "data1" )
    item4.Add( item6, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item7 = wx.StaticText( parent, ID_TEXT, "Al:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item4.Add( item7, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item8 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item9 = DateCtrl( parent, ID_DATA2, "", wx.DefaultPosition, [80,-1], 0 )
    item9.SetName( "data2" )
    item8.Add( item9, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item10 = wx.CheckBox( parent, ID_CHECKBOX, "Includi anche i documenti già trasmessi", wx.DefaultPosition, wx.DefaultSize, 0 )
    item10.SetName( "includigt" )
    item8.Add( item10, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item11 = wx.Button( parent, ID_BUTSRC, "Cerca", wx.DefaultPosition, wx.DefaultSize, 0 )
    item11.SetDefault()
    item11.SetName( "butsrc" )
    item8.Add( item11, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item4.Add( item8, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item12 = wx.StaticText( parent, ID_TEXT, "Clienti trovati:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item4.Add( item12, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.BOTTOM, 5 )

    item13 = NumCtrl(parent, ID_NUMCLI, integerWidth=3, name='num_clienti'); item13.SetEditable(False)
    item4.Add( item13, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item14 = wx.StaticText( parent, ID_TEXT, "Cliente:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item4.Add( item14, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.BOTTOM, 5 )

    item15 = alib.LinkTableCliente(parent, ID_FOREIGN, name='id_pdc'); item15.Disable()
    item4.Add( item15, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item2.Add( item4, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item1.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item17 = wx.StaticBox( parent, -1, "Trasmissione documenti selezionati" )
    item16 = wx.StaticBoxSizer( item17, wx.VERTICAL )
    
    item18 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item19 = wx.StaticText( parent, ID_TEXT, "Documenti:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item18.Add( item19, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.BOTTOM, 5 )

    item20 = NumCtrl(parent, ID_DOCSEL_NUM, integerWidth=3, name='docsel_num'); item20.SetEditable(False)
    item18.Add( item20, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item21 = wx.StaticText( parent, ID_TEXT, "Totale importo documenti:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item18.Add( item21, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.BOTTOM, 5 )

    item22 = NumCtrl(parent, ID_DOCSEL_TOT, integerWidth=9, fractionWidth=2, name='docsel_tot'); item22.SetEditable(False)
    item18.Add( item22, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item16.Add( item18, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item23 = wx.StaticLine( parent, ID_LINE, wx.DefaultPosition, [20,-1], wx.LI_HORIZONTAL )
    item16.Add( item23, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item24 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item25 = wx.StaticText( parent, ID_TEXT, "Trasmetti con il num.:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item24.Add( item25, 0, wx.ALIGN_CENTER|wx.LEFT|wx.BOTTOM, 5 )

    item26 = NumCtrl(parent, integerWidth=5, fractionWidth=0, allowNegative=False); item26.SetName('numprogr')
    item24.Add( item26, 0, wx.ALIGN_CENTER|wx.LEFT|wx.BOTTOM, 5 )

    item27 = wx.Button( parent, ID_BUTGEN, "Genera file", wx.DefaultPosition, wx.DefaultSize, 0 )
    item27.SetName( "butgen" )
    item27.Enable(False)
    item24.Add( item27, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item16.Add( item24, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

    item1.Add( item16, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item1.AddGrowableCol( 1 )

    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item28 = wx.StaticText( parent, ID_TEXT, "Documenti trovati:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item28.SetForegroundColour( wx.BLUE )
    item0.Add( item28, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item29 = wx.Panel( parent, ID_PANGRIDOCS, wx.DefaultPosition, [1000,250], wx.SUNKEN_BORDER )
    item29.SetName( "pangridocs" )
    item0.Add( item29, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item30 = wx.StaticText( parent, ID_TEXT, "-", wx.DefaultPosition, wx.DefaultSize, 0 )
    item30.SetForegroundColour( wx.RED )
    item30.SetFont( wx.Font( 10, wx.SWISS, wx.NORMAL, wx.BOLD ) )
    item30.SetName( "warning" )
    item0.Add( item30, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item31 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item32 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item33 = wx.Panel( parent, ID_LEGEND_GIA_TRASMESSO, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item33.SetName( "LEGEND_GIA_TRASMESSO" )
    item32.Add( item33, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item34 = wx.StaticText( parent, ID_TEXT, "Già trasmesso", wx.DefaultPosition, wx.DefaultSize, 0 )
    item32.Add( item34, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item35 = wx.Panel( parent, ID_LEGEND_DA_TRASMETTERE, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item35.SetName( "LEGEND_DA_TRASMETTERE" )
    item32.Add( item35, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item36 = wx.StaticText( parent, ID_TEXT, "Da trasmettere", wx.DefaultPosition, wx.DefaultSize, 0 )
    item32.Add( item36, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item37 = wx.Panel( parent, ID_LEGEND_MANCA_CODICE_CIG, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item37.SetName( "LEGEND_MANCA_CODICE_CIG" )
    item32.Add( item37, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item38 = wx.StaticText( parent, ID_TEXT, "Manca Cod.CIG o Num. o Data ordine acquisto", wx.DefaultPosition, wx.DefaultSize, 0 )
    item32.Add( item38, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item39 = wx.Panel( parent, ID_LEGEND_MANCA_CODICE_CUP, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item39.SetName( "LEGEND_MANCA_CODICE_CUP" )
    item32.Add( item39, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item40 = wx.StaticText( parent, ID_TEXT, "Manca Cod.CUP", wx.DefaultPosition, wx.DefaultSize, 0 )
    item32.Add( item40, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item41 = wx.Panel( parent, ID_LEGEND_SELEZIONATO, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item41.SetName( "LEGEND_SELEZIONATO" )
    item32.Add( item41, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item42 = wx.StaticText( parent, ID_TEXT, "Selezionato per la trasmissione", wx.DefaultPosition, wx.DefaultSize, 0 )
    item32.Add( item42, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item31.Add( item32, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

    item43 = wx.Button( parent, ID_BUTPRT, "Stampa", wx.DefaultPosition, wx.DefaultSize, 0 )
    item43.SetName( "butprt" )
    item43.Enable(False)
    item31.Add( item43, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item31.AddGrowableCol( 1 )

    item0.Add( item31, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item0.AddGrowableCol( 0 )

    item0.AddGrowableRow( 2 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

ID_DATRASM = 10019
ID_SOLOTRASM = 10020
ID_BOLLOVIRT = 10021

def ElencoDocumentiFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item2 = wx.StaticText( parent, ID_TEXT, "Ricerca documenti dal:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.Add( item2, 0, wx.ALIGN_CENTER|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item3 = DateCtrl( parent, ID_DATA1, "", wx.DefaultPosition, [80,-1], 0 )
    item3.SetName( "data1" )
    item1.Add( item3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item4 = wx.StaticText( parent, ID_TEXT, "al:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item1.Add( item4, 0, wx.ALIGN_CENTER|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item5 = DateCtrl( parent, ID_DATA2, "", wx.DefaultPosition, [80,-1], 0 )
    item5.SetName( "data2" )
    item1.Add( item5, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item6 = wx.CheckBox( parent, ID_DATRASM, "Da trasmettere", wx.DefaultPosition, wx.DefaultSize, 0 )
    item6.SetValue( True )
    item6.SetName( "datrasm" )
    item1.Add( item6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item7 = wx.CheckBox( parent, ID_SOLOTRASM, "Solo trasmessi", wx.DefaultPosition, wx.DefaultSize, 0 )
    item7.SetName( "solotrasm" )
    item1.Add( item7, 0, wx.ALIGN_CENTER|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item8 = wx.CheckBox( parent, ID_BOLLOVIRT, "Solo con Bollo virtuale", wx.DefaultPosition, wx.DefaultSize, 0 )
    item8.SetName( "bollovirt" )
    item1.Add( item8, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item9 = wx.Button( parent, ID_BUTSRC, "Cerca", wx.DefaultPosition, wx.DefaultSize, 0 )
    item9.SetDefault()
    item9.SetName( "butsrc" )
    item1.Add( item9, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item0.Add( item1, 0, 0, 5 )

    item10 = wx.StaticText( parent, ID_TEXT, "Documenti trovati:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item10.SetForegroundColour( wx.BLUE )
    item0.Add( item10, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item11 = wx.Panel( parent, ID_PANGRIDOCS, wx.DefaultPosition, [1000,250], wx.SUNKEN_BORDER )
    item11.SetName( "pangridocs" )
    item0.Add( item11, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item12 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item13 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item14 = wx.Panel( parent, ID_LEGEND_GIA_TRASMESSO, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item14.SetName( "LEGEND_GIA_TRASMESSO" )
    item13.Add( item14, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item15 = wx.StaticText( parent, ID_TEXT, "Già trasmesso", wx.DefaultPosition, wx.DefaultSize, 0 )
    item13.Add( item15, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item16 = wx.Panel( parent, ID_LEGEND_DA_TRASMETTERE, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item16.SetName( "LEGEND_DA_TRASMETTERE" )
    item13.Add( item16, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item17 = wx.StaticText( parent, ID_TEXT, "Da trasmettere", wx.DefaultPosition, wx.DefaultSize, 0 )
    item13.Add( item17, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item18 = wx.Panel( parent, ID_LEGEND_MANCA_CODICE_CIG, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item18.SetName( "LEGEND_MANCA_CODICE_CIG" )
    item13.Add( item18, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item19 = wx.StaticText( parent, ID_TEXT, "Manca Cod.CIG o Num. o Data ordine acquisto", wx.DefaultPosition, wx.DefaultSize, 0 )
    item13.Add( item19, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item20 = wx.Panel( parent, ID_LEGEND_MANCA_CODICE_CUP, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item20.SetName( "LEGEND_MANCA_CODICE_CUP" )
    item13.Add( item20, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item21 = wx.StaticText( parent, ID_TEXT, "Manca Cod.CUP", wx.DefaultPosition, wx.DefaultSize, 0 )
    item13.Add( item21, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item22 = wx.Panel( parent, ID_LEGEND_SELEZIONATO, wx.DefaultPosition, [20,20], wx.RAISED_BORDER )
    item22.SetName( "LEGEND_SELEZIONATO" )
    item13.Add( item22, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item23 = wx.StaticText( parent, ID_TEXT, "Selezionato per la trasmissione", wx.DefaultPosition, wx.DefaultSize, 0 )
    item13.Add( item23, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, 5 )

    item12.Add( item13, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

    item24 = wx.Button( parent, ID_BUTPRT, "Stampa", wx.DefaultPosition, wx.DefaultSize, 0 )
    item24.SetName( "butprt" )
    item24.Enable(False)
    item12.Add( item24, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item12.AddGrowableCol( 1 )

    item0.Add( item12, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item0.AddGrowableCol( 0 )

    item0.AddGrowableRow( 1 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

# Menubar functions

# Toolbar functions

# Bitmap functions


# End of generated file
