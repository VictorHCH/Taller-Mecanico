import sys
import sqlite3
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QToolBar, QTableView, QVBoxLayout, QLineEdit, QHBoxLayout,
                             QWidget, QPushButton, QHeaderView, QStyledItemDelegate, QDateEdit, QMessageBox, QTableWidgetItem, QAbstractItemView)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QSize, Qt, QRect, QTimer, QDate
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel, QSqlDatabase, QSqlTableModel
from datetime import date


class VentanaPrincipal(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaPrincipal, self).__init__(parent)
        loadUi('ventanas\Inicio.ui', self)
        self.lb.setPixmap(QPixmap("JL.png"))
        self.lb.setScaledContents(True)

        self.pb.setMaximum(100)
        self.pb.setValue(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.barraP)
        self.timer.start(100)

    def barraP(self):
        for i in range(101):
            time.sleep(0.02)
            self.pb.setValue(i)
            self.pb.value()+1
        if self.pb.value() == 100:
            self.timer.stop()
            self.pb.setValue(0)
            self.hide()
            otraventana = MenuPrincipal(self)
            otraventana.show()


class MenuPrincipal(QMainWindow):
    def __init__(self, parent=None):
        super(MenuPrincipal, self).__init__(parent)
        loadUi('ventanas\MenuPrincipal.ui', self)

        self.btn.setIconSize(QSize(200, 200))
        self.btn.setIcon(QIcon('iconos/venta.ico'))
        self.btn.setToolTip("Venta")
        self.btn_4.setIconSize(QSize(200, 200))
        self.btn_4.setIcon(QIcon('iconos/cliente.ico'))
        self.btn_4.setToolTip("Clientes")
        self.btn_3.setIconSize(QSize(200, 200))
        self.btn_3.setIcon(QIcon('iconos/inv.ico'))
        self.btn_3.setToolTip("Inventario")
        self.btn_2.setIconSize(QSize(200, 200))
        self.btn_2.setIcon(QIcon('iconos/registro.ico'))
        self.btn_2.setToolTip("Registro de ventas")

        self.btn.clicked.connect(self.venta)
        self.btn_2.clicked.connect(self.registro)
        self.btn_3.clicked.connect(self.inventario)
        self.btn_4.clicked.connect(self.clientes)

    def venta(self):
        self.hide()
        otraventana = VentanaVenta(self)
        otraventana.show()

    def clientes(self):
        self.hide()
        otraventana = VentanaClientes(self)
        otraventana.show()

    def inventario(self):
        self.hide()
        otraventana = VentanaInventario(self)
        otraventana.show()

    def registro(self):
        self.hide()
        otraventana = VentanaRegistros(self)
        otraventana.show()


class VentanaVenta(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaVenta, self).__init__(parent)
        loadUi('ventanas\Venta.ui', self)

        #venta nueva
        self.ventaNueva()

        self.leCliente.setPlaceholderText("Nombre del cliente")
        self.leVehiculo.setPlaceholderText("Nombre del Vehiculo")
        self.leCliente.textChanged.connect(self.actualizarQuery1)

        #Tabla Clientes
        self.twCliente.setDragDropOverwriteMode(False)
        self.twCliente.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.twCliente.setTextElideMode(Qt.ElideRight)
        self.twCliente.setWordWrap(False)
        self.twCliente.setSortingEnabled(False)
        self.twCliente.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter |
                                                              Qt.AlignCenter)
        self.twCliente.horizontalHeader().setHighlightSections(False)
        self.twCliente.horizontalHeader().setStretchLastSection(True)
        self.twCliente.verticalHeader().setVisible(False)
        self.twCliente.horizontalHeader().setVisible(False)
        self.twCliente.setAlternatingRowColors(True)
        self.twCliente.setColumnHidden(0, True)
        self.twCliente.itemClicked.connect(self.completa)

        self.actualizarQuery1()

        # Tabla Conceptos
        delegateFloat = InitialDelegate(2, self.twConcepto)
        self.twConcepto.setItemDelegateForColumn(4, delegateFloat)
        self.twConcepto.setItemDelegateForColumn(2, delegateFloat)
        self.twConcepto.setDragDropOverwriteMode(False)
        self.twConcepto.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.twConcepto.setTextElideMode(Qt.ElideRight)
        self.twConcepto.setWordWrap(False)
        self.twConcepto.setSortingEnabled(False)
        self.twConcepto.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter |
                                                              Qt.AlignCenter)
        self.twConcepto.horizontalHeader().setHighlightSections(False)
        self.twConcepto.horizontalHeader().setStretchLastSection(True)
        self.twConcepto.verticalHeader().setVisible(False)
        self.twConcepto.setAlternatingRowColors(True)

        # VENTANA NUEVO USUARIO
        self.btn.clicked.connect(self.btnNuevoCliente)
        self.btn.setToolTip("Agregar nuevo cliente")

        # Ventana agregar concepto
        self.btnConcepto.clicked.connect(self.agregarConcepto)
        self.btnConcepto.setToolTip("Agregar concepto")

        #Actualizar
        self.btnActualizar.clicked.connect(self.actualizar)

        #borrar
        self.btnBorrar.clicked.connect(self.borrar)

        #Venta
        self.btnVenta.clicked.connect(self.venta)

        #cancelar venta
        self.btnCancelar.clicked.connect(self.borrarVenta)

        #boton regresa
        self.btnRegresa.clicked.connect(self.regresarMenu)

    def regresarMenu(self):
        self.borrarVenta()
        self.menuPrincipal()

    def menuPrincipal(self):
        self.close()
        otraventana = MenuPrincipal(self)
        otraventana.show()

    def borrarVenta(self):
        conexion = sqlite3.connect('puntoVenta.db')
        consulta = conexion.cursor()
        dato = (int(self.numVenta), )
        #Borra conceptos
        sql = """DELETE FROM Concepto WHERE numVenta = ?"""

        consulta.execute(sql, dato)
        conexion.commit()
        #Borrar Venta
        sql = """DELETE FROM Venta WHERE numVenta = ?"""

        consulta.execute(sql, dato)
        conexion.commit()
        conexion.close()
        self.menuPrincipal()

    def venta(self):
        conexion = sqlite3.connect('puntoVenta.db')
        consulta = conexion.cursor()
        vehiculo = self.leVehiculo.text()
        total = int(self.total)
        item = self.twCliente.item(0, 0)
        cliente = int(item.text())
        idVenta = self.numVenta
        datos = (vehiculo, total, cliente, idVenta)

        sql = """UPDATE Venta SET vehiculo = ?, total = ?, cliente = ? WHERE (numVenta = ?)"""

        consulta.execute(sql, datos)
        conexion.commit()
        conexion.close()
        self.menuPrincipal()

    def borrar(self):
        row = self.twConcepto.currentRow()
        item = self.twConcepto.item(row, 0)
        idb = int(item.text())
        dato = (idb, )
        conexion = sqlite3.connect('puntoVenta.db')
        consulta = conexion.cursor()

        sql = """DELETE FROM Concepto WHERE (idConcepto = ?)"""
        consulta.execute(sql, dato)
        conexion.commit()
        conexion.close()
        self.actualizarQuery2()
        self.calculaTotal()

    def actualizar(self):
        self.actualizarQuery2()
        self.calculaTotal()

    def completa(self):
        row = self.twCliente.currentRow()
        item = self.twCliente.item(row, 1)
        self.leCliente.setText(item.text())

    def btnVenta(self):
        pass

    def btnCliente(self):
        self.hide()
        otraventana = VentanaClientes(self)
        otraventana.show()

    def btnInv(self, s):
        self.hide()
        otraventana = VentanaInventario(self)
        otraventana.show()

    def btnReg(self, s):
        self.hide()
        otraventana = VentanaRegistros(self)
        otraventana.show()

    def btnNuevoCliente(self):
        otraventana = VentanaClienteNuevo(self)
        otraventana.show()

    def numeroVenta(self):
        conexion = sqlite3.connect("puntoVenta.db")
        consulta = conexion.cursor()

        sql = """SELECT MAX(numVenta) AS numVenta FROM Venta"""
        self.numVenta = ""
        try:
            consulta.execute(sql)
            datosDevueltos = consulta.fetchall()
            conexion.close()
            if datosDevueltos:
                for datos in datosDevueltos:
                    self.numVenta = datos[0]
        except:
            pass

    def agregarConcepto(self):
        otraventana = VentanaProductos(self.numVenta, self)
        otraventana.show()
        self.actualizarQuery2()
        self.calculaTotal()

    def calculaTotal(self):
        conexion = sqlite3.connect("puntoVenta.db")
        consulta = conexion.cursor()
        dato = (int(self.numVenta), )
        self.total = 0
        sql = """SELECT importe FROM Concepto 
             INNER JOIN Venta ON Venta.numVenta = Concepto.numVenta WHERE Venta.numVenta = ?"""

        try:
            consulta.execute(sql, dato)
            datosDevueltos = consulta.fetchall()
            conexion.close()
            if datosDevueltos:
                for datos in datosDevueltos:
                    self.total += float(datos[0])
        except:
            pass
        self.leTotal.setText("${:,.{}f}".format(self.total, 2))

    def ventaNueva(self):
        conexion = sqlite3.connect('puntoVenta.db')
        consulta = conexion.cursor()
        fecha = date.today()
        f = (fecha.strftime("%Y-%m-%d"), )

        sql = """INSERT INTO Venta VALUES (NULL, ?, "", 0, 0)"""

        consulta.execute(sql, f)
        conexion.commit()
        conexion.close()
        self.numeroVenta()

    def actualizarQuery1(self):
        conexion = sqlite3.connect("puntoVenta.db")
        consulta = conexion.cursor()

        dato = ("%"+self.leCliente.text()+"%", self.leCliente.text())

        sql = """SELECT idCliente, nombre FROM Cliente
        WHERE nombre LIKE ? OR idCliente = ?"""

        try:
            consulta.execute(sql, dato)
            datosDevueltos = consulta.fetchall()
            conexion.close()

            if datosDevueltos:
                fila = 0
                for datos in datosDevueltos:
                    self.twCliente.setRowCount(fila + 1)

                    self.twCliente.setItem(fila, 0, QTableWidgetItem(str(datos[0])))
                    self.twCliente.setItem(fila, 1, QTableWidgetItem(str(datos[1])))

                    fila += 1
        except:
            pass

    def actualizarQuery2(self):
        conexion = sqlite3.connect("puntoVenta.db")
        consulta = conexion.cursor()

        idVen = int(self.numVenta)
        dato = (idVen, )

        sql = """SELECT idConcepto, Refaccion.nombre, Refaccion.precio, Concepto.cantidad, importe FROM Concepto INNER JOIN Refaccion ON Refaccion.idRefaccion = Concepto.refaccion
                INNER JOIN Venta ON Venta.numVenta = Concepto.numVenta WHERE Venta.numVenta = ?"""
        try:
            consulta.execute(sql, dato)
            datosDevueltos = consulta.fetchall()
            conexion.close()

            if datosDevueltos:
                fila = 0
                for datos in datosDevueltos:
                    self.twConcepto.setRowCount(fila + 1)

                    self.twConcepto.setItem(fila, 0, QTableWidgetItem(str(datos[0])))
                    self.twConcepto.setItem(fila, 1, QTableWidgetItem(str(datos[1])))
                    self.twConcepto.setItem(fila, 2, QTableWidgetItem(str(datos[2])))
                    self.twConcepto.setItem(fila, 3, QTableWidgetItem(str(datos[3])))
                    self.twConcepto.setItem(fila, 4, QTableWidgetItem(str(datos[4])))

                    fila += 1
        except:
            pass


class VentanaClientes(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaClientes, self).__init__(parent)
        loadUi('ventanas\Clientes.ui', self)

        self.lineEdit.setPlaceholderText("Nombre del cliente")
        self.lineEdit.textChanged.connect(self.actualizarQuery)

        self.modelo = QSqlQueryModel()
        self.tableView.setModel(self.modelo)
        self.tableView.setWordWrap(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setFont(QFont("ITC Avant Garde Std Bk Cn", 10, QFont.Bold))
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.setDragDropOverwriteMode(False)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setTextElideMode(Qt.ElideRight)
        self.tableView.setWordWrap(False)
        self.tableView.setSortingEnabled(False)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter |
                                                              Qt.AlignCenter)
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setAlternatingRowColors(True)

        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT * FROM Cliente WHERE "
            "nombre LIKE '%' || :nombreCliente || '%'"
        )
        self.actualizarQuery()

        # VENTANA NUEVO USUARIO
        self.btn.setIconSize(QSize(40, 30))
        self.btn.setIcon(QIcon('iconos/agregar.ico'))
        self.btn.clicked.connect(self.btnNuevoCliente)
        self.btn.setToolTip("Agregar nuevo cliente")

        self.btn_4.setIconSize(QSize(50, 40))
        self.btn_4.setIcon(QIcon('iconos\menu.ico'))
        self.btn_4.setToolTip("Menú principal")
        self.btn_4.clicked.connect(self.menuPrincipal)

        self.btn_2.setIconSize(QSize(40, 30))
        self.btn_2.setIcon(QIcon('iconos/editar.ico'))
        self.btn_2.setToolTip("Editar cliente")
        self.btn_2.clicked.connect(self.editar)

        self.btn_3.setIconSize(QSize(40, 30))
        self.btn_3.setIcon(QIcon('iconos/borrar.ico'))
        self.btn_3.setToolTip("Borrar cliente")
        self.btn_3.clicked.connect(self.borrar)

    def menuPrincipal(self):
        self.close()
        otraventana = MenuPrincipal(self)
        otraventana.show()

    def editar(self):
        otraventana = VentanaEditarCliente(self)
        otraventana.show()

    def borrar(self):
        otraventana = VentanaBorrarCliente(self)
        otraventana.show()

    def btnNuevoCliente(self):
        otraventana = VentanaClienteNuevo(self)
        otraventana.show()

    def actualizarQuery(self):
        nombreCliente = self.lineEdit.text()
        self.query.bindValue(":nombreCliente", nombreCliente)

        self.query.exec_()
        self.modelo.setQuery(self.query)


class VentanaInventario(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaInventario, self).__init__(parent)
        loadUi('ventanas\Inventario.ui', self)

        self.lineEdit.setPlaceholderText("Nombre del producto")
        self.lineEdit.textChanged.connect(self.actualizarQuery)

        self.modelo = QSqlQueryModel()
        self.tableView.setModel(self.modelo)
        self.tableView.setWordWrap(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setFont(QFont("ITC Avant Garde Std Bk Cn", 9, QFont.Bold))
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.setDragDropOverwriteMode(False)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setTextElideMode(Qt.ElideRight)
        self.tableView.setWordWrap(False)
        self.tableView.setSortingEnabled(False)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter |
                                                              Qt.AlignCenter)
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setAlternatingRowColors(True)

        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT * FROM Refaccion WHERE "
            "nombre LIKE '%' || :nombreProducto || '%'"
        )
        self.actualizarQuery()

        delegateFloat = InitialDelegate(2, self.tableView)
        self.tableView.setItemDelegateForColumn(2, delegateFloat)
        self.modelo.setHeaderData(0, Qt.Horizontal, "Id producto")
        self.modelo.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.modelo.setHeaderData(2, Qt.Horizontal, "Precio")
        self.modelo.setHeaderData(3, Qt.Horizontal, "Cantidad")
        self.modelo.setHeaderData(4, Qt.Horizontal, "Unidad de medida")

        #Agregar producto
        self.btn_2.clicked.connect(self.agregarProducto)
        self.btn_2.setToolTip("Agregar producto")
        self.btn_2.setIconSize(QSize(40, 30))
        self.btn_2.setIcon(QIcon('iconos/agregar.ico'))

        self.btn_5.setIconSize(QSize(50, 40))
        self.btn_5.setIcon(QIcon('iconos/menu.ico'))
        self.btn_5.setToolTip("Menú principal")
        self.btn_5.clicked.connect(self.menuPrincipal)

        self.btn_3.setIconSize(QSize(40, 30))
        self.btn_3.setIcon(QIcon('iconos/editar.ico'))
        self.btn_3.setToolTip("Editar producto")
        self.btn_3.clicked.connect(self.editar)

        self.btn_4.setIconSize(QSize(40, 30))
        self.btn_4.setIcon(QIcon('iconos/borrar.ico'))
        self.btn_4.setToolTip("Borrar producto")
        self.btn_4.clicked.connect(self.borrar)

        #Pruebas

    def menuPrincipal(self):
        self.close()
        otraventana = MenuPrincipal(self)
        otraventana.show()

    def editar(self):
        otraventana = VentanaEditarProducto(self)
        otraventana.show()

    def borrar(self):
        otraventana = VentanaBorrarProducto(self)
        otraventana.show()

    def agregarProducto(self):
        otraventana = VentanaRegistroProducto(self)
        otraventana.show()

    def actualizarQuery(self):
        nombreProducto = self.lineEdit.text()
        self.query.bindValue(":nombreProducto", nombreProducto)

        self.query.exec_()
        self.modelo.setQuery(self.query)


class VentanaRegistros(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaRegistros, self).__init__(parent)
        loadUi('ventanas\RegistroVentas.ui', self)

        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.setMaximumDate(QDate.currentDate())
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setCursor(Qt.PointingHandCursor)

        self.lineEdit.setPlaceholderText("Nombre del cliente")
        self.lineEdit.textChanged.connect(self.actualizarQuery)
        self.dateEdit.dateChanged.connect(self.actualizarQuery)

        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.itemDoubleClicked.connect(self.detalleVenta)
        self.tableWidget.setAlternatingRowColors(True)
        delegateFloat = InitialDelegate(2, self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(4, delegateFloat)

        self.actualizarQuery()

        #Boton regresar menu
        self.btnMenu.clicked.connect(self.menuPrincipal)

    def detalleVenta(self):
        row = self.tableWidget.currentRow()
        item = self.tableWidget.item(row, 0)
        if item is not None:
            otraventana = VentanaDetalleRegistro(item.text(), self)
            otraventana.show()

    def menuPrincipal(self):
        self.close()
        otraventana = MenuPrincipal(self)
        otraventana.show()

    def btnVenta(self):
        self.hide()
        otraventana = VentanaVenta(self)
        otraventana.show()

    def btnCliente(self):
        self.hide()
        otraventana = VentanaClientes(self)
        otraventana.show()

    def btnInv(self, s):
        self.hide()
        otraventana = VentanaInventario(self)
        otraventana.show()

    def btnReg(self, s):
        pass

    def actualizarQuery(self):
        conexion = sqlite3.connect("puntoVenta.db")
        consulta = conexion.cursor()

        dato = ("%"+self.lineEdit.text()+"%", "%"+self.dateEdit.text()+"%")

        sql = """SELECT Venta.numVenta, nombre, Venta.vehiculo, Venta.fecha, Venta.total FROM Cliente INNER JOIN Venta ON Venta.cliente = Cliente.idCliente
        WHERE Cliente.nombre LIKE ? AND Venta.fecha LIKE ?"""
        try:
            consulta.execute(sql, dato)
            datosDevueltos = consulta.fetchall()
            conexion.close()

            if datosDevueltos:
                fila = 0
                for datos in datosDevueltos:
                    self.tableWidget.setRowCount(fila + 1)

                    self.tableWidget.setItem(fila, 0, QTableWidgetItem(str(datos[0])))
                    self.tableWidget.setItem(fila, 1, QTableWidgetItem(str(datos[1])))
                    self.tableWidget.setItem(fila, 2, QTableWidgetItem(str(datos[2])))
                    self.tableWidget.setItem(fila, 3, QTableWidgetItem(str(datos[3])))
                    self.tableWidget.setItem(fila, 4, QTableWidgetItem(str(datos[4])))

                    fila += 1
            else:
                QMessageBox.information(self, "Buscar venta", "No se encontro "
                                                                "información.   ", QMessageBox.Ok)
        except:
            pass


class VentanaClienteNuevo(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaClienteNuevo, self).__init__(parent)
        loadUi("ventanas\ClienteNuevo.ui", self)

        self.pushButton_2.clicked.connect(self.cancelar)
        self.pushButton.clicked.connect(self.aceptar)

    def cancelar(self):
        self.hide()

    def aceptar(self):
        nombre = self.lineEdit.text()
        telefono = self.lineEdit_2.text()
        agregarCliente(nombre, telefono)
        self.hide()


def agregarCliente(nombre, telefono):
    conexion = sqlite3.connect('puntoVenta.db')
    consulta = conexion.cursor()

    datos = (nombre, telefono)

    sql = """INSERT INTO Cliente (nombre, telefono) VALUES (?,?)"""

    consulta.execute(sql, datos)
    conexion.commit()
    conexion.close()


class VentanaProductos(QMainWindow):
    def __init__(self, numVenta, parent=None):
        super(VentanaProductos, self).__init__(parent)
        loadUi("ventanas\Productos.ui", self)

        self.numVenta = numVenta
        self.lineEdit.setPlaceholderText("Nombre del producto")
        self.lineEdit.textChanged.connect(self.actualizarQuery)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setFont(QFont("ITC Avant Garde Std Bk Cn", 10, QFont.Bold))

        delegateFloat = InitialDelegate(2, self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(2, delegateFloat)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setTextElideMode(Qt.ElideRight)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter |
                                                              Qt.AlignCenter)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.itemDoubleClicked.connect(self.agregaProducto)

        self.actualizarQuery()

    def agregaProducto(self):
        row = self.tableWidget.currentRow()
        item = self.tableWidget.item(row, 0)
        otraventana = VentanaAgregarProducto(item.text(), self.numVenta, self)
        otraventana.show()

    def actualizarQuery(self):
        conexion = sqlite3.connect("puntoVenta.db")
        consulta = conexion.cursor()

        dato = ("%"+self.lineEdit.text()+"%", )

        sql = """SELECT idRefaccion, nombre, precio FROM Refaccion WHERE nombre LIKE ?"""

        try:
            consulta.execute(sql, dato)
            datosDevueltos = consulta.fetchall()
            conexion.close()

            if datosDevueltos:
                fila = 0
                for datos in datosDevueltos:
                    self.tableWidget.setRowCount(fila + 1)

                    self.tableWidget.setItem(fila, 0, QTableWidgetItem(str(datos[0])))
                    self.tableWidget.setItem(fila, 1, QTableWidgetItem(str(datos[1])))
                    self.tableWidget.setItem(fila, 2, QTableWidgetItem(str(datos[2])))

                    fila += 1
        except:
            pass


class VentanaRegistroProducto(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaRegistroProducto, self).__init__(parent)
        loadUi("ventanas\Registros.ui", self)

        self.comboBox.addItems(["Unidades", "Metros", "Kilogramos"])

        self.pushButton_2.clicked.connect(self.cancelar)
        self.pushButton.clicked.connect(self.aceptar)

    def cancelar(self):
        self.close()

    def aceptar(self):
        idP = self.lineEdit.text()
        nombre = self.lineEdit_2.text()
        cantidad = self.spinBox.text()
        precio = self.lineEdit_4.text()
        unidad = self.comboBox.currentText()
        agregarProducto(idP, nombre, cantidad, precio, unidad)
        self.hide()


def agregarProducto(idP, nombre, cantidad, precio, unidad):
    conexion = sqlite3.connect('puntoVenta.db')
    consulta = conexion.cursor()

    datos = (idP, nombre, cantidad, precio, unidad)

    sql = """INSERT INTO Refaccion (idRefaccion, nombre, cantidad, precio, uniMedida) VALUES (?,?,?,?,?)"""

    consulta.execute(sql, datos)
    conexion.commit()
    conexion.close()


class InitialDelegate(QStyledItemDelegate):
    def __init__(self, decimals, parent=None):
        super().__init__(parent)
        self.nDecimals = decimals

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
        try:
            text = index.model().data(index, Qt.DisplayRole)
            number = float(text)
            option.text = "${:,.{}f}".format(number, self.nDecimals)
        except:
            pass


class VentanaDetalleRegistro(QMainWindow):
    def __init__(self, id,  parent=None):
        super(VentanaDetalleRegistro, self).__init__(parent)
        loadUi("ventanas\DetalleVenta.ui", self)

        self.id = id
        delegateFloat = InitialDelegate(2, self.tableView)
        self.tableView.setItemDelegateForColumn(3, delegateFloat)
        self.tableView.setItemDelegateForColumn(4, delegateFloat)
        self.modelo = QSqlQueryModel()
        self.tableView.setModel(self.modelo)
        self.tableView.setDragDropOverwriteMode(False)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setTextElideMode(Qt.ElideRight)
        self.tableView.setWordWrap(False)
        self.tableView.setSortingEnabled(False)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter |
                                                          Qt.AlignCenter)
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setAlternatingRowColors(True)


        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT idConcepto, Refaccion.nombre, Concepto.cantidad, Refaccion.precio, importe FROM Concepto "
            "INNER JOIN Refaccion ON Refaccion.idRefaccion = Concepto.refaccion "
            "INNER JOIN Venta ON Venta.numVenta = Concepto.numVenta "
            "WHERE Venta.numVenta = :numVenta"
        )
        self.actualizarQuery()

    def actualizarQuery(self):
        numVenta = self.id
        self.query.bindValue(":numVenta", numVenta)

        self.query.exec_()
        self.modelo.setQuery(self.query)


class VentanaAgregarProducto(QMainWindow):
    def __init__(self, idPro, idVen,  parent=None):
        super(VentanaAgregarProducto, self).__init__(parent)
        loadUi("ventanas\Agregarproducto.ui", self)

        self.idPro = idPro
        self.idVen = int(idVen)
        self.agregar.clicked.connect(self.agregaP)
        self.leNombre.setPlaceholderText("Nombre de Refaccion")
        self.leCantidad.setPlaceholderText("Cantidad")
        self.lePrecio.setPlaceholderText("Precio")
        self.producto()
        self.leCantidad.setFocus()

    def agregaP(self):
        conexion = sqlite3.connect('puntoVenta.db')
        consulta = conexion.cursor()
        cantidad = int(self.leCantidad.text())
        precio = float(self.lePrecio.text())
        importe = float(cantidad * precio)
        datos = (cantidad, importe, self.idPro, self.idVen)
        sql = """INSERT INTO Concepto (cantidad, importe, refaccion, numVenta) VALUES (?,?,?,?)"""

        consulta.execute(sql, datos)
        conexion.commit()
        conexion.close()
        self.close()

    def producto(self):
        conexion = sqlite3.connect("puntoVenta.db")
        consulta = conexion.cursor()

        sql = """SELECT nombre, precio FROM Refaccion WHERE idRefaccion = ?"""
        dato = (self.idPro, )

        try:
            consulta.execute(sql, dato)
            datosDevueltos = consulta.fetchall()
            conexion.close()
            if datosDevueltos:
                for datos in datosDevueltos:
                    self.leNombre.setText(str(datos[0]))
                    self.lePrecio.setText(str(datos[1]))
        except:
            pass


class VentanaEditarCliente(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaEditarCliente, self).__init__(parent)
        loadUi('ventanas\EditarCliente.ui', self)

        self.btn.setIconSize(QSize(40, 30))
        self.btn.setIcon(QIcon('iconos/busqueda.ico'))
        self.btn.setToolTip("Buscar")
        self.btn.clicked.connect(self.buscar)

        self.btn_2.clicked.connect(self.editar)

        self.btn_3.clicked.connect(self.cancelar)

        self.le.setPlaceholderText("Id cliente")

    def buscar(self):
        self.le_2.setText("")
        self.le_4.setText("")
        id = int(self.le.text())
        datos = busqueda(id)
        self.le_2.setText(datos[0])
        self.le_4.setText(datos[1])

    def editar(self):
        id = int(self.le.text())
        nombre = self.le_2.text()
        telefono = self.le_4.text()
        editarCliente(id, nombre, telefono)
        self.hide()

    def cancelar(self):
        self.hide()


def busqueda(id):
    conexion = sqlite3.connect('puntoVenta.db')
    consulta = conexion.cursor()
    datos = ("", "")
    dato = (id, )
    sql = """SELECT nombre, telefono FROM Cliente WHERE (idCliente = ?)"""
    encontro = False
    try:
        consulta.execute(sql, dato)
        for i in consulta:
            datos = (i[0], i[1])
            encontro = True
        if encontro == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Registro no encontrado")
            msg.setWindowIcon(QIcon('iconos/m.ico'))
            msg.setWindowTitle(" ")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        return datos
    except:
        print("")
    conexion.close()


def editarCliente(id, nombre, telefono):
    conexion = sqlite3.connect('puntoVenta.db')
    consulta = conexion.cursor()
    datos = (nombre, telefono, id)
    sql = """UPDATE Cliente SET nombre = ?, telefono = ? WHERE (idCliente = ?)"""
    consulta.execute(sql, datos)
    conexion.commit()
    conexion.close()


class VentanaBorrarCliente(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaBorrarCliente, self).__init__(parent)
        loadUi('ventanas\BorrarCliente.ui', self)

        self.btn.setIconSize(QSize(40, 30))
        self.btn.setIcon(QIcon('iconos/busqueda.ico'))
        self.btn.setToolTip("Buscar")
        self.btn.clicked.connect(self.buscar)

        self.btn_2.clicked.connect(self.borrar)

        self.btn_3.clicked.connect(self.cancelar)

        self.le.setPlaceholderText("Id cliente")


    def buscar(self):
        self.le_2.setText("")
        self.le_4.setText("")
        id = self.le.text()
        datos = busqueda(id)
        self.le_2.setText(datos[0])
        self.le_4.setText(datos[1])


    def borrar(self):
        id = self.le.text()
        borrarCliente(id)
        self.hide()


    def cancelar(self):
        self.hide()


def borrarCliente(id):
    conexion = sqlite3.connect('puntoVenta.db')
    consulta = conexion.cursor()
    dato = (id, )
    sql = """DELETE FROM Cliente WHERE (idCliente = ?)"""
    consulta.execute(sql, dato)
    conexion.commit()
    conexion.close()


class VentanaEditarProducto(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaEditarProducto, self).__init__(parent)
        loadUi('ventanas\EditarProducto.ui', self)

        self.le.setPlaceholderText("Id producto")

        self.comboBox_2.addItems(["Seleccionar", "Unidades", "Metros", "Kilogramos", "Sin unidad"])

        self.btn.setIconSize(QSize(40, 30))
        self.btn.setIcon(QIcon('iconos/busqueda.ico'))
        self.btn.setToolTip("Buscar")
        self.btn.clicked.connect(self.buscar)

        #self.btn_2.clicked.connect(self.borrar)

        #self.btn_3.clicked.connect(self.cancelar)

    def buscar(self):
        self.le.setFocus()
        self.le_3.setText("")
        self.le_5.setText("")
        self.spinBox_2.setValue(0)
        count = self.comboBox_2.count()
        for i in range(count):
            text = self.comboBox_2.itemText(i)
            if text == "Seleccionar":
                break
        index = self.comboBox_2.findText(text)
        self.comboBox_2.itemText(index)
        id = self.le.text()
        datos = busqueda2(id)
        self.le_3.setText(datos[0])
        self.le_5.setText(datos[1])
        self.spinBox_2.setValue(datos[2])
        text = datos[3]
        inde = self.comboBox_2.findText(text)
        self.comboBox_2.itemText(inde)


class VentanaBorrarProducto(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaBorrarProducto, self).__init__(parent)
        loadUi('ventanas\BorrarProducto.ui', self)

        self.le.setPlaceholderText("Id producto")

        self.comboBox_2.addItems(["Seleccionar", "Unidades", "Metros", "Kilogramos", "Sin unidad"])

        self.btn.setIconSize(QSize(40, 30))
        self.btn.setIcon(QIcon('iconos/busqueda.ico'))
        self.btn.setToolTip("Buscar")
        self.btn.clicked.connect(self.buscar)

    def buscar(self):
        pass


def busqueda2(id):
    conexion = sqlite3.connect('puntoVenta.db')
    consulta = conexion.cursor()
    datos = ("", "", "", "")
    dato = (id, )
    sql = """SELECT nombre, precio, cantidad, uniMedida FROM Refaccion WHERE (idRefaccion = ?)"""
    encontro = False
    try:
        consulta.execute(sql, dato)
        for i in consulta:
            datos = (i[0], i[1], i[2], i[3])
            encontro = True
        if encontro == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Registro no encontrado")
            msg.setWindowIcon(QIcon('iconos/m.ico'))
            msg.setWindowTitle(" ")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        return datos
    except:
        print("")
    conexion.close()


app = QApplication(sys.argv)
dba = QSqlDatabase("QSQLITE")
dba.setDatabaseName("puntoVenta.db")
dba.open()
win = VentanaPrincipal()
win.show()
app.exec_()