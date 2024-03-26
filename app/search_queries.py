"""
Open search article search queries
"""
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


host = 'search-mit-hyaallprjuqkbegysx7qswz7qq.us-east-1.es.amazonaws.com' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    pool_maxsize = 20
)
index_name = 'discogs_releases'

def fetch_songs(title):
    query = {
        "query": {
            "match_all": {}
        }
    }
    result = client.search(index=index_name, body=query) 
    print(result)
    if result["hits"]["hits"]:
        
        return result["hits"]["hits"][0]["_source"]
    return [title]
