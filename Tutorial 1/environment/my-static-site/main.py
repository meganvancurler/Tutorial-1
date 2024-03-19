from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws import AwsProvider, S3Bucket, S3BucketWebsite, S3BucketPolicy

class MyStaticSiteStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, 'AWS', region='us-east-1')

        bucket = S3Bucket(self, 'MyWebsiteBucket',
                          bucket='<UNIQUE-BUCKET-NAME>',
                          website=S3BucketWebsite(index_document='index.html'))

        S3BucketPolicy(self, 'BucketPolicy',
                       bucket=bucket.bucket,
                       policy=f'''
                       {{
                           "Version": "2012-10-17",
                           "Statement": [{{
                               "Sid": "PublicReadGetObject",
                               "Effect": "Allow",
                               "Principal": "*",
                               "Action": "s3:GetObject",
                               "Resource": "arn:aws:s3:::{bucket.bucket}/*"
                           }}]
                       }}
                       ''')

app = App()
MyStaticSiteStack(app, "my-static-site")
app.synth()
