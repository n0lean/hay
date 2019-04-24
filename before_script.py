import os
import json


if __name__ == '__main__':
    with open('./.chalice/config.json', 'r') as f:
        d = json.load(f)
    d['stages']['dev']['manage_iam_role'] = False
    d['stages']['dev']['iam_role_arn'] = os.environ['iam_role_arn']
    with open('./.chalice/config.json', 'w') as f:
        json.dump(d, f)
