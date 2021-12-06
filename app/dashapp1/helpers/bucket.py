from google.cloud import storage
from datetime import datetime, timezone
import os
import io

def read_file_blob(bucket_name, folder):
    # Instantiate a CGS client
    client = storage.Client()

    # The "folder" where the files you want to download are

    # Create this folder locally
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Retrieve all blobs with a prefix matching the folder
    bucket = client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=folder))
    file_list = []
    for blob in blobs:
        if (not blob.name.endswith("/")):
            file_list.append(blob.name)
    return file_list



def write_file_blob(bucket_name, user, text):
    # Instantiate a CGS client
    client = storage.Client()
    # cur_files = read_file_blob('central-bucket-george', f'{user}/dataset')

    # should i time stamp them? ->
    # my problem with this is if they want to overwrite I would have to delete the timestamp which isn't bad


    time = datetime.now(timezone.utc).isoformat(timespec='seconds')
    time = str(time).split('+')[0]

    filename = f'{user}_{time}.txt'


    # Retrieve all blobs with a prefix matching the folder
    bucket = client.get_bucket(bucket_name)
    # Create a new blob and upload the file's content.
    my_file = bucket.blob(f'{user}/dataset/{filename}')

    # create in memory file
    output = io.StringIO(text)

    # upload from string
    my_file.upload_from_string(output.read(), content_type="text/plain")

    output.close()


# read_file_blob('central-bucket-george','george/dataset')
# write_file_blob('central-bucket-george', 'george', 'George text')
