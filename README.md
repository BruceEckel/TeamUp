
# TeamUp

> A tool for pairing people during a workshop or seminar, so everyone eventually works with everyone.

To eliminate that terrible moment when the workshop leader says "find a partner."

## Install

1. Clone this project or download and unpack the zip file.
2. Run `python setup.py install`
3. `teamup` should now run from any directory
4. You need an `Attendees.txt` file with one name per line in the directory where you run `teamup`.
5. If you want to run the tests:
   - Run `venv.bat` from https://github.com/BruceEckel/tools to set up and/or enter virtualenv.
   - `pip install pytest`
   - Move to the `tests` directory
   - Run `pytest` and everything should complete successfully
