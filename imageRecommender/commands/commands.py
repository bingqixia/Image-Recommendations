import sys
import pandas as pd
sys.path.append('../')

from flask import Blueprint
from imageRecommender.models import Galleryimages, Imagerecommendations
from imageRecommender import db 
import os
import pickle
from numpy.testing import assert_almost_equal

global numRec
numRec = 4

def getNames(inputName, similarNames, similarValues):
    images = list(similarNames.loc[inputName, :])
    values = list(similarValues.loc[inputName, :])
    if inputName in images:
        assert_almost_equal(max(values), 1, decimal = 5)
        images.remove(inputName)
        values.remove(max(values))
    return inputName, images[0:numRec], values[0:numRec]


def getImages(inputImage):
    similarNames = pickle.load(open(os.path.join("imageRecommender/static/pickles/similarNames.pkl"), 'rb'))
    similarValues = pickle.load(open(os.path.join("imageRecommender/static/pickles/similarValues.pkl"), 'rb'))
    
    if inputImage in set(similarNames.index):
        return getNames(inputImage, similarNames, similarValues)
    else:
        print("'{}' was not found.".format(inputImage))
        sys.exit(2)

cmd = Blueprint('db', __name__)

@cmd.cli.command('createDB')
def createDB():
    db.create_all()

@cmd.cli.command('dropDB')
def dropDB():
    db.drop_all() 

@cmd.cli.command('importDB')
def importDB():
    print('in')
    # ,cat_id,item_name,price,img_url
    images = pd.read_csv('db.csv')
    grouped = images.groupby(['cat_id'])
    data = None
    for name, group in grouped:
        group = group[(group['price'] > 10) & (group['price'] < 1000)]
        tmp = group[:2000]
        if data is not None:
            data = pd.concat([data, tmp], ignore_index=True)
        else:
            data = tmp
    print(name, data.shape[0])
    for i, r in data.iterrows():
        img = Galleryimages(itemId=str(int(r['item_id'])), catId=str(int(r['cat_id'])), imageName=r['item_name'], \
        itemPrice=r['price'], imageUrl=r['img_url'])
        db.session.add(img)
        db.session.commit()
    db.session.close() 