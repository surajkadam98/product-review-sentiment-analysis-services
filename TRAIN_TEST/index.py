import json
import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import joblib

nltk.download('vader_lexicon')

SAClassifier = SentimentIntensityAnalyzer()

# createBaseModel()
def createBaseModel():
    with open("./MODEL/baseModel.joblib", "wb") as modelFile:
        joblib.dump(SAClassifier, modelFile)

# Train Model
def trainModel(trainingData):
    try:
        with open("./MODEL/latestModel.joblib", "rb") as modelFile: # get model
            oldModel = joblib.load(modelFile)
        
        tempModel = oldModel # createcopy
        tempModel.lexicon.update(json.loads(trainingData)) # update model
        
        try:
            os.remove("./MODEL/latestModel.joblib") # remove latest model
        except:
            print('latest model not found')

        with open("./MODEL/latestModel.joblib", "wb") as modelFile: # save new model
            joblib.dump(tempModel, modelFile)
        
        return "success"
    except:
        return "fail"

# Test Model
def testModel(testData):
    try:
        with open("./MODEL/latestModel.joblib", "rb") as modelFile: # get model
            oldModel = joblib.load(modelFile)
        return oldModel.polarity_scores(testData)
    except:
        return "fail"

# Reset Model
def resetModel():
    try:
        with open("./MODEL/baseModel.joblib", "rb") as modelFile: # get base model
            baseModel = joblib.load(modelFile)
            joblib.dump(baseModel, './MODEL/latestModel.joblib') # save base model as lates
        return "success"
    except:
        return "fail"





