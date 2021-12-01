#!/usr/bin/python3
"""Set e107 admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import sys
import getopt
import hashlib
from datetime import datetime
from time import mktime
from mysqlconf import MySQL

from libinithooks import inithooks_cache
from libinithooks.dialog_wrapper import Dialog

def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s [options]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError as e:
        usage(e)

    password = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "e107 Password",
            "Enter new password for the e107 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "e107 Email",
            "Enter email address for the e107 'admin' account.",
            "admin@example.com")

    inithooks_cache.write('APP_EMAIL', email)

    hash = hashlib.md5(password.encode('utf8')).hexdigest()
    timestamp = int(mktime(datetime.now().timetuple()))

    m = MySQL()
    m.execute('UPDATE e107.e107_user SET user_password=%s WHERE user_loginname=\"admin\";', (hash,))
    m.execute('UPDATE e107.e107_user SET user_email=%s WHERE user_loginname=\"admin\";', (email,))
    m.execute('UPDATE e107.e107_user SET user_pwchange=%s WHERE user_loginname=\"admin\";', (timestamp,))

if __name__ == "__main__":
    main()

