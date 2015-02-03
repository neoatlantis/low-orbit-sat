## Low orbit satellite Calculation

This small program provides some tools for calculating satellites running on
low earth orbits. You may supply TLE(Two Line Element) files into the directory
`tlefiles` and begin.

Currently observer position and many other parameters are hardcoded in both
python scripts. It's not hard to find them and change to yours.

And you have to make sure, that TLE file has a filename consistent with it's
first line in content.

This program may be extended in the future to provide instructions for other
systems, such as automatic satellite weather image reception(that's why I was
interested in the committed TLE files), or more(it's python XD).

### Usage

#### Get satellite passes

This gets calculates passes of all satellites in `tlefiles` over the observer.
Just run

    python passes.py

to get it run.

#### Get satellite orbit

Use:

    python orbit.py <PATH TO TLE FILE>

to get a prediction of the specified orbit from now on.
