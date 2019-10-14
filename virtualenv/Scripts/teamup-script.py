#!C:\Users\Bruce\OneDrive\Documents\Git\TeamUp\virtualenv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'teamup==0.1.0','console_scripts','teamup'
__requires__ = 'teamup==0.1.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('teamup==0.1.0', 'console_scripts', 'teamup')()
    )
