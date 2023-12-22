import sys
import re
import os
import MySQLdb
from Tkinter import *
import tkMessageBox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Image
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak,
Image, Spacer)
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
import datetime
from posadastodorio import *

class MiForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self. ui.mdiArea.addSubWindow(self.ui.altaproductos)
        self.ui.mdiArea.addSubWindow(self.ui.altaproveedores)
        self.ui.mdiArea.addSubWindow(self.ui.buscarproducto)
        self.ui.mdiArea.addSubWindow(self.ui.buscarproveedor)
        self.ui.mdiArea.addSubWindow(self.ui.modificarprecio)
        self.ui.mdiArea.addSubWindow(self.ui.verlistas)
        self.ui.mdiArea.addSubWindow(self.ui.ayuda)
        self.ui.mdiArea.addSubWindow(self.ui.inicio)
        QtCore.QObject.connect(self.ui.btnaceptar, QtCore.SIGNAL('clicked()'), self.altaproductos)
        QtCore.QObject.connect(self.ui.btnaceptarpro, QtCore.SIGNAL('clicked()'), self.altaproveedores)
        QtCore.QObject.connect(self.ui.btnverlistamp, QtCore.SIGNAL('clicked()'), self.verlista)
        QtCore.QObject.connect(self.ui.btnmodificarmp, QtCore.SIGNAL('clicked()'), self.modificarprecio)
        QtCore.QObject.connect(self.ui.btnlisproductos, QtCore.SIGNAL('clicked()'), self.listaproductos)
        QtCore.QObject.connect(self.ui.btnlispropro, QtCore.SIGNAL('clicked()'), self.listapropro)
        QtCore.QObject.connect(self.ui.btnlisproveedores, QtCore.SIGNAL('clicked()'), self.listaproveedores)
        QtCore.QObject.connect(self.ui.btnbuscarbp, QtCore.SIGNAL('clicked()'), self.buscarproductos)
        QtCore.QObject.connect(self.ui.btnmodificarbp, QtCore.SIGNAL('clicked()'), self.modificarproductos)
        QtCore.QObject.connect(self.ui.btnbuscarbprov, QtCore.SIGNAL('clicked()'), self.buscarproveedores)
        QtCore.QObject.connect(self.ui.btnmodificarbprov, QtCore.SIGNAL('clicked()'), self.modificarproveedores)
        QtCore.QObject.connect(self.ui.radiobp, QtCore.SIGNAL('clicked()'), self.habilitaronopr)
        QtCore.QObject.connect(self.ui.radiobprov, QtCore.SIGNAL('clicked()'), self.habilitaronoprov)
        QtCore.QObject.connect(self.ui.btncancelarmp, QtCore.SIGNAL('clicked()'), self.borrarlistaprecio)
        QtCore.QObject.connect(self.ui.linecodigo, QtCore.SIGNAL('editingFinished()'), self.opemulaltaproductos)
        QtCore.QObject.connect(self.ui.linecodpro, QtCore.SIGNAL('editingFinished()'), self.opemulaltaproveedores)
        QtCore.QObject.connect(self.ui.linecodigobp, QtCore.SIGNAL('editingFinished()'), self.opemulbuscarproductos)
        QtCore.QObject.connect(self.ui.linecodigobprov, QtCore.SIGNAL('editingFinished()'), self.opemulbuscarproveedores)
        QtCore.QObject.connect(self.ui.linecodigobp, QtCore.SIGNAL('editingFinished()'), self.opemulbuscarproductos)
        QtCore.QObject.connect(self.ui.linepormp, QtCore.SIGNAL('editingFinished()'), self.opemulmodificarprecio)
        QtCore.QObject.connect(self.ui.btnlisproductos, QtCore.SIGNAL('editingFinished()'), self.opemulverlistas)
        QtCore.QObject.connect(self.ui.lineprovdes, QtCore.SIGNAL('editingFinished()'), self.opemulverlistas)
        QtCore.QObject.connect(self.ui.btncancelarbp, QtCore.SIGNAL('clicked()'), self.limpiarbp)
        QtCore.QObject.connect(self.ui.btncancelarbprov, QtCore.SIGNAL('clicked()'), self.limpiarbprov)

    def altaproductos(self):
        print 'paso 0'
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        ade = ''
        apr = ''
        aca = ''
        abo = ''
        apo = ''
        aob = ''
        aux = self.ui.linecodigo.text()
        if not re.match("^[0-9A-Z]{6}$", aux):
            aco = 'codigo, '
        aux = self.ui.linedescripcion.text()
        if aux == '':
            ade = 'descripcion, '
        aux = self.ui.lineprecio.text()
        if not re.match("^[0-9.]{1,7}$", aux):
            apr = 'precio, '
        aux = self.ui.linecantidad.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            aca = 'cantidad, '
        aux = self.ui.linebonificacion.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            abo = 'bonificacion '
        aux = self.ui.lineobservaciones.text()
        if aux == '':
            aob = 'observaciones, '
        aux = self.ui.lineproveedor.text()
        if not re.match("^[0-9]{1,2}$", aux):
            apo = 'proveedor '
        if ade != '' or aco != '' or apr != '' or aca != '' or abo != '' or aob != '' or apo !='':
            print 'paso 00'
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar bien los campos: " + aco + ade + apr + aca + abo + aob + apo)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigo.setFocus()
        else:
            print 'paso 01'
            cod = str(self.ui.linecodigo.text())
            des = str(self.ui.linedescripcion.text())
            pre = float(self.ui.lineprecio.text())
            can = float(self.ui.linecantidad.text())
            bon = float(self.ui.linebonificacion.text())
            obs = str(self.ui.lineobservaciones.text())
            pro = int(self.ui.lineproveedor.text())
            print cod
            try:
                print 'paso 10'
                cursor.execute("Select *from productos where ptr_cod ='%s'" % cod)
                row = cursor.fetchone()
                print 'paso 100'
                if row is not None:
                    print 'paso 11'
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="Ya existe un producto con ese codigo")
                    self.ui.mdiArea.setEnabled(True)
                else:
                    cursor.execute("Select *from proveedores where pro_cod = %d" % pro)
                    row = cursor.fetchone()
                    if row is None:
                        self.ui.mdiArea.setEnabled(False)
                        window = Tk()
                        window.wm_withdraw()
                        tkMessageBox.showinfo(title="Mensaje",message="No existe un proveedor con el codigo ingresado")
                        self.ui.mdiArea.setEnabled(True)
                    else:
                        print 'paso 1'
                        cursor.execute("""
                        INSERT INTO productos(ptr_cod, ptr_des, ptr_pre, ptr_bon, ptr_can, ptr_obs, ptr_pro)
                        VALUES('%s','%s', %f, %f, %f, '%s', %d)
                        """ % (cod, des, pre, bon, can, obs, pro))
                        conn.commit()
                        print 'paso 2'
                        self.ui.mdiArea.setEnabled(False)
                        window = Tk()
                        window.wm_withdraw()
                        tkMessageBox.showinfo(title="Mensaje",message="El producto ha ingresado correctamente")
                        print 'paso 3'
                        self.ui.mdiArea.setEnabled(True)
                        self.ui.linecodigo.setText("")
                        self.ui.linedescripcion.setText("")
                        self.ui.lineprecio.setText("")
                        self.ui.linecantidad.setText("")
                        self.ui.linebonificacion.setText("")
                        self.ui.lineobservaciones.setText("")
                        self.ui.lineproveedor.setText("")
                        self.ui.linecodigo.setFocus()
            except MySQLdb.Error:
                conn.rollback()
                sys.exit(1)
                print "Error"
        cursor.close()
        conn.close()

    def altaproveedores(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        ano = ''
        adi = ''
        ate = ''
        aem = ''
        aux = self.ui.linecodpro.text()
        if not re.match("^[0-9]{1,2}$", aux):
            aco = 'codigo, '
        aux = self.ui.linenompro.text()
        if aux== '':
            ano = 'nombre, '
        aux = self.ui.linedirpro.text()
        if aux =='':
            adi = 'direccion, '
        aux = self.ui.linetelpro.text()
        if aux =='':
            ate = 'telefono, '
        aux = self.ui.lineemapro.text()
        if aux =='':
            aem = 'email'
        if  aco != '' or ano != '' or adi != '' or ate != '' or aem!='':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar bien los campos: " + aco + ano + adi + ate + aem)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigo.setFocus()
        else:
            cod = int(self.ui.linecodpro.text())
            nom = str(self.ui.linenompro.text())
            dir = str(self.ui.linedirpro.text())
            tel = str(self.ui.linetelpro.text())
            ema = str(self.ui.lineemapro.text())
            try:
                cursor.execute("Select *from proveedores where pro_cod=%d" % cod)
                row = cursor.fetchone()
                if row is not None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="Ya existe un proveedor con ese codigo")
                    self.ui.mdiArea.setEnabled(True)
                else:
                    cursor.execute("""
                    INSERT INTO proveedores(pro_cod, pro_nom, pro_dir, pro_tel, pro_ema)
                    VALUES(%d,'%s', '%s', '%s', '%s')
                    """ % (cod, nom, dir, tel, ema))
                    conn.commit()
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="El proveedor ha ingresado correctamente")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodpro.setText("")
                    self.ui.linenompro.setText("")
                    self.ui.linedirpro.setText("")
                    self.ui.linetelpro.setText("")
                    self.ui.lineemapro.setText("")
            except MySQLdb.Error:
                    conn.rollback()
                    sys.exit(1)
            cursor.close()
            conn.close()

    def verlista(self):
        conn= conectar()
        cursor = conn.cursor()
        aux= self.ui.linepromp.text()
        try:
            if not re.match("^[0-9]{1,2}$", aux):
               cursor.execute("Select *from productos order by ptr_cod")
            else:
                pro = int(aux)
                cursor.execute("Select *from productos where ptr_pro = %d order by ptr_cod" % pro)
            rows = cursor.fetchall()
            for row in rows:
               itl = row[0] + ' | ' + row[1] + '->' + str(row[2])
               self.ui.listproductos.addItem(itl)
        except MySQLdb.Error:
                sys.exit(1)

    def modificarprecio(self):
        conn = conectar()
        cursor = conn.cursor()
        mpr = ''
        mpl = ''
        aux = self.ui.linepormp.text()
        if not re.match("^[0-9.]{1,5}$", aux):
            mpr = 'porcentaje, '
        aux = self.ui.listproductos.count()
        if aux == 0:
            mpl = 'lista, '
        if mpr != '' or mpl!= '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar bien los campos: " + mpr + mpl)
            self.ui.mdiArea.setEnabled(True)
        else:
            self.ui.listultcam.clear()
            items= self.ui.listproductos.selectedItems()
            if len(items)== 0:
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="Debe seleccionar algunos elementos de la lista. ")
                self.ui.mdiArea.setEnabled(True)
            else:
                #Array para guardar los items seleccionados
                selected = []
                for x in range(len(items)):
                    selected.append(self.ui.listproductos.selectedItems()[x].text()[0:6])
                por = float(self.ui.linepormp.text())
                try:
                    for cod in selected:
                        cursor.execute("Select ptr_pre, ptr_des from productos where ptr_cod = '%s'" % cod)
                        row = cursor.fetchone()
                        npr = float(row[0]*(1 + por/100))
                        cursor.execute("Update productos set ptr_pre= %f where ptr_cod ='%s'" % (
                            npr, cod))
                        conn.commit()
                        itemsuc= str(row[1]) + ": " + str(row[0]) + " + " + str(por) + " = " + str(npr)
                        self.ui.listultcam.addItem(itemsuc)
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="Los precios han sido modificados correctamente.")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.listproductos.clear()
                    self.ui.linepromp.setText('')
                    self.ui.linepormp.setText('')
                except MySQLdb.Error:
                    conn.rollback()
                    sys.exit(1)
                cursor.close()
                conn.close()

    def borrarlistaprecio(self):
        self.ui.listproductos.clear()

    def listaproductos(self):
        conn= conectar()
        cursor = conn.cursor()
        estilo = getSampleStyleSheet()
        story = []
        fichero_imagen = "logolista.png"
        imagen_logo = Image(os.path.realpath(fichero_imagen),width=155,height=16)
        story.append(imagen_logo)
        cabecera = estilo['Heading2']
        cabecera.pageBreakBefore=0
        cabecera.keepWithNext=0
        #cabecera.backColor=colors.blue
        fecha = datetime.date.today()
        hoy = fecha.strftime("%d/%m/20%y")
        titulo = "LISTA DE PRODUCTOS, FECHA: " + str(hoy)
        parrafo = Paragraph(titulo ,cabecera)
        story.append(parrafo)
        t=Table([['Codigo','Descripcion','Precio','Observaciones']],colWidths=[54,155,60,220], rowHeights=30)
        t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.blue),('FONTSIZE',(0,0),(-1,-1),12)])
        story.append(t)
        try:
            cursor.execute("Select *from productos order by ptr_cod")
            rows = cursor.fetchall()
            for row in rows:
                t=Table([[row[0],row[1],row[2],row[5]]],colWidths=[54,155,60,220], rowHeights=30)
                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('FONTSIZE',(0,0),(-1,-1),12)])
                story.append(t)
            #os.chdir('C:/Users/Lenovo/Desktop/informes')
            doc=SimpleDocTemplate("listadeproductos.pdf",pagesize=A4)
            doc.build(story)
            os.system('listadeproductos.pdf')
        except MySQLdb.Error:
               print "Error"
               sys.exit(1)
        cursor.close()
        conn.close()

    def listapropro(self):
        conn= conectar()
        cursor = conn.cursor()
        mpde = ''
        mpha = ''
        mpdh = ''
        apde = self.ui.lineprovdes.text()
        if not re.match("^[0-9]{1,2}$", apde):
            mpde = 'proveedor desde, '
        apha = self.ui.lineprovhas.text()
        if not re.match("^[0-9]{1,2}$", apha):
            mpha = 'proveedor hasta, '

        if mpde != '' or mpha != '' or mpdh != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar bien los campos: " + mpde + mpha + mpdh)
            self.ui.mdiArea.setEnabled(True)
        else:
            cpde= int(apde)
            cpha= int(apha)
            if cpde > cpha:
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="El proveedor desde es mayor que el proveedor hasta.")
                self.ui.mdiArea.setEnabled(True)
            else:
                #Creacion de la consulta
                try:
                    print "1"
                    ssql = "Select ptr_cod, ptr_des, ptr_pre, ptr_obs, ptr_pro from productos"
                    ssql+= " where ptr_pro >= %d and ptr_pro <= %d order by ptr_pro, ptr_cod" % (cpde, cpha)
                    cursor.execute(ssql)
                    rows = cursor.fetchall()
                    if len(rows)== 0:
                        self.ui.mdiArea.setEnabled(False)
                        window = Tk()
                        window.wm_withdraw()
                        tkMessageBox.showinfo(title="Mensaje",message="No se encontro ningun producto.")
                        self.ui.mdiArea.setEnabled(True)
                    else:
                        print "3"
                        ant = -1
                        estilo = getSampleStyleSheet()
                        story = []
                        fichero_imagen = "logolista.png"
                        imagen_logo = Image(os.path.realpath(fichero_imagen),width=155,height=16)
                        story.append(imagen_logo)
                        cabecera = estilo['Heading3']
                        cabecera.pageBreakBefore=0
                        cabecera.keepWithNext=0
                        #cabecera.backColor=colors.blue
                        fecha = datetime.date.today()
                        hoy = fecha.strftime("%d/%m/20%y")
                        titulo = "LISTA DE PRODUCTOS POR PROVEEDOR, FECHA: " + str(hoy)
                        parrafo = Paragraph(titulo ,cabecera)
                        story.append(parrafo)
                        print "4"
                        for row in rows:
                            if row[4]!= ant:
                                t=Table([["","","",""]],colWidths=120, rowHeights=30)
                                story.append(t)
                                cursor.execute("Select pro_nom from proveedores where pro_cod = %d" % row[4])
                                nprov = cursor.fetchone()
                                t=Table([["Codigo:",row[4],"Nombre:",nprov[0],"",""]],colWidths=[50,40,50,100], rowHeights=30)
                                t.setStyle([('TEXTCOLOR', (0, 0), (-1, -0), colors.blue),('FONTSIZE',(0,0),(-1,-1),12),('ALIGN', (0,0), (-1,-1), 'LEFT')])
                                story.append(t)
                                t=Table([['Codigo','Descripcion','Precio','Observaciones']],colWidths=[54,155,60,220], rowHeights=30)
                                t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.blue),('FONTSIZE',(0,0),(-1,-1),12)])
                                story.append(t)
                                ant = row[4]
                            t=Table([[row[0],row[1],row[2],row[3]]],colWidths=[54,155,60,220], rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('FONTSIZE',(0,0),(-1,-1),12)])
                            story.append(t)
                        print "5"
                        #os.chdir('C:/Users/Lenovo/Desktop/informes')
                        doc=SimpleDocTemplate("listaproprov.pdf",pagesize=A4)
                        print "6"
                        doc.build(story)
                        print "7"
                        os.system('listaproprov.pdf')
                except MySQLdb.Error:
                       print "Error"
                       sys.exit(1)
                cursor.close()
                conn.close()

    def listaproveedores(self):
        conn= conectar()
        cursor = conn.cursor()
        mpde = ''
        mpha = ''
        mpdh = ''
        apde = self.ui.lineprovdes.text()
        if not re.match("^[0-9]{1,2}$", apde):
            mpde = 'proveedor desde, '
        apha = self.ui.lineprovhas.text()
        if not re.match("^[0-9]{1,2}$", apha):
            mpha = 'proveedor hasta, '
        if mpde != '' or mpha != '':
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Completar bien los campos: " + mpde + mpha)
        else:
            pdes= int(self.ui.lineprovdes.text())
            phas= int(self.ui.lineprovhas.text())
            if pdes > phas:
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="El proveedor desde es mayor que el proveedor hasta.")
            else:
                try:
                    cursor.execute("Select *from proveedores where pro_cod >= %d and pro_cod <= %d" % (pdes, phas))
                    rows = cursor.fetchall()
                    if len(rows)== 0:
                        self.ui.mdiArea.setEnabled(False)
                        window = Tk()
                        window.wm_withdraw()
                        tkMessageBox.showinfo(title="Mensaje",message="No se encontro ningun proveedor.")
                        self.ui.mdiArea.setEnabled(True)
                    else:
                        print pdes, phas
                        estilo = getSampleStyleSheet()
                        story = []
                        fichero_imagen = "logolista.png"
                        imagen_logo = Image(os.path.realpath(fichero_imagen),width=155,height=16)
                        story.append(imagen_logo)
                        cabecera = estilo['Heading2']
                        cabecera.pageBreakBefore=0
                        cabecera.keepWithNext=0
                        #cabecera.backColor=colors.blue
                        fecha = datetime.date.today()
                        hoy = fecha.strftime("%d/%m/20%y")
                        titulo = "LISTA DE PROVEEDORES, FECHA: " + str(hoy)
                        parrafo = Paragraph(titulo ,cabecera)
                        story.append(parrafo)
                        t=Table([['Codigo','Nombre','Direccion','Telefono']],colWidths=[45,167,167,167], rowHeights=30)
                        t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('TEXTCOLOR', (0, 0), (-1, -0), colors.blue),('FONTSIZE',(0,0),(-1,-1),12)])
                        story.append(t)
                        for row in rows:
                            print row[0]
                            t=Table([[row[0],row[1],row[2],row[3]]],colWidths=[45,167,167,167], rowHeights=30)
                            t.setStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BOX',(0,0),(-1,-1),2,colors.black),('FONTSIZE',(0,0),(-1,-1),12)])
                            story.append(t)
                        #os.chdir('C:/Users/Lenovo/Desktop/informes')
                        doc=SimpleDocTemplate("listadeproveedores.pdf",pagesize=A4)
                        doc.build(story)
                        os.system('listadeproveedores.pdf')
                except MySQLdb.Error:
                       print "Error"
                       sys.exit(1)
                cursor.close()
                conn.close()

    def buscarproductos(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        aux = self.ui.linecodigobp.text()
        if not re.match("^[0-9A-Z]{6}$", aux):
            aco = 'codigo'
        if aco != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigobp.setFocus()
        else:
            cod = str(self.ui.linecodigobp.text())
            try:
                cursor.execute("Select *from productos where ptr_cod='%s'" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se encontro ningun producto")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigobp.setFocus()
                else:
                    self.ui.linecodigobp.setEnabled(True)
                    self.ui.radiobp.setEnabled(True)
                    self.ui.linedescripcionbp.setText(str(row[1]))
                    self.ui.linepreciobp.setText(str(row[2]))
                    self.ui.linecantidadbp.setText(str(row[4]))
                    self.ui.linebonificacionbp.setText(str(row[3]))
                    self.ui.lineobservacionesbp.setText(str(row[5]))
                    self.ui.lineproveedorbp.setText(str(row[6]))
                    self.ui.radiobp.setChecked(0)
            except MySQLdb.Error:
                sys.exit(1)
            cursor.close()
            conn.close()

    def modificarproductos(self):
        #conn = conectar()
        #cursor = conn.cursor()
        aco = ''
        apr = ''
        aca = ''
        abo = ''
        aob = ''
        apo = ''
        aux = self.ui.linecodigobp.text()
        if not re.match("^[0-9A-Z]{6}$", aux):
            aco = 'codigo, '
        aux = self.ui.linepreciobp.text()
        if not re.match("^[0-9.]{1,7}$", aux):
            apr = 'precio, '
        aux = self.ui.linecantidadbp.text()
        if not re.match("^[0-9.]{1,6}$", aux):
            aca = 'cantidad, '
        aux = self.ui.linebonificacionbp.text()
        if not re.match("^[0-9.]{1,5}$", aux):
            abo = 'bonificacion, '
        aux = self.ui.lineobservacionesbp.text()
        if aux == '':
            aob = 'observaciones, '
        aux = self.ui.lineproveedorbp.text()
        if not re.match("^[0-9]{1,2}$", aux):
            apo = 'proveedor, '
        if aco != '' or apr != '' or aca != '' or abo != '' or apo != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco + apr + aca + abo + apo + aob)
            self.ui.mdiArea.setEnabled(True)
        else:
            #conn2 = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="22922965j", db="angelita")
            conn2 = conectar()
            cursor2 = conn2.cursor()
            cod = str(self.ui.linecodigobp.text())
            nom = str(self.ui.linedescripcionbp.text())
            pre = float(self.ui.linepreciobp.text())
            can = float(self.ui.linecantidadbp.text())
            bon = float(self.ui.linebonificacionbp.text())
            obs = str(self.ui.lineobservacionesbp.text())
            pro = int(self.ui.lineproveedorbp.text())
            print pre
            try:
                cursor2.execute("Update productos set ptr_des='%s', ptr_pre=%f, ptr_can=%f, ptr_bon=%f, ptr_obs='%s', ptr_pro=%d where ptr_cod='%s'" % (
                    nom, pre, can, bon, obs, pro, cod))
                conn2.commit()
                self.ui.linecodigobp.setText('')
                self.ui.linedescripcionbp.setText('')
                self.ui.linepreciobp.setText('')
                self.ui.linecantidadbp.setText('')
                self.ui.linebonificacionbp.setText('')
                self.ui.lineobservacionesbp.setText('')
                self.ui.lineproveedorbp.setText('')
                self.ui.btnmodificarbp.setEnabled(False)
                self.ui.btnbuscarbp.setEnabled(True)
                self.ui.btncancelarbp.setEnabled(True)
                self.ui.radiobp.setEnabled(False)
                self.ui.linecodigobp.setEnabled(True)
                self.ui.linedescripcionbp.setEnabled(False)
                self.ui.linepreciobp.setEnabled(False)
                self.ui.linecantidadbp.setEnabled(False)
                self.ui.linebonificacionbp.setEnabled(False)
                self.ui.lineobservacionesbp.setEnabled(False)
                self.ui.lineproveedorbp.setEnabled(False)
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="El producto se modifico correctamente")
                self.ui.mdiArea.setEnabled(True)
                self.ui.linecodigobp.setFocus()
            except MySQLdb.Error:
                sys.exit(1)
            cursor2.close()
            conn2.close()

    def habilitaronopr(self):
        if self.ui.radiobp.isChecked()== True:
            self.ui.btnmodificarbp.setEnabled(True)
            self.ui.btnbuscarbp.setEnabled(False)
            self.ui.linecodigobp.setEnabled(False)
            self.ui.linedescripcionbp.setEnabled(True)
            self.ui.linepreciobp.setEnabled(True)
            self.ui.linecantidadbp.setEnabled(True)
            self.ui.linebonificacionbp.setEnabled(True)
            self.ui.lineobservacionesbp.setEnabled(True)
            self.ui.lineproveedorbp.setEnabled(True)
            self.ui.btncancelarbp.setEnabled(False)
            self.ui.linedescripcionbp.setFocus()
        else:
            self.ui.btnmodificarbp.setEnabled(False)
            self.ui.btnbuscarbp.setEnabled(True)
            self.ui.linecodigobp.setEnabled(True)
            self.ui.linedescripcionbp.setEnabled(False)
            self.ui.linepreciobp.setEnabled(False)
            self.ui.linecantidadbp.setEnabled(False)
            self.ui.linebonificacionbp.setEnabled(False)
            self.ui.lineobservacionesbp.setEnabled(False)
            self.ui.lineproveedorbp.setEnabled(False)
            self.ui.btncancelarbp.setEnabled(True)
            if self.ui.linecodigobp.text()== '':
                self.ui.radiobp.setEnabled(False)
            self.ui.linecodigobp.setFocus()

    def buscarproveedores(self):
        conn = conectar()
        cursor = conn.cursor()
        aco = ''
        aux = self.ui.linecodigobprov.text()
        if not re.match("^[0-9]{1,2}$", aux):
            aco = 'codigo'
        if aco != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco)
            self.ui.mdiArea.setEnabled(True)
            self.ui.linecodigomp.setFocus()
        else:
            cod = int(self.ui.linecodigobprov.text())
            try:
                cursor.execute("Select *from proveedores where pro_cod=%d" % cod)
                row = cursor.fetchone()
                if row is None:
                    self.ui.mdiArea.setEnabled(False)
                    window = Tk()
                    window.wm_withdraw()
                    tkMessageBox.showinfo(title="Mensaje",message="No se encontro ningun proveedor")
                    self.ui.mdiArea.setEnabled(True)
                    self.ui.linecodigobprov.setFocus()
                else:
                    self.ui.linecodigobprov.setEnabled(True)
                    self.ui.radiobprov.setEnabled(True)
                    self.ui.linenombrebprov.setText(str(row[1]))
                    self.ui.linedireccionbprov.setText(str(row[2]))
                    self.ui.linetelefonobprov.setText(str(row[3]))
                    self.ui.lineemailbprov.setText(str(row[4]))
                    self.ui.radiobprov.setChecked(0)
                    self.ui.btnbuscarbprov.setEnabled(True)
            except MySQLdb.Error:
                sys.exit(1)
            cursor.close()
            conn.close()

    def modificarproveedores(self):
        #conn = conectar()
        #cursor = conn.cursor()
        aco = ''
        ano = ''
        adi = ''
        ate = ''
        aem = ''
        aux = self.ui.linecodigobprov.text()
        if not re.match("^[0-9]{1,2}$", aux):
            aco = 'codigo'
        aux = self.ui.linenombrebprov.text()
        if aux == '':
            ano = 'nombre'
        aux = self.ui.linedireccionbprov.text()
        if aux == '':
            adi = 'direccion'
        aux = self.ui.linetelefonobprov.text()
        if aux == '':
            ate = 'telefono'
        aux = self.ui.lineemailbprov.text()
        if aux == '':
            aem = 'email'
        if aco != '' or ano !='' or adi != '' or ate != '' or aem != '':
            self.ui.mdiArea.setEnabled(False)
            window = Tk()
            window.wm_withdraw()
            tkMessageBox.showinfo(title="Mensaje",message="Colocar o completar bien los campos: " + aco + ',' + ano + ',' + adi + ',' + ate + ',' + aem)
            self.ui.mdiArea.setEnabled(True)
        else:
            #conn2 = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="22922965j", db="angelita")
            conn2 = conectar()
            cursor2 = conn2.cursor()
            cod = int(self.ui.linecodigobprov.text())
            nom = str(self.ui.linenombrebprov.text())
            dir = str(self.ui.linedireccionbprov.text())
            tel = str(self.ui.linetelefonobprov.text())
            ema = str(self.ui.lineemailbprov.text())
            try:
                cursor2.execute("Update proveedores set pro_nom='%s', pro_dir='%s', pro_tel='%s', pro_ema='%s' where pro_cod=%d" % (
                    nom, dir, tel, ema, cod))
                conn2.commit()
                self.ui.linecodigobprov.setText('')
                self.ui.linenombrebprov.setText('')
                self.ui.linedireccionbprov.setText('')
                self.ui.linetelefonobprov.setText('')
                self.ui.lineemailbprov.setText('')
                self.ui.btnmodificarbprov.setEnabled(False)
                self.ui.btnbuscarbprov.setEnabled(True)
                self.ui.btncancelarbprov.setEnabled(True)
                self.ui.radiobprov.setEnabled(False)
                self.ui.linecodigobprov.setEnabled(True)
                self.ui.linenombrebprov.setEnabled(False)
                self.ui.linetelefonobprov.setEnabled(False)
                self.ui.linedireccionbprov.setEnabled(False)
                self.ui.lineemailbprov.setEnabled(False)
                self.ui.mdiArea.setEnabled(False)
                window = Tk()
                window.wm_withdraw()
                tkMessageBox.showinfo(title="Mensaje",message="El proveedor se modifico correctamente")
                self.ui.mdiArea.setEnabled(True)
                self.ui.linecodigobprov.setFocus()
            except MySQLdb.Error:
                sys.exit(1)
            cursor2.close()
            conn2.close()

    def habilitaronoprov(self):
        if self.ui.radiobprov.isChecked()== True:
            self.ui.btnmodificarbprov.setEnabled(True)
            self.ui.btnbuscarbprov.setEnabled(False)
            self.ui.linecodigobprov.setEnabled(False)
            self.ui.linenombrebprov.setEnabled(True)
            self.ui.linedireccionbprov.setEnabled(True)
            self.ui.linetelefonobprov.setEnabled(True)
            self.ui.lineemailbprov.setEnabled(True)
            self.ui.btncancelarbprov.setEnabled(False)
            self.ui.linenombrebprov.setFocus()
        else:
            self.ui.btnmodificarbprov.setEnabled(False)
            self.ui.btnbuscarbprov.setEnabled(True)
            self.ui.linecodigobprov.setEnabled(True)
            self.ui.linenombrebprov.setEnabled(False)
            self.ui.linedireccionbprov.setEnabled(False)
            self.ui.linetelefonobprov.setEnabled(False)
            self.ui.lineemailbprov.setEnabled(False)
            self.ui.btncancelarbprov.setEnabled(True)
            if self.ui.linecodigobprov.text()== '':
                self.ui.radiobprov.setEnabled(False)
            self.ui.linecodigobprov.setFocus()

    def opemulaltaproductos(self):
        self.ui.linecodpro.setText('')
        self.ui.linenompro.setText('')
        self.ui.linedirpro.setText('')
        self.ui.linetelpro.setText('')
        self.ui.lineemapro.setText('')
        self.ui.linecodigobp.setText('')
        self.ui.linedescripcionbp.setText('')
        self.ui.linecantidadbp.setText('')
        self.ui.linepreciobp.setText('')
        self.ui.linebonificacionbp.setText('')
        self.ui.lineobservacionesbp.setText('')
        self.ui.lineproveedorbp.setText('')
        self.ui.linecodigobprov.setText('')
        self.ui.linenombrebprov.setText('')
        self.ui.linedireccionbprov.setText('')
        self.ui.linetelefonobprov.setText('')
        self.ui.lineemailbprov.setText('')
        self.ui.radiobprov.setChecked(0)
        self.ui.radiobprov.setEnabled(False)
        self.ui.linecodigobprov.setEnabled(True)
        self.ui.linenombrebprov.setEnabled(False)
        self.ui.linedireccionbprov.setEnabled(False)
        self.ui.linetelefonobprov.setEnabled(False)
        self.ui.radiobp.setChecked(0)
        self.ui.radiobp.setEnabled(False)
        self.ui.linecodigobp.setEnabled(True)
        self.ui.linedescripcionbp.setEnabled(False)
        self.ui.linecantidadbp.setEnabled(False)
        self.ui.linepreciobp.setEnabled(False)
        self.ui.lineobservacionesbp.setEnabled(False)
        self.ui.linebonificacionbp.setEnabled(False)
        self.ui.lineproveedorbp.setEnabled(False)
        self.ui.lineemailbprov.setEnabled(False)
        self.ui.linepromp.setText('')
        self.ui.linepormp.setText('')
        self.ui.listproductos.clear()
        self.ui.lineprovdes.setText('')
        self.ui.lineprovhas.setText('')
        self.ui.btnbuscarbp.setEnabled(True)
        self.ui.btncancelarbp.setEnabled(True)
        self.ui.btnmodificarbp.setEnabled(False)
        self.ui.btnbuscarbprov.setEnabled(True)
        self.ui.btncancelarbprov.setEnabled(True)
        self.ui.btnmodificarbprov.setEnabled(False)

    def opemulaltaproveedores(self):
        self.ui.linecodigo.setText('')
        self.ui.linedescripcion.setText('')
        self.ui.linecantidad.setText('')
        self.ui.lineprecio.setText('')
        self.ui.linebonificacion.setText('')
        self.ui.lineobservaciones.setText('')
        self.ui.lineproveedor.setText('')
        self.ui.linecodigobp.setText('')
        self.ui.linedescripcionbp.setText('')
        self.ui.linecantidadbp.setText('')
        self.ui.linepreciobp.setText('')
        self.ui.linebonificacionbp.setText('')
        self.ui.lineobservacionesbp.setText('')
        self.ui.radiobp.setChecked(0)
        self.ui.radiobp.setEnabled(False)
        self.ui.linecodigobp.setEnabled(True)
        self.ui.linedescripcionbp.setEnabled(False)
        self.ui.linecantidadbp.setEnabled(False)
        self.ui.linepreciobp.setEnabled(False)
        self.ui.lineobservacionesbp.setEnabled(False)
        self.ui.linebonificacionbp.setEnabled(False)
        self.ui.lineproveedorbp.setEnabled(False)
        self.ui.lineproveedorbp.setText('')
        self.ui.linecodigobprov.setText('')
        self.ui.linenombrebprov.setText('')
        self.ui.linedireccionbprov.setText('')
        self.ui.linetelefonobprov.setText('')
        self.ui.lineemailbprov.setText('')
        self.ui.radiobprov.setChecked(0)
        self.ui.radiobprov.setEnabled(False)
        self.ui.linecodigobprov.setEnabled(True)
        self.ui.linenombrebprov.setEnabled(False)
        self.ui.linedireccionbprov.setEnabled(False)
        self.ui.linetelefonobprov.setEnabled(False)
        self.ui.lineemailbprov.setEnabled(False)
        self.ui.linepromp.setText('')
        self.ui.linepormp.setText('')
        self.ui.listproductos.clear()
        self.ui.lineprovdes.setText('')
        self.ui.lineprovhas.setText('')
        self.ui.btnbuscarbp.setEnabled(True)
        self.ui.btncancelarbp.setEnabled(True)
        self.ui.btnmodificarbp.setEnabled(False)
        self.ui.btnbuscarbprov.setEnabled(True)
        self.ui.btncancelarbprov.setEnabled(True)
        self.ui.btnmodificarbprov.setEnabled(False)

    def opemulbuscarproductos(self):
        self.ui.linecodpro.setText('')
        self.ui.linenompro.setText('')
        self.ui.linedirpro.setText('')
        self.ui.linetelpro.setText('')
        self.ui.lineemapro.setText('')
        self.ui.linecodigo.setText('')
        self.ui.linedescripcion.setText('')
        self.ui.linecantidad.setText('')
        self.ui.lineprecio.setText('')
        self.ui.linebonificacion.setText('')
        self.ui.lineobservaciones.setText('')
        self.ui.lineproveedor.setText('')
        self.ui.linecodigobprov.setText('')
        self.ui.linenombrebprov.setText('')
        self.ui.linedireccionbprov.setText('')
        self.ui.linetelefonobprov.setText('')
        self.ui.lineemailbprov.setText('')
        self.ui.radiobprov.setChecked(0)
        self.ui.radiobprov.setEnabled(False)
        self.ui.linecodigobprov.setEnabled(True)
        self.ui.linenombrebprov.setEnabled(False)
        self.ui.linedireccionbprov.setEnabled(False)
        self.ui.linetelefonobprov.setEnabled(False)
        self.ui.lineemailbprov.setEnabled(False)
        self.ui.linepromp.setText('')
        self.ui.linepormp.setText('')
        self.ui.listproductos.clear()
        self.ui.lineprovdes.setText('')
        self.ui.lineprovhas.setText('')
        self.ui.btnbuscarbprov.setEnabled(True)
        self.ui.btncancelarbprov.setEnabled(True)
        self.ui.btnmodificarbprov.setEnabled(False)

    def opemulbuscarproveedores(self):
        self.ui.linecodpro.setText('')
        self.ui.linenompro.setText('')
        self.ui.linedirpro.setText('')
        self.ui.linetelpro.setText('')
        self.ui.lineemapro.setText('')
        self.ui.linecodigo.setText('')
        self.ui.linedescripcion.setText('')
        self.ui.linecantidad.setText('')
        self.ui.lineprecio.setText('')
        self.ui.linebonificacion.setText('')
        self.ui.lineobservaciones.setText('')
        self.ui.lineproveedor.setText('')
        self.ui.linecodigobp.setText('')
        self.ui.linedescripcionbp.setText('')
        self.ui.linecantidadbp.setText('')
        self.ui.linepreciobp.setText('')
        self.ui.linebonificacionbp.setText('')
        self.ui.lineobservacionesbp.setText('')
        self.ui.lineproveedorbp.setText('')
        self.ui.radiobp.setChecked(0)
        self.ui.radiobp.setEnabled(False)
        self.ui.linecodigobp.setEnabled(True)
        self.ui.linedescripcionbp.setEnabled(False)
        self.ui.linecantidadbp.setEnabled(False)
        self.ui.linepreciobp.setEnabled(False)
        self.ui.lineobservacionesbp.setEnabled(False)
        self.ui.linebonificacionbp.setEnabled(False)
        self.ui.lineproveedorbp.setEnabled(False)
        self.ui.linepromp.setText('')
        self.ui.linepormp.setText('')
        self.ui.listproductos.clear()
        self.ui.lineprovdes.setText('')
        self.ui.lineprovhas.setText('')
        self.ui.btnbuscarbp.setEnabled(True)
        self.ui.btncancelarbp.setEnabled(True)
        self.ui.btnmodificarbp.setEnabled(False)

    def opemulmodificarprecio(self):
        self.ui.linecodpro.setText('')
        self.ui.linenompro.setText('')
        self.ui.linedirpro.setText('')
        self.ui.linetelpro.setText('')
        self.ui.lineemapro.setText('')
        self.ui.linecodigo.setText('')
        self.ui.linedescripcion.setText('')
        self.ui.linecantidad.setText('')
        self.ui.lineprecio.setText('')
        self.ui.linebonificacion.setText('')
        self.ui.lineobservaciones.setText('')
        self.ui.lineproveedor.setText('')
        self.ui.linecodigobp.setText('')
        self.ui.linedescripcionbp.setText('')
        self.ui.linecantidadbp.setText('')
        self.ui.linepreciobp.setText('')
        self.ui.linebonificacionbp.setText('')
        self.ui.lineobservacionesbp.setText('')
        self.ui.lineproveedorbp.setText('')
        self.ui.radiobp.setChecked(0)
        self.ui.radiobp.setEnabled(False)
        self.ui.linecodigobp.setEnabled(True)
        self.ui.linedescripcionbp.setEnabled(False)
        self.ui.linecantidadbp.setEnabled(False)
        self.ui.linepreciobp.setEnabled(False)
        self.ui.lineobservacionesbp.setEnabled(False)
        self.ui.linebonificacionbp.setEnabled(False)
        self.ui.lineproveedorbp.setEnabled(False)
        self.ui.linecodigobprov.setText('')
        self.ui.linenombrebprov.setText('')
        self.ui.linedireccionbprov.setText('')
        self.ui.linetelefonobprov.setText('')
        self.ui.lineemailbprov.setText('')
        self.ui.lineemailbprov.setText('')
        self.ui.radiobprov.setChecked(0)
        self.ui.radiobprov.setEnabled(False)
        self.ui.linecodigobprov.setEnabled(True)
        self.ui.linenombrebprov.setEnabled(False)
        self.ui.linedireccionbprov.setEnabled(False)
        self.ui.linetelefonobprov.setEnabled(False)
        self.ui.lineemailbprov.setEnabled(False)
        self.ui.lineprovdes.setText('')
        self.ui.lineprovhas.setText('')
        self.ui.btnbuscarbp.setEnabled(True)
        self.ui.btncancelarbp.setEnabled(True)
        self.ui.btnmodificarbp.setEnabled(False)
        self.ui.btnbuscarbprov.setEnabled(True)
        self.ui.btncancelarbprov.setEnabled(True)
        self.ui.btnmodificarbprov.setEnabled(False)

    def opemulverlistas(self):
        self.ui.linecodpro.setText('')
        self.ui.linenompro.setText('')
        self.ui.linedirpro.setText('')
        self.ui.linetelpro.setText('')
        self.ui.lineemapro.setText('')
        self.ui.linecodigo.setText('')
        self.ui.linedescripcion.setText('')
        self.ui.linecantidad.setText('')
        self.ui.lineprecio.setText('')
        self.ui.linebonificacion.setText('')
        self.ui.lineobservaciones.setText('')
        self.ui.lineproveedor.setText('')
        self.ui.linecodigobp.setText('')
        self.ui.linedescripcionbp.setText('')
        self.ui.linecantidadbp.setText('')
        self.ui.linepreciobp.setText('')
        self.ui.linebonificacionbp.setText('')
        self.ui.lineobservacionesbp.setText('')
        self.ui.lineproveedorbp.setText('')
        self.ui.radiobp.setChecked(0)
        self.ui.radiobp.setEnabled(False)
        self.ui.linecodigobp.setEnabled(True)
        self.ui.linedescripcionbp.setEnabled(False)
        self.ui.linecantidadbp.setEnabled(False)
        self.ui.linepreciobp.setEnabled(False)
        self.ui.lineobservacionesbp.setEnabled(False)
        self.ui.linebonificacionbp.setEnabled(False)
        self.ui.lineproveedorbp.setEnabled(False)
        self.ui.linecodigobprov.setText('')
        self.ui.linenombrebprov.setText('')
        self.ui.linedireccionbprov.setText('')
        self.ui.linetelefonobprov.setText('')
        self.ui.lineemailbprov.setText('')
        self.ui.radiobprov.setChecked(0)
        self.ui.radiobprov.setEnabled(False)
        self.ui.linecodigobprov.setEnabled(True)
        self.ui.linenombrebprov.setEnabled(False)
        self.ui.linedireccionbprov.setEnabled(False)
        self.ui.linetelefonobprov.setEnabled(False)
        self.ui.lineemailbprov.setEnabled(False)
        self.ui.linepromp.setText('')
        self.ui.linepormp.setText('')
        self.ui.listproductos.clear()
        self.ui.btnbuscarbp.setEnabled(True)
        self.ui.btncancelarbp.setEnabled(True)
        self.ui.btnmodificarbp.setEnabled(False)
        self.ui.btnbuscarbprov.setEnabled(True)
        self.ui.btncancelarbprov.setEnabled(True)
        self.ui.btnmodificarbprov.setEnabled(False)

    def limpiarbp(self):
        self.ui.linedescripcionbp.setText('')
        self.ui.linecantidadbp.setText('')
        self.ui.linepreciobp.setText('')
        self.ui.linebonificacionbp.setText('')
        self.ui.lineobservacionesbp.setText('')
        self.ui.lineproveedorbp.setText('')
        self.ui.radiobp.setEnabled(False)

    def limpiarbprov(self):
        self.ui.linenombrebprov.setText('')
        self.ui.linedireccionbprov.setText('')
        self.ui.linetelefonobprov.setText('')
        self.ui.lineemailbprov.setText('')
        self.ui.radiobprov.setEnabled(False)

def conectar():
        conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="22922965j", db="posadastodorio")
        return conn

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MiForm()
    myapp.show()
    sys.exit(app.exec_())
