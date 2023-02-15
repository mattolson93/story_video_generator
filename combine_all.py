import os
import sys
import subprocess

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--pics", help="echo the string you use here")
parser.add_argument("--voices", help="echo the string you use here")
parser.add_argument("--mp3", help="echo the string you use here")
args = parser.parse_args()


final_file = [i for i in args.pics.split("/") if i][-1] + ".mp4"

#get all the voice files
voices = os.listdir(args.voices)
#get all the ken-burns 3d
pics = os.listdir(args.pics)
pics.sort()
voices.sort()
pics   = [p for p in pics if "mp4" in p]
voices = [v for v in voices if "pads" in v]
#import pdb; pdb.set_trace()
if len(pics) != len(voices):
    exit(f"error pics {len(pics)} !=  voices {len(voices)}")
#sort all of the above
#line them up
out_files = []
for i, (p, v) in enumerate(zip(pics,voices)):
    p = os.path.join(args.pics,p)
    v = os.path.join(args.voices,v)
    out = f"tempfiles/{i}.mp4"
    ffmpeg_cmd = f'ffmpeg -y -i {p} -i {v} -filter_complex "[1:0]apad" -shortest {out}'
    print(ffmpeg_cmd)
    subprocess.call(ffmpeg_cmd , shell=True)
    out_files.append(f"{i}.mp4")

#ffmpeg concate them all

filelist_txt = "./tempfiles/files.txt"
  
with open(filelist_txt, 'w') as tmpf:
    for f in out_files:
        tmpf.write(f"file '{f}'\n")
ffmpeg_cmd = f"ffmpeg -y -f concat -safe 0 -i {filelist_txt} -c copy tempfiles/mergedVideo.mp4"
#print(ffmpeg_cmd)
subprocess.call(ffmpeg_cmd, shell=True)
subprocess.call("ffmpeg -y -i tempfiles/mergedVideo.mp4 tempfiles/mergedvideo_audio_only.mp3", shell=True)
#import pdb; pdb.set_trace()
subprocess.call(f'ffmpeg -y -i tempfiles/mergedvideo_audio_only.mp3 -i {args.mp3}  -filter_complex amerge=inputs=2 -ac 2 tempfiles/merged.mp3', shell=True)

ffmpeg_cmd = f"ffmpeg -y -i tempfiles/mergedVideo.mp4 -i tempfiles/merged.mp3 -map 0:v -map 1:a -c:v copy -shortest {final_file}"
print(ffmpeg_cmd)
subprocess.call(ffmpeg_cmd, shell=True)


#combine mp3 with the all!
