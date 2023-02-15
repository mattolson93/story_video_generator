from transformers import GPT2Tokenizer, OPTForCausalLM

model = OPTForCausalLM.from_pretrained("facebook/opt-6.7b").cuda()
tokenizer = GPT2Tokenizer.from_pretrained("facebook/opt-6.7b")

prompt = "Please enjoy the following children's story I wrote. THE LITTLE GIRL AND HER DOG."
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
generate_ids = model.generate(inputs.input_ids.cuda(), max_length=1024, repetition_penalty=1.2)
output = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
print(output)

extra = "\nSimplify the previous story to only its nouns: "


inputs = tokenizer(output + extra, return_tensors="pt")

# Generate
generate_ids = model.generate(inputs.input_ids.cuda(), max_length=1124, repetition_penalty=1.2)
output = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
print(output)
