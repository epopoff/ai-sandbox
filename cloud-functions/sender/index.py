import boto3
import os
import requests
import yandexcloud
import json
import logging
from yandex.cloud.lockbox.v1.payload_service_pb2 import GetPayloadRequest
from yandex.cloud.lockbox.v1.payload_service_pb2_grpc import PayloadServiceStub

boto_session = None
storage_client = None

def get_boto_session():
    global boto_session
    if boto_session is not None:
        return boto_session

    # initialize lockbox and read secret value
    yc_sdk = yandexcloud.SDK()
    channel = yc_sdk._channels.channel("lockbox-payload")
    lockbox = PayloadServiceStub(channel)
    response = lockbox.Get(GetPayloadRequest(secret_id=os.environ['SECRET_ID']))

    # extract values from secret
    access_key = None
    secret_key = None
    for entry in response.entries:
        if entry.key == 'ACCESS_KEY_ID':
            access_key = entry.text_value
        elif entry.key == 'SECRET_ACCESS_KEY':
            secret_key = entry.text_value
    if access_key is None or secret_key is None:
        raise Exception("secrets required")
    print("Key id: " + access_key)

    # initialize boto session
    boto_session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    # print('get_boto_session:', boto_session)
    return boto_session

def get_storage_client():
    global storage_client
    if storage_client is not None:
        return storage_client

    storage_client = get_boto_session().client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        region_name='ru-central1'
    )
    # print('get_storage_client:', storage_client)
    return storage_client

def get_url(object_name):
    client = get_storage_client()
    bucket = os.environ['S3_BUCKET']
    url = client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': object_name}, ExpiresIn=3600)
    # print('get_url:', url)
    return url


def handler(event, context):
    # logger.info('start handler')
    presigned_url = get_url(event['messages'][0]['details']['object_id'])
    print('presigned_url:', presigned_url)
    return {
        'statusCode': 200,
        # 'body': event['messages'][0]['details']['object_id'],
        'body': presigned_url,
    }