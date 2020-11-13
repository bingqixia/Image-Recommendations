from imageRecommender import db

class Itemimages(db.Model):
    itemId = db.Column(db.Integer, primary_key=True)
    catId = db.Column(db.Integer, unique=False, nullable=False)
    imageName = db.Column(db.String(150), unique=True, nullable=False)
    itemPrice = db.Column(db.Float, unique=True, nullable=False)
    imageUrl = db.Column(db.String(300), unique=True, nullable=False)
    def __repr__(self):
        return "(%s, %s, %s)" % (self.itemId, self.imageName, self.imageUrl)

class Galleryimages(db.Model):
    itemId = db.Column(db.Integer, primary_key=True)
    catId = db.Column(db.Integer, unique=False, nullable=False)
    imageName = db.Column(db.String(150), unique=False, nullable=False)
    itemPrice = db.Column(db.Float, unique=False, nullable=True,default=0.0)
    imageUrl = db.Column(db.String(300), unique=False, nullable=False)
    def __repr__(self):
        return "(%s, %s, %s)" % (self.itemId, self.imageName, self.imageUrl)

class UserStar(db.Model):
    userName = db.Column(db.String(50), primary_key=True, unique=False, nullable=False)
    itemId = db.Column(db.Integer, primary_key=True, unique=False, nullable=False)
    insertDate = db.Column(db.TIMESTAMP)
    def __repr__(self):
        return "(%s, %s, %s)" % (self.userName, self.itemId, self.insertDate)


class Imagerecommendations(db.Model): 
    itemId = db.Column(db.Integer, primary_key=True)
    recommendedId = db.Column(db.Integer, db.ForeignKey('galleryimages.itemId'), nullable=False)
    recommendedName = db.Column(db.String(50), unique=False, nullable=False)
    similarityValue = db.Column(db.Float, unique=False, nullable=False) 

    def __repr__(self):
        return "(%s, %s, %s, %s)" % (self.itemId, self.recommendedId, self.recommendedName, self.similarityValue)