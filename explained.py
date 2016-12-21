import moviepy.editor as mpy
import numpy as np
import matplotlib.pyplot as plt

ui = raw_input("Enter the location of a smallish song like file to convert to a gif: ")

clip = mpy.VideoFileClip(ui)
cut = lambda i: clip.audio.subclip(i,i+1).to_soundarray(fps=22000)
volume = lambda array: np.sqrt(((1.0*array)**2).mean())
volumes = [volume(cut(i)) for i in range(0,int(clip.duration-1))]

#this is the plot of volumes
gvol = plt.plot(volumes)
plt.show()

#this is the plot of averaged volumes
averaged_volumes = np.array([sum(volumes[i:i+10])/10
				for i in range(len(volumes)-10)])
gavgvol = plt.plot(averaged_volumes)
plt.show()

#remember thinking hwo to handle the beginning rise from zero
#and the ending dip to zero in the volumes or avg vol curves?
#well we should really thank the guy who introduced us to this 
#little beauty of a code
increases = np.diff(averaged_volumes)[:-1]>=0
# the above code well do np.diff for all elements in averaged volumes except the last
decreases = np.diff(averaged_volumes)[1:]<=0
# same for decreases but excluding the first element

