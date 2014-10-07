#!/bin/env/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Author:       Fabio Cassini <fc@f4b10.org>
# Copyright:    (C) 2014 Fabio Cassini <fc@f4b10.org>
# ------------------------------------------------------------------------------

import magazz.dbtables as dbm
import fatturapa_cfg.dbtables as dbcfg

import Env

from xml.dom.minidom import Document
import re

import os
def opj(*x):
    return os.path.join(*x).replace('\\', '/')

import report as rpt


class FatturaElettronicaException(Exception):
    pass


def normalize(x, upper=False):
    c = True
    x = x.encode('ascii', 'xmlcharrefreplace')
    if upper:
        x = x.upper()
    y = ''
    for n in range(len(x)):
        if x[n] == '.':
            c = True
        if c and x[n].isalpha():
            y += x[n].upper()
            c = False
        elif x[n].isalnum() or x[n].isspace():
            y += x[n]
    return y


class ClientiMovimentati(dbm.adb.DbMem):
    
    def __init__(self):
        dbm.adb.DbMem.__init__(self, fields='id,codice,descriz')
        self.Reset()


class FatturaElettronica(dbm.DocMag):
    
    def __init__(self, *args, **kwargs):
        dbm.DocMag.__init__(self, *args, **kwargs)
        self.AddBaseFilter('config.ftel_tipdoc IS NOT NULL AND config.ftel_tipdoc<>""')
        self.AddBaseFilter('pdc.ftel_codice IS NOT NULL AND pdc.ftel_codice<>""')
        self.Reset()
    
#     def get_xml_test(self):
#         
#         cli = self.GetAnag()
#         
#         doc = FTEL_Document()
#         
#         # elemento principale: fattura ("p:FatturaElettronica")
#         
#         fat = doc.createRoot()
#         # dati di testata
#         head = doc.appendElement(fat, 'FatturaElettronicaHeader')
#         
#         datitrasm = doc.appendElement(head, 'DatiTrasmissione')
#         
#         idtrasm = doc.appendElement(datitrasm, 'IdTrasmittente')
#         doc.appendItems(idtrasm, (('IdPaese',  Env.Azienda.stato),
#                                   ('IdCodice', Env.Azienda.codfisc),))
#         
#         doc.appendItems(datitrasm, (('ProgressivoInvio',    '00001'),
#                                     ('FormatoTrasmissione', 'SDI10'),
#                                     ('CodiceDestinatario',  'AAAAAA'),))
#         
#         contattitrasm = doc.appendElement(datitrasm, 'ContattiTrasmittente',)
#         doc.appendItems(contattitrasm, (('Telefono', Env.Azienda.numtel),
#                                         ('Email',    Env.Azienda.email),))
#         
#         cedente = doc.appendElement(head, 'CedentePrestatore')
#         
#         cedente_datianag = doc.appendElement(cedente, 'DatiAnagrafici')
#         
#         cedente_datianag_datifisc = doc.appendElement(cedente_datianag, 'IdFiscaleIVA')
#         doc.appendItems(cedente_datianag_datifisc, (('IdPaese',  Env.Azienda.stato),
#                                                     ('IdCodice', Env.Azienda.codfisc)))
#         
#         cedente_datianag_anagraf = doc.appendElement(cedente_datianag, 'Anagrafica')
#         doc.appendItems(cedente_datianag_anagraf, (('Denominazione', Env.Azienda.descrizione),))
#         
#         doc.appendItems(cedente_datianag, (('RegimeFiscale', 'RF01'),))
#         
#         cedente_sede = doc.appendElement(cedente, 'Sede')
#         doc.appendItems(cedente_sede, (('Indirizzo', Env.Azienda.indirizzo),
#                                        ('CAP',       Env.Azienda.cap),
#                                        ('Comune',    Env.Azienda.citta),
#                                        ('Provincia', Env.Azienda.prov),
#                                        ('Nazione',   Env.Azienda.stato),))
#         
#         cedente_staborg = doc.appendElement(cedente, 'StabileOrganizzazione')
#         doc.appendItems(cedente_staborg, (('Indirizzo', 'Piazza Garibaldi'),
#                                           ('CAP',       '00100'),
#                                           ('Comune',    'Roma'),
#                                           ('Provincia', 'RM'),
#                                           ('Nazione',   'IT'),))
#         
#         cessionario = doc.appendElement(head, 'CessionarioCommittente')
#         
#         cessionario_datianag = doc.appendElement(cessionario, 'DatiAnagrafici')
#         doc.appendItems(cessionario_datianag, (('CodiceFiscale', '09876543210'),))
#         
#         cessionario_datianag_anagraf = doc.appendElement(cessionario_datianag, 'Anagrafica')
#         doc.appendItems(cessionario_datianag_anagraf, (('Denominazione', 'Societa beta\' S.r.l.'),))
#         
#         cessionario_sede = doc.appendElement(cessionario, 'Sede')
#         doc.appendItems(cessionario_sede, (('Indirizzo', 'Via Milano'),
#                                             ('CAP',       '00100'),
#                                             ('Comune',    'Roma'),
#                                             ('Provincia', 'RM'),
#                                             ('Nazione',   'IT'),))
#         
#         doc.appendItems(head, (('SoggettoEmittente', 'CC'),))
#         
#         # dati di dettaglio
#         body = doc.appendElement(fat, 'FatturaElettronicaBody')
#         
#         body_gen = doc.appendElement(body, 'DatiGenerali')
#         
#         body_gen_doc = doc.appendElement(body_gen, 'DatiGeneraliDocumento')
#         doc.appendItems(body_gen_doc, (('TipoDocumento', 'TD01'),
#                                        ('Divisa',        'EUR'),
#                                        ('Data',          '2012-11-27'),
#                                        ('Numero',        '00001'),
#                                        ('Art73',         'SI'),))
#         
#         body_gen_acq = doc.appendElement(body_gen, 'DatiOrdineAcquisto')
#         doc.appendItems(body_gen_acq, (('RiferimentoNumeroLinea', '1'),
#                                        ('IdDocumento',            '123'),
#                                        ('CodiceCUP',              '123abc'),
#                                        ('CodiceCIG',              '456def'),))
#         
#         body_gen_ctr = doc.appendElement(body_gen, 'DatiContratto')
#         doc.appendItems(body_gen_ctr, (('RiferimentoNumeroLinea', '1'),
#                                        ('IdDocumento',            '123'),
#                                        ('Data',                   '2012-09-01'),
#                                        ('NumItem',                '5'),
#                                        ('CodiceCUP',              '123abc'),
#                                        ('CodiceCIG',              '456def'),))
#         
#         body_gen_cvz = doc.appendElement(body_gen, 'DatiConvenzione')
#         doc.appendItems(body_gen_cvz, (('RiferimentoNumeroLinea', '1'),
#                                        ('IdDocumento',            '123'),
#                                        ('Data',                   '2012-09-01'),
#                                        ('NumItem',                '5'),
#                                        ('CodiceCUP',              '123abc'),
#                                        ('CodiceCIG',              '456def'),))
#         
#         body_gen_ric = doc.appendElement(body_gen, 'DatiRicezione')
#         doc.appendItems(body_gen_ric, (('RiferimentoNumeroLinea', '1'),
#                                        ('IdDocumento',            '123'),
#                                        ('Data',                   '2012-09-01'),
#                                        ('NumItem',                '5'),
#                                        ('CodiceCUP',              '123abc'),
#                                        ('CodiceCIG',              '456def'),))
#         
#         body_gen_tra = doc.appendElement(body_gen, 'DatiTrasporto')
#         
#         body_gen_tra_vet = doc.appendElement(body_gen_tra, 'DatiAnagraficiVettore')
#         
#         body_gen_tra_vet_fis = doc.appendElement(body_gen_tra_vet, 'IdFiscaleIVA')
#         doc.appendItems(body_gen_tra_vet_fis, (('IdPaese', 'IT'),
#                                                ('IdCodice', '24681012141')))
#         
#         body_gen_tra_vet_ana = doc.appendElement(body_gen_tra_vet, 'Anagrafica')
#         doc.appendItems(body_gen_tra_vet_ana, (('Denominazione', 'Trasporto spa'),))
#         
#         doc.appendItems(body_gen_tra, (('DataOraConsegna', '2012-10-22T16:46:12.000+02:00'),))
#         
#         body_det = doc.appendElement(body, 'DatiBeniServizi')
#         for dnum, ddes, dpre, dimp, diva in ((1, 'BADGES MAGNETICI - PVC laminato bianco',                           3.00000000,  3,    21),
#                                              (2, 'QUOTA ENERGIA MATERIA PRIMA GAS',                                  0.29785848, 33.66, 21),
#                                              (3, 'QUOTA ENERGIA COMMERCIALIZZAZIONE AL DETTAGLIO (PARTE VARIABILE)', 0.00480000,  0.54, 21),
#                                              (4, 'QUOTA ENERGIA CORRISPETTIVI DI RETE',                              0.04165785,  4.71, 21),):
#             body_det_row = doc.appendElement(body_det, 'DettaglioLinee')
#             doc.appendItems(body_det_row, (('NumeroLinea',    str(dnum)),
#                                            ('Descrizione',    ddes),
#                                            ('PrezzoUnitario', '%.8f' % dpre),
#                                            ('PrezzoTotale',   '%.2f' % dimp),
#                                            ('AliquotaIVA',    '%.2f' % diva),))
#         
#         body_det_rie = doc.appendElement(body_det, 'DatiRiepilogo')
#         for iper, iimp, iiva in ((21, 3, 0.63),):
#             doc.appendItems(body_det_rie, (('AliquotaIVA',       '%.2f' % iper),
#                                            ('ImponibileImporto', '%.2f' % iimp),
#                                            ('Imposta',           '%.2f' % iiva),))
#         
#         body_pag = doc.appendElement(body, 'DatiPagamento')
#         doc.appendItems(body_pag, (('CondizioniPagamento', 'TP01'),))
#         
#         for pcod, pdat, pimp in (('MP01', '2012-12-31', 2.63),
#                                  ('MP01', '2013-01-31', 1),):
#             body_pag_det = doc.appendElement(body_pag, 'DettaglioPagamento')
#             doc.appendItems(body_pag_det, (('ModalitaPagamento',     pcod),
#                                            ('DataScadenzaPagamento', pdat),
#                                            ('ImportoPagamento',      '%.2f' % pimp),))
#         
#         return doc.toprettyxml(indent="  ", encoding="UTF-8")
    
    @classmethod
    def ftel_get_name(cls, numprogr):
        return 'IT%s_%s' % (Env.Azienda.codfisc, str(numprogr).zfill(5))
    
    @classmethod
    def ftel_get_basepath(cls):
        try:
            path = Env.Azienda.config.get('Site', 'folder')  # @UndefinedVariable
        except:
            path = None
        if not path:
            path = Env.xpaths.GetConfigPath()
        path = opj(path, 'ftel')
        if not os.path.isdir(path):
            os.mkdir(path)
        path = opj(path, 'azienda_%s' % Env.Azienda.codice)
        if not os.path.isdir(path):
            os.mkdir(path)
        return path
    
    @classmethod
    def ftel_get_pathname(cls, numprogr):
        path = cls.ftel_get_basepath()
        path = opj(path, cls.ftel_get_name(numprogr))
        if not os.path.isdir(path):
            os.mkdir(path)
        return path
    
    @classmethod
    def ftel_get_filename(cls, numprogr, ext='xml'):
        path = cls.ftel_get_pathname(numprogr)
        name = cls.ftel_get_name(numprogr)
        return opj(path, '%s.%s' % (name, ext))
    
    @classmethod
    def get_clienti_periodo(cls, data1, data2, includi_gt=False):
        f = FatturaElettronica()
        f.Synthetize()
        for name in 'id codice descriz'.split():
            f.AddGroupOn('pdc.%s' % name)
        f.AddFilter('doc.datdoc>=%s AND doc.datdoc<=%s', data1, data2)
        if not includi_gt:
            f.AddFilter('doc.ftel_numtrasm IS NULL')
        f.Retrieve()
        clienti = ClientiMovimentati()
        clienti.SetRecordset(f.GetRecordset())
        return clienti
    
    def ftel_get_printname(self, numprogr):
        return '%s %s del %s-%s-%s - %s' % (normalize(self.config.descriz),
                                            self.numdoc,
                                            str(self.datdoc.day).zfill(2),
                                            str(self.datdoc.month).zfill(2),
                                            str(self.datdoc.year).zfill(4),
                                            normalize(self.pdc.descriz))
    
    def ftel_get_datiazienda(self):
        cfg = dbm.adb.DbTable('cfgsetup', 'setup')
        dataz = {}
        for name in """cognome nome regfisc reanum reauff """\
                    """soind socap socit sopro capsoc socuni socliq """\
                    """rfnome rfcognome rfdes rfind rfcap rfcit rfpro rfcodfis rfpiva """.split():
            cfg.Retrieve('setup.chiave=%s', 'azienda_ftel_%s' % name)
            if cfg.importo:
                dataz[name] = cfg.importo
            else:
                dataz[name] = cfg.descriz
        return dataz
    
    def ftel_make_files(self, numprogr):
        
        def si_no(test, v1="SI", v2="NO"):
            if test:
                return v1
            return v2
        
        def data(data):
            try:
                return data.strftime('%Y-%m-%d')
            except:
                return ''
        
        if self.IsEmpty():
            raise FatturaElettronicaException, "Il documento è vuoto"
        
        dataz = self.ftel_get_datiazienda()
        
        pdc = self.pdc
        cli = self.GetAnag()
        
        xmldoc = FTEL_Document()
        
        fat = xmldoc.createRoot()
        
        # 1 <FatturaElettronicaHeader>
        head = xmldoc.appendElement(fat, 'FatturaElettronicaHeader')
        
        # 1.1 <DatiTrasmissione>
        datitrasm = xmldoc.appendElement(head, 'DatiTrasmissione')
        
        # 1.1.1 <IdTrasmittente>
        idtrasm = xmldoc.appendElement(datitrasm, 'IdTrasmittente')
        xmldoc.appendItems(idtrasm, (('IdPaese',  Env.Azienda.stato),
                                     ('IdCodice', Env.Azienda.codfisc),))
        
        # 1.1.2 <ProgressivoInvio>
        xmldoc.appendItems(datitrasm, (('ProgressivoInvio',    str(numprogr).zfill(5)),
                                       ('FormatoTrasmissione', xmldoc.sdicver),
                                       ('CodiceDestinatario',  self.pdc.ftel_codice),))
        
        # 1.1.5 <ContattiTrasmittente>
        dati = []
        if Env.Azienda.numtel:
            numtel = ''
            for x in Env.Azienda.numtel.replace('+39',''):
                if x.isalnum():
                    numtel += x
            if numtel:
                dati.append(('Telefono', numtel))
        if Env.Azienda.email:
            dati.append(('Email', Env.Azienda.email))
        if dati:
            contattitrasm = xmldoc.appendElement(datitrasm, 'ContattiTrasmittente',)
            xmldoc.appendItems(contattitrasm, dati)
        
        # 1.2 <CedentePrestatore>
        cedente = xmldoc.appendElement(head, 'CedentePrestatore')
        
        # 1.2.1 <DatiAnagrafici>
        cedente_datianag = xmldoc.appendElement(cedente, 'DatiAnagrafici')
        
        # 1.2.1.1 <IdFiscaleIVA>
        cedente_datianag_datifisc = xmldoc.appendElement(cedente_datianag, 'IdFiscaleIVA')
        xmldoc.appendItems(cedente_datianag_datifisc, (('IdPaese',  Env.Azienda.stato or "IT"),
                                                       ('IdCodice', Env.Azienda.codfisc or Env.Azienda.piva)))
        
        # 1.2.1.3 <Anagrafica>
        cedente_datianag_anagraf = xmldoc.appendElement(cedente_datianag, 'Anagrafica')
        dati = []
        if dataz['cognome']:
            dati.append(('Nome', dataz['nome']))
            dati.append(('Cognome', dataz['cognome']))
        else:
            dati.append(('Denominazione', Env.Azienda.descrizione))
        xmldoc.appendItems(cedente_datianag_anagraf, dati)
        
        # 1.2.1.8 <RegimeFiscale>
        try:
            regfisc = 'RF%s' % str(int(dataz['regfisc'])).zfill(2)
        except:
            regfisc = 'RF01'
        xmldoc.appendItems(cedente_datianag, (('RegimeFiscale', regfisc),))
        
        # 1.2.2 <Sede>
        cedente_sede = xmldoc.appendElement(cedente, 'Sede')
        xmldoc.appendItems(cedente_sede, (('Indirizzo', Env.Azienda.indirizzo),
                                          ('CAP',       Env.Azienda.cap),
                                          ('Comune',    Env.Azienda.citta),
                                          ('Provincia', Env.Azienda.prov),
                                          ('Nazione',   Env.Azienda.stato),))
        
        if dataz['soind'] and dataz['socap'] and dataz['socit'] and dataz['sopro']:
            # 1.2.3 <StabileOrganizzazione>
            cedente_staborg = xmldoc.appendElement(cedente, 'StabileOrganizzazione')
            xmldoc.appendItems(cedente_staborg, (('Indirizzo', dataz['soind']),
                                                 ('CAP',       dataz['socap']),
                                                 ('Comune',    dataz['socit']),
                                                 ('Provincia', dataz['sopro']),
                                                 ('Nazione',   'IT'),))
        
        if dataz['rfdes'] or dataz['rfcognome']:
            dati = []
            if dataz['rfcognome']:
                dati.append(('Cognome', dataz['rfcognome']))
                dati.append(('Nome', dataz['rfnome']))
            else:
                dati.append(('Denominazione', dataz['rfdes']))
            # 1.3 <RappresentanteFiscale>
            cedente_rapfis = xmldoc.appendElement(cedente, 'RappresentanteFiscale')
            # 1.3.1 <DatiAnagrafici>
            cedente_rapfis_anag = xmldoc.appendElement(cedente_rapfis, 'DatiAnagrafici')
            xmldoc.appendItems(cedente_rapfis_anag, dati)
            # 1.3.1.1 <IdFiscaleIVA>
            cedente_rapfis_anag = xmldoc.appendElement(cedente_rapfis, 'IdFiscaleIVA')
            xmldoc.appendItems(cedente_rapfis_anag, (('IdPaese',  dataz['rfstato']),
                                                     ('IdCodice', dataz['rfcodfis'] or dataz['rfpiva'])),)
        
        # 1.4 <CessionarioCommittente>
        cessionario = xmldoc.appendElement(head, 'CessionarioCommittente')
        
        # 1.4.1 <DatiAnagrafici>
        cessionario_datianag = xmldoc.appendElement(cessionario, 'DatiAnagrafici')
        xmldoc.appendItems(cessionario_datianag, (('CodiceFiscale', cli.codfisc or cli.piva),))
        
        # 1.4.1.3 <Anagrafica>
        cessionario_datianag_anagraf = xmldoc.appendElement(cessionario_datianag, 'Anagrafica')
        xmldoc.appendItems(cessionario_datianag_anagraf, (('Denominazione', pdc.descriz),))
        
        #1.4.2 <Sede>
        cessionario_sede = xmldoc.appendElement(cessionario, 'Sede')
        xmldoc.appendItems(cessionario_sede, (('Indirizzo', cli.indirizzo),
                                              ('CAP',       cli.cap),
                                              ('Comune',    cli.citta),
                                              ('Provincia', cli.prov),
                                              ('Nazione',   cli.nazione),))
        
        loop = True
        while loop:
            
            # 2 <FatturaElettronicaBody>
            body = xmldoc.appendElement(fat, 'FatturaElettronicaBody')
            
            # 2.1 <DatiGenerali>
            body_gen = xmldoc.appendElement(body, 'DatiGenerali')
            
            # 2.1.1 <DatiGeneraliDocumento>
            body_gen_doc = xmldoc.appendElement(body_gen, 'DatiGeneraliDocumento')
            
            xmldoc.appendItems(body_gen_doc, (('TipoDocumento', self.config.ftel_tipdoc),
                                              ('Divisa',        'EUR'),
                                              ('Data',          data(self.datdoc)),
                                              ('Numero',        str(self.numdoc).zfill(5)),))
            
            # 2.1.2 <DatiOrdineAcquisto>
            v = []
            if self.ftel_ordnum:
                v.append(('IdDocumento', self.ftel_ordnum))
            if self.ftel_orddat:
                v.append(('Data', data(self.ftel_orddat)))
            if self.ftel_codcup:
                v.append(('CodiceCUP', self.ftel_codcup))
            if self.ftel_codcig:
                v.append(('CodiceCIG', self.ftel_codcig))
            if v:
                body_gen_acq = xmldoc.appendElement(body_gen, 'DatiOrdineAcquisto')
                xmldoc.appendItems(body_gen_acq, v)
            
            # 2.1.8 <DatiDDT>
            ddt = dbm.DocMag()
            ddt.ClearOrders()
            ddt.AddOrder('doc.datdoc')
            ddt.AddOrder('doc.numdoc')
            ddt.Retrieve("doc.id_docacq=%s" % self.id)
            if ddt.RowsCount() > 0:
                for _ in ddt:
                    body_gen_ddt = xmldoc.appendElement(body_gen, 'DatiDDT')
                    xmldoc.appendItems(body_gen_ddt, (('NumeroDDT', str(ddt.numdoc)),
                                                      ('DataDDT',   data(ddt.datdoc)),))
            
            # 2.2 <DatiBeniServizi>
            body_det = xmldoc.appendElement(body, 'DatiBeniServizi')
            
            # 2.2.1 <DettaglioLinee>
            for mov in self.mov:
                
                if not mov.importo:
                    continue
                
                #body dettaglio linea
                body_det_row = xmldoc.appendElement(body_det, 'DettaglioLinee')
                imp_netto_sc = mov.importo
                if mov.qta and mov.prezzo:
                    imp_lordo_sc = round(mov.qta*mov.prezzo, 2)
                else:
                    imp_lordo_sc = imp_netto_sc
                imp_sconto = round((imp_lordo_sc or 0)\
                                  -(imp_netto_sc or 0), 2)
                dati = []
                dati.append(('NumeroLinea', str(mov.numriga)))
                dati.append(('Descrizione', mov.descriz))
#                 if mov.qta:
#                     dati.append(('Quantita', '%.8f' % mov.qta))
#                 if mov.um:
#                     dati.append(('UnitaMisura', mov.um))
                if mov.prezzo:
                    dati.append(('PrezzoUnitario', '%.8f' % mov.prezzo))
                else:
                    dati.append(('PrezzoUnitario', '%.8f' % mov.importo))
                xmldoc.appendItems(body_det_row, dati)
                dati = []
                if imp_sconto:
                    #body dettaglio sconto
                    sdati = []
                    sdati.append(('Tipo', 'SC'))
                    sdati.append(('Percentuale', '%.2f' % (imp_sconto/imp_lordo_sc*100)))
                    sdati.append(('Importo', '%.2f' % imp_sconto))
                    body_det_row_sconto = xmldoc.appendElement(body_det_row, 'ScontoMaggiorazione')
                    xmldoc.appendItems(body_det_row_sconto, sdati)
                if imp_netto_sc:
                    dati.append(('PrezzoTotale', '%.2f' % imp_netto_sc))
                if mov.iva.id:
                    dati.append(('AliquotaIVA', '%.2f' % mov.iva.perciva))
                if dati:
                    xmldoc.appendItems(body_det_row, dati)
            
            # 2.2.2 <DatiRiepilogo>
            body_det_rie = xmldoc.appendElement(body_det, 'DatiRiepilogo')
            for ivaid, ivacod, ivades, imponib, imposta, importo, imposcr, isomagg, perciva, percind, tipoalq in self._info.totiva:
                xmldoc.appendItems(body_det_rie, (('AliquotaIVA',       '%.2f' % perciva),
                                                  ('ImponibileImporto', '%.2f' % imponib),
                                                  ('Imposta',           '%.2f' % imposta),))
            
            # 2.4 <DatiPagamento>
            body_pag = xmldoc.appendElement(body, 'DatiPagamento')
            
            # 2.4.1 <CondizioniPagamento>
            xmldoc.appendItems(body_pag, (('CondizioniPagamento', self.modpag.ftel_tippag),))
            
            if self.id_reg is not None:
                reg = self.regcon
                reg.Get(self.id_reg)
                if reg.OneRow():
                    for scad in self.regcon.scad:
                        # 2.4.2 <DettaglioPagamento>
                        datipag = [('ModalitaPagamento',     self.modpag.ftel_modpag),
                                   ('DataScadenzaPagamento', data(scad.datscad)),
                                   ('ImportoPagamento',      '%.2f' % scad.importo),]
                        if cli.id_bancapag:
                            dbban = dbm.adb.DbTable('banche')
                            if dbban.Get(cli.id_bancapag) and dbban.OneRow():
                                if len(dbban.iban or '') > 0:
                                    datipag.append(('IBAN', dbban.iban))
                        body_pag_det = xmldoc.appendElement(body_pag, 'DettaglioPagamento')
                        xmldoc.appendItems(body_pag_det, datipag)
            
            db = dbm.adb.db.__database__
            db.Execute("UPDATE movmag_h SET ftel_numtrasm=%%s WHERE id=%s" % self.id, numprogr)
            
            #genero file pdf dei documenti elaborati
            rptname = self.config.ftel_layout
            if rptname:
                doc = FatturaElettronica()
                doc.Get(self.id)
                doc._info.anag = doc.GetAnag()
                r = rpt.Report(None, doc, rptname, output="STORE", 
                               changepathname=self.ftel_get_pathname(numprogr),
                               changefilename=self.ftel_get_printname(numprogr)) 
            
            if not self.MoveNext():
                loop = False
        
        #genero file xml dei documenti elaborati
        stream = xmldoc.toprettyxml(indent="  ", encoding="UTF-8")
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
        stream = text_re.sub('>\g<1></', stream)
        n = stream.index('>')+1
        stream = stream[:n] + '\n<?xml-stylesheet type="text/xsl" href="fatturapa_v1.0.xsl"?>' + stream[n:]
        
        filename = self.ftel_get_filename(numprogr)
        h = open(filename, 'w')
        h.write(stream)
        h.close()
        
        self.ftel_make_style(numprogr)
        
        p = dbcfg.ProgrMagazz_FatturaElettronica()
        p.Retrieve()
        if p.IsEmpty():
            p.CreateNewRow()
        if numprogr > (p.progrimp1 or 0):
            p.progrimp1 = numprogr
            p.Save()
        
        return os.path.split(filename)
    
    def ftel_make_style(self, numprogr):
        path = self.ftel_get_pathname(numprogr)
        import fatturapa_magazz.fatturapa_v10_xsl as xsl
        open(os.path.join(path, 'fatturapa_v1.0.xsl'), 'w').write(xsl.xsl)


class FTEL_Document(Document):
    
    version = '1.0'
    sdicver = 'SDI10'
    
    def createRoot(self):
        
#         style = self.appendElement(self, '?xml-stylesheet')
#         style.setAttribute('type', "text/xsl")
#         style.setAttribute('href', "fatturapa_v1.0.xsl")
#         
        fat = self.appendElement(self, "p:FatturaElettronica")
        fat.setAttribute('xmlns:p', "http://www.fatturapa.gov.it/sdi/fatturapa/v%s" % self.version)
        fat.setAttribute('xmlns:ds', "http://www.w3.org/2000/09/xmldsig#")
        fat.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        fat.setAttribute('versione', self.version)
        
        return fat
    
    def appendElement(self, parent, tagName):
        element = self.createElement(tagName)
        parent.appendChild(element)
        return element
    
    def appendItems(self, node, key_values):
        for name, val in key_values:
            item = self.createElement(name)
            item_content = self.createTextNode(val)
            item.appendChild(item_content)
            node.appendChild(item)
        return node


