from flask import Flask, jsonify, request
import TRAIN_TEST.index as train_test
import CREATE_INSIGHT.dataAnalyse
import CREATE_INSIGHT.scraper
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app)

@app.route('/api/quick-insights', methods = ['GET'])
def QI_Service():
    url = request.args.get('url')
    result = None 

    if (url):
        data = CREATE_INSIGHT.scraper.getdata(url)
        if(data):
            if(data['reviewCount'] < 5):
                return data['productInfo']
            result  = CREATE_INSIGHT.dataAnalyse.analyseReviews(data)
        else:
            result = "no review found"
    else:
        result = 'no url'
    return result

@app.route('/api/train-model', methods = ['POST'])
def trainModelService():
    trainingData = request.get_json()
    result = train_test.trainModel(trainingData['data'])
    return result

@app.route('/api/test-model', methods = ['POST'])
def testModelService():
    testData = request.get_json()
    result = train_test.testModel(testData['data'])
    return result

@app.route('/api/reset-model', methods = ['GET'])
def resetModelService():
    result = train_test.resetModel()
    return result

@app.route('/')
def main():
    return jsonify('base page')

if __name__ == '__main__':
    app.run(debug =True)
