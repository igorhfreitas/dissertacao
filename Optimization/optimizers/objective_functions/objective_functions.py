import numpy as np
import pandas as pd
from pycaret.regression import load_model, predict_model
from pycaret.internal.pipeline import Pipeline

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
        return load_model(self.path)

    def predict(self,X):
        if self.type in ["ml"]:
            if self.model.__class__ == Pipeline:
                prediction=predict_model(self.model,X).drop_duplicates()["prediction_label"].values
            else:
                prediction=self.model.predict(X)
        else:
            prediction=self.model(X)
        prediction=-prediction if self.maximize else prediction
        return prediction