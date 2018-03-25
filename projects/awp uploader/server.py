import os
import datetime
import shutil
import sys
import logging
import json
import fnmatch
from flask import Flask,render_template,request,redirect,url_for
from werkzeug import secure_filename
from pprint import pprint
from boto3.s3.transfer import S3Transfer
import boto3
import boto.s3
from botocore.client import Config
from flask import jsonify


__author__='ibininja'
app = Flask(__name__)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))
@app.route("/",methods=["POST","GET"])
def route():
    return render_template("choose.html")
    


     
@app.route("/upload",methods=["GET","POST"])
def upload():
    print("hello")
    m=date()
    logging.basicConfig(filename='./log/'+m+'.log',level=logging.DEBUG)
    logging.info('Files started to upload')
    path="video"+"/"+m
    target=os.path.join(APP_ROOT,path)
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        print(file)
        filename=file.filename
        destination="/".join([target,filename])
        print(destination)
        file.save(destination)
        name=str(file)
        logging.info(name+'uploaded')
    videopath="./"+path

   
    outputpath="./courses_videos/"+m
    bucketpath=request.form['s3path']
    quality=request.form['quality']
    hls_time=request.form['hlstime']
    print(bucketpath)
    print(quality)
    print(hls_time)
    print(videopath)
    print(outputpath)
    if outputpath:
       convertor(videopath,outputpath,quality,hls_time,bucketpath)
    else:
        outputpath="output"
        convertor(videopath,outputpath)
    for file in os.listdir(videopath): 
         file_path = os.path.join(videopath, file)
         if os.path.isfile(file_path):
            os.remove(file_path)
            print("deleted")
    os.rmdir(videopath)
    shutil.rmtree(outputpath)
 
    
    return render_template("web2.html")
         

      
def convertor(videopath,outputpath,quality,hls_time,bucketpath):
     
     logging.info('Hls conversion started ')
     for file in os.listdir('./'+videopath):
         print(videopath)
         out1=outputpath+"/"+os.path.splitext(os.path.basename(file))[0] +"/"
         folder=os.makedirs(out1)
         str = "ffmpeg -i "+"\"./" +videopath+ "/"+os.path.basename(file)+"\""+" " + quality +" -s 1920*1080 -start_number 0 -hls_time "+hls_time+" -hls_list_size 0 -f hls ./"+"\""+"./"+outputpath+"/"+os.path.splitext(os.path.basename(file))[0]+"/" +"index.m3u8"+"\""
         os.system(str)
         logging.info(str)
         
         logging.info('converted')
         print(outputpath)
         print(os.path.basename(file))
         print(os.path.splitext(os.path.basename(file)))
         print(os.path.splitext(os.path.basename(file))[0])
        
     ACCESS_KEY_ID="KAIAJ6BZMFBLF7K2XIXA"
     ACCESS_SECRET_KEY="45rXXwkNl5Dwi6qmFDm3VXyuMC3hm1FNbqBlGAE3F"
     BUCKET_NAME='videos.kavi.in'
     
     client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key=ACCESS_SECRET_KEY)
     transfer = S3Transfer(client)
     s3=boto3.client('s3')
     s3=boto3.resource('s3',
                    aws_access_key_id= ACCESS_KEY_ID,
                    aws_secret_access_key=ACCESS_SECRET_KEY,
                    config=Config(signature_version='s3v4'))
     logging.info('connected with s3 server')
     logging.info('bucket name in s3:'+bucketpath)
     for dir in os.listdir('./'+outputpath):
         
         if True:
             print(dir)
             print("welcome")
             for file in os.listdir('./'+outputpath+'/'+dir):
                 
                 print(file)
                 
                 full_path='./'+outputpath+'/'+dir+'/'+file
                 print(full_path)
                 
                 with open(full_path,'r+') as data:
                    
                     transfer.upload_file('./'+outputpath+'/'+dir+'/'+file,BUCKET_NAME, 'hls-test'+'/'+bucketpath+"/"+dir+"/"+file)
                
                     print("filedone")
                     logging.info(file)
                     logging.info('uploaded')
                  
                     print("Done")
def date():
    i = datetime.datetime.now()
    day=str(i.day)
    month=str(i.month)
    year=str(i.year)
    hour=str(i.hour)
    minute=str(i.minute)
    second=str(i.second)
    date=day+"_"+month+"_"+year+"_"+hour+"_"+minute+"_"+second
    print(date)
    return date

    
if __name__== "__main__" :
    app.run(port=5000,debug=True)
