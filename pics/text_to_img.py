from diffusers import StableDiffusionPipeline
import os
import sys
from tqdm import tqdm

TOKEN=os.environ.get("HF_API_TOKEN")

engineering = [
    " cute, adorable, funko pop, digital art, artstation, high detail, cinematic photo"
    " extremely detailed, textured, high detail, 4k, 8k, 10k, 20k, 40k, painted by Rossdraws",
    " artist: Stephen McCranie, 3d, unreal engine, unreal, 3d art, high detail, real time, 4k, 8k, resolution",
    " by Abdul-Rahman Munif, published in the book of short stories \"The Chronicles of a Vanished\"",
    " conceptual art, detailed, artstation, high resolution, illustration by andrew miller, walter foster, kyle bailey, mario gavrilovic, matt koloska, richard isaacson",
    " 8k, concept art, high detail, illustration, artstation, 4k, uHD, ultra hd, ultra high definition, art and rendering, realistic, stylized, by kuvshinov ilya, james",
    " shallow depth of field, shifting perspective, detail, focus, concept art, illustration by Daniel Lieske, made for the Brothers Grimm, by Greg Rutkowski",
    " by Andrey Kuzkin, stunning, surreal, conceptual, surreal art, digital painting, surreal fantasy, digital art, digital painting, surreal art, fantasy art, fantasy art, 8k, fantasy illustration, photorealistic",
]

#if not 0 <= int(sys.argv[2]) <= len(engineering): exit("argv2 needs to be int <= ", len(engineering))

#ec = engineering[int(sys.argv[2]) % len(engineering)] 


with open(sys.argv[1], 'r') as file:
    full_story = file.read()
outdir = (os.path.splitext(sys.argv[1]))[0].split("/")[-1] 
os.makedirs(outdir, exist_ok=True)




lines = full_story.split("\n")
prompts = []
for l in lines[1:]:
    if len(l) > 1:
        prompts.append(l)



pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=TOKEN)
pipe = pipe.to("cuda:0")

for i, prompt in tqdm(enumerate(prompts)):
    for j in tqdm(range(10)):
        ec = engineering[j % len(engineering)]
    
        out = pipe(prompt + ec, seed = ec)['sample'][0]

        out.save(os.path.join(outdir, f"img{i:03d}_seed{j:03d}.png"))
