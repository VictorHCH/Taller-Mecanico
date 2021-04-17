import sys
import sqlite3
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QToolBar, QTableView, QVBoxLayout, QLineEdit, QHBoxLayout,
                             QWidget, QPushButton, QHeaderView, QStyledItemDelegate, QDateEdit, QMessageBox)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QSize, Qt, QRect, QTimer, QDate
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel, QSqlDatabase, QSqlTableModel

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

        self.btn_2.setIconSize(QSize(50, 40))
        self.btn_2.setIcon(QIcon('iconos/menu.ico'))
        self.btn_2.setToolTip("Menú principal")
        self.btn.setIconSize(QSize(40, 30))
        self.btn.setIcon(QIcon('iconos/agregar.ico'))
        self.pushButton_3.setIconSize(QSize(40, 30))

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

        self.btn_2.clicked.connect(self.menuPrincipal)
        self.pushButton_2.clicked.connect(self.cancelar)

        #VENTANA NUEVO USUARIO
        self.btn.clicked.connect(self.btnNuevoCliente)
        self.btn.setToolTip("Agregar nuevo cliente")

        #Ventana agregar concepto
        self.pushButton_3.clicked.connect(self.agregarConcepto)
        self.pushButton_3.setToolTip("Agregar concepto")

    def menuPrincipal(self):
        self.hide()
        otraventana = MenuPrincipal(self)
        otraventana.show()

    def cancelar(self):
        self.hide()
        otraventana = MenuPrincipal(self)
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

        self.lineEdit.setPlaceholderText("Nombre del cliente")
        self.lineEdit.textChanged.connect(self.actualizarQuery)

        self.modelo = QSqlQueryModel()
        self.tableView.setModel(self.modelo)
        self.tableView.setWordWrap(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setFont(QFont("Franklin Gothic Book", 11, QFont.Bold))
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
        self.hide()
        otraventana = MenuPrincipal(self)
        otraventana.show()

    def btnNuevoCliente(self):
        otraventana = VentanaClienteNuevo(self)
        otraventana.show()

    def editar(self):
        otraventana = VentanaEditarCliente(self)
        otraventana.show()

    def borrar(self):
        otraventana = VentanaBorrarCliente(self)
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
        self.tableView.horizontalHeader().setFont(QFont("Franklin Gothic Book", 11, QFont.Bold))
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

    def menuPrincipal(self):
        self.hide()
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
        self.lineEdit.textChanged.connect(self.actualizarQuery1)
        self.dateEdit.dateChanged.connect(self.actualizarQuery1)
        self.btnDetalle.clicked.connect(self.actualizarQuery2)

        self.modelo1 = QSqlQueryModel()
        self.modelo2 = QSqlQueryModel()
        self.tableView.setModel(self.modelo1)
        self.tableView_2.setModel(self.modelo2)
        self.tableView.setWordWrap(True)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_2.setWordWrap(True)
        self.tableView_2.horizontalHeader().setStretchLastSection(True)
        self.tableView_2.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.query1 = QSqlQuery(db=dba)

        self.query1.prepare(
            "SELECT Venta.numVenta, nombre, Venta.vehiculo, Venta.fecha, Venta.total FROM Cliente "
            "INNER JOIN Venta ON Venta.cliente = Cliente.idCliente "
            "WHERE Cliente.nombre LIKE '%' || :nombreCliente || '%' AND "
            "Venta.fecha LIKE '%' || :fechaVenta || '%'"
        )
        self.actualizarQuery1()

        self.query2 = QSqlQuery(db=dba)

        self.query2.prepare(
            "SELECT idConcepto, Refaccion.nombre, Concepto.cantidad, Refaccion.precio, importe FROM Concepto "
            "INNER JOIN Refaccion ON Refaccion.idRefaccion = Concepto.refaccion "
            "INNER JOIN Venta ON Venta.numVenta = Concepto.numVenta "
            "WHERE Venta.numVenta = :numVenta"
        )

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

    def actualizarQuery1(self):
        nombreCliente = self.lineEdit.text()
        fechaVenta = self.dateEdit.text()
        self.query1.bindValue(":nombreCliente", nombreCliente)
        self.query1.bindValue(":fechaVenta", fechaVenta)

        self.query1.exec_()
        self.modelo1.setQuery(self.query1)

    def actualizarQuery2(self):
        numVenta = self.detalles.text()
        self.query2.bindValue(":numVenta", numVenta)

        self.query2.exec_()
        self.modelo2.setQuery(self.query2)


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
            "SELECT idRefaccion, nombre, precio FROM Refaccion WHERE "
            "nombre LIKE '%' || :nombreProducto || '%'"
        )
        self.actualizarQuery()

        delegateFloat = InitialDelegate(2, self.tableView)
        self.tableView.setItemDelegateForColumn(1, delegateFloat)
        self.modelo.setHeaderData(0, Qt.Horizontal, "Nombre")
        self.modelo.setHeaderData(1, Qt.Horizontal, "Precio")
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        #self.tableView.hideColumn(0)
        #self.btnAgregar.clicked.connect(self.agregaProducto)

    def agregaProducto(self):
        pass


    def actualizarQuery(self):
        nombreProducto = self.lineEdit.text()
        self.query.bindValue(":nombreProducto", nombreProducto)

        self.query.exec_()
        self.modelo.setQuery(self.query)


class VentanaRegistroProducto(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaRegistroProducto, self).__init__(parent)
        loadUi("ventanas\Registros.ui", self)

        self.comboBox.addItems(["Seleccionar", "Unidades", "Metros", "Kilogramos", "Sin unidad"])

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
        id = self.le.text()
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
    sql = """SELECT nombre, telefono FROM Cliente WHERE (idCliente = ?)"""
    encontro = False
    try:
        consulta.execute(sql, id)
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

    sql = """DELETE FROM Cliente WHERE (idCliente = ?)"""
    consulta.execute(sql, id)
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
    sql = """SELECT nombre, precio, cantidad, uniMedida FROM Refaccion WHERE (idRefaccion = ?)"""
    encontro = False
    try:
        consulta.execute(sql, id)
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