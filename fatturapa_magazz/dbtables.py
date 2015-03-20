#!/bin/env/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturpa_magazz/dbtables.py
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


def fmt_qt(x):
    mask = '%%.%df' % Env.Azienda.BaseTab.MAGQTA_DECIMALS
    return mask % x

def fmt_pr(x):
    mask = '%%.%df' % Env.Azienda.BaseTab.MAGPRE_DECIMALS
    return mask % x

def fmt_sc(x):
    mask = '%%.%df' % 2
    return mask % x

def fmt_ii(x):
    mask = '%%.%df' % Env.Azienda.BaseTab.VALINT_DECIMALS
    return mask % x


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
                    """rfnome rfcognome rfdes rfind rfcap rfcit rfpro rfcodfis rfpiva """\
                    """trcodfis trstato """\
                    """senome secognome sedes secodfis sepiva sestato setit seeori sesogemi""".split():
            cfg.Retrieve('setup.chiave=%s', 'azienda_ftel_%s' % name)
            if name == 'sesogemi':
                if cfg.flag == "C":
                    dataz[name] = "CC"
                elif cfg.flag == "T":
                    dataz[name] = "TZ"
                else:
                    dataz[name] = ""
            else:
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
        if dataz['trcodfis']:
            trcodfis = dataz['trcodfis']
            trstato = dataz['trstato'] or "IT"
        else:
            trcodfis = Env.Azienda.codfisc or Env.Azienda.piva
            trstato = Env.Azienda.stato or "IT"
        xmldoc.appendItems(idtrasm, (('IdPaese',  trstato),
                                     ('IdCodice', trcodfis),))
        
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
                                              ('Nazione',   cli.nazione or "IT"),))
        
        if dataz['secodfis']:
            #1.5 <TerzoIntermediarioOSoggettoEmittente>
            tsogemi = xmldoc.appendElement(head, 'TerzoIntermediarioOSoggettoEmittente')
            #1.5.1 <DatiAnagrafici>
            tsogemi_datianag = xmldoc.appendElement(tsogemi, 'DatiAnagrafici')
            tsogemi_datianag_id_iva = xmldoc.appendElement(tsogemi_datianag, 'IdFiscaleIVA')
            xmldoc.appendItems(tsogemi_datianag_id_iva, (('IdPaese', dataz['sestato'] or "IT"),
                                                         ('IdCodice', dataz['sepiva'])))
            #1.5.2 <CodiceFiscale>
            xmldoc.appendItems(tsogemi_datianag, (('CodiceFiscale', dataz['secodfis']),))
            #1.5.3 <Anagrafica>
            tsogemi_datianag_anag = xmldoc.appendElement(tsogemi_datianag, 'Anagrafica')
            f = []
            if dataz['sedes']:
                f.append(('Denominazione', dataz['sedes']))
            if dataz['senome']:
                f.append(('Nome', dataz['senome']))
            if dataz['secognome']:
                f.append(('Cognome', dataz['secognome']))
            if dataz['setit']:
                f.append(('Titolo', dataz['setit']))
            if dataz['seeori']:
                f.append(('CodEORI', dataz['seeori']))
            xmldoc.appendItems(tsogemi_datianag_anag, f)
        
        if dataz['sesogemi']:
            #1.6 <SoggettoEmittente>
            xmldoc.appendItems(head, (('SoggettoEmittente', dataz['sesogemi']),))
        
        loop = True
        while loop:
            
            # 2 <FatturaElettronicaBody>
            body = xmldoc.appendElement(fat, 'FatturaElettronicaBody')
            
            # 2.1 <DatiGenerali>
            body_gen = xmldoc.appendElement(body, 'DatiGenerali')
            
            # 2.1.1 <DatiGeneraliDocumento>
            body_gen_doc = xmldoc.appendElement(body_gen, 'DatiGeneraliDocumento')
            
            xmldoc.appendItems(body_gen_doc, 
                               (('TipoDocumento',          self.config.ftel_tipdoc),
#                                 ('Causale',                self.config.descriz),  #indicato in v.1.1, ma da errore
                                ('Divisa',                 'EUR'),
                                ('Data',                   data(self.datdoc)),
                                ('Numero',                 str(self.numdoc).zfill(5)),
                                ('ImportoTotaleDocumento', fmt_ii(self.totimporto)),))
            
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
#                     dati.append(('Quantita', fmt_qt(mov.qta)))
#                 if mov.um:
#                     dati.append(('UnitaMisura', mov.um))
                if mov.prezzo:
                    dati.append(('PrezzoUnitario', fmt_pr(mov.prezzo)))
                else:
                    dati.append(('PrezzoUnitario', fmt_pr(mov.importo)))
                xmldoc.appendItems(body_det_row, dati)
                dati = []
                if imp_sconto:
                    #body dettaglio sconto
                    sdati = []
                    sdati.append(('Tipo', 'SC'))
                    sdati.append(('Percentuale', fmt_ii(imp_sconto/imp_lordo_sc*100)))
                    sdati.append(('Importo', fmt_sc(imp_sconto)))
                    body_det_row_sconto = xmldoc.appendElement(body_det_row, 'ScontoMaggiorazione')
                    xmldoc.appendItems(body_det_row_sconto, sdati)
                if imp_netto_sc:
                    dati.append(('PrezzoTotale', fmt_ii(imp_netto_sc)))
                if mov.iva.id:
                    dati.append(('AliquotaIVA', fmt_sc(mov.iva.perciva)))
                if dati:
                    xmldoc.appendItems(body_det_row, dati)
            
            # 2.2.2 <DatiRiepilogo>
            body_det_rie = xmldoc.appendElement(body_det, 'DatiRiepilogo')
            iva = dbm.adb.DbTable('aliqiva')
            for ivaid, ivacod, ivades, imponib, imposta, importo, imposcr, isomagg, perciva, percind, tipoalq in self._info.totiva:
                dativa = []
                dativa.append(('AliquotaIVA',       fmt_sc(perciva)))
                dativa.append(('ImponibileImporto', fmt_ii(imponib)))
                dativa.append(('Imposta',           fmt_ii(imposta)))
                if iva.id != ivaid:
                    iva.Get(ivaid)
                if iva.samefloat(iva.perciva, 0):
                    dativa.append(('Natura', iva.ftel_natura))
                if iva.tipo == "S":
                    #split payment
                    esig = "S"
                else:
                    #esigilità immediata
                    esig = "I"
                dativa.append(('EsigibilitaIVA', esig))
                xmldoc.appendItems(body_det_rie, dativa)
            
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
                                   ('ImportoPagamento',      fmt_ii(scad.importo)),]
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
#         stream = stream[:n] + '\n<?xml-stylesheet type="text/xsl" href="fatturapa_v1.0.xsl"?>' + stream[n:]
        stream = stream[:n] + '\n<?xml-stylesheet type="text/xsl" href="fatturapa_v1.1.xsl"?>' + stream[n:]
        
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
#         import fatturapa_magazz.fatturapa_v10_xsl as xsl
#         open(os.path.join(path, 'fatturapa_v1.0.xsl'), 'w').write(xsl.xsl)
        import fatturapa_magazz.fatturapa_v11_xsl as xsl
        open(os.path.join(path, 'fatturapa_v1.1.xsl'), 'w').write(xsl.xsl)


class FTEL_Document(Document):
    
    version = '1.1'
    sdicver = 'SDI11'
    
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


