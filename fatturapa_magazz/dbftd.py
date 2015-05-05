# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturapa_magazz/dbftd.py
# Copyright:    (C) 2015 Marcello Montaldo <m.montaldo@astra-srl.com>
# ------------------------------------------------------------------------------


from magazz.dbftd import FtDif

class _FatturaPA_FtDif(FtDif):
    """
    Fatturazione differita con  plugin fatturapa
    """
    def Estrai(self):
        FtDif.Estrai(self)
        if self.f_tipopdc in ['A', 'E']:
            self.docrag.SetDebug()
            if self.f_tipopdc=='A':
                self.docrag.AddFilter('pdc.ftel_codice is null or LENGTH(pdc.ftel_codice)=0')
            else:
                self.docrag.AddFilter('not pdc.ftel_codice is null and LENGTH(pdc.ftel_codice)>0')
            self.docrag.Retrieve()

import magazz.dbftd as dbftd
dbftd.FtDif = _FatturaPA_FtDif
