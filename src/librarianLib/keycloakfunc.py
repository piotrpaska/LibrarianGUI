import keycloak

class KeycloakLib():

    def __init__(self, url, realm, clientId, clientSecret) -> None:
        
        self.keycloakOpenId = keycloak.KeycloakOpenID(server_url=url,
                                                      realm_name=realm,
                                                      client_id=clientId,
                                                      client_secret_key=clientSecret)
        
    
    def login(self, username, password):
        try:
            token = self.keycloakOpenId.token(username, password)
            return True, token
        except:
            return False, None


    def checkToken(self, token):
        introspect = self.keycloakOpenId.introspect(token['access_token'])

        if introspect['active'] is True:
            return True
        else:
            return False