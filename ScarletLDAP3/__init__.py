from ldap3 import (Server, Connection, 
                    SEARCH_SCOPE_WHOLE_SUBTREE, LDAPBindError)

class ScarletLDAP:

    def __init__(self, server, search_base, port,
             user_srv = ['eden', 'pegasus', 'clam'], admin_srv = ['rci']):

        self.server    = Server(host=server, port=port, use_ssl=True)
        self.base      = search_base
        self.user_srv  = user_srv
        self.admin_srv = admin_srv

    def authenticate(self, netid, passwd, use_enigma=False):
        
        # establish initial connection to ldap server and bind anonymously
        conn = Connection(self.server, user=netid, auto_bind=True)
       
        # search for dn to authenticate against
        conn.search(
                search_base   = self.base,
                search_scope  = SEARCH_SCOPE_WHOLE_SUBTREE,
                search_filter = '(uid='+netid+')',
                attributes    = ['dn']
        )

        # the user may have an account in any of the servers in server_names
        server_names = self.admin_srv if use_enigma else self.user_srv

        dn = None
        for resp in conn.response:

            # check if dn is associated with a valid account in server_names
            if len( [ s for s in server_names if s in resp['dn'] ] ):
                dn = resp['dn']
                break

        if dn == None:
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
