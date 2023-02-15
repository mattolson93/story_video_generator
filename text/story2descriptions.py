from transformers import GPT2Tokenizer, OPTForCausalLM
import sys

model = OPTForCausalLM.from_pretrained("facebook/opt-6.7b").cuda()
tokenizer = GPT2Tokenizer.from_pretrained("facebook/opt-6.7b")

import pdb; pdb.set_trace()
with open(sys.argv[1], 'r') as file:
    full_story = file.read().replace('\n', '')

full_story_len = tokenizer(full_story, return_tensors="pt")['input_ids'].shape[1]

senetences = full_story.split(".")

outputs = []

for sentence in senetences:

    extra = f"\nThe following is a picture, in some detail, from the previous story's sentence \"{sentence} \":" 

    inputs = tokenizer(full_story + extra, return_tensors="pt")

    # Generate
    generate_ids = model.generate(inputs.input_ids.cuda(), max_length=full_story_len + 50, repetition_penalty=1.5)
    output = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    outputs.append(output)

print(outputs)
