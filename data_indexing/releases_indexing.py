import os
from pathlib import Path
import boto3
import ndjson

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from opensearchpy.helpers import bulk



INDEX_NAME="discogs_releases"
host = 'search-mit-hyaallprjuqkbegysx7qswz7qq.us-east-1.es.amazonaws.com' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)

# Connect to opensearch
es = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    pool_maxsize = 20
)




def create_index(index_name):

    try:
        response = es.indices.create(index_name)
        print('\nCreating index:')
        print(response)
    except Exception as e:
        # If, for example, my_index already exists, do not much!
        print(e)

def bulk_indexing(index_name, file_name):
    """
    Bulk index the data into OpenSearch Index

    Args:
        index_name (str): the name of the index
        file_name (str): the file name that holds the data it has to end with .ndjson
    """
    file_path = os.path.join(Path(__file__).parents[1], f"data/{file_name}")

    with open(file_path, 'r') as file:   
            records = ndjson.load(file)

    actions = []

    # Iterate over each record in the NDJSON file
    for idx, record in enumerate(records, start=1):
        # Construct the action object for each record
        action = {
            "_op_type": "index",
            "_index": index_name,
            "_id": idx,  # Use incremental number as _id
            "_source": record  # Use the record as _source
        }
        # Append the action object to the actions list
        actions.append(action)

    
                # Loop over the list directly
    success, failed = bulk(es, actions=actions)
    
    return success, failed
    


if __name__=="__main__":
    
    file_name ="releases.ndson"
    success, failed = bulk_indexing(INDEX_NAME, file_name)
    
    print("---------- SUCCESSFULL LOADS ---------")
    print(success)
    
    print("---------- FAILED LOADS ---------")
    print(failed)