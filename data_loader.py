import pandas as pd
import boto3
from io import StringIO

# AWS S3 Configuration

AWS_BUCKET_NAME = 'my-s3-dashboard'


# Initialize S3 client
s3 = boto3.client('s3')

def load_data():
    # Load recruiter_detail
    obj = s3.get_object(Bucket=AWS_BUCKET_NAME, Key='recruiter_detail.csv')
    recruiter_detail = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
    
    # Load job_requirements
    obj = s3.get_object(Bucket=AWS_BUCKET_NAME, Key='job_requirements.csv')
    job_requirements = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
    
    # Load submission_table
    obj = s3.get_object(Bucket=AWS_BUCKET_NAME, Key='submission_table.csv')
    submission_table = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
    
    return recruiter_detail, job_requirements, submission_table
