# Audio Scripts

This script allows the user to play mp3 audio files on a Raspberry Pi.

For wiring, check `/assets`

# Audio Driver
## Installing Dependencies 
```shell
sudo chmod +x ./setup.sh
./setup.sh
```
## How To Import
```python
from RPI-Useful-Python-master.AUDIO.audio_driver import mp3

audio = mp3(files_directory="./AudioFiles/",sample_rate=48000,bit_depth= -16,channels=2,buffer_size=2048)
```
- files_directory = *ABSOLUTE DIRECTORY TO AUDIO FILES*
- sample_rate = *PLAYBACK SMAPLE RATE* (Should match the devices playback sample-rate)
- bit_depth = -*PLAYBACK BIT DEPTH* (Should match the devices playback bit-dpeth)
- channels = *CHANNEL COUNT* (1 = Mono, 2 = Stereo)
- buffer_size = *BUFFEr SIZE*

### play
Play an audio file

```python
audio.play(file_name="test.mp3",volume.0.85)
```

### stop
Stops any playing audio

```python
audio.stop()
```

# Dependencies
- Adafruit pygame - `sudo pip install python-pygame`
