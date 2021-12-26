import requests, json
import re
from bs4 import BeautifulSoup

def getProductInfo(url, soup):

    try:
        productId =  url.split('?pid=', 1)[1].replace('&', '')
    except:
        productId = ''

    # Images
    try: #for fashion product
        productImages = soup.findAll('div', class_='q6DClP _2_B7hD')
        if(len(productImages) < 1):
            productImages = soup.findAll('div', class_='q6DClP')
    except: #for other product
        productImages = []

    productImagesUrls = []
    for image in productImages:
        imageUrl = (image['style'].split(':url(', 1)[1]).split('?q=', 1)[0]
        imageUrl = imageUrl.replace('/128', '/1500')
        productImagesUrls.append(imageUrl)

    # PRODUCT BRAND 
    try:
        productBrand = soup.find('span', class_="G6XhRU").text
    except:
        productBrand = ""  

    #PRODUCT NAME
    try:
        productName = soup.find('span', class_="B_NuCI").text
    except:
        productName = ""

    #PRODUCTPRICE
    try:
        productPrice = soup.find('div', class_="_30jeq3 _16Jk6d").text
    except:
        productPrice = ""

    #PRODUCT ACTUAL PRICE
    try:
        productActualPrice = soup.find('div', class_="_3I9_wc _2p6lqe").text
    except:
        productActualPrice = ""
    
    #PRODUCT DISCOUNT 
    try: #for fashion product
        productDiscount = soup.find('div', class_="_3Ay6Sb _31Dcoz pZkvcx").find('span').text
    except: #for other product
        try:
            productDiscount = soup.find('div', class_="_3Ay6Sb _31Dcoz").find('span').text
        except:
            productDiscount = 0
    #PRODUCT CATEGORY
    try:
        productCategory = []
        productCat = soup.findAll('div', class_ ="_3GIHBu")
        for category in productCat:
            try:
                productCategory.append(category.find('a').text)
            except:
                productCategory.append('')
    except:
        productCategory = []

    productInfo = {
        "productId": productId,
        "productBrand": productBrand,
        "productName": productName,
        "productImages": productImagesUrls,
        "productPrice": productPrice,
        "productActualPrice": productActualPrice,
        "productDiscount": productDiscount,
        "productCategory": productCategory
    }

    return productInfo


def getProductReviewsInfo(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    pagesAvailable = soup.find('div', class_ = '_2MImiq _1Qnn1K').find('span').text.split(' of ', 1)[1]
    try:
        ratingAndReviewCount = soup.find('div', class_ = '_3zoWhv').find('span').text or '-' 
        ratingCount = ratingAndReviewCount.split(' ratings', 1)[0]
        reviewCount = ratingAndReviewCount.split('and ', 1)[1].split(' ', 1)[0]
    except:
        ratingCount = soup.findAll('div', class_ = 'row _2afbiS')[0].find('span').text.split(' Rating', 1)[0]
        reviewCount = soup.findAll('div', class_ = 'row _2afbiS')[1].find('span').text.split(' Review', 1)[0]

    ratingsList = soup.find('ul', class_ = '_36LmXx').findAll('li')
    ratings = []
    for rating in ratingsList:
        ratings.append((rating.find('div').text).replace(',',''))

    reviews = []
    for page in range(int(pagesAvailable.replace(',', ''))):
        data = requests.get(url + '&page='+ str(page+1))
        soup = BeautifulSoup(data.text, "html.parser")
        reviewBlocks = soup.findAll('div', 'col _2wzgFH K0kLPL _1QgsS5')
        if(len(reviewBlocks) < 1):
            reviewBlocks = soup.findAll('div', 'col _2wzgFH K0kLPL')
        for review in reviewBlocks:
            reviewerTag = ''
            try:
                reviewerTag = review.find('p', class_ = '_2mcZGG').findAll('span')[0].text
            except:
                reviewerTag = '-'
        
            reviwerLocation = ''
            try:
                reviwerLocation = review.find('p', class_ = '_2mcZGG').findAll('span')[1].text
            except:
                reviwerLocation = '-'

            try:
                ratingGiven = review.find('div', class_ = '_3B8WaH').text 
            except:
                try:
                    ratingGiven = review.find('div', class_ = '_3LWZlK _1BLPMq').text
                except:
                    try:
                        ratingGiven = review.find('div', class_ = '_3LWZlK _1rdVr6 _1BLPMq').text
                    except:
                        ratingGiven = review.find('div', class_ = '_3LWZlK _32lA32 _1BLPMq').text #for 2 star
            
            try:
                reviewTitle = review.find('p', class_ = '_2-N8zT').text
            except:
                reviewTitle = ""
 
            try:
                reviewText = review.find('div', class_ = '_6K-7Co').text
            except:
                reviewText = review.find('div', class_ = 't-ZTKy').find('div').find('div').text
            
            try:
                reviewerName = review.find('div', class_ = "row _1ExUpQ").findAll('p')[0].text
            except:
                reviewerName = review.find('p', class_ = "_2sc7ZR _2V5EHH").text

            try:
                reviewerDate = review.find('div', class_ = "row _1ExUpQ").findAll('p')[1].text or '-'
            except:
                reviewerDate = review.find('p', class_ = '_2sc7ZR').text 

            reviewData = {
                'reviewTitle': reviewTitle,
                'reviewText': reviewText,
                'reviewerName': reviewerName,
                'reviewDate': reviewerDate,
                'reviewertag': reviewerTag,
                'reviwerLocation': reviwerLocation.strip(' ,')
            }
            reviews.append(reviewData) 
        if page >= 9:  break

    return  {
        'ratingCount': ratingCount,
        'ratings': ratings,
        'reviewCount': reviewCount,
        'reviews': reviews
    }


def getdata(url=""):

    if(url == ""):
        return {}

    url = url.split("&lid", 1)[0]
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    # check reviews count
    try: #check review count for fashion product
        reviewsCheck = soup.find('div', class_ ="_3UAT2v _33R3aa").find('span', class_= "_3at_-o").text
    except: #check review count for other product
        try:
            reviewsCheck = soup.find('div', class_ ="_3UAT2v _16PBlm").find('span').text
        except:
            reviewsCheck = ''

    
    try:
        reviewCount = int(reviewsCheck.split(' ', 1)[1].split(' ', 1)[0]) or 0
    except:
        reviewCount = 0


    if(reviewCount < 5):
        productInfo = getProductInfo(url, soup)
        productInfo['totalReviewCount'] = reviewCount
        return {
            "productInfo": productInfo,
            'reviewCount': reviewCount
        }
    else:
        productReviewsUrl = url.split('/p/', 1)[0] + '/product-reviews/' + url.split('/p/', 1)[1] + '&sortOrder=MOST_RECENT'
        productInfo = getProductInfo(url, soup)
        productReviewsInfo = getProductReviewsInfo(productReviewsUrl)
        return {
            "productInfo": productInfo,
            "productReviewsInfo": productReviewsInfo,
            "reviewCount": reviewCount
        }
    
