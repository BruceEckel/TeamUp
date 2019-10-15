
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

## Usage

In `demo/html` you can find example pairings which you can open in your
browser.

When the green bar moves onto your name, you raise your hand and look for the
other person(s) in the room who've also raised their hand. That way you don't
have to know people's names to find them. I've used this in workshops and it
works very well; it gets people working with each other and knowing each other,
then you move them onto other people for the next exercise. The round-robin
algorithm keeps matching people with new people until everyone's been matched
with everyone else, then cycles back and starts over.
