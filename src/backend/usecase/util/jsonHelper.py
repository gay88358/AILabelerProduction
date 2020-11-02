
import json

class JsonHelper:

    @staticmethod
    def replace_document(json_file_path, document_want_to_replace):
        json_document = JsonHelper.load_json_document(json_file_path)
        json_document['Labels'] = document_want_to_replace['Labels']
        JsonHelper.write_json(json_file_path, json_document)
        
    @staticmethod
    def load_json_document(json_file):
        json_str = JsonHelper.load_json_string(json_file)
        json_document = json.loads(json_str)
        return json_document

    @staticmethod
    def load_json_string(json_file):
        with open(json_file) as file:
            document = json.load(file)
            return json.dumps(document)

    @staticmethod
    def write_json(json_file, json_document):
        with open(json_file, 'w') as outfile:
            json.dump(json_document, outfile)


    
