from flask import Flask, request, render_template, redirect, url_for
import boto3
from botocore.exceptions import NoCredentialsError
import os

app = Flask(__name__)

 # S3 Configuration
ACKEY = ''
SECKEY = ''
S3_BUCKET_NAME = 's3-leverage-01'


# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=ACKEY,
    aws_secret_access_key=SECKEY
)
# Route to show the file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    try:
        # Upload file to S3
        s3_client.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            file.filename,
            ExtraArgs={'ACL': 'public-read'}  # Set to 'private' if you want to keep the file private
        )
        return redirect(url_for('index'))  # Redirect to the main page after success
    
    except NoCredentialsError:
        return "Credentials not available"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)  
