from flask import render_template, request, Blueprint,make_response,redirect, Response
from imageRecommender.models import Galleryimages,UserStar
from imageRecommender.ImageUtils import ImageInfo
from imageRecommender.ImageUtils import ImageOption
import json
import numpy as np
from imageRecommender import db 
from datetime import datetime
import time
main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if 'userName' in request.cookies:
        page = request.args.get('page', 1, type=int)
        gImages = Galleryimages.query.paginate(page=page, per_page=100)
        sImages = getStar(request.cookies.get('userName'))
        # print(sImages)
        return render_template('home.html', images = gImages, stars=sImages)
    else:
        return render_template('login.html')

@main.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
        user = request.form['nm']
   
   resp = make_response(redirect(request.referrer or '/home'))
   resp.set_cookie('userName', user, expires=time.time()+3*24*3600)
   return resp 

@main.route('/getcookie')
def getcookie():
   name = request.cookies.get('userName')
   return '<h1>welcome ' + name + '</h1>'
   
def search(image, start, num):
    imgOption = ImageOption()
    img = ImageInfo(image.itemId, image.catId, image.imageUrl, image.imageName, image.itemPrice)
    res = imgOption.search_by_Pic(img, start, num)
    images = []
    items = []
    if res:
        auctions = res['Auctions']
        for itm in auctions:
            if int(itm['ProductId']) == image.itemId:
                continue
            pid = int(itm['ProductId'])
            # print('pid: %d'%pid)
            imgItem = Galleryimages.query.filter_by(itemId=pid)
            if imgItem:
                for i in imgItem:
                    if i.itemId not in set(items):
                        items.append(i.itemId)
                        images.append([i, np.round(float(itm['SortExprValues'].split(';')[0]), decimals=2)])   
    return images

@main.route("/similar")
def similar():
    selectedId = request.args.get('itemId')
    if selectedId is not None and selectedId != '':
        imageEntry = Galleryimages.query.filter_by(itemId=int(selectedId)) 
        if imageEntry:
            image = imageEntry[0]
            # print('select: %d'%image.itemId)
            images = search(image, 0, 100)
            # print(images)
            return render_template('similar.html', title='Recommendations', customstyle='recommend.css', inputImage=image, similarImages=images)
        else:
            print('Inconsistency!') 
    else:
        r = Response()
        r.set_cookie('userName', name, expires=time.time()+3*24*3600)
        # resp = make_response(redirect(request.referrer or '/home'))
        return r,204

@main.route("/recommend", methods=["GET","POST",])
def recommend():
    # .order_by(model.Entry.amount.desc())
    def sortKey_img(val): 
        return val.itemId
    def sortKey_list(val): 
        if val:
            return val[1]
    if 'userName' in request.cookies:
        sImages = getStar(request.cookies.get('userName'))
        sImages.sort(key=sortKey_img, reverse = True)
        lst = sImages[:10]
        similars = []
        for l in lst:
            imgEntry = Galleryimages.query.filter_by(itemId=l.itemId)
            if imgEntry:
                img = imgEntry[0]
                ims = search(img, 0, 100)
                # print(ims)
                similars.extend(ims)
        # print('similar')
        # print(similars[0])
        similars.sort(key=sortKey_list, reverse = True)
        return render_template('recommend.html', images = similars, stars=sImages)
    else:
        return render_template('login.html')    

@main.route("/addstar", methods=['POST'])
def addStar():
    if 'userName' in request.cookies:
        # print('in addStar')
        name = request.cookies.get('userName')
        # print(request.form)
        pid = request.form['toStar']
        if pid is not None and pid != '':
            # print('pid: %s' % pid)
            record = UserStar.query.filter_by(itemId=int(pid), userName=name).first()
            if record:
                db.session.delete(record)
            newFollow = UserStar(itemId=int(pid), userName=name, insertDate=datetime.now())
            db.session.add(newFollow)
            db.session.commit()
            db.session.close
        r = Response()
        r.set_cookie('userName', name, expires=time.time()+3*24*3600)
        # resp = make_response(redirect(request.referrer or '/home'))
        return r,204
    else:
        return render_template('login.html')

@main.route("/delstar", methods=['POST'])
def delStar():
    if 'userName' in request.cookies:
        name = request.cookies.get('userName')
        # print('in delStar')
        pid = request.form['delStar']
        if pid is not None and pid != '':
            # newFollow = UserStar(itemId=int(pid), userName=name, insertDate=datetime.now())
            record = UserStar.query.filter_by(itemId=int(pid), userName=name).first()
            db.session.delete(record)
            db.session.commit()
            db.session.close
        r = Response()
        r.set_cookie('userName', name, expires=time.time()+3*24*3600)
        # resp = make_response(redirect(request.referrer or '/home'))
        return r,204
    else:
        return render_template('login.html')

def getStar(name):
    stars = UserStar.query.filter_by(userName=name)
    sImages = []
    for s in stars:
        imgItem = Galleryimages.query.filter_by(itemId=s.itemId)
        for i in imgItem:
            sImages.append(i)
    return sImages

@main.route("/mystar", methods=['POST', 'GET'])
def myStar():
    if 'userName' in request.cookies:
        name = request.cookies.get('userName')
        # print(request.get_json())
        gImages = getStar(name)
        total = len(gImages)
        return render_template('mystar.html', images = gImages, stars=gImages)
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)