#!env/bin/python3.3
from ScarletLDAP3 import ScarletLDAP
from getpass import getpass


SERVER      = 'ldaps://ldap.nbcs.rutgers.edu'
SEARCH_BASE = 'dc=rutgers,dc=edu'
PORT        =  636

def main():

    ld = ScarletLDAP(SERVER, SEARCH_BASE, PORT)

    netid      = input("Enter netid: ")
    passwd     = getpass("Enter passwd: ")
    use_enigma = input("Enigmatized? Enter y/n: ") == 'y'

    auth_success = ld.authenticate(
                        netid=netid,
                        passwd=passwd,
                        use_enigma=use_enigma
                   )

    if auth_success:
        print('Success!')
    else:
        print('Failure')

if __name__ == '__main__':

    main()
