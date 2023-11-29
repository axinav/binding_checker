

from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtSql import QSqlQueryModel
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeature, QgsGeometry, QgsProject
from qgis.gui import QgisInterface, QgsMapCanvas


class DistCheckerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None ) -> None:
        super().__init__(parent )
        self.iface=QgisInterface()
        self.regionCBox = QtWidgets.QComboBox(self)
        self.regionCBox.setGeometry(10, 10, 191, 22)
        self.regionModel = QSqlQueryModel()
        self.regionModel.setQuery('select * from regions')
        self.regionCBox.setModel(self.regionModel)
        self.regionCBox.setModelColumn(2)
        self.regionCBox.currentIndexChanged.connect(self.regionCBoxChanged)

        self.districtCBox = QtWidgets.QComboBox(self)
        self.districtCBox.setGeometry(220,10,191,22)
        self.districtModel = QSqlQueryModel()
        self.districtCBox.setModel(self.districtModel)

        self.canvas = QgsMapCanvas(self)
        self.canvas.setGeometry(10,50,400,266)
        self.canvas.setCanvasColor(Qt.white)
        self.canvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:3395"))

        self.selectPushBtn = QtWidgets.QPushButton('Select', self)
        self.selectPushBtn.setGeometry(320,180,60,22)



    def regionCBoxChanged(self, index):
        regionCn = self.regionModel.record(index).value(1)
        self.districtModel.setQuery(f'SELECT * FROM districts WHERE regionkn="{regionCn}"')
        self.districtCBox.setModelColumn(2)

    def selectFeature(self):
        crs = QgsCoordinateReferenceSystem("EPSG:3395")
        selectedFeat = self.iface.activeLayer().selectedFeatures()[0]             
        selectedGeom = selectedFeat.geometry()
        checkedGeom = QgsGeometry(selectedGeom)
        checkedGeom.transform(self.getXform3395(self.iface.activeLayer()))
        sourseGeom = QgsGeometry(selectedGeom)
        sourseGeom.transform(self.getXform3395(self.iface.activeLayer()))


    def getXform3395(self, layer):
        crsDest = QgsCoordinateReferenceSystem("EPSG:3395")
        crsSrc = layer.crs()
        xformContext = QgsProject.instance().transformContext()
        return QgsCoordinateTransform (crsSrc, crsDest, xformContext)
