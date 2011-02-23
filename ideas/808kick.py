#! /usr/local/bin/python2.2

# Vaguely 808-esque kick drum

import operator, math, wave

duration_in_ms = 300				# Last 300ms
fundamental_harmonic = 50			# Start at 50Hz.
samplerate = 44100				# CD quality would be nice.

output = wave.open("808kick.wav", "wb")		# Write to this file.
duration_in_samples = samplerate * (duration_in_ms / 1000.0) + 1 # Work out the number of samples.
output.setparams((1, 2, samplerate, duration_in_samples - 1, "NONE", "not compressed")) # Mono, 16-bit, the samplerate selected, the right length, no compression.

def env_decay(time):				# Outputs a decay envelope
	if (time > 1):
		amplitude = 0
	else:
		amplitude = 1 - (math.sin(time * 0.5 * math.pi)) # Time * 2 * pi,  then * that by 0.25 to only get the first quarter. Subtract that from 1 so the output starts at 1 and decays to 0.
	return amplitude

def osc_triangle(time):				# Outputs a triangle wave
	amplitude = 0
	time = time - math.floor(time)
	for x in range(1, 64):
		amplitude = amplitude + math.sin((x * 2 - 1) * 2 * math.pi * time) / math.pow(2, (x * 2 - 1))
	amplitude = amplitude * 0.5
	return amplitude

single_cycle_in_ms = 1000 / fundamental_harmonic

for time in range(1, (samplerate / 1000) * single_cycle_in_ms): # Make a triangle wave. This should be one cycle long.
	wavestate = osc_triangle((time * fundamental_harmonic) / samplerate) # Make the triangle wave
	wavestate = (wavestate + 1) / 2 	# Turn the range from (-1 to 1) to (0 to 1).
	wavestate = int(wavestate * 65535)	# Make it a 16-bit integer.
	wavestate = wavestate + 32768		# Shift the whole thing
	if wavestate > 65535:
		wavestate = wavestate - 65536	# Still shifting
	rightbyte = operator.mod(wavestate, 256)# Get the last eight bits
	leftbyte = (wavestate - rightbyte) / 256# Get the first eight bits
	output.writeframes(chr(rightbyte))	# Write the right half
	output.writeframes(chr(leftbyte))	# Write the left half

for time in range(1, duration_in_samples - ((single_cycle_in_ms / 1000) * samplerate)): # Make the sine wave. This length should miss off the first cycle.
	frequency = fundamental_harmonic # Eventually make the pitch go down *slightly* over time
	wavestate = math.sin((math.pi * 2 * time * frequency) / samplerate) # Actually generate the sine wave
	wavestate = wavestate * math.pow(env_decay(time / duration_in_samples), 2) # Attenuate the sound over time. Squre the curve to steepen it.
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

