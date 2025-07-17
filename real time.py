# Record, Denoise, Enhance and Play Speech
#
# This script first records background noise, then records your speech.
# It then performs two steps:
# 1. Denoises the audio to remove background noise.
# 2. Enhances the cleaned speech by boosting key voice frequencies.
# Finally, it plays the original, denoised, and enhanced audio for comparison.
#
# Installation:
# You need to install the following libraries. You can do this by running:
# pip install sounddevice noisereduce numpy scipy
#
# On Linux, you might need to install PortAudio development libraries:
# sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev

import sounddevice as sd
import numpy as np
import noisereduce as nr
import time
from scipy.signal import butter, lfilter

# --- Configuration ---
# You can adjust these parameters to fine-tune the performance.
SAMPLE_RATE = 16000  # Sample rate in Hz. 16000 is common for speech.
NOISE_CAPTURE_DURATION = 3 # Duration in seconds to capture initial background noise.
RECORD_DURATION = 5 # Duration in seconds for the main audio recording.

def enhance_voice(audio, sample_rate):
    """
    Enhances the voice by applying a band-pass filter to focus on speech frequencies.
    Human speech is typically in the 300 Hz to 3400 Hz range.
    """
    lowcut = 300.0
    highcut = 3400.0
    
    # Design a Butterworth band-pass filter.
    # The order (nyq_rate) determines the steepness of the cutoff.
    nyq_rate = sample_rate / 2.0
    low = lowcut / nyq_rate
    high = highcut / nyq_rate
    b, a = butter(2, [low, high], btype='band')
    
    # Apply the filter to the audio signal.
    enhanced_audio = lfilter(b, a, audio)
    return enhanced_audio

def main():
    """
    Main function to run the record, denoise, enhance, and play process.
    """
    # --- 1. Capture Initial Noise Profile ---
    print("Starting audio enhancer application.")
    print(f"Please be quiet for {NOISE_CAPTURE_DURATION} seconds to capture the background noise profile...")
    try:
        # Record audio for the noise profile
        noise_capture = sd.rec(int(NOISE_CAPTURE_DURATION * SAMPLE_RATE),
                               samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait() # Wait for the recording to complete.
        noise_clip = noise_capture.flatten()
        print("Noise profile captured successfully.")
    except Exception as e:
        print(f"An error occurred during noise capture: {e}")
        return

    # --- 2. Record Speech ---
    print(f"\nGet ready to speak. Recording for {RECORD_DURATION} seconds...")
    time.sleep(1) # Give user a moment to prepare
    try:
        # Record the main audio
        recorded_audio = sd.rec(int(RECORD_DURATION * SAMPLE_RATE),
                                samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait() # Wait for the recording to complete.
        recorded_audio_mono = recorded_audio.flatten()
        print("Recording finished.")
    except Exception as e:
        print(f"An error occurred during recording: {e}")
        return

    # --- 3. Denoise the Recorded Audio ---
    print("\nDenoising the recorded audio...")
    reduced_noise_audio = nr.reduce_noise(y=recorded_audio_mono, 
                                          sr=SAMPLE_RATE, 
                                          y_noise=noise_clip, 
                                          prop_decrease=1.0, 
                                          stationary=True)
    print("Denoising complete.")

    # --- 4. Enhance the Denoised Voice ---
    print("\nEnhancing the voice signal...")
    enhanced_audio = enhance_voice(reduced_noise_audio, SAMPLE_RATE)
    print("Voice enhancement complete.")

    # --- 5. Play Back Audio for Comparison ---
    print("\nPlaying original audio...")
    try:
        sd.play(recorded_audio, SAMPLE_RATE)
        sd.wait()
    except Exception as e:
        print(f"An error occurred during playback of original audio: {e}")
        return
        
    time.sleep(1) # Pause between playbacks

    print("\nPlaying denoised audio...")
    try:
        sd.play(reduced_noise_audio, SAMPLE_RATE)
        sd.wait()
    except Exception as e:
        print(f"An error occurred during playback of denoised audio: {e}")
        return
        
    time.sleep(1) # Pause between playbacks
    
    print("\nPlaying enhanced audio...")
    try:
        sd.play(enhanced_audio, SAMPLE_RATE)
        sd.wait()
    except Exception as e:
        print(f"An error occurred during playback of enhanced audio: {e}")
        return

    print("\nApplication finished.")


if __name__ == "__main__":
    main()
                                                      