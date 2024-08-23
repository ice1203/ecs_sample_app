from flask import Flask
import requests
import boto3
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
@app.route('/outgoing-http-call')
def call_http():
    response = requests.get("https://aws.amazon.com/")
    return response.text

# Test AWS SDK instrumentation
@app.route("/aws-sdk-call")
def call_aws_sdk():

    client = boto3.client("s3")
    client.list_buckets()

    return app.make_response(
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
