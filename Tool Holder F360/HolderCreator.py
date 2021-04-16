#Author-George.
#Description-draw tools.

import adsk.core, adsk.fusion, traceback, math, time, tempfile, adsk.cam, os, sys, json, random
import tkinter as tk
from tkinter import filedialog

app = adsk.core.Application.get()
ui  = app.userInterface

def createHolder():  
    ui = app.userInterface

    if (not ui.activeWorkspace.id == "FusionSolidEnvironment"):
        modelWS = ui.workspaces.itemById("FusionSolidEnvironment")
        modelWS.activate()    
            
    doc = app.activeDocument
    
    products = doc.products
    design = adsk.fusion.Design.cast(products.itemByProductType("DesignProductType"))
    rootComp = design.rootComponent

    if not design:
        ui.messageBox('It is not supported in current workspace, please change to MODEL workspace and try again.')
        return
    
    sel = app.userInterface.selectEntity('Select the holder', 'SolidBodies')
    if sel:
        holder = adsk.fusion.BRepBody.cast(sel.entity)
        sections = []
        points = []
        for ed in holder.edges:
            points.append(round(ed.startVertex.geometry.z, 3))
        points.sort()
        ## only allow TWO duplicate points
        currentPoint = 0
        addPoint = True
        newPoints = []
        for point in points:
            if point == currentPoint:
                if addPoint:
                    newPoints.append(point + 0.001)
                    newPoints.append(point - 0.001)
                    currentPoint = point
                    addPoint = False
            else:
                addPoint = True
                newPoints.append(point)
                currentPoint = point
        newPoints.sort()
        normal = adsk.core.Vector3D.create(0,0,1)
        for p in newPoints:
            ## create the plane
            point = adsk.core.Point3D.create(0,0,p)
            plane = adsk.core.Plane.create(point, normal)
            planes = rootComp.constructionPlanes
            pInput = planes.createInput()
            pInput.setByPlane(plane)
            newPlane = planes.add(pInput)
            ## put a sketch on it
            sketches = rootComp.sketches
            sketch = sketches.add(newPlane)
            sketch.projectCutEdges(holder)
            box = sketch.boundingBox
            sizeX = abs(box.minPoint.x - box.maxPoint.x) * 10
            sizeY = abs(box.minPoint.y - box.maxPoint.y) * 10
            maxSize = 0
            sketch.deleteMe()
            newPlane.deleteMe()
            if sizeX > sizeY:
                maxSize = sizeX
            else:
                maxSize = sizeY
            sections.append((maxSize, p * 10))
          
        first = True
        lastPos = (0, 0)
        guid = "00000000-0000-0000-0000-" + str(random.randint(100000000000,999999999999))
        jsonOut = {
            "data": [
                {
                    "description": rootComp.name,
                    "guid": guid,
                    "last_modified": 1570310972973,
                    "product-id": "",
                    "product-link": "",
                    "reference_guid": guid,
                    "segments": [],
                    "type": "holder",
                    "unit": "millimeters",
                    "vendor": ""
                }

        ],
        "version": 1
        }
        
        for s in sections:
            if not first:
                seg = {
                    "height": round(abs(s[1] - lastPos[1]),3),
                    "lower-diameter": round(lastPos[0],3),
                    "upper-diameter": round(s[0],3)
                }
                if abs(s[1] - lastPos[1]) > 0.1:
                    jsonOut["data"][0]["segments"].append(seg)
                lastPos = (s[0], s[1])
            else:
                first = False
                lastPos = (s[0], s[1])
    root = tk.Tk()
    root.withdraw()    
    filename = filedialog.asksaveasfilename()
    if filename:
        with open(filename, 'w') as f:
            json.dump(jsonOut, f)

def run(context):
    try:
        createHolder()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
