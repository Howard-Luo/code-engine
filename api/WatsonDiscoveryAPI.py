from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV2 
from ibm_watson.discovery_v2 import QueryLargePassages


class WatsonDiscoveryAPI:
    def __init__(self, config):
        self.wd_config = config
        self.authenticator = IAMAuthenticator(self.wd_config["api_key"])
        self.discovery = DiscoveryV2(
            version=self.wd_config["version"],
            authenticator=self.authenticator
        )
        self.discovery.set_service_url('https://api.us-south.discovery.watson.cloud.ibm.com')
    def _query(self, query, project_id, collection_ids):
        query_result = self.discovery.query(
            project_id=project_id,
            collection_ids=collection_ids,
            natural_language_query=query,
            passages = QueryLargePassages(
                enabled = self.wd_config["enable_passages"],
                fields = self.wd_config["query_fields"],
                characters = self.wd_config["result_characters"]
            ),
            count=self.wd_config["result_count"]
        ).get_result()
        return query_result