from dataclasses import dataclass

from qgis.PyQt.QtSql import QSqlQuery, QSqlRecord

@dataclass
class Pic:
    path: str


class Pnt:
    def __init__(self, rec: QSqlRecord) -> None:
        self.name = rec.value('nomer')
        self.statusCode = int(rec.value('status'))
        self.rastrImgPath = rec.value('picr')
        self.googleImgPath = rec.value('picg')
        self.statusCodeConvert()
        
    def statusCodeConvert(self):
        if self.statusCode == 1:
            self.statusStr = 'Совпадает'
        else:
            self.statusStr = 'Не совпадает'

    def __lt__(self, other):
        return self.name<other.name

    def __gt__(self, other):
        return self.name>other.name

    def __add__(self, other):
        return self.statusCode+other.statusCode

class Dist:
    def __init__(self, rec: QSqlRecord) -> None:
        self.name = rec.value('nomer')
        self.dist = rec.value('dist')
        

    def __lt__(self, other):
        return self.name<other.name

    def __gt__(self, other):
        return self.name>other.name

    def __add__(self, other):
        return self.statusCode+other.statusCode

class Distr:
    def __init__(self, rec: QSqlRecord) -> None:
        self.shortName = rec.value('name')
        self.region = rec.value('regionname')
        self.imgPath = rec.value('picname')
        self.farmname = rec.value('farmname')
        self.id = rec.value('id')
        self.setPntLst()
        self.setStatus()

    def __add__(self, other):
        return self.status + other.status

    def fullName(self):
        return self.shortName + ' район'

    def farmFullName (self):
        return f'{self.farmname}, {self.region}, {self.fullName()}'

    def setPntLst(self):
        self.pnts =[]
        query = QSqlQuery(f"SELECT * FROM points WHERE districtid = {self.id}")
        while query.next():
            self.pnts.append(Pnt(query.record()))

    def sumPntStatus (self):
        sum = 0
        for pnt in self.pnts:
            sum += pnt.statusCode
        return sum

    def setStatus(self):
        if self.sumPntStatus()>(len(self.pnts)/2):
            self.status =1
        else:
            self.status = 0

    def getStatusStr(self):
        if self.status == 1:
            return 'Совпадает'
        else:
            return 'Не совпадает'

    def getPntsData4Report(self):
        data = []
        for pnt in self.pnts:
            data.append([pnt.name, pnt.statusStr,
                         pnt.rastrImgPath, pnt.googleImgPath])
        return data    

class DistrDist:
    def __init__(self, rec: QSqlRecord) -> None:
        self.shortName = rec.value('name')
        self.region = rec.value('regionname')
        self.imgPath = rec.value('picname')
        self.farmname = rec.value('farmname')
        self.id = rec.value('id')
        self.setDistLst()
        self.status = self.setStatus()

    def __add__(self, other):
        return self.status + other.status

    def fullName(self):
        return self.shortName + ' район'

    def farmFullName (self):
        return f'{self.farmname}, {self.region}, {self.fullName()}'

    def setDistLst(self):
        self.dists =[]
        query = QSqlQuery(f"SELECT * FROM distances WHERE districtid = {self.id}")
        while query.next():
            self.dists.append(Dist(query.record()))

    def sumDists (self):
        sum = 0
        for dist in self.dists:
            sum += float(dist.dist)
        return sum

    def setStatus(self):
        return int((self.sumDists/len(self.dists))<=12)

    def getStatusStr(self):
        if self.status == 1:
            return 'Совпадает'
        else:
            return 'Не совпадает'

    def getDistsData4Report(self):
        data = []
        for dist in self.dists:
            data.append([dist.name, dist.dist])
        return data    

class Region:
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        self.distDistricts=self.setDistDistrs() 
        self.setDistrst()

    def setDistDistrs(self):
        distDistricts =[]
        query = QSqlQuery(f"SELECT * FROM checkdistdistricts WHERE regionid = {self.id}")
        while query.next():
            distDistricts.append(DistrDist(query.record()))
        return distDistricts

    def setDistrst(self):
        self.districts =[]
        query = QSqlQuery(f"SELECT * FROM checkeddistricts WHERE regionid = {self.id}")
        while query.next():
            self.districts.append(Distr(query.record()))

    def sumDistStatus(self):
        sum = 0
        for dis in self.distDistricts:
            sum += dis.status
        return sum
    def sumDistrStatus(self):
        sum = 0
        for dis in self.districts:
            sum += dis.status
        return sum

    def getDistData4Report(self):
        data =[]
        i =1
        for dis in self.distDistricts:
            data.append([str(i), dis.fullName(), dis.farmname, dis.getStatusStr()])
            i+=1
        return data    
    def getDistrData4Report(self):
        data =[]
        i =1
        for dis in self.districts:
            data.append([str(i), dis.fullName(), dis.farmname, dis.getStatusStr()])
            i+=1
        return data    
