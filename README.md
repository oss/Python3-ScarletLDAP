Python3-ScarletLDAP
===================
OSS doesn't always authenticate with LDAP. 

But when it does, it uses __Python3.3__.

Virtual Environment
-------------------

To set up development environment, just run:

    $ ./setup.sh

### The following packages may need to be installed using yum:
- python3-devel
- openldap-devel

Test Code
---------

To test the code, run:

	$ . env/bin/activate
	$ ./test

You will be prompted to enter a netid, password, and whether or not
you wish to authenticate using an enigma card.

The test script will then display "Success!" if you have successfully
authenticated, and "Failure" if you have provided invalid credentials.

