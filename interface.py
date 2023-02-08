from PySimpleGUI import PySimpleGUI as sg
from pathlib import Path
from zipfile import ZipFile
import os
from os.path import basename
from shutil import rmtree
root = Path().absolute()
ap = '"'
chi = '{'
chf = '}'
sg.theme('Reddit')

layout = [
    [sg.Text('Widget Name: '), sg.Input(key='widgetName')],
    [sg.Text('Extension ID: '), sg.Input(key='extensionId')],
    [sg.Text('Elements: '), sg.Input(key='elements')],
    [sg.Text('/Os elements devem ser separados apenas por espaço/')],
    [sg.Text('Date (yyyy-mm-dd): '), sg.Input(key='date')],
    [sg.Button('Gerar arquivo')],
]

screen = sg.Window('Gerador de arquivo zip para upload no OCC', layout)

def returnExtJsonContent(extensionID, widgetName, date):
    return f"{chi}\n  {ap}createdBy{ap}: {ap}Compasso{ap},\n  {ap}developerID{ap}: {ap}compasso{ap},\n  {ap}extensionID{ap}: {ap}{extensionID}{ap},\n  {ap}translations{ap}: [\n    {chi}\n      {ap}language{ap}: {ap}en{ap},\n      {ap}name{ap}: {ap}{widgetName}{ap},\n      {ap}description{ap}: {ap}{widgetName}{ap}\n    {chf},\n   {chi}\n      {ap}language{ap}: {ap}pt_BR{ap},\n      {ap}name{ap}: {ap}{widgetName}{ap},\n      {ap}description{ap}: {ap}{widgetName}{ap}\n    {chf},\n  ],\n  {ap}timeCreated{ap}: {ap}{date}{ap},\n  {ap}version{ap}: 1\n{chf}"

def returnWidgetJsonContent(widgetName):
    return f"{chi}\n  {ap}config{ap}: {chi}\n	{ap}defaultPropertyExample{ap}: {ap}{widgetName}{ap}\n  {chf},\n  {ap}defaultLayout{ap}: {ap}{widgetName}{ap},\n  {ap}availableToAllPages{ap}: true,\n  {ap}globalEnabled{ap}: true,\n  {ap}i18nresources{ap}: {ap}{widgetName}{ap},\n  {ap}imports{ap}: [],\n  {ap}javascript{ap}: {ap}{widgetName}{ap},\n  {ap}jsEditable{ap}: true,\n  {ap}minWidth{ap}: 1,\n  {ap}translations{ap}: [{chi}\n    {ap}language{ap}: {ap}en{ap},\n    {ap}name{ap}: {ap}{widgetName}{ap}\n  {chf},\n  {chi}\n    {ap}language{ap}: {ap}pt_BR{ap},\n    {ap}name{ap}: {ap}{widgetName}{ap}\n  {chf}],\n  {ap}version{ap}: 1,\n  {ap}widgetFamily{ap}: {ap}{widgetName}{ap},\n  {ap}widgetType{ap}: {ap}{widgetName}{ap}\n{chf}"

def returnConfigJsonContent(widgetName):
    return f"{chi}\n  {ap}widgetDescriptorName{ap}: {ap}{widgetName}{ap},\n  {ap}properties{ap}: []\n{chf}"

def returnLocalesConfigContent():
    return f"{chi}\n  {ap}resources{ap}: {chi}{chf}\n{chf}"

def returnElementTemplateContent():
    return f"<h2 data-bind={ap}widgetLocaleText : '_comment'{ap}></h2>"

def returnElementJsonContent(widgetName, elementName):
    return f"{chi}\n  {ap}availableToAllWidgets{ap}: false,\n  {ap}configOptions{ap}: [],\n  {ap}global{ap}: false,\n  {ap}inline{ap}: false,\n  {ap}supportedWidgetType{ap}: [{ap}{widgetName}{ap}],\n  {ap}tag{ap}: {ap}{elementName}{ap},\n  {ap}translations{ap}: [\n    {chi}\n      {ap}description{ap}: {ap}{elementName}{ap},\n      {ap}language{ap}: {ap}pt_BR{ap},\n      {ap}title{ap}: {ap}{elementName}{ap}\n    {chf},\n    {chi}\n      {ap}description{ap}: {ap}{elementName}{ap},\n      {ap}language{ap}: {ap}en{ap},\n      {ap}title{ap}: {ap}{elementName}{ap}\n    {chf}\n  ],\n  {ap}type{ap}: {ap}fragment{ap},\n  {ap}version{ap}: 1\n{chf}"

def returnJsContent():
    return f"define(\n    [],\n\n    function () {chi}\n\n        {ap}use strict{ap};\n\n        return {chi}\n\n        {chf};\n    {chf}\n);"

def returnDisplayTemplateContent():
    return f"<h1>Hello World!</h1>"

def returnWidgetLessContent():
    return f"h1 {chi}\n    color: #0572ce;\n{chf}"

def returnLocalesContent():
    return f"{chi}\n  {ap}resources{ap}: {chi}\n	  {ap}_comment{ap}: {ap}Field example used in the application and translated into en{ap}\n  {chf}\n{chf}"

while True:
    event, values = screen.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Gerar arquivo':
        if values['widgetName'] == '':
            values['widgetName'] = 'Nome inválido'
        elif values['extensionId'] == '':
            values['extensionId'] = 'Extension ID inválida'
        elif values['date'] == '':
            values['date'] = 'Data inválida'
        else:
            widgetName = values['widgetName']
            extensionId = values['extensionId']
            elementsNames = values['elements']
            date = values['date']
            print(widgetName)
            print(extensionId)
            print(elementsNames)
            print(date)
            print(root)

            #cria a pasta widget
            widgetDir = root / 'widget'
            widgetDir.mkdir()
            #cria o ext.json
            extFile = root / 'ext.json'
            extFile.touch()
            extFile.write_text(returnExtJsonContent(extensionId, widgetName, date))
            #cria pasta com nome do widget
            widgetNameDir = widgetDir / widgetName
            widgetNameDir.mkdir()

            #cria arquivo widget.json
            widgetFile = widgetNameDir / 'widget.json'
            widgetFile.touch()
            widgetFile.write_text(returnWidgetJsonContent(widgetName))

            #cria a pasta config
            configDir = widgetNameDir / 'config'
            configDir.mkdir()
            #cria o config.json
            configFile = configDir / 'config.json'
            configFile.touch()
            configFile.write_text(returnConfigJsonContent(widgetName))
            #cria a pasta locales do config
            localesConfigDir = configDir / 'locales'
            localesConfigDir.mkdir()
            #cria o config/locales/en.json
            enLocalesConfigFile = localesConfigDir / 'en.json'
            enLocalesConfigFile.touch()
            enLocalesConfigFile.write_text(returnLocalesConfigContent())
            #cria o config/locales/pt-BR.json
            ptbrLocalesConfigFile = localesConfigDir / 'pt-BR.json'
            ptbrLocalesConfigFile.touch()
            ptbrLocalesConfigFile.write_text(returnLocalesConfigContent())
            
            #cria a pasta element
            elementDir = widgetNameDir / 'element'
            elementDir.mkdir()

            if elementsNames != '':
                arrayElementsNames = elementsNames.split()
                for i in range(len(arrayElementsNames)):
                    #cria pasta do element
                    elementIndexDir = elementDir / arrayElementsNames[i]
                    elementIndexDir.mkdir()
                    #cria arquivo element.json
                    jsonElementIndexFile = elementIndexDir / 'element.json'
                    jsonElementIndexFile.touch()
                    jsonElementIndexFile.write_text(returnElementJsonContent(widgetName, arrayElementsNames[i]))

                    #cria pasta js do element
                    jsElementIndexDir = elementIndexDir / 'js'
                    jsElementIndexDir.mkdir()
                    #cria arquivo js do element
                    jsElementIndexFile = jsElementIndexDir / 'element.js'
                    jsElementIndexFile.touch()
                    jsElementIndexFile.write_text(returnJsContent())

                    #cria pasta templates do element
                    templateElementIndexDir = elementIndexDir / 'templates'
                    templateElementIndexDir.mkdir()
                    #cria arquivo template do element
                    templateElementIndexFile = templateElementIndexDir / 'template.txt'
                    templateElementIndexFile.touch()
                    templateElementIndexFile.write_text(returnElementTemplateContent())

            #cria a pasta images
            imagesDir = widgetNameDir / 'images'
            imagesDir.mkdir()

            #cria a pasta js
            jsDir = widgetNameDir / 'js'
            jsDir.mkdir()
            #cria arquivo js principal
            jsName = widgetName + '.js'
            jsFile = jsDir / jsName
            jsFile.touch()
            jsFile.write_text(returnJsContent())

            #cria a pasta layouts
            layoutsDir = widgetNameDir / 'layouts'
            layoutsDir.mkdir()
            #cria a pasta com o nome do widget dentro dos layouts
            layoutWidgetNameDir = layoutsDir / widgetName
            layoutWidgetNameDir.mkdir()
            #cria o arquivo template do layout
            layoutTemplateFile = layoutWidgetNameDir / 'widget.template'
            layoutTemplateFile.touch()
            layoutTemplateFile.write_text(returnDisplayTemplateContent())

            #cria a pasta less
            lessDir = widgetNameDir / 'less'
            lessDir.mkdir()
            #cria o arquivo template do layout
            widgetLessFile = lessDir / 'widget.less'
            widgetLessFile.touch()
            widgetLessFile.write_text(returnWidgetLessContent())

            #cria a pasta locales
            localesDir = widgetNameDir / 'locales'
            localesDir.mkdir()
            #cria a pasta en do locales
            enLocalesDir = localesDir / 'en'
            enLocalesDir.mkdir()
            #cria o arquivo en do locales
            enLocalesName = 'ns.' + widgetName + '.json'
            enLocalesFile = enLocalesDir / enLocalesName
            enLocalesFile.touch()
            enLocalesFile.write_text(returnLocalesContent())
            #cria a pasta pt-BR do locales
            ptbrLocalesDir = localesDir / 'pt-BR'
            ptbrLocalesDir.mkdir()
            #cria o arquivo pt-BR do locales
            ptbrLocalesName = 'ns.' + widgetName + '.json'
            ptbrLocalesFile = ptbrLocalesDir / ptbrLocalesName
            ptbrLocalesFile.touch()
            ptbrLocalesFile.write_text(returnLocalesContent())
            
            #cria a pasta templates
            templatesDir = widgetNameDir / 'templates'
            templatesDir.mkdir()
            #cria o arquivo display.template dos templates
            displayTemplateFile = templatesDir / 'display.template'
            displayTemplateFile.touch()
            displayTemplateFile.write_text(returnDisplayTemplateContent())
            
            with ZipFile(f"{widgetName}.zip", "w") as zip:
                
                zip.mkdir("widget")
                zip.write("ext.json")
            
            # rmtree(widgetDir)
            # extFile.unlink()