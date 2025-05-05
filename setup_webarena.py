import os

base_url = "http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com"

websites = {"SHOPPING" : 7770, "SHOPPING_ADMIN" : 7780, "REDDIT" : 9999, "GITLAB" : 8023, "MAP" : 3000, "WIKIPEDIA" : 8888, "HOMEPAGE" : 4399}

for name, port in websites.items():
	os.environ[name] = f"{base_url}:{port}"
	os.environ[f"WA_{name}"] = f"{base_url}:{port}"