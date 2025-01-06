import pandas as pd
import numpy as np

def population_sorter(genes,fitness):
    return pd.DataFrame([genes,fitness],index=["individuals","fitness"]).T.sort_values("fitness",ascending=False)

def rolette_wheel_selector(df,choices=4):
    sum_of_fitness=df["fitness"].sum()
    df["fitness_cumsum"]=df["fitness"].cumsum().abs()
    choices_cutoff=np.random.uniform(0,sum_of_fitness,size=choices)
    candidates=pd.concat([df[df["fitness_cumsum"]>=cutoff].iloc[[0]] for cutoff in choices_cutoff]).reset_index(drop=True)
    return candidates
