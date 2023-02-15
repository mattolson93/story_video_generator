import os
import sys



with open(sys.argv[1], 'r') as file:
    full_story = file.read()

outdir = (os.path.splitext(sys.argv[1]))[0].split("/")[-1] + "_"+sys.argv[2]
os.makedirs(outdir, exist_ok=True)

lines = full_story.split("\n")[0].replace("\"","").replace("!",".")
prompts = []
print("cat << EOF |")
for i, sentence in enumerate(lines.split(".")[:-1]):
    print(f"s{i:03d}|"+sentence + ".")
print("EOF")
print(f"mimic3  --voice en_US/vctk_low --cuda --csv --length-scale {sys.argv[2]} --output-dir {outdir}")
print(f"cd {outdir}")
print('for f in `ls`; do ffmpeg -i $f  -af "adelay=250|100" pad$f ; done')
print(f"cd ..")

