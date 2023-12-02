

from pathlib import Path
from typing import Any
from qgis.PyQt import QtGui, QtWidgets
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.PyQt.QtSql import QSqlQuery, QSqlQueryModel
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeature, QgsField, QgsGeometry, QgsPalLayerSettings, QgsProject, QgsVectorLayer, QgsVectorLayerSimpleLabeling
from qgis.gui import QgisInterface, QgsMapCanvas

from get_unique_pnts import getUniquePnts


class DistCheckerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None ) -> None:
        super().__init__(parent )
        self.iface=QgisInterface()
        self.projectDir = QgsProject.instance().homePath()
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

        self.rastrLayerCB = QgsMapLayerComboBox(self)
        self.rastrLayerCB.setGeometry(10,30,191,22)
        self.rastrLayerCB.setFilters(QgsMapLayerProxyModel.Filter.RasterLayer)

        self.canvas = QgsMapCanvas(self)
        self.canvas.setGeometry(10,60,400,266)
        self.canvas.setCanvasColor(Qt.white)
        self.canvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:3395"))

        self.preparePushBtn = QtWidgets.QPushButton('Prepare', self)
        self.preparePushBtn.setGeometry(180,350,60,22)
        self.preparePushBtn.clicked.connect(self.prepareLayers)



    def regionCBoxChanged(self, index):
        regionCn = self.regionModel.record(index).value(1)
        self.districtModel.setQuery(f'SELECT * FROM districts WHERE regionkn="{regionCn}"')
        self.districtCBox.setModelColumn(2)

    def prepareLayers(self):
        crs = QgsCoordinateReferenceSystem("EPSG:3395")
        selectedFeat = self.iface.activeLayer().selectedFeatures()[0]             
        fields = selectedFeat.fields()
        farmName = selectedFeat.attributes()[1]
        selectedGeom = selectedFeat.geometry()
        checkedGeom = QgsGeometry(selectedGeom)
        checkedGeom.transform(self.getXform3395(self.iface.activeLayer()))
        sourseGeom = QgsGeometry(selectedGeom)
        sourseGeom.transform(self.getXform3395(self.iface.activeLayer()))
        params = {
                "uri": "Polygon?crs=epsg:3395&field=name:string(50)",
                "layerName": farmName,
                "geom": [sourseGeom],
                "attr": [[farmName]]
                }
        self.sourceLayer = self.createMemLayer(**params)
        params["layerName"] = f"{farmName}_checked"
        params["geom"] = [checkedGeom]
        self.checkedLayer = self.createMemLayer(**params)

        pntsLst = getUniquePnts(sourseGeom)
        numbers = [[i] for i in range(1, len(pntsLst)+1)]
        params = {
                "uri": "Point?crs=epsg:3395&field=name:integer",
                "layerName": f"{farmName}_pnts",
                "geom": pntsLst,
                "attr": numbers
                }
        self.pntLayer = self.createMemLayer(**params)
        pal = QgsPalLayerSettings()
        pal.fieldName = 'name'
        pal.enabled = True
        self.pntLayer.setLabelsEnabled(True)
        self.pntLayer.setLabeling(QgsVectorLayerSimpleLabeling(pal))
        QgsProject.instance().addMapLayer(self.checkedLayer)
        self.canvas.setLayers([self.rastrLayerCB.currentLayer(),
                               self.sourceLayer, self.pntLayer])
        extentRestangle = sourseGeom.boundingBox().buffered(50)
        self.canvas.setExtent(extentRestangle)

    def createMemLayer(self, uri:str="", layerName:str="",
                       geom:list[QgsGeometry]=[QgsGeometry()],attr:list[list[Any,...]]=[]):
        sourceLayer = QgsVectorLayer(uri, layerName, "memory" )
        feats = []
        for i,geo in enumerate(geom):
            feat = QgsFeature()
            feat.setGeometry(geo)
            feat.setAttributes(attr[i])
            feats.append(feat)
        sourceLayer.dataProvider().addFeatures(feats)
        sourceLayer.updateExtents()
        return sourceLayer


    def getDistMap(self):
        sourceGeom = self.sourceLayer.getFeatures()[0].geometry()
        checkedGeom = self.checkedLayer.getFeatures()[0].geometry()
        distDict = {}
        for i, pnt in enumerate(sourceGeom.vertices()):
            distDict[i+1] = pnt.distance(checkedGeom.vertexAt(i))
        return distDict

    def addDataToDB(self):
        distMap = self.getDistMap()
        districtid = self.districtModel.record(self.districtCBox.currentIndex()).value(0)
        query = QSqlQuery()
        queryStr = """INSERT INTO distances
        ( nomer, dist, districtid)
        VALUES (:name, :dist, :districtid)"""
        query.prepare(queryStr)
        for key in distMap.keys():
            query.bindValue(':nomer',key)
            query.bindValue(':dist', str(round(distMap[key],2)))
            query.bindValue(':distictid',districtid)
            query.exec_()
        picName = f"{self.rastrLayerCB.currentText()}_dist.png"
        picPath = str(Path(self.projectDir)/'Pic'/picName)
        id = self.districtModel.record(self.districtCBox.currentIndex()).value(0)
        name = self.districtModel.record(self.districtCBox.currentIndex()).value(2)
        regionname = self.regionModel.record(self.regionCBox.currentIndex()).value(2)
        farmname=  self.sourceLayer.getFeatures()[0].attributes()[0]
        query = QSqlQuery()
        queryStr = """INSERT INTO checkdistdistricts
        (id, name, regionid, regionname, picname,farmname)
        VALUES (:id, :name, :regionid, :regionname, :picname, :farmname)"""
        query.prepare(queryStr)
        query.bindValue(':id', id)
        query.bindValue(':name', name)
        query.bindValue(':regionid', regionid)
        query.bindValue(':regionname', regionname)
        query.bindValue(':picname', picPath)
        query.bindValue(':farmname', farmname)
        query.exec_()
        self.saveImage(self.canvas, picPath)

    def saveImage(self, canvas, filename):
        pixmap = QtGui.QPixmap(400,260)
        canvas.saveAsImage(filename, pixmap, 'png')

    def getXform3395(self, layer):
        crsDest = QgsCoordinateReferenceSystem("EPSG:3395")
        crsSrc = layer.crs()
        xformContext = QgsProject.instance().transformContext()
        return QgsCoordinateTransform (crsSrc, crsDest, xformContext)
