# -*- coding: utf-8 -*-
import connectorBehavior
import displayGroupOdbToolset as dgo
import xyPlot
import visualization
import sketch
import job
import optimization
import mesh
import load
import interaction
import step
import assembly
import material
import part
import displayGroupMdbToolset as dgm
import regionToolset
import section
from abaqus import *
from abaqusConstants import *
import __main__
import datetime

# Para ler as áreas
import csv
import os
session.mdbData.summary()

base_path='C:/Users/LFS/Documents/IgorFreitas_NUSP12477186/Simulacoes/reproducao_paper_v3/'

list_=['OrthogonalCut-Section1-DP025-MS06.odb',
       'OrthogonalCut-Section1-DP025-MS06-mesh015-aisi1020.odb',
       'OrthogonalCut-Section1-DP025-MS07.odb',
       'OrthogonalCut-Section1-DP025-MS07-mesh015-aisi1020.odb',
       'OrthogonalCut-Section1-DP025-MS9.odb',
       'OrthogonalCut-Section1-DP025-MS9-mesh015-aisi1020.odb',
       'OrthogonalCut-Section1-DP025-MS11.odb',
       'OrthogonalCut-Section1-DP025-MS11-mesh015-aisi1020.odb',
       'OrthogonalCut-Section1-DP025-MS9-mesh02.odb',
       'OrthogonalCut-Section1-DP025-MS9-mesh02-aisi1020.odb',
       'OrthogonalCut-Section1-DP025-MS9-mesh01.odb',
       'OrthogonalCut-Section1-DP025-MS9-mesh01-aisi1020.odb',       
]
for report in list_:
    o3 = session.openOdb(
        name=base_path+report)
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=False)
    odb = session.odbs[base_path+report]
    xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=((
        'RT', NODAL, ((COMPONENT, 'RF1'), )), ), nodePick=(('TOOL-1', 1, (
        '[#0 #40000 ]', )), ), )
    #xyp = session.xyPlots['XYPlot-1']
    #chartName = xyp.charts.keys()[0]
    #chart = xyp.charts[chartName]
    #curveList = session.curveSet(xyData=xyList)
    #chart.setValues(curvesToPlot=curveList)
    #session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
    session.xyDataObjects.changeKey(fromName='_RT:RF1 PI: TOOL-1 N: 51', toName=report)