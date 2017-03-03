from moviepy.editor import VideoFileClip, concatenate_videoclips
clip = VideoFileClip("Memory.mov")
clip1 = clip.subclip(2, 18)
clip2 = clip.subclip(32, 34)
clip3 = clip.subclip(42, 150)
clip4 = clip.subclip(175, clip.end)
final_clip = concatenate_videoclips([clip1,clip2,clip3,clip4])
final_clip.write_videofile("final.mp4")
