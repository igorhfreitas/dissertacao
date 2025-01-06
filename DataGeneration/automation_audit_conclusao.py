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
basedir = 'C:/Users/LFS-MT22S-02/Documents/IgorFreitas_NUSP_12477186/data_gen_5'
os.chdir(basedir)

# Para gravar em um csv único
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d_%H-%M")
result_csv = '{0}/dados_automation_conclusao_{1}.csv'.format(basedir, now)
result_index = '{0}/dados_index_conclusao_{1}.csv'.format(basedir, now)

# Imports do ABAQUS

# Grava os cabeçalhos da saída
#with open(result_csv, 'w') as f:
#    f.write('iteration,{},'.format(
#        ','.join(['area{}'.format(x) for x in range(1, 11)])))
#    f.write('{},'.format(','.join(['d{}'.format(x) for x in range(1, 9)])))

factorial_table=[
("LGBMRegressor","AISI_1020",8.38,253.64,4227.333333,86.17,"brute force"),
#("Lasso","AISI_1020",3.54,30,500,62.28,"brute force"),
#("LGBMRegressor","AISI_1045",-8.38,291.82,4863.666667,205.32,"brute force"),
#("Lasso","AISI_1045",-0.71,30,500,213.01,"brute force"),
#("LGBMRegressor","AISI_4140",8.18,291.82,4863.666667,238.47,"brute force"),
#("Lasso","AISI_4140",-3.13,30,500,1.121.42,"brute force"),
#("LGBMRegressor","AISI_4340",2.32,158.18,2636.333333,573.28,"brute force"),
#("Lasso","AISI_4340",-10,30,500,545.15,"brute force"),
#("LGBMRegressor","AISI_52100",-10,73.64,1227.333333,127.09,"brute force"),
#("Lasso","AISI_52100",7.58,30,500,272.77,"brute force"),
#("Lasso","AISI_4140",-3.11,60,1000,1.124.26,"GA"),
#("LGBMRegressor","AISI_4140",6.62,299.99,4999.833333,238.47,"GA"),
#("Lasso","AISI_4340",-10,60,1000,547.73,"GA"),
#("LGBMRegressor","AISI_4340",2.95,159.39,2656.5,573.28,"GA"),
#("Lasso","AISI_52100",7.63,60,1000,274.44,"GA"),
#("LGBMRegressor","AISI_52100",9.97,85.59,1426.5,254.99,"GA"),
#("Lasso","AISI_304",10,60.01,1000.166667,661.88,"GA"),
#("LGBMRegressor","AISI_304",10,109.8,1830,337.05,"GA"),
#("Lasso","AISI_1020",3.42,60.01,1000.166667,63.1,"GA"),
#("LGBMRegressor","AISI_1020",8.53,255.27,4254.5,86.17,"GA"),
#("Lasso","AISI_1020",3.44,180,3000,66.38,"powell"),
#("Lasso","AISI_52100",7.58,180,3000,281.15,"powell"),
#("Lasso","AISI_4340",-13.36,180,3000,555.69,"powell"),
#("Lasso","AISI_4140",-3.11,180,3000,1.135.62,"powell"),
#("Lasso","AISI_1045",0.72,180,3000,223.34,"powell"),
#("LGBMRegressor","AISI_1020",7.92,206.53,3442.166667,89.05,"powell"),
#("LGBMRegressor","AISI_52100",-3.78,253.16,4219.333333,293.02,"powell"),
#("LGBMRegressor","AISI_4340",4.09,259.8,4330,646.07,"powell"),
#("LGBMRegressor","AISI_4140",12.29,289.18,4819.666667,237.71,"powell"),
#("LGBMRegressor","AISI_1045",-5.21,254.16,4236,211.56,"powell"),
]


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
        THROUGHOUT_STEP, 0.0, 1e-09, BELOW_MIN, 1, 0, 0.0, 0.0, 0, None), ))

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
    #s.parameters['tool_radius'].setValues(expression=str(tool_radius)) --> nao alterar
    s1.unsetPrimaryObject()
    p = mdb.models[model].parts['Tool']
    p.features['Wire-1'].setValues(sketch=s1)
    del mdb.models[model].sketches['__edit__']
    p = mdb.models[model].parts['Tool']
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

with open(result_index, 'a') as f:
    for item in factorial_table:
        print(item)
        f.write(str(item))

for i, combination in enumerate(factorial_table):
    start_time=datetime.now()
    depth_cut=0.25
    clearance_angle=5
    model,material,rake_angle,vc_m_min,vc,predicted_cut_force;algo_opt=combination
    print("============================ parametros ===============================")
    print(combination)
    print("=======================================================================")
    # Define a área da seção transversal
    muda_material(material,model="Model-1",section="Section-1")
    ToolChange(rake_angle=rake_angle,relief_angle=clearance_angle,tool_radius=0.1,model="Model-1")
    #CutDepth(cut_depth=depth_cut,model="Model-1")
    CutSpeed(cut_speed=vc,model="Model-1")
    muda_step(vc=vc,model="Model-1")

    p = mdb.models["Model-1"].parts['Tool']
    p.regenerate()

    job_name="v5_job_"+str(i)+"_"+str(material)+"_RA"+str(rake_angle)+"_VC"+str(vc)

    # Cria o trabalho e o executa
    mdb.Job(name=job_name, model='Model-1',
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
    
    print("passou pelo job")

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
        f.write('{},{},{},{},{},{},{},{},{},'.format(i,(end_time-start_time).seconds, model,material,vc,vc_m_min,rake_angle,predicted_cut_force,algo_opt))
        f.write('{}\n'.format(','.join((str(x) for x in rfx))))

    xyKeys = session.xyDataObjects.keys()
    for key in xyKeys:
        del session.xyDataObjects[key]

    #a1 = mdb.models["Model-1"].rootAssembly
    #a1.translate(instanceList=('Tool-1', ), vector=(0.0, depth_cut, 0.0))

print("END!!!! ;)")
