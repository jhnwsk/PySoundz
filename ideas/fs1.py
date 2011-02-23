#! /usr/local/bin/python2.2

import operator, math, wave, mod_synth

# Settings you'll want to change on the command line later:

decay_in_ms = 500				# Generate a sound that lasts 500ms.
fundamental_harmonic = 55			# It should be 55Hz.
osc2_shift = 2					# OSC2 should be twice the pitch of OSC1

# Settings you won't want to change often:

samplerate = 44100				# CD quality would be nice.

duration_in_ms = decay_in_ms			# This'll get more complex if I use an ADSR contour generator
output = wave.open("fs-1.wav", "wb")		# Write to this file.
output.setnchannels(1)				# Make it mono.
output.setsampwidth(2)				# Hopefully this makes it 16-bit.
output.setframerate(samplerate)			# This should make it the quality specified above.
duration_in_samples = samplerate * (duration_in_ms / 1000.0) + 1 # Work out the number of samples.
output.setnframes(duration_in_samples - 1)	# Specify that number.
output.setcomptype("NONE", "not compressed")	# Don't compress it.

percenter = 0
for time in range(1, duration_in_samples):	# Do the magic!
	if int((time / duration_in_samples) * 100) != percenter:
		percenter = int((time / duration_in_samples) * 100)
		print percenter
	osc_1 = mod_synth.osc_sawtooth((1.0 * time * fundamental_harmonic) / samplerate, 1 - (time / duration_in_samples)) # Generate first wave
	osc_2 = mod_synth.osc_sawtooth((1.0 * osc2_shift * time * (fundamental_harmonic)) / samplerate, 1 - (time / duration_in_samples)) # Generate second wave

	wavestate = (osc_1 + osc_2) / 2		# Mix the two waveforms together equally
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

