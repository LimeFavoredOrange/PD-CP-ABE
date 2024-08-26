from flask import Flask, request, jsonify, send_file
import json

import pickle
import os
import sys
import uuid

from zipfile import ZipFile
from io import BytesIO
from glob import glob
import base64
import pickle

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path: sys.path.append(project_root)

from PD_CP_ABE import PD_CP_ABE, abe_utils


app = Flask(__name__)

# Initialize the CP-ABE scheme
cpabe = PD_CP_ABE.ABE()
(pk, mk) = cpabe.setup()

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        file_content = file.read()
        content = json.loads(file_content.decode('utf-8'))

        access_policy = json.loads(request.form['access_policy'])
        heir_attributes = json.loads(request.form['heir_attributes'])


        print(access_policy)
        ciphers, access_tree = cpabe.encrypt(pk, content, access_policy)

        # Save the file in a temporary location for encryption
        # Random dir name
        dir_name = str(uuid.uuid4())
        os.mkdir(dir_name)
        abe_utils.export_ciphers_to_file(cpabe.group, ciphers, access_tree, dir_name)

        for (heir_name, attributes) in heir_attributes.items():
            key = cpabe.keygen(pk, mk, attributes, heir_name)
            abe_utils.export_key_to_file(cpabe.group, "{}/{}_key".format(dir_name, heir_name), key)

        # Return all the files itself for the user to download
        # Create a zip file to store all the files
        stream = BytesIO()
        with ZipFile(stream, 'w') as zipf:
            for file in glob('{}/*'.format(dir_name)):
                zipf.write(file, os.path.basename(file))
        
        stream.seek(0)
        
        # Clean up the temporary directory
        for file in glob('{}/*'.format(dir_name)):
            os.remove(file)
        os.rmdir(dir_name)

        return send_file(stream, download_name='DigitalWill.zip', as_attachment=True)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400
    

@app.route("/decrypt", methods=['POST'])
def decrypt():
    try:
        if 'cipher' not in request.files or 'key' not in request.files or 'data' not in request.files:
            return jsonify({"error": "Not upload enough number of files"}), 400

        cipher = request.files['cipher']
        key = request.files['key']
        data = request.files['data']

        if cipher.filename == '' or key.filename == '' or data.filename == '':
            return jsonify({"error": "Not upload enough number of files"}), 400
        
        cipher = abe_utils.deserialize(cpabe.group, pickle.loads(cipher.read()))
        data = pickle.loads(data.read())
        key = abe_utils.deserializeKey(cpabe.group, pickle.loads(key.read()))
        decrypted_messages = cpabe.decrypt(cipher, key, data)
        return jsonify({"decrypted_messages": decrypted_messages}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400



@app.route("/keygen", methods=['POST'])
def keygen():
    try:
        target = json.loads(request.data)

        user_id = target['user_id']
        heir_attributes = target['heir_attributes']

        key = cpabe.keygen(pk, mk, heir_attributes, user_id)

        return jsonify({'key': base64.b64encode(pickle.dumps(abe_utils.serializeKey(cpabe.group,key))).decode("utf-8")})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!!!'})


if __name__ == '__main__':
    app.run(debug=True)
