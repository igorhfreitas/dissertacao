import numpy as np
import pandas as pd

class Chromossome(np.ndarray):
    def __new__(cls,sequence,construct_dict,type="bin",mutation_rate=0.03):

        genes_lenght=0
        for parameter, value in construct_dict.items():
            genes_lenght+=value["sequence_len"]
        
        self = np.asarray(np.full(genes_lenght,0)).view(cls)
        self.subsequences={}
        self.subsequences_decimal={}       

        if type in ["decimal"]:
            self.subsequences={}
            self.subsequences_decimal={}
            for counter,(subsequence_name,subsequence_dict) in enumerate(construct_dict.items()):
                self.subsequences_decimal[subsequence_name]=sequence[counter]
                self.subsequences[subsequence_name]=self.encode(sequence[counter],len=subsequence_dict["sequence_len"])
            self = self.setattr(sum(self.subsequences.values(),[]))
                
        elif type in ["bin"]:
            self = self.setattr(sequence)
            for counter,(subsequence_name,subsequence_dict) in enumerate(construct_dict.items()):
                subsequence_len=subsequence_dict["sequence_len"]
                if counter==0:
                    low_bound=0
                    high_bound=subsequence_len
                else:
                    low_bound=high_bound
                    high_bound+=subsequence_len
                self.subsequences[subsequence_name]=sequence[low_bound:high_bound]
                self.subsequences_decimal[subsequence_name]=self.decode(sequence[low_bound:high_bound])

        self.mutation_rate=mutation_rate
        self.individual_property=construct_dict

        return self

    def setattr(self,value):
        for i in range(len(self)):
            self[i]=value[i]
        return self
    
    def encode(self,value,len=10):        
        negative_value=0
        if value<0:
            negative_value=1
            value=value*-1
        list_=[]
        bin_str=str(negative_value)+bin(value).replace("0b","").rjust(len,"0")
        list_[:0]=bin_str
        return [int(x) for x in list_]

    def decode(self,value,base=2):
        negative_value=value[0]
        value=value[1:]
        value_str="".join([str(gene) for gene in value])
        new_value=int(value_str,base) if negative_value==0 else int(value_str,base)*-1
        return new_value

    def mutate(self,property):
        new_property=[1-int(gene) if np.random.rand() > (1-self.mutation_rate) else gene for gene in property]
        return new_property

    def mutation_cycle(self,check_feasibility=False):
        for property,value in self.subsequences.items():
            feasible=False
            while not feasible:
                new_value=self.mutate(value)
                new_value_decimal=self.decode(new_value)
                feasible=self.check_feasibility(property,new_value_decimal)
                if not check_feasibility:
                    feasible=True
            self.subsequences[property]=new_value
            self.subsequences_decimal[property]=new_value_decimal
        self.setattr(sum(self.subsequences.values(),[]))

        return self

    def check_feasibility(self,property,value):
        return value>=self.individual_property[property]["lower_bound"] and value<=self.individual_property[property]["max_bound"]
