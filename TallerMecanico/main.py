import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QToolBar, QTableView, QVBoxLayout, QLineEdit, QHBoxLayout,
                             QWidget, QPushButton, QHeaderView)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon
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

        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT idConcepto, refaccion, cantidad, importe, numVenta FROM Concepto"
        )
        self.actualizarQuery()

        self.modelo.setHeaderData(0, Qt.Horizontal, "Número")

        #VENTANA NUEVO USUARIO
        self.btn.clicked.connect(self.btnNuevoCliente)

        #Ventana agregar concepto
        self.pushButton_3.clicked.connect(self.agregarConcepto)

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
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT * FROM Cliente WHERE "
            "nombre LIKE '%' || :nombreCliente || '%'"
        )
        self.actualizarQuery()

        # VENTANA NUEVO USUARIO
        self.btn.clicked.connect(self.btnNuevoCliente)

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
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT * FROM Refaccion WHERE "
            "nombre LIKE '%' || :nombreProducto || '%'"
        )
        self.actualizarQuery()

        self.modelo.setHeaderData(0, Qt.Horizontal, "Id producto")
        self.modelo.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.modelo.setHeaderData(2, Qt.Horizontal, "Precio")
        self.modelo.setHeaderData(3, Qt.Horizontal, "Cantidad")
        self.modelo.setHeaderData(4, Qt.Horizontal, "Unidad de medida")

        #Agregar producto
        self.btn_2.clicked.connect(self.agregarProducto)

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

    def cancelar(self):
        self.hide()


class VentanaProductos(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaProductos, self).__init__(parent)
        loadUi("ventanas\Productos.ui", self)

        self.lineEdit.setPlaceholderText("Nombre del producto")
        self.lineEdit.textChanged.connect(self.actualizarQuery)

        self.modelo = QSqlQueryModel()
        self.tableView.setModel(self.modelo)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setStretchLastSection(True)


        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT nombre, precio FROM Refaccion WHERE "
            "nombre LIKE '%' || :nombreProducto || '%'"
        )
        self.actualizarQuery()

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

        self.pushButton_2.clicked.connect(self.cancelar)

    def cancelar(self):
        self.hide()


app = QApplication(sys.argv)
dba = QSqlDatabase("QSQLITE")
dba.setDatabaseName("puntoVenta.db")
dba.open()
win = VentanaPrincipal()
win.show()
app.exec_()