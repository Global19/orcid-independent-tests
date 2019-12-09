import OrcidBaseTest
from OrcidBrowser import OrcidBrowser
import properties

class OauthOpenId(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.firefox = OrcidBrowser()
        self.public_record_id    = properties.staticId
        self.public_record_token = "c9974dc3-451b-420f-ae6e-b76d7009062e"
        self.limited_record_token = "2fe47c3c-aae6-4a80-981b-fc221a067abe"
        self.client_id = properties.OpenClientId
        self.client_secret = properties.OpenClientSecret
        self.scope = "openid"
        self.wrong_scope = "/read-limited%20/activities/update%20/person/update"

        self.member_obo_id = properties.OBOMemberClientId
        self.member_obo_secret = properties.OBOMemberClientSecret
        self.client_id     = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.member_obo_scope = "openid%20/read-limited%20/activities/update%20/person/update"
        self.member_obo_code = self.generate_auth_code(self.member_obo_id, self.member_obo_scope, "api2PostUpdateCode")
        self.member_obo_access, self.member_obo_refresh, self.member_obo_id_token = self.orcid_exchange_auth_token(self.member_obo_id,self.member_obo_secret,self.member_obo_code)

    def test_existing_token_flow(self):
        id_token = self.get_id_token()
        print "id_token: " + id_token
        newaccess = self.get_obo_token()
        print "new access token: " + newaccess

    def get_id_token(self):
        self.assertIsNotNone(self.member_obo_access,"Bearer not recovered: " + str(self.member_obo_access))
        curl_params = ['-i', '-L', '-H', "Accept: application/json", '--data' 'client_id=' + self.member_obo_id + '&client_secret=' + self.member_obo_secret + '&subject_token=' + self.member_obo_access +
        '&grant_type=urn:ietf:params:oauth:grant-type:token-exchange&subject_token_type=urn:ietf:params:oauth:token-type:access_token&requested_token_type=urn:ietf:params:oauth:token-type:id_token']
        response = self.orcid_curl("https://" + properties.test_server + "/oauth/token", curl_params)
        return response

    def get_obo_token(self):
        curl_params = ['-i', '-L', '-H', "Accept: application/json", '--data' 'client_id=' + self.client_id + '&client_secret=' + self.client_secret +
                     '&grant_type=urn:ietf:params:oauth:grant-type:token-exchange&subject_token=' +
                     '&subject_token_type=urn:ietf:params:oauth:token-type:id_token&requested_token_type=urn:ietf:params:oauth:token-type:access_token']

        response = self.orcid_curl("https://" + properties.test_server + "/oauth/token", curl_params)
        return response
'''
    def test_oauth_token(self):
        code = self.generate_auth_code(self.client_id, self.scope, "open")
        access, refresh = self.orcid_exchange_auth_token(self.client_id, self.client_secret, code)
        self.assertTrue(access, "Failed to retrieve access token")

    def test_public_record_info(self):
        user_info = self.get_user_info(self.public_record_token)
        user_info_body = user_info.partition('{"id')[1] + user_info.partition('{"id')[2]
        print "response: " + user_info_body
        self.assertTrue(user_info_body.strip() == open('saved_records/user_info_public.json', 'r').read(),'User info does not match saved file: ' + user_info)

    def test_limited_record_info(self):
        user_info = self.get_user_info(self.limited_record_token)
        user_info_body = user_info.partition('{"id')[1] + user_info.partition('{"id')[2]
        print "response: " + user_info_body
        self.assertTrue(user_info_body.strip() == open('saved_records/user_info_limited.json', 'r').read(),'User info does not match saved file: ' + user_info)

    def test_implicit_token(self):
        implicit = self.generate_implicit_code_selenium(self.client_id, self.scope, "open")
        print "implicit: " + implicit
        self.assertTrue(implicit, "Failed to retrieve implicit token")

    def test_wrong_scope_token(self):
        wrong_implicit = self.generate_implicit_code_selenium(self.client_id, self.wrong_scope, "open")
        print "wrong_implicit: " + wrong_implicit
        user_info = self.get_user_info(wrong_implicit)
        print "user_info: " + user_info
        self.assertTrue("access_denied" in user_info, "Wrong scope test failed: " + user_info)
'''