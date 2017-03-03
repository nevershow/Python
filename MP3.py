from pydub import AudioSegment
song = AudioSegment.from_mp3("a.mp3")
song1 = song[:40 * 1000]
song2 = song[75 * 1000:]
song = song1 + song2
song.export("b.mp3", format="mp3")

