import sys
import sqlite3
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QToolBar, QTableView, QVBoxLayout, QLineEdit, QHBoxLayout,
                             QWidget, QPushButton, QHeaderView, QStyledItemDelegate)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QSize, Qt, QRect, QTimer
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel, QSqlDatabase, QSqlTableModel


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

        self.modelo = QSqlQueryModel()
        self.tableView.setModel(self.modelo)
        self.tableView.setWordWrap(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setFont(QFont("ITC Avant Garde Std Bk Cn", 10, QFont.Bold))
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT idConcepto, refaccion, cantidad, importe, numVenta FROM Concepto"
        )
        self.actualizarQuery()

        self.modelo.setHeaderData(0, Qt.Horizontal, "#")
        self.modelo.setHeaderData(1, Qt.Horizontal, "Concepto")
        self.modelo.setHeaderData(2, Qt.Horizontal, "Cantidad")
        self.modelo.setHeaderData(3, Qt.Horizontal, "Importe")
        self.modelo.removeColumn(4)

        #VENTANA NUEVO USUARIO
        self.btn.clicked.connect(self.btnNuevoCliente)
        self.btn.setToolTip("Agregar nuevo cliente")

        #Ventana agregar concepto
        self.pushButton_3.clicked.connect(self.agregarConcepto)
        self.pushButton_3.setToolTip("Agregar concepto")

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
        otraventana = VentanaProductos(self)
        otraventana.show()

    def actualizarQuery(self):
        self.query.exec_()
        self.modelo.setQuery(self.query)


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

        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT * FROM Cliente WHERE "
            "nombre LIKE '%' || :nombreCliente || '%'"
        )
        self.actualizarQuery()

        self.modelo.setHeaderData(0, Qt.Horizontal, "#")
        self.modelo.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.modelo.setHeaderData(2, Qt.Horizontal, "Teléfono")

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

        #fechas = self.lineEdit_2.date()

        self.lineEdit.setPlaceholderText("Nombre del cliente")
        self.lineEdit_2.setPlaceholderText("Fecha")
        self.lineEdit.textChanged.connect(self.actualizarQuery)

        self.modelo = QSqlQueryModel()
        self.tableView.setModel(self.modelo)
        self.tableView.setWordWrap(True)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT * FROM Venta WHERE "
            "rfc LIKE '%' || :nombreCliente || '%' AND "
            "fecha LIKE '%' || :fecha || '%'"
        )
        self.actualizarQuery()

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
        nombreCliente = self.lineEdit.text()
        self.query.bindValue(":nombreCliente", nombreCliente)

        fecha = self.lineEdit_2.text()
        self.query.bindValue(":fecha", fecha)

        self.query.exec_()
        self.modelo.setQuery(self.query)


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
    def __init__(self, parent=None):
        super(VentanaProductos, self).__init__(parent)
        loadUi("ventanas\Productos.ui", self)

        self.lineEdit.setPlaceholderText("Nombre del producto")
        self.lineEdit.textChanged.connect(self.actualizarQuery)

        self.modelo = QSqlQueryModel()
        self.tableView.setModel(self.modelo)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setFont(QFont("ITC Avant Garde Std Bk Cn", 10, QFont.Bold))
        self.tableView.horizontalHeader().setStretchLastSection(True)


        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT nombre, precio FROM Refaccion WHERE "
            "nombre LIKE '%' || :nombreProducto || '%'"
        )
        self.actualizarQuery()

        delegateFloat = InitialDelegate(2, self.tableView)
        self.tableView.setItemDelegateForColumn(1, delegateFloat)
        self.modelo.setHeaderData(0, Qt.Horizontal, "Nombre")
        self.modelo.setHeaderData(1, Qt.Horizontal, "Precio")


    def actualizarQuery(self):
        nombreProducto = self.lineEdit.text()
        self.query.bindValue(":nombreProducto", nombreProducto)

        self.query.exec_()
        self.modelo.setQuery(self.query)


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


app = QApplication(sys.argv)
dba = QSqlDatabase("QSQLITE")
dba.setDatabaseName("puntoVenta.db")
dba.open()
win = VentanaPrincipal()
win.show()
app.exec_()