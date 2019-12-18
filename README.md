# Wiki-Philosophy
## A script to pick a random (Or not!) Wikipedia article and follow the first link in each article until it finds Philosophy.
## How to run:
1. Put wiki.py and philosophy.py in the same directory.
2. Run philosophy.py from the terminal with a number n as an argument. The search will run on a new random page n times and display the results.

I'll add the ability to specify a certain page later. Currently, you can import philosophy in a file and then instantiate the object with a URL as the parameter to run the search starting from that page. The .result property will run the search when accessed and return the success/failure message as a string.
