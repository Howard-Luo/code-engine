from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods
from ibm_watson_machine_learning.foundation_models import Model


class WatsonxAPI:
    def __init__(self, config):
        self.api_key = config["api_key"]
        self.url = config["url"]
        self.project_id = config["project_id"]
        self.max_tokens = config["max_tokens"]
        self.stop_seq = config["stop_seq"]
        self.model_type = ModelTypes[config["model_type"]]

    def _generate_text(self, prompt):
        credentials = {
            "url": self.url,
            "apikey": self.api_key
        }
        model_id = self.model_type.value
        parameters = {
            GenParams.MIN_NEW_TOKENS: 0,
            GenParams.MAX_NEW_TOKENS: self.max_tokens,
            GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
            GenParams.REPETITION_PENALTY: 1,
            GenParams.TEMPERATURE: 0.05,
            GenParams.STOP_SEQUENCES: self.stop_seq
        }
        llm = Model(model_id=model_id, params=parameters, credentials=credentials, project_id=self.project_id)
 
        return llm.generate_text(prompt=prompt)