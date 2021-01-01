import requests

apiurl = 'http://ec2-54-170-66-205.eu-west-1.compute.amazonaws.com/'
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.4)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

def loginuser(username, password):
    userid = session.get(apiurl+'/robo/userid/'+username).json().get('id')
    if userid:
        token = session.post(apiurl+'/login', params={
            'userid': userid,
            'password': password}).json().get('token')
        if not token:
            return False
        with open('.token', 'w') as f:
            f.write(token + '>' + str(userid) + '>' + username)

        return True
    return False



def signupuser(u,p1,p2,i):
    try:
        userid = session.get(apiurl + '/robo/userid/' + u).json().get('id')
        if not userid:
            if p1 == p2:
                session.post(apiurl + '/robo/adduser', params={
                    'username': u,
                    'password': p1,
                    'initials': i})
                userid = session.get(apiurl + '/robo/userid/' + u).json().get('id')
                token = session.post(apiurl + '/login', params={
                    'userid': userid,
                    'password': p1}).json().get('token')

                with open('.token', 'w') as f:
                    f.write(token + '>' + str(userid) + '>' + u)

                return True
        else:
            return False
    except:
        False