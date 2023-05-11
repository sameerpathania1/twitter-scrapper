from flask import Flask, request, jsonify
from twspace_dl import Twspace, TwspaceDL
from pathlib import Path
import boto3
import os
import shutil
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ignoreFiles = ['.env', '.git', 'main.py', '.gitignore', 'ffmpeg.exe', 'ffmpeg']

accessKey = os.getenv('AWS_APP_ACCESS_KEY')
secretKey = os.getenv('AWS_APP_SECERT_KEY')
bucketName = os.getenv('AWS_APP_BUCKET_NAME')
bucketUrl = os.getenv('AWS_APP_S3_BUCKET_URL')

print(accessKey, secretKey)

session = boto3.Session(
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretKey,
)
s3 = session.resource('s3')

app = Flask(__name__)


@app.route('/', methods=['GET'])
async def home():
    try:
        url = request.args.get('url', "")
        if not url:
            return jsonify({'message': 'URL is missing'})
        spaceId = url.split('/')[5]
        space = Twspace.from_space_url(url)
        download = TwspaceDL(space, format_str=None)
        download.download()
        path = download.filename

        uploadedpath = "twitter-space-podcasts/" + spaceId + ".m4a"

        print('uploading file')
        s3.meta.client.upload_file(Filename=path + ".m4a", Bucket=bucketName,
                                   Key=uploadedpath, ExtraArgs={'ContentType': "audio/m4a", 'ACL': "public-read"})
        print('removing file')
        allFiles = os.listdir()
        for file in allFiles:
            try:
                ignoreFiles.index(file)
            except ValueError:
                try:
                    os.remove(file)
                except:
                    shutil.rmtree(file, ignore_errors=True)
        return jsonify({'location': bucketUrl + "/" + uploadedpath})
    except:
        return jsonify({'message': 'Error while uploading'})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
