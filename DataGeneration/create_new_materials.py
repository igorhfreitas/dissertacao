import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior


material_list=[
{
    "material": "AISI_304",
    "Young modulus": 207800,
    "Poisson`s ratio": 0.3,
    "Densidade": 0.000000008,
    "reference strain": 1.0,
    "d1": 0.69,
    "d2": 0,
    "d3": 0,
    "d4": 0.0546,
    "d5": 0,
    "Epsilon dot zero": 0.1,
    "A (MPa)": 280,
    "B (MPa)": 802.5,
    "n": 0.0622,
    "m": 1,
    "melt_temp": 1673,
    "temp_ref": 293
    "C": 0.0799,
},

{
    "material": "AISI_304_2",
    "Young modulus": 193000,
    "Poisson`s ratio": 0.28,
    "Densidade": 0.00000000795,
    "reference strain": 0.001,
    "d1": 0.53,
    "d2": 0.5,
    "d3": -6.8,
    "d4": -0.014,
    "d5": 0,
    "Epsilon dot zero": 0.001,
    "A (MPa)": 452,
    "B (MPa)": 694,
    "n": 0.311,
    "m": 0.996,
    "melt_temp": 1673,
    "temp_ref": 273
    "C": 0.0067,
},

{
    "material": "AISI_1020",
    "Young modulus": 200000,
    "Poisson`s ratio": 0.3,
    "Densidade": 0.0000000078,
    "reference strain": 0.004,
    "d1": 0.24,
    "d2": 0.54,
    "d3": -1.5,
    "d4": 0,
    "d5": 0,
    "Epsilon dot zero": 0.01,
    "A (MPa)": 213,
    "B (MPa)": 53,
    "n": 0.34,
    "m": 0.81,
    "melt_temp": 1623,
    "temp_ref": 293
    "C": 0.0055,
},

{
    "material": "AISI_1045",
    "Young modulus": 200000,
    "Poisson`s ratio": 0.3,
    "Densidade": 0.0000000078,
    "reference strain": 1,
    "d1": 0.1,
    "d2": 0.76,
    "d3": -1.57,
    "d4": 0.005,
    "d5": -0.84,
    "Epsilon dot zero": 1,
    "A (MPa)": 506,
    "B (MPa)": 320,
    "n": 0.28,
    "m": 1.06,
    "melt_temp": 1795,
    "temp_ref": 300,
    "C": 0.0064,
},

{
    "material": "AISI_1045-2",
    "Young modulus": 210000,
    "Poisson`s ratio": 0.269,
    "Densidade": 0.00000000795,
    "reference strain": 0.001,
    "d1": 0.06,
    "d2": 1.31,
    "d3": -1.96,
    "d4": 0.0018,
    "d5": 0.58,
    "Epsilon dot zero": 0.001,
    "A (MPa)": 553,
    "B (MPa)": 600,
    "n": 0.234,
    "m": 1,
    "melt_temp": 1733,
    "temp_ref": 293
    "C": 0.0134,
},

{
    "material": "AISI_4130",
    "Young modulus": 160000,
    "Poisson`s ratio": 0.29,
    "Densidade": 0.00000000785,
    "reference strain": 0.5,
    "d1": -0.1895,
    "d2": 0.7324,
    "d3": 0.6633,
    "d4": 0.0291,
    "d5": 0.7162,
    "Epsilon dot zero": 0.1,
    "A (MPa)": 673,
    "B (MPa)": 190,
    "n": 0.1538,
    "m": 107,
    "melt_temp": 1705,
    "temp_ref": 293
    "C": 0.017,
},

{
    "material": "AISI_4340",
    "Young modulus": 209000,
    "Poisson`s ratio": 0.28,
    "Densidade": 0.00000000786,
    "reference strain": 1.0,
    "d1": 0.05,
    "d2": 3.44,
    "d3": -2.12,
    "d4": 0.002,
    "d5": 0.61,
    "Epsilon dot zero": 1,
    "A (MPa)": 792,
    "B (MPa)": 510,
    "n": 1.03,
    "m": 0.26,
    "melt_temp": 1790,
    "temp_ref": 300
    "C": 0.014,
},

{
    "material": "AISI_52100",
    "Young modulus": 201330,
    "Poisson`s ratio": 0.277,
    "Densidade": 0.000000007853,
    "reference strain": 1.0,
    "d1": 0.0368,
    "d2": 2.34,
    "d3": -1.484,
    "d4": 0.0035,
    "d5": 0.411,
    "Epsilon dot zero": 1,
    "A (MPa)": 774.78,
    "B (MPa)": 134,
    "n": 0.37,
    "m": 3.171,
    "melt_temp": 1760.15,
    "temp_ref": 293.15
    "C": 0.0018,
},

]

for tool in ['Model-1-MS_tool2','Model-1-MS_tool3','Model-1-MS_tool4','Model-1-MS_tool5','Model-1-MS_tool6']:
    for material in material_list:
        mdb.models[tool].Material(name=material["material"], objectToCopy=mdb.models[tool].materials['ALUMINIO'])
        mdb.models[tool].materials[material["material"]].johnsonCookDamageInitiation.setValues(table=((material["d1"], material["d2"], material["d3"], material["d4"],material["d5"], material["melt_temp"], material["temp_ref"], material["reference strain"]), ))
        #mdb.models[tool].materials[material["material"]].johnsonCookDamageInitiation.damageEvolution.setValues(type=DISPLACEMENT)
        mdb.models[tool].materials[material["material"]].elastic.setValues(table=((material["Young modulus"], material["Poisson`s ratio"]), ))
        mdb.models[tool].materials[material["material"]].plastic.setValues(table=((material["A (MPa)"], material["B (MPa)"], material["n"], material["m"], material["melt_temp"], material["temp_ref"]), ))
        mdb.models[tool].materials[material["material"]].plastic.rateDependent.setValues(table=((material["C"], material["Epsilon dot zero"]), ))