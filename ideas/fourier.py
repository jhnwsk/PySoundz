#! /usr/local/bin/python2.2

# Pure 8-harmonic tone

import operator, math, wave

duration_in_ms = 2000				# Last 2000ms
fundamental_harmonic = 55			# Start at 55Hz.
samplerate = 44100				# CD quality would be nice.

output = wave.open("pure.wav", "wb")		# Write to this file.
duration_in_samples = samplerate * (duration_in_ms / 1000.0) + 1 # Work out the number of samples.
output.setparams((1, 2, samplerate, duration_in_samples - 1, "NONE", "not compressed")) # Mono, 16-bit, the samplerate selected, the right length, no compression.

def osc_triangle(time):				# Outputs a triangle wave
	amplitude = 0
	time = time - math.floor(time)
	for x in range(1, 8):
		amplitude = amplitude + math.sin((x * 2 - 1) * 2 * math.pi * time) / math.pow(2, (x * 2 - 1))
	return amplitude

for time in range(1, duration_in_samples): # Make the waveform.
	wavestate = osc_triangle((1.0 * time * fundamental_harmonic) / samplerate) # Actually generate the waveform

	wavestate = (wavestate + 1) / 2 	# Turn the range from (-1 to 1) to (0 to 1).
	wavestate = int(wavestate * 65535)	# Make it a 16-bit integer.
	wavestate = wavestate + 32768		# Shift the whole thing
	if wavestate > 65535:
		wavestate = wavestate - 65536	# Still shifting
	rightbyte = operator.mod(wavestate, 256)# Get the last eight bits
	leftbyte = (wavestate - rightbyte) / 256# Get the first eight bits
	output.writeframes(chr(rightbyte))	# Write the right half
	output.writeframes(chr(leftbyte))	# Write the left half
output.close()

