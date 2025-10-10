"""
Deepgram Flux Latency Analyzer
Based on: https://deepgram.com/learn/understanding-and-reducing-latency-in-speech-to-text-apis

Measures:
1. Non-transcription latency (network roundtrip)
2. Total latency (full STT pipeline)
3. Transcription latency (model processing time)
"""

import asyncio
import time
import wave
import os
from dotenv import load_dotenv, find_dotenv
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

# Load environment variables
load_dotenv(find_dotenv('.env'))

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Test audio file (you can replace with your own)
TEST_AUDIO_FILE = "test_audio.wav"  # Make sure you have a test WAV file

class LatencyMeasurement:
    def __init__(self):
        self.connection_start = None
        self.connection_established = None
        self.first_audio_sent = None
        self.first_transcript_received = None
        self.transcripts = []
        self.timestamps = []
        
    def reset(self):
        """Reset all measurements for a new test"""
        self.connection_start = None
        self.connection_established = None
        self.first_audio_sent = None
        self.first_transcript_received = None
        self.transcripts = []
        self.timestamps = []


async def measure_network_latency():
    """
    Measure non-transcription latency (network roundtrip to Deepgram)
    This uses a simple connection test to measure network overhead
    """
    print("\n🌐 MEASURING NETWORK LATENCY")
    print("=" * 60)
    
    client = DeepgramClient(DEEPGRAM_API_KEY)
    
    start_time = time.time()
    
    try:
        # Establish connection to Deepgram Flux
        connection = client.listen.live.v("2")
        
        connection_established = False
        
        def on_open(self, open, **kwargs):
            nonlocal connection_established
            if not connection_established:
                connection_established = True
        
        connection.on(LiveTranscriptionEvents.Open, on_open)
        
        # Connect with minimal options
        options = LiveOptions(
            model="flux-general-en",
            encoding="linear16",
            sample_rate=16000,
        )
        
        await connection.start(options)
        
        # Wait for connection to establish
        timeout = 5
        elapsed = 0
        while not connection_established and elapsed < timeout:
            await asyncio.sleep(0.01)
            elapsed += 0.01
        
        connection_time = time.time() - start_time
        
        await connection.finish()
        
        print(f"✅ Connection established in: {connection_time * 1000:.2f} ms")
        print(f"   This is your baseline network latency to Deepgram servers")
        
        return connection_time * 1000  # Return in milliseconds
        
    except Exception as e:
        print(f"❌ Error measuring network latency: {e}")
        return None


async def measure_total_latency(audio_file: str):
    """
    Measure total latency from sending audio to receiving transcription
    """
    print("\n📊 MEASURING TOTAL LATENCY (End-to-End)")
    print("=" * 60)
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        print("   Please provide a test WAV file (16kHz, mono, linear16)")
        return None
    
    client = DeepgramClient(DEEPGRAM_API_KEY)
    connection = client.listen.live.v("2")
    
    measurements = LatencyMeasurement()
    
    def on_open(self, open, **kwargs):
        measurements.connection_established = time.time()
        print(f"🔗 WebSocket connection opened")
    
    def on_message(self, result, **kwargs):
        if result.channel:
            transcript = result.channel.alternatives[0].transcript
            
            if transcript and not measurements.first_transcript_received:
                measurements.first_transcript_received = time.time()
                
                # Calculate latency from first audio sent
                if measurements.first_audio_sent:
                    latency = (measurements.first_transcript_received - measurements.first_audio_sent) * 1000
                    print(f"⚡ First transcript received: {latency:.2f} ms after first audio chunk")
                    print(f"   Transcript: '{transcript}'")
            
            if transcript:
                measurements.transcripts.append(transcript)
                measurements.timestamps.append(time.time())
    
    def on_error(self, error, **kwargs):
        print(f"❌ Error: {error}")
    
    def on_close(self, close, **kwargs):
        print(f"🔒 Connection closed")
    
    # Register event handlers
    connection.on(LiveTranscriptionEvents.Open, on_open)
    connection.on(LiveTranscriptionEvents.Transcript, on_message)
    connection.on(LiveTranscriptionEvents.Error, on_error)
    connection.on(LiveTranscriptionEvents.Close, on_close)
    
    # Configure Flux options
    options = LiveOptions(
        model="flux-general-en",
        encoding="linear16",
        sample_rate=16000,
    )
    
    measurements.connection_start = time.time()
    
    # Start connection
    if not await connection.start(options):
        print("❌ Failed to start connection")
        return None
    
    # Wait for connection to establish
    await asyncio.sleep(0.5)
    
    # Stream audio file
    print(f"🎤 Streaming audio from: {audio_file}")
    
    with wave.open(audio_file, 'rb') as wf:
        sample_rate = wf.getframerate()
        frames_per_chunk = int(sample_rate * 0.2)  # 200ms chunks
        
        chunk_count = 0
        while True:
            data = wf.readframes(frames_per_chunk)
            if not data:
                break
            
            if chunk_count == 0:
                measurements.first_audio_sent = time.time()
                print(f"📤 First audio chunk sent at t=0")
            
            connection.send(data)
            chunk_count += 1
            
            # Simulate real-time streaming
            await asyncio.sleep(0.2)
    
    # Wait for final transcriptions
    await asyncio.sleep(2)
    
    # Close connection
    await connection.finish()
    
    # Calculate metrics
    if measurements.first_transcript_received and measurements.first_audio_sent:
        total_latency = (measurements.first_transcript_received - measurements.first_audio_sent) * 1000
        
        print(f"\n📈 TOTAL LATENCY BREAKDOWN:")
        print(f"   Total latency (first audio → first transcript): {total_latency:.2f} ms")
        print(f"   Number of transcripts received: {len(measurements.transcripts)}")
        
        return total_latency
    else:
        print("⚠️ No transcripts received")
        return None


async def main():
    """
    Main function to run all latency measurements
    """
    print("\n" + "=" * 60)
    print("🔬 DEEPGRAM FLUX LATENCY ANALYZER")
    print("=" * 60)
    
    # Step 1: Measure network latency
    network_latency = await measure_network_latency()
    
    # Step 2: Measure total latency
    # You need to provide a test audio file
    if os.path.exists(TEST_AUDIO_FILE):
        total_latency = await measure_total_latency(TEST_AUDIO_FILE)
        
        # Step 3: Calculate transcription latency
        if network_latency and total_latency:
            print("\n🎯 FINAL LATENCY BREAKDOWN")
            print("=" * 60)
            print(f"Network latency (roundtrip):    {network_latency:.2f} ms")
            print(f"Total latency (end-to-end):     {total_latency:.2f} ms")
            
            # Transcription latency = Total - (Network/2)
            # We divide network by 2 because network latency is roundtrip
            transcription_latency = total_latency - (network_latency / 2)
            print(f"Transcription latency (model):  {transcription_latency:.2f} ms")
            print("=" * 60)
            
            print(f"\n💡 INTERPRETATION:")
            print(f"   • {network_latency:.0f}ms is your network overhead")
            print(f"   • {transcription_latency:.0f}ms is Flux model processing time")
            print(f"   • Total time from speech → text: {total_latency:.0f}ms")
            
            # Compare to Deepgram's advertised ~300ms
            if transcription_latency < 350:
                print(f"   ✅ Flux is performing as expected (~300ms target)")
            elif transcription_latency < 500:
                print(f"   ⚠️ Flux is slightly slower than expected (~300ms target)")
            else:
                print(f"   ❌ Flux is significantly slower than expected (~300ms target)")
    else:
        print(f"\n⚠️ Test audio file not found: {TEST_AUDIO_FILE}")
        print("   Create a test WAV file to measure total latency")
        print("   Requirements: 16kHz sample rate, mono, linear16 encoding")
        print("\n   You can generate one with:")
        print(f"   ffmpeg -i your_audio.mp3 -ar 16000 -ac 1 -f wav {TEST_AUDIO_FILE}")


if __name__ == "__main__":
    asyncio.run(main())

