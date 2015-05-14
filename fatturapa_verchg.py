#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturapa_changes.py
# Copyright:    (C) 2015 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------

"""
Riepilogo dei cambiamenti apportati alla versione del plugin
"""

import mx.DateTime as dt

plugin_history = (

    ('1.1.09', dt.DateTime(2015, 5, 14), (
         ("BUG4004",
         """Corretta l'espansione visuale della griglia di selezione
         documenti."""),
        ),),
    
    ('1.1.08', dt.DateTime(2015, 5, 5), (
         ("BET4008",
         """Aggiunta consultazione documenti emessi/da trasmettere."""),
        ),),
    
    ('1.1.07', dt.DateTime(2015, 5, 5), (
         ("BUG4003",
         """Fix identificativo fiscale del cedente, prima metteva
         il codice fiscale o la partita iva in assenza del codice fiscale,
         ora mette la partita iva o il codice fiscale in assenza della
         partita iva."""),
        ),),
    
    ('1.1.06', None, (
         ("BET4007",
         """Aggiunta gestione bollo virtuale."""),
        ),),
    
    ('1.1.05', None, (
         ("BUG4001",
         """Corretto la generazione errata del file xml nel caso di fatture con più aliquote Iva."""),
         ("BUG4002",
         """Inserita indicazione della quantità e unità di misura sulle singole righe di dettaglio."""),
         ("BET4003",
         """Inserita la gestione del riferimento alla riga a cui il ddt si riferisce analizzando 
         il corpo del documento Fattura generato in fase di raggruppamento."""),
         ("BET4004",
         """Inserita la possibilita' di indicare in sede di setup i tipi di documenti 
         da considerare ai fini della rilevazione dei ddt da riportare nel file xml
         generato."""),
         ("BET4005",
         """Data la possibilità di utilizzare più tipi di raggruppamenti ognuno dei quali puo'
         essere configurato in modo da agire su:
         - Tutte le Anagrafiche
         - Solo Soggetti a Fatturazione Elettronica
         - Escludi Soggetti a Fattura Eletronica."""),
         ("BET4006",
         """Aggiunta la possibilità di specificare in sede di configurazione se si desideraa 
         o meno inserire le righe descrittive nel file xml generato."""),
        ),),
    
    ('1.1.04', None, (
         ("BET4002",
         """Possibilità di specificare i dati del soggetto emittente
         o terzo intermediario."""),
        ),),
    
    ('1.1.03', None, (
         ("BET4001",
         """Possibilità di specificare soggetto trasmittente diverso
         dal soggetto cedente/prestatore."""),
        ),),
    
)
