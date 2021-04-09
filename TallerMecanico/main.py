import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QTableView, QVBoxLayout, QLineEdit, QHBoxLayout, QWidget, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel, QSqlDatabase, QSqlTableModel


class VentanaPrincipal(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaPrincipal, self).__init__(parent)
        loadUi('Inicio.ui', self)
        self.btn.clicked.connect(self.VentanaVenta)
        self.lb.setPixmap(QPixmap("Fondo.png"))
        self.lb.setScaledContents(True)

    def VentanaVenta(self):
        self.hide()
        otraventana = VentanaVenta(self)
        otraventana.show()


class VentanaVenta(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaVenta, self).__init__(parent)
        loadUi('Venta.ui', self)

        barra = QToolBar()
        barra.setIconSize(QSize(30, 30))
        self.addToolBar(barra)

        venta = QAction(QIcon("venta.ico"), "Venta", self)
        venta.triggered.connect(self.btnVenta)
        barra.addAction(venta)

        barra.addSeparator()

        cliente = QAction(QIcon("cliente.ico"), "Clientes", self)
        cliente.triggered.connect(self.btnCliente)
        barra.addAction(cliente)

        barra.addSeparator()

        inv = QAction(QIcon("inv.ico"), "Inventario", self)
        inv.triggered.connect(self.btnInv)
        barra.addAction(inv)

        barra.addSeparator()

        reg = QAction(QIcon("registro.ico"), "Registro de ventas", self)
        reg.triggered.connect(self.btnReg)
        barra.addAction(reg)

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


class VentanaClientes(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaClientes, self).__init__(parent)
        loadUi('Clientes.ui', self)

        barra = QToolBar()
        barra.setIconSize(QSize(30, 30))
        self.addToolBar(barra)

        venta = QAction(QIcon("venta.ico"), "Venta", self)
        venta.triggered.connect(self.btnVenta)
        barra.addAction(venta)

        barra.addSeparator()

        cliente = QAction(QIcon("cliente.ico"), "Clientes", self)
        cliente.triggered.connect(self.btnCliente)
        barra.addAction(cliente)

        barra.addSeparator()

        inv = QAction(QIcon("inv.ico"), "Inventario", self)
        inv.triggered.connect(self.btnInv)
        barra.addAction(inv)

        barra.addSeparator()

        reg = QAction(QIcon("registro.ico"), "Registro de ventas", self)
        reg.triggered.connect(self.btnReg)
        barra.addAction(reg)

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


class VentanaInventario(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaInventario, self).__init__(parent)
        #loadUi('Inventario.ui', self)
        widget = QWidget()
        lay1 = QVBoxLayout()
        lay2 = QHBoxLayout()

        self.nombreProducto = QLineEdit()
        self.nombreProducto.setPlaceholderText("Nombre del Producto")
        self.nombreProducto.textChanged.connect(self.actualizarQuery)

        self.btn = QPushButton("+")

        lay2.addWidget(self.nombreProducto)
        lay2.addWidget(self.btn)
        lay1.addLayout(lay2)

        self.tabla = QTableView()

        lay1.addWidget(self.tabla)
        widget.setLayout(lay1)
        widget.setLayout(lay2)

        self.modelo = QSqlQueryModel()
        self.tabla.setModel(self.modelo)

        self.query = QSqlQuery(db=dba)

        self.query.prepare(
            "SELECT pista.nombre, compositor, album.nombre FROM pista "
            "INNER JOIN album ON pista.idAlbum_Album = album.idAlbum WHERE "
            "pista.compositor LIKE '%' || :pista_nombreProducto || '%'"
        )
        self.actualizarQuery()

        self.setMinimumSize(QSize(800, 600))
        self.setCentralWidget(widget)

        barra = QToolBar()
        barra.setIconSize(QSize(30, 30))
        self.addToolBar(barra)

        venta = QAction(QIcon("venta.ico"), "Venta", self)
        venta.triggered.connect(self.btnVenta)
        barra.addAction(venta)

        barra.addSeparator()

        cliente = QAction(QIcon("cliente.ico"), "Clientes", self)
        cliente.triggered.connect(self.btnCliente)
        barra.addAction(cliente)

        barra.addSeparator()

        inv = QAction(QIcon("inv.ico"), "Inventario", self)
        inv.triggered.connect(self.btnInv)
        barra.addAction(inv)

        barra.addSeparator()

        reg = QAction(QIcon("registro.ico"), "Registro de ventas", self)
        reg.triggered.connect(self.btnReg)
        barra.addAction(reg)

        #Agregar producto
        self.btn.clicked.connect(self.agregarProducto)

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
        pista_nombreProducto = self.nombreProducto .text()
        self.query.bindValue(":pista_nombreProducto", pista_nombreProducto)

        self.query.exec_()
        self.modelo.setQuery(self.query)


class VentanaRegistros(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaRegistros, self).__init__(parent)
        loadUi('RegistroVentas.ui', self)

        barra = QToolBar()
        barra.setIconSize(QSize(30, 30))
        self.addToolBar(barra)

        venta = QAction(QIcon("venta.ico"), "Venta", self)
        venta.triggered.connect(self.btnVenta)
        barra.addAction(venta)

        barra.addSeparator()

        cliente = QAction(QIcon("cliente.ico"), "Clientes", self)
        cliente.triggered.connect(self.btnCliente)
        barra.addAction(cliente)

        barra.addSeparator()

        inv = QAction(QIcon("inv.ico"), "Inventario", self)
        inv.triggered.connect(self.btnInv)
        barra.addAction(inv)

        barra.addSeparator()

        reg = QAction(QIcon("registro.ico"), "Registro de ventas", self)
        reg.triggered.connect(self.btnReg)
        barra.addAction(reg)

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


class VentanaClienteNuevo(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaClienteNuevo, self).__init__(parent)
        loadUi("ClienteNuevo.ui", self)


class VentanaProductos(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaProductos, self).__init__(parent)
        loadUi("Productos.ui", self)


class VentanaRegistroProducto(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaRegistroProducto, self).__init__(parent)
        loadUi("Registros.ui", self)


app = QApplication(sys.argv)
dba = QSqlDatabase("QSQLITE")
dba.setDatabaseName("canciones.db")
dba.open()
win = VentanaPrincipal()
win.show()
app.exec_()