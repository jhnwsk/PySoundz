'''
Created on 24-02-2011

@author: johnDonson
'''
import operator, math, wave

class Sound:
    duration_in_ms = 2000                # Let's generate a sine wave that lasts 500ms!
    fundamental_harmonic = 55            # It should be 55Hz.
    samplerate = 44100                # CD quality would be nice.
    
    output = wave.open("cutoff.wav", "wb")          # Write to this file.
    output.setnchannels(1)                          # Make it mono.
    output.setsampwidth(2)                          # Hopefully this makes it 16-bit.
    output.setframerate(samplerate)                 # This should make it the quality specified above.
    duration_in_samples = samplerate * (duration_in_ms / 1000.0) + 1 # Work out the number of samples.
    output.setnframes(duration_in_samples - 1)      # Specify that number.
    output.setcomptype("NONE", "not compressed")    # Don't compress it.
    
    def __init__(self, contents = None):
        self.contents = contents or []
        
    def ramp(self, time, oscs):
        amplitude = 0
        time = time - math.floor(time)
        for x in range(1, int(oscs * 0.001)):        # Change the number of sine waves over time :D Should be similar to increasing the cutoff point on a low pass filter.
            amplitude = amplitude + math.sin(x * 2 * math.pi * time) / x
        amplitude = amplitude * 0.5
        return amplitude
    
    def subtle_lfo(self, time):
        time = time - math.floor(time)
        return math.sin(2 * math.pi * time) * 0.01
    
    def generateWave(self, filters, progress):
        
        percenter = 0
        for time in range(1, int(self.duration_in_samples)):    # Do the magic!
            if int((time / self.duration_in_samples) * 100) != percenter:
                percenter = int((time / self.duration_in_samples) * 100) + 1 
                progress.setValue(percenter)
            osc_1 = self.ramp((1.0 * time * self.fundamental_harmonic) / self.samplerate, time) # Generate stable ramp wave
            osc_2 = self.ramp((2.0 * time * (self.fundamental_harmonic + self.subtle_lfo(time / self.duration_in_samples))) / self.samplerate, time) # Generate unstable ramp wave, an octave up
        
            wavestate = (osc_1 + osc_2) / 2
            wavestate = (wavestate + 1) / 2     # Turn the range from (-1 to 1) to (0 to 1).
            wavestate = int(wavestate * 65535)    # Make it a 16-bit integer.
            wavestate = wavestate + 32768        # Shift the whole thing
            if wavestate > 65535:
                wavestate = wavestate - 65536    # Still shifting
            rightbyte = operator.mod(wavestate, 256)# Get the last eight bits
            leftbyte = (wavestate - rightbyte) / 256# Get the first eight bits
            self.output.writeframes(chr(rightbyte))    # Write the right half
            self.output.writeframes(chr(leftbyte))    # Write the left half
        self.output.close()
