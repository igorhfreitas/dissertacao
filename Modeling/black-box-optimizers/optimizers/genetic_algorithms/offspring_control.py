import numpy as numpy
import pandas as pd

def gerenerate_population(population_size=20,mutation_rate=0.03,
                          population_description={"var_1":{"sequence_len":10,"max_bound":10,"lower_boud":0,"type":"int"}}):
    
    gene_values=[]
    for parameter_name,parameters in population_description.items():
        if parameters["type"]=="int":
            gene_values.append(np.random.randint(parameters["lower_bound"],parameters["max_bound"],size=(population_size,1)))
        elif parameters["type"]=="float":
            float_genes=np.random.uniform(parameters["lower_bound"],parameters["max_bound"],size=(population_size,1))
            float_genes_conversion=(float_genes*10).astype(int)
            gene_values.append(float_genes_conversion)
        else:
            print("type not suppoted")
            raise
    
    population=[Chromossome(individual,population_description,type="decimal",mutation_rate=mutation_rate) 
                for individual in np.concatenate(gene_values,axis=1)]
    
    return population

def uniform_crossover(fathers,construct_dict,mutation_rate,crossover_probability=0.1,population_size=20):
    fathers=fathers.sort_values("fitness",ascending=False)
    fathers_sorted_genes=fathers["individuals"].values
    
    new_offspring=[]
    for individual in range(population_size):
        new_individual=[]
        for gene_number in range(len(fathers_sorted_genes[0])):
            if np.random.random()>(1-crossover_probability):
                new_individual.append(fathers_sorted_genes[np.random.choice(fathers_sorted_genes.shape[0])][gene_number])
            else:
                new_individual.append(fathers_sorted_genes[0][gene_number])
        new_offspring.append(new_individual)
    return [Chromossome(individual,construct_dict,type="bin",mutation_rate=mutation_rate) for individual in new_offspring]

def parameter_point_crossover():
    pass
    #ToDo: faz o crossover trocando todo os genes do parâmetro de cada pai e não gene à gene.
