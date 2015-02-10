#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturapa_env.py
# Copyright:    (C) 2014 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------

def TabStru(cls):
    
    a = cls.cfgmagdoc.append
    a(["ftel_tipdoc",   "CHAR",     4, None, "Fattura elettronica: Tipo documento", None ])
    a(["ftel_layout",   "CHAR",    16, None, "Fattura elettronica: Formato di stampa", None ])
    
    a = cls.modpag.append
    a(["ftel_tippag",   "CHAR",     4, None, "Fattura elettronica: Tipo pagamento", None ])
    a(["ftel_modpag",   "CHAR",     4, None, "Fattura elettronica: Modo pagamento", None ])
    
    a = cls.aliqiva.append
    a(["ftel_natura",   "CHAR",     2, None, "Fattura elettronica: Natura aliquota", None ])
    
    a = cls.pdc.append
    a(["ftel_codice",   "VARCHAR", 10, None, "Fattura elettronica: codice destinatario pa", None])
    
    a = cls.movmag_h.append
    a(["ftel_ordnum",   "VARCHAR", 15, None, "Fattura elettronica: numero ordine acquisto", None ])
    a(["ftel_orddat",   "DATE",  None, None, "Fattura elettronica: data ordine acquisto", None ])
    a(["ftel_codcig",   "VARCHAR", 15, None, "Fattura elettronica: codice GIG", None ])
    a(["ftel_codcup",   "VARCHAR", 15, None, "Fattura elettronica: codice CUP", None ])
    a(["ftel_numtrasm", "INT",      5, None, "Fattura elettronica: numero trasmissione", None ]) 
