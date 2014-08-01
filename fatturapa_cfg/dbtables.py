#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturapa_cfg/dbtables.py
#               (C) 2014 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------


import stormdb as adb


class ProgrMagazz(adb.DbTable):
    
    _key = None
    
    def __init__(self):
        if self._key is None:
            raise Exception, "Classe non istanziabile"
        adb.DbTable.__init__(self, 'cfgprogr', 'progr')
        self.AddBaseFilter('progr.codice=%s', self._key)
        self.Reset()
    
    def CreateNewRow(self, *args, **kwargs):
        adb.DbTable.CreateNewRow(self)
        self.codice = self._key


class ProgrMagazz_FatturaElettronica(ProgrMagazz):
    _key = 'ftel_numprogr'



class FatturaElettronica_Causali(adb.DbTable):
    
    def __init__(self):
        adb.DbTable.__init__(self, 'cfgmagdoc', 'tipdoc', fields='id,codice,descriz,ftel_tipdoc,ftel_layout')
        self.AddOrder('tipdoc.codice')
        self.Reset()


class FatturaElettronica_ModPagamento(adb.DbTable):
    
    def __init__(self):
        adb.DbTable.__init__(self, 'modpag', fields='id,codice,descriz,ftel_tippag,ftel_modpag')
        self.AddOrder('modpag.codice')
        self.Reset()


class FatturaElettronica_Clienti(adb.DbTable):
    
    def __init__(self):
        adb.DbTable.__init__(self, 'pdc', fields='id,codice,descriz,ftel_codice')
        self.AddJoin('clienti', 'anag', idLeft='id', idRight='id', fields='id')
        self.AddOrder('pdc.descriz')
        self.AddFilter('anag.nazione IS NULL OR anag.nazione="" OR anag.nazione="IT"')
        self.Reset()
