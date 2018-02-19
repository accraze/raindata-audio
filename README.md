# raindata-audio

Data Sonification of hourly rain data from Portland, OR.

## Usage

Run the `init.ck` chuck code from miniAudicle.

In another terminal window, run the python script:
```
$ python controlller.py
```

The Python controller will read in the hourly rain data from PDX,
generate a twelve tone melody based on each value and then pass
those notes over OSC.

The chuck code has two parts. The OSC arbiter (`ChucK2OSC.ck`) will receive
all OSC events on port 6449 (address `/weather`) and then pass them to our
sound making objects that are listening on port 6448. The sound making objects
will then generate a synthesis based on the rain data.