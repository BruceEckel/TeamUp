# Description of how it will eventually work

## When you start the program, it:
* Opens to the last generated pairing and shows the date and time that pairing was generated.
  - If no `pairings.txt` exists, creates the file and generates and stores the initial pairing.
* Allows you to move forward and backward through pairings. Moving forward generates a new pairing if one
  doesn't exist.
* Once a new pairing is created, you can't create another new one for 5 minutes unless you override.
* People can be temporarily commented out of the source list when making a pairing, and they will not
  be included in that pairing.
* Pairing sequences are repeatable. That is, if you erase `pairings.txt`, you'll produce the same
  pairings in the same order.
* The pairings are displayed in a grid and the color bar moves to highlight each pair after a specified
  number of seconds.
