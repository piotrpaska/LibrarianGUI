import keycloak

class KeycloakLib():

    def __init__(self, url, realm, clientId, clientSecret, adminUsername, adminPass, roles) -> None:
        
        self.keycloakOpenId = keycloak.KeycloakOpenID(server_url=url,
                                                      realm_name=realm,
                                                      client_id=clientId,
                                                      client_secret_key=clientSecret)
        
        self.keycloakAdmin = keycloak.KeycloakAdmin(server_url=url,
                                                    username=adminUsername,
                                                    password=adminPass,
                                                    realm_name=realm,
                                                    verify=True)
        
        self.roles = roles
        
    
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
        
    def checkRole(self, username, roleLevel: int):
        userId = self.keycloakAdmin.get_user_id(username)

        userRoles = self.keycloakAdmin.get_realm_roles_of_user(userId)

        includedRoles = []

        if roleLevel == 0:
            includedRoles = self.roles[0:3]
        elif roleLevel == 1:
            includedRoles = self.roles[1:3]
        elif roleLevel == 2:
            includedRoles = self.roles[2:3]

        unAllowedRoles = 0
        for role in userRoles:
            if role['name'] in includedRoles:
                return True
            else:
                unAllowedRoles += 1
        
        if unAllowedRoles == 0:
            return False