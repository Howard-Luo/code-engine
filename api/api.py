from flask import Flask, request, jsonify, send_from_directory
import json
import main
from collections.abc import Mapping

app = Flask(__name__)

def update_nested_dict(original_dict, update_dict):
    for key, value in update_dict.items():
        if isinstance(value, Mapping):
            original_dict[key] = update_nested_dict(original_dict.get(key, {}), value)
        else:
            original_dict[key] = value
    return original_dict

@app.route('/search', methods=['POST'])
def update_and_run():
    try:
        req_data = request.json["config"]
        with open('config.json', 'r') as f:
            current_config = json.load(f)
        updated_config = update_nested_dict(current_config, req_data)
        with open('config.json', 'w') as f:
            json.dump(updated_config, f)

        results = main.main()
        return jsonify({"status": "success", "results": results}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)