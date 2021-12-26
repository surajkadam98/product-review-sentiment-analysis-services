import json
import string
import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import joblib

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

stopWords =  stopwords.words('english')
porter =  PorterStemmer()

with open("./MODEL/latestModel.joblib", "rb") as modelFile: # get model
    SAClassifier = joblib.load(modelFile)

def preProcessText(singleReview):

    # convert to lowercse
    singleReview.lower()

    #remove puntuation
    singleReview = "".join([char for char in singleReview if char not in string.punctuation])
    
    # tokenize
    singleReview = nltk.word_tokenize(singleReview)

    #remove stopwords
    singleReview = [word for word in singleReview if word not in stopWords]

    #stemmming
    # singleReview = [porter.stem(word) for word in singleReview]

    # add part of speech
    tags = nltk.pos_tag(singleReview)    
    # print(tags)
    return tags



def analyseReviews(data = {}):

    if(data == {}):
        return { "result" : "please provide input"}

    reviewsCount = 0
    positiveReviewCount = 0
    negativeReviewCount = 0
    neutralReviewCount = 0
    tagsContainer = []

    for review in data['productReviewsInfo']['reviews']:
        reviewsCount+=1
        singleReview = review['reviewText']
        tags = preProcessText(singleReview)
        if(SAClassifier.polarity_scores(review['reviewText'])['compound'] > 0):
            positiveReviewCount+=1
        elif(SAClassifier.polarity_scores(review['reviewText'])['compound'] < 0  ):
            negativeReviewCount+=1
        else:
            neutralReviewCount+=1
        for i in tags:
            if(i[1] == "JJ" or i[1] == "NN" or i[1] == "VBN" or i[1] == "RB" or i[1] == "NNP" or i[1] == "VBG" or i[1] == "NNS" or i[1] == "VBP" or i[1] == "VBD" or i[1] == "IN" or i[1] == "JJS" or i[1] == "RBR"):
                tagsContainer.append(i[0])


    fdist = FreqDist(tagsContainer)
    mostCommon = fdist.most_common(25)
    mostCommonWords = []
    for dataWords in mostCommon:
        temp = {}
        mostCommonWords.append({"word": dataWords[0], "value": dataWords[1]})

    result = {
        "productId": data["productInfo"]["productId"],
        "productBrand": data["productInfo"]["productBrand"],
        "productName": data["productInfo"]["productName"],
        "productImages": data["productInfo"]["productImages"],
        "productPrice": data["productInfo"]["productPrice"],
        "productActualPrice": data["productInfo"]["productActualPrice"],
        "productDiscount": data["productInfo"]["productDiscount"],
        "productCategory": data["productInfo"]["productCategory"],
        "ratings": data["productReviewsInfo"]['ratings'],
        "reviewsCount": reviewsCount,
        "totalReviewCount": data["productReviewsInfo"]['reviewCount'],
        "positiveReviewCount": positiveReviewCount,
        "negativeReviewCount": negativeReviewCount,
        "neutralReviewCount": neutralReviewCount,
        "mostCommonWords": mostCommonWords,
    }

    return result

