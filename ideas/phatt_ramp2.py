#! /usr/local/bin/python2.2

import math, wave

duration_in_ms = 2000				# Let's generate a sine wave that lasts 500ms!
fundamental_harmonic = 55			# It should be 55Hz.
samplerate = 44100				# CD quality would be nice.

output = wave.open("pr.wav", "wb")            # Write to this file.
output.setnchannels(1)                          # Make it mono.
output.setsampwidth(1)                          # Hopefully this makes it 8-bit.
output.setframerate(samplerate)                 # This should make it the quality specified above.
duration_in_samples = samplerate * (duration_in_ms / 1000.0) + 1 # Work out the number of samples.
output.setnframes(duration_in_samples - 1)	# Specify that number.
output.setcomptype("NONE", "not compressed")    # Don't compress it.

def ramp(time):
	time = time - math.floor(time)
	amplitude = 1 - (time * 2)
	return amplitude

def subtle_lfo(time):
	time = time - math.floor(time)
	return math.sin(2 * math.pi * time) * 0.01


for time in range(1, duration_in_samples):	# Do the magic!
	osc_1 = ramp((1.0 * time * fundamental_harmonic) / samplerate) # Generate stable ramp wave
	osc_2 = ramp((2.0 * time * (fundamental_harmonic + subtle_lfo(time / duration_in_samples))) / samplerate) # Generate unstable ramp wave, an octave up

	wavestate = (osc_1 + osc_2) / 2
	wavestate = (wavestate + 1) / 2 	# Turn the range from (-1 to 1) to (0 to 1).
	wavestate = int(wavestate * 255)	# Make it an 8-bit integer.
	output.writeframes(chr(wavestate))	# Write it to the file!
output.close()

