import numpy as np
import pandas as pd

class objective_function():
    def __init__(self,path=None, func=None,model=None, maximize=True):
        self.path=path
        self.maximize=maximize

        if model:
            self.type="ml"
            self.model=self.load()
        elif func:
            self.type="func"
            self.model=func
        else:
            print("No model or function passed")
            raise

    def load(self):
        return load_model('my_best_pipeline')

    def predict(self,X):
        if self.type in ["ml"]:
            prediction=self.model.predict(X)
        else:
            prediction=self.model(X)
        prediction=prediction if self.maximize else -prediction
        return prediction