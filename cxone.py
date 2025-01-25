import requests as rq
import sys

apikey=""
tenant='cbms'
base='https://iam.checkmarx.net/auth/realms/{tenant_account_name}/'

accesstoken_api='{base_url}/protocol/openid-connect/token'
accesstoken_body={'grant_type':'refresh_token','client_id':'ast-app','client_id=ast-app':apikey}
accesstoken_headers={'Content-Type':'application/x-www-form-urlencoded','Accept':'application/json'}
r1=rq.post(accesstoken_api,headers=accesstoken_headers,data=accesstoken_body)
token=r1.json()['access_token']
if token is not None: print(token)
else: print('Issue in getting access token,exiting...');sys.exit(0)


