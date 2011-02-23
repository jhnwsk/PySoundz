#! /usr/local/bin/python2.2

import sys, operator, math, wave, mod_synth

if len(sys.argv) < 2:
	print "Usage: fs-101 frequency waveform harmonic mix filter-release"
	sys.exit(1)

# Settings from the command line:

frequency = int(sys.argv[1])

waveform = sys.argv[2]

harmonic = int(sys.argv[3])

mix = int(sys.argv[4])

filter_release = int(sys.argv[5])

# Settings you won't want to change often:

samplerate = 44100				# CD quality would be nice.

output = wave.open("fs-101.wav", "wb")		# Write to this file.
output.setnchannels(1)				# Make it mono.
output.setsampwidth(2)				# Hopefully this makes it 16-bit.
output.setframerate(samplerate)			# This should make it the quality specified above.
duration_in_samples = samplerate * (filter_release / 1000.0) + 1 # Work out the number of samples.
output.setnframes(duration_in_samples - 1)	# Specify that number.
output.setcomptype("NONE", "not compressed")	# Don't compress it.

percenter = 0
for time in range(1, duration_in_samples):	# Do the magic!
	if int((time / duration_in_samples) * 100) != percenter:
		percenter = int((time / duration_in_samples) * 100)
		print percenter, "%"
	osc_1 = mod_synth.osc_sawtooth((1.0 * time * frequency) / samplerate, 1 - (time / duration_in_samples)) # Generate first wave. This should be changed to take "waveform" into account, and to use "filter_attack" and "filter_release".
	osc_2 = mod_synth.osc_sawtooth((1.0 * harmonic * time * (frequency)) / samplerate, 1 - (time / duration_in_samples)) # Generate second wave. Change as above.

	wavestate = (osc_1 + osc_2) / 2		# Mix the two waveforms together equally. This should be changed to take "mix" into account.
	wavestate = (wavestate + 1) / 2 	# Turn the range from [-1 to 1] to [0 to 1].
	wavestate = int(wavestate * 65535)	# Make it a 16-bit integer.
	wavestate = wavestate + 32768		# Shift the whole thing
	if wavestate > 65535:
		wavestate = wavestate - 65536	# Still shifting
	rightbyte = operator.mod(wavestate, 256)# Get the last eight bits
	leftbyte = (wavestate - rightbyte) / 256# Get the first eight bits
	output.writeframes(chr(rightbyte))	# Write the right half
	output.writeframes(chr(leftbyte))	# Write the left half
output.close()

