import os
from .my_docx import MyDocx
from .my_data_types import Region

def createAppendix11(reg:Region, fileName:str):
    template = os.path.join(
            os.path.dirname(__file__), 'template.docx')
    docx = MyDocx(template, fileName)
    docx.doc.add_paragraph('Приложение 1. Проверка качества привязки растровых материалов ГФД', style='BoldCenter')
    for i,dis in enumerate(reg.districts):
        docx.doc.add_paragraph(f"{i+1}. {dis.farmFullName()}")
        table = docx.pntTable(dis.getPntsData4Report())
        lastRowCells = table.add_row().cells
        lastRowCells[0].text='Результат'
        lastRowCells[1].text = dis.getStatusStr()
        lastRowCells[2].merge(lastRowCells[3])
        lastRowCells[2].paragraphs[0].add_run().add_picture(dis.imgPath)
    docx.save()

def createAppendix12(reg:Region, fileName:str):
    template = os.path.join(
            os.path.dirname(__file__), 'template.docx')
    docx = MyDocx(template, fileName)
    docx.doc.add_paragraph('Таблица 1.  Проверка качества привязки растровых материалов ГФДЗ', style='TableName')
    docx.pntSumaryTable(reg.getDistrData4Report()) 
    docx.doc.add_paragraph('')
    para = f"В результате контроля качества привязки растровых материалов ГФДЗ проверено {len(reg.districts)} документов по {len(reg.districts)} муниципальным образованиям."
    docx.doc.add_paragraph(para)
    docx.doc.add_paragraph('Выявлено:')
    para = f"1) Привязка {reg.sumDistrStatus()} документов соответствует требованиям к точности. Величина отклонения не превышает максимальное установленное расхождение."
    docx.doc.add_paragraph(para)
    docx.save()

def createAppendix21(reg:Region, fileName:str):
    template = os.path.join(
            os.path.dirname(__file__), 'template.docx')
    docx = MyDocx(template, fileName)
    docx.doc.add_paragraph('Приложение 2. Проверка местоположения контуров, полученных в результате векторизации данных ГФДЗ', style='BoldCenter')
    for i,dis in enumerate(reg.distDistricts):
        docx.doc.add_paragraph(f"{i+1}. {dis.farmFullName()}")
        table = docx.distTable(dis.getDistsData4Report())
        preLastRowCells = table.add_row().cells
        preLastRowCells[0].text='Сравнение геометрии'
        lastRowCells = table.add_row().cells
        lastRowCells[0].text = f" Выявленные расхождения {dis.getStatusStr()} превышают нормативную погрешность определения координат"
        lastRowCells[1].paragraphs[0].add_run().add_picture(dis.imgPath)
        preLastRowCells[0].merge(preLastRowCells[1])
    docx.save()

def createAppendix22(reg:Region, fileName:str):
    template = os.path.join(
            os.path.dirname(__file__), 'template.docx')
    docx = MyDocx(template, fileName)
    docx.doc.add_paragraph('Таблица 2. Контроль местоположения контуров, полученных в результате векторизации данных', style='TableName')
    docx.distSumaryTable(reg.getDistData4Report()) 
    docx.doc.add_paragraph('')
    para = f"В результате контроля местоположения полученных в результате векторизации данных проверено {len(reg.distDistricts)} контуров по {len(reg.distDistricts)} муниципальным образованиям. "
    docx.doc.add_paragraph(para)
    docx.doc.add_paragraph('Выявлено:')
    para = f"Выявлено что  {len(reg.distDistricts)} контуров имеют расхождения с исходными растровыми изображениями, но величина отклонения не превышает нормативную погрешность определения координат."
    docx.doc.add_paragraph(para)
    docx.save()
