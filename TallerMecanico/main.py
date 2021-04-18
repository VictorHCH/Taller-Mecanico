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
        self.lb.setPixmap(QPixmap("Fondo.png"))
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
            otraventana = VentanaVenta(self)
            otraventana.show()


class VentanaVenta(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaVenta, self).__init__(parent)
        loadUi('ventanas\Venta.ui', self)

        barra = QToolBar()
        barra.setIconSize(QSize(30, 30))
        self.addToolBar(barra)

        venta = QAction(QIcon("iconos/venta.ico"), "Venta", self)
        venta.triggered.connect(self.btnVenta)
        barra.addAction(venta)

        barra.addSeparator()

        cliente = QAction(QIcon("iconos/cliente.ico"), "Clientes", self)
        cliente.triggered.connect(self.btnCliente)
        barra.addAction(cliente)

        barra.addSeparator()

        inv = QAction(QIcon("iconos/inv.ico"), "Inventario", self)
        inv.triggered.connect(self.btnInv)
        barra.addAction(inv)

        barra.addSeparator()

        reg = QAction(QIcon("iconos/registro.ico"), "Registro de ventas", self)
        reg.triggered.connect(self.btnReg)
        barra.addAction(reg)

        barra.addSeparator()

        #venta nueva
        self.ventaNueva()

        self.leCliente.setPlaceholderText("Nombre del cliente")
        self.leVehiculo.setPlaceholderText("Nombre del Vehiculo")
        self.leCliente.textChanged.connect(self.actualizarQuery)

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

        self.actualizarQuery()

        # VENTANA NUEVO USUARIO
        self.btn.clicked.connect(self.btnNuevoCliente)
        self.btn.setToolTip("Agregar nuevo cliente")

        # Ventana agregar concepto
        self.btnConcepto.clicked.connect(self.agregarConcepto)
        self.btnConcepto.setToolTip("Agregar concepto")

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

    def agregarConcepto(self):
        conexion = sqlite3.connect("puntoVenta.db")
        consulta = conexion.cursor()

        sql = """SELECT MAX(numVenta) AS numVenta FROM Venta"""
        numVenta = ""
        try:
            consulta.execute(sql)
            datosDevueltos = consulta.fetchall()
            conexion.close()
            if datosDevueltos:
                for datos in datosDevueltos:
                    numVenta = datos[0]
            else:
                QMessageBox.information(self, "Buscar venta", "No se encontro "
                                                              "información.   ", QMessageBox.Ok)
        except:
            pass
        otraventana = VentanaProductos(numVenta, self)
        otraventana.show()

    def ventaNueva(self):
        conexion = sqlite3.connect('puntoVenta.db')
        consulta = conexion.cursor()
        fecha = date.today()
        f = (fecha.strftime("%Y-%m-%d"), )

        sql = """INSERT INTO Venta VALUES (NULL, ?, "", 0, 0)"""

        consulta.execute(sql, f)
        conexion.commit()
        conexion.close()

    def actualizarQuery(self):
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
            else:
                QMessageBox.information(self, "Buscar venta", "No se encontro "
                                                                "información.   ", QMessageBox.Ok)
        except:
            pass


class VentanaClientes(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaClientes, self).__init__(parent)
        loadUi('ventanas\Clientes.ui', self)

        barra = QToolBar()
        barra.setIconSize(QSize(30, 30))
        self.addToolBar(barra)

        venta = QAction(QIcon("iconos/venta.ico"), "Venta", self)
        venta.triggered.connect(self.btnVenta)
        barra.addAction(venta)

        barra.addSeparator()

        cliente = QAction(QIcon("iconos/cliente.ico"), "Clientes", self)
        cliente.triggered.connect(self.btnCliente)
        barra.addAction(cliente)

        barra.addSeparator()

        inv = QAction(QIcon("iconos/inv.ico"), "Inventario", self)
        inv.triggered.connect(self.btnInv)
        barra.addAction(inv)

        barra.addSeparator()

        reg = QAction(QIcon("iconos/registro.ico"), "Registro de ventas", self)
        reg.triggered.connect(self.btnReg)
        barra.addAction(reg)

        barra.addSeparator()

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
        self.btn.clicked.connect(self.btnNuevoCliente)
        self.btn.setToolTip("Agregar nuevo cliente")

    def btnVenta(self):
        self.hide()
        otraventana = VentanaVenta(self)
        otraventana.show()

    def btnCliente(self):
        pass

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

    def actualizarQuery(self):
        nombreCliente = self.lineEdit.text()
        self.query.bindValue(":nombreCliente", nombreCliente)

        self.query.exec_()
        self.modelo.setQuery(self.query)


class VentanaInventario(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaInventario, self).__init__(parent)
        loadUi('ventanas\Inventario.ui', self)

        barra = QToolBar()
        barra.setIconSize(QSize(30, 30))
        self.addToolBar(barra)

        venta = QAction(QIcon("iconos/venta.ico"), "Venta", self)
        venta.triggered.connect(self.btnVenta)
        barra.addAction(venta)

        barra.addSeparator()

        cliente = QAction(QIcon("iconos/cliente.ico"), "Clientes", self)
        cliente.triggered.connect(self.btnCliente)
        barra.addAction(cliente)

        barra.addSeparator()

        inv = QAction(QIcon("iconos/inv.ico"), "Inventario", self)
        inv.triggered.connect(self.btnInv)
        barra.addAction(inv)

        barra.addSeparator()

        reg = QAction(QIcon("iconos/registro.ico"), "Registro de ventas", self)
        reg.triggered.connect(self.btnReg)
        barra.addAction(reg)

        barra.addSeparator()

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

        #Pruebas

    def btnVenta(self):
        self.hide()
        otraventana = VentanaVenta(self)
        otraventana.show()

    def btnCliente(self):
        self.hide()
        otraventana = VentanaClientes(self)
        otraventana.show()

    def btnInv(self, s):
        pass

    def btnReg(self, s):
        self.hide()
        otraventana = VentanaRegistros(self)
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

        barra = QToolBar()
        barra.setIconSize(QSize(30, 30))
        self.addToolBar(barra)

        venta = QAction(QIcon("iconos/venta.ico"), "Venta", self)
        venta.triggered.connect(self.btnVenta)
        barra.addAction(venta)

        barra.addSeparator()

        cliente = QAction(QIcon("iconos/cliente.ico"), "Clientes", self)
        cliente.triggered.connect(self.btnCliente)
        barra.addAction(cliente)

        barra.addSeparator()

        inv = QAction(QIcon("iconos/inv.ico"), "Inventario", self)
        inv.triggered.connect(self.btnInv)
        barra.addAction(inv)

        barra.addSeparator()

        reg = QAction(QIcon("iconos/registro.ico"), "Registro de ventas", self)
        reg.triggered.connect(self.btnReg)
        barra.addAction(reg)

        barra.addSeparator()

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

        self.actualizarQuery()

    def detalleVenta(self):
        row = self.tableWidget.currentRow()
        item = self.tableWidget.item(row, 0)
        if item is not None:
            otraventana = VentanaDetalleRegistro(item.text(), self)
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
        print("Hola")
        pass

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
            else:
                QMessageBox.information(self, "Buscar venta", "No se encontro "
                                                              "información.   ", QMessageBox.Ok)
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
        self.hide()

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


app = QApplication(sys.argv)
dba = QSqlDatabase("QSQLITE")
dba.setDatabaseName("puntoVenta.db")
dba.open()
win = VentanaPrincipal()
win.show()
app.exec_()