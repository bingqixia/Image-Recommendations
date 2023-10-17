# Similar image recommendation application based on Flask for Heroku

This is a gallery application for similar image recommender, used Python Object-Oriented Development, Flask framework, developed on Heroku.

Recommendation algorithms use `Alibaba Cloud's machine learning API`. So if you want run this dome application, you need replace the Access Key with your own.

# Installation

## install packages
```shell
pip install -r requirements.txt
```

## create database
```shell
flask createDB
```

## import the test data
```shell
flask importDB
```

## start the application 
```shell
flask run
```

and you should be able to access it in your browser via

http://localhost:5000/

Then you can browse the gallery and recommendations with the images provided in the repository.

