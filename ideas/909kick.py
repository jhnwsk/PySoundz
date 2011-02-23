#! /usr/local/bin/python2.2

# Vaguely 909-esque kick drum

import operator, math, wave

duration_in_ms = 200				# Last 200ms
fundamental_harmonic = 160			# Start at 160Hz.
samplerate = 44100				# CD quality would be nice.

output = wave.open("909kick.wav", "wb")		# Write to this file.
duration_in_samples = samplerate * (duration_in_ms / 1000.0) + 1 # Work out the number of samples.
output.setparams((1, 2, samplerate, duration_in_samples - 1, "NONE", "not compressed")) # Mono, 16-bit, the samplerate selected, the right length, no compression.

def env_decay(time):
	if (time > 1):
		amplitude = 0
	else:
		amplitude = 1 - (math.sin(time * 0.5 * math.pi)) # Time * 2 * pi,  then * that by 0.25 to only get the first quarter. Subtract that from 1 so the output starts at 1 and decays to 0.
	return amplitude

for time in range(1, duration_in_samples):	# Do the magic!
	frequency = fundamental_harmonic * env_decay(time / (duration_in_samples * 3)) # I can't for the life of me work out why the decay needs to be three times the length of the actual sample
	wavestate = math.sin((math.pi * 2 * time * frequency) / samplerate) # Actually generate the sine wave
	wavestate = wavestate * env_decay(time / duration_in_samples) # Make it go quieter as time goes on
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

