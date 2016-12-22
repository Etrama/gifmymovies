import moviepy.editor as mpy
import numpy as np

ui = raw_input("Enter the location of a smallish song like file to convert to a gif: ")
clip = mpy.VideoFileClip(ui)
#clip.preview()
#how to close a clip when it's running in pygame?
#how to save matplotlib images as well as display them, not necessarily in your hdd, but as an object or sth?
#write code to extract the bass heavy parts of a song, like in let it happen
#why does write_gif not work with program='imageio'?

cut = lambda i: clip.audio.subclip(i,i+1).to_soundarray(fps=22000)
volume = lambda array: np.sqrt(((1.0*array)**2).mean())
volumes = [volume(cut(i)) for i in range(0,int(clip.duration-1))]

averaged_volumes = np.array([sum(volumes[i:i+6])/6
				for i in range(len(volumes)-6)])

increases = np.diff(averaged_volumes)[:-1]>=0
decreases = np.diff(averaged_volumes)[1:]<=0
peaks_times = (increases*decreases).nonzero()[0]
peaks_vols = averaged_volumes[peaks_times]
peaks_times = peaks_times[peaks_vols>np.percentile(peaks_vols,80)]

final_times = [peaks_times[0]]
for t in peaks_times:
	if(t - final_times[-1]) < 20:
		if averaged_volumes[t] > averaged_volumes[final_times[-1]]:
			final_times[-1] = t
	else:
            final_times.append(t)

final = mpy.concatenate([clip.subclip(max(t-2.5,0),min(t+2.5, clip.duration))
				 for t in final_times])

ui2 = raw_input("Enter location and name of final clip, eg: d:/finalclip.mp4 ")
final.write_videofile(ui2)
dispclip = mpy.VideoFileClip(ui2)
#dispclip.preview()

print("Converting .mp4 to a .gif file: ")
ui3 = raw_input("Enter gif file location and name to store, eg:d:/test.gif ")
dispclip.write_gif(ui3, fps=None, program='ffmpeg',verbose=True, loop=0, dispose=False, colors=None, tempfiles=False)
#gifclip = mpy.VideoFileClip(ui3)
#gifclip.preview(), pygame can't handle animated gifs.
