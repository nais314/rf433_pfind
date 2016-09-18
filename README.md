# rf433_pfind
rf 433 "doorbell" signal pattern finder python3 tk

program for analysing rf signal records
based on the work of http://theforce.dk

usage: 
main program file: pfind_tk.py
(copy the recordings from the arduino ide serial monitor to a .txt file.)
select the file, hit GO!
play with min/max sample sizes

story:
i use raspberry pi or nodemcu to switch 433mhz remote wall sockets on or off.
i used rcswitch to record/replay signals, while i came across a device, that not worked such way.
i had to find another way to record and playback.
theforce.dk had a way, to use an arduinos analogRead method to capture LOW/HIGH signal durations.
analogRead takes 100ms to complete, so the results should be multiplied x100..x130.

this program normalizes and extracts repeating signals from a txt file, wich created from the output of the arduino sketch.

it is not throughly optimised for the task, only a little bit - the last part of the analysis is to crop the patterns at the first occurence of the highest signal, wich in this usecase is the SYNC signal.
this could be reached other ways, but it needs more time (analysing with lower sample sizes, or finding sub-patterns in the patterns )

the current method is, to find patterns from LONG to SMALL length, 
after that delete the small patterns, wich are part of larger patterns,
see if patterns could be expanded (occurance[1]'s next byte == occurance[2]'s next byte? then the pattern continues).
some functions are only for reducing results.

the fun will continue, as i try to make it a more generic pattern finder.

