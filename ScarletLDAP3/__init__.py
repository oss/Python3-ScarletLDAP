from ldap3 import (Server, Connection, 
                    SEARCH_SCOPE_WHOLE_SUBTREE, LDAPBindError)

class ScarletLDAP:

    def __init__(self, server, search_base, port,
                    user_srv = ['eden', 'pegasus', 'clam'], 
                        admin_srv = ['rci'], search_params=None):

        self.server    = Server(host=server, port=port, use_ssl=True)
        self.base      = search_base
        self.user_srv  = user_srv
        self.admin_srv = admin_srv

        # set default search parameters
        self.search_params = {
            'filter' : '(uid=%s)',
            'scope'  : SEARCH_SCOPE_WHOLE_SUBTREE,
            'base'   : search_base
        }

        if search_params is not None:

            # update self.search_params from valid keys search_params.keys()
            self.search_params.update(
                { key:val for key,val in search_params.items() 
                  if key in self.search_params.keys() }
            )
        
    def authenticate(self, passwd, netid=None, use_enigma=False, dn=None):
        
        if dn is None:

            if netid is None:
                raise Exception("Must specify either netid or dn as keyword arg")
                
            # establish initial connection to ldap server and bind anonymously
            conn = Connection(self.server, user=netid, auto_bind=True)
       
            # search for dn to authenticate against
            conn.search(
                    search_base   = self.search_params['base'],
                    search_scope  = self.search_params['scope'],
                    search_filter = self.search_params['filter'] % ( netid ),
                    attributes    = ['dn']
            )

            # the user may have an account in any of the servers in server_names
            server_names = self.admin_srv if use_enigma else self.user_srv

            for resp in conn.response:

                # check if dn is associated with a valid account in server_names
                if len( [ s for s in server_names if s in resp['dn'] ] ):
                    dn = resp['dn']
                    break

            if dn is None:
                return False

            conn.unbind()
    
        # attempt to authenticate against dn using passwd
        try:

            conn = Connection(
                        self.server, user=dn,
                        password=passwd,
                        auto_bind=True
            )

        except LDAPBindError:
            return False
    
        conn.unbind()
        return True
