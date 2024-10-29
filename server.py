import json

from flask import Flask, request
from eansearch import EANSearch
import subprocess

def run_command_with_output_after(command: str) ->  subprocess.CompletedProcess[str] | subprocess.CalledProcessError:
    """
    Runs the given bash command and prints the output once the command has finished running.
    :param command: Bash command to run.
    :return: The result object containing stdout and stderr.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        print(f'\n{result.stdout}')
        return result
    except subprocess.CalledProcessError as e:
        return e


def make_api_call(barcode: str):
    """

    :param barcode:
    :return:
    """
    apiToken = "584c14adf603758ea9d11b4d7f4db7012d8b659a"

    # lookup = EANSearch(apiToken)
    #
    # name = lookup.barcodeLookup(barcode)
    # print(barcode, " is ", name)
    t = run_command_with_output_after(f'curl '
        f'"https://api.ean-search.org/api?token={apiToken}&op=barcode-lookup&'
        f'format=json&ean={barcode}"').stdout
    print(json.dumps(json.loads(t), indent=4))


app = Flask(__name__)

@app.route('/submit', methods=['GET'])
def submit():
    data = request.args.get('data')
    if data:
        make_api_call(data)
        return "product data found", 200
    else:
        return "No data received", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
