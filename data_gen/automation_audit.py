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

# MUDAR ISSO ANTES DE RODAR!
basedir = 'C:/Users/LFS/Documents/IgorFreitas_NUSP12477186/Simulacoes/data_gen'
os.chdir(basedir)

# Para gravar em um csv único
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d_%H-%M")
result_csv = '{0}/dados_automation_{1}.csv'.format(basedir, now)

# Imports do ABAQUS

# Grava os cabeçalhos da saída
#with open(result_csv, 'w') as f:
#    f.write('iteration,{},'.format(
#        ','.join(['area{}'.format(x) for x in range(1, 11)])))
#    f.write('{},'.format(','.join(['d{}'.format(x) for x in range(1, 9)])))

materiais=[#"ALUMINIO",
           #"AA_5754_H11",
           #"AA_6082_T6",
           #"AA_7075_T651",
           #"AA_7075_T6",
           #"AA_1100",
           #"AA_5083_H116",
           #"AlSi10Mg",
           #"AA_6061_T6",
           "AISI_1045",
           "AISI_1045",
           "AISI_1020",
           "AISI_1045",
           "STEEL_304",
           "AISI_4340",
           "STEEL_52100",
           "AISI_4340_52_HRC",
           "AISI_1045",
           "Armour_steel",]

depth_cut_list=[1]
vc_list=range(500,1000,100)
rake_angle_list=range(-10,15,3)
clearance_angle_list=[2,5,7]

#rake_angle_list=[-15,-10,-5,-2,0,2,5,10,15] #ToDo: alterar atquivo inp no assembly ou implementar isso via lib 
#clearance_angle_list=[0,2,5,10,15] #ToDo: alterar atquivo inp no assembly ou implementar isso via lib 

factorial_table=[]
for material in materiais:
    for depth_cut in depth_cut_list:
        for vc in vc_list:
            for rake_angle in rake_angle_list:
                for clearance_angle in clearance_angle_list:
                    factorial_table.append((material,depth_cut,vc,rake_angle,clearance_angle))


# Importa o arquivo de entrada gerado
# Não irei importar o arquivo pois o sketch não vem aberto para ser editado, portanto será alterado o modelo "original"
#mdb.ModelFromInputFile(
#    name='newinput', inputFileName='{0}/Atuomation_base.inp'.format(basedir))

#session.viewports['Viewport: 1'].assemblyDisplay.setValues(
#    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
#a = mdb.models['newinput'].rootAssembly

# Garante a funcionalidade do código anterior, mantendo o nome do modelo
#try:
#    del mdb.models['Model-1-MS_tool1']
#except:
#    pass
#mdb.models.changeKey(fromName='newinput', toName='Model-1-MS_tool1')

# Altera as áreas das seções transversais para um vetor ordenado "areas"

def muda_step(vc=3000,model="Model-1-MS_tool1"):
    step=(3000*0.0008)/vc
    mdb.models[model].steps['CuttingTime'].setValues(
        timePeriod=step, massScaling=((SEMI_AUTOMATIC, MODEL, 
        THROUGHOUT_STEP, 0.0, 1e-11, BELOW_MIN, 1, 0, 0.0, 0.0, 0, None), ), 
        improvedDtMethod=ON)

def muda_material(material,model="Model-1-MS_tool1",section="Secao_workpiece"):
    mdb.models[model].sections[section].setValues(
        material=material)
    mdb.models[model].sections[section].setValues(
        material=material)

def ToolChange(rake_angle=2.5,relief_angle=2,tool_radius=0.1,model="Model-1-MS_tool1"):
    if rake_angle<0:
        rake_angle=360+rake_angle
    p = mdb.models[model].parts['Tool']
    s = p.features['Wire-1'].sketch
    mdb.models[model].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s1 = mdb.models[model].sketches['__edit__']
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s1, upToFeature=p.features['Wire-1'], 
        filter=COPLANAR_EDGES)
    s=mdb.models[model].sketches['__edit__']
    s.parameters['rake_angle'].setValues(expression=str(rake_angle))
    s.parameters['clearance_angle'].setValues(expression=str(relief_angle))
    s.parameters['tool_radius'].setValues(expression=str(tool_radius))
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1-MS_tool1'].parts['Tool']
    p.features['Wire-1'].setValues(sketch=s1)
    del mdb.models['Model-1-MS_tool1'].sketches['__edit__']
    p = mdb.models['Model-1-MS_tool1'].parts['Tool']
    p.regenerate()
    p.generateMesh()

def CutDepth(cut_depth=1,model="Model-1-MS_tool1"):
    print("changing asssembly cutting depth")
    print(cut_depth)
    a1 = mdb.models[model].rootAssembly
    a1.translate(instanceList=('Tool-1', ), vector=(0.0, -cut_depth, 0.0))

def CutSpeed(cut_speed=4000,model="Model-1-MS_tool1"):
    mdb.models[model].boundaryConditions['CuttingSpeed'].setValues(
        v1=-cut_speed)

for i, combination in enumerate(factorial_table):
    start_time=datetime.now()
    material,depth_cut,vc,rake_angle,clearance_angle=combination
    print("============================ parametros ===============================")
    print(combination)
    print("=======================================================================")
    # Define a área da seção transversal
    muda_material(material)
    ToolChange(rake_angle=rake_angle,relief_angle=clearance_angle,tool_radius=0.1)
    CutDepth(cut_depth=depth_cut)
    CutSpeed(cut_speed=vc)
    muda_step(vc=vc)

    p = mdb.models["Model-1-MS_tool1"].parts['Tool']
    p.regenerate()

    job_name="v2_job_"+str(i)

    # Cria o trabalho e o executa
    mdb.Job(name=job_name, model='Model-1-MS_tool1',
            description=str(combination), type=ANALYSIS, atTime=None,
            waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=DOUBLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB,
            parallelizationMethodExplicit=DOMAIN,numCpus=6,numDomains=6)
    mdb.jobs[job_name].submit(consistencyChecking=OFF)
    mdb.jobs[job_name].waitForCompletion()
    session.mdbData.summary()
    mdb.jobs[job_name].waitForCompletion()
    now_=datetime.now()
    while (datetime.now()-now_).microseconds<500:
        pass
    o3 = session.openOdb(name='{}/{}.odb'.format(basedir,job_name))
    print("open data odb")
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        DEFORMED, ))

    # Para retirar os dados
    odb = session.openOdb(name='{}/{}.odb'.format(basedir,job_name))
    # Retirando os deslocamentos
    NSETS = odb.rootAssembly.nodeSets.keys()
    set_name="não encontrou set-name"
    print(NSETS)
    for set in NSETS:
        if "REFERENCE_POINT_TOOL-1" in set:
            set_name=set
    rfx=session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('RF',
                                                                          NODAL), ), nodeSets=(set_name, ))
    
    print('{} of {}'.format(i+1, len(factorial_table)))
    #rfx = session.xyDataObjects['RF:RF1 PI: TOOL-1 N: 49']
    print(rfx)
    end_time=datetime.now()

    # Adiciona ao arquivo de saída os deslocamentos obtidos nessa iteração
    with open(result_csv, 'a') as f:
        f.write('{},{},{},{},{},{},{},'.format(i,(end_time-start_time).seconds, material,depth_cut,vc,rake_angle,clearance_angle))
        f.write('{}\n'.format(','.join((str(x) for x in rfx))))

    xyKeys = session.xyDataObjects.keys()
    for key in xyKeys:
        del session.xyDataObjects[key]

    a1 = mdb.models["Model-1-MS_tool1"].rootAssembly
    a1.translate(instanceList=('Tool-1', ), vector=(0.0, depth_cut, 0.0))
print("END!!!! ;)")