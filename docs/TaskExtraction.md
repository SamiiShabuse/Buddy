
Question: What should the extraction process look like?

# Option 1:
Use generative ai read text and bucket tasks accrodingly.

## Pros:
- Low complexity
- Easy to setup
- Works with abstract text
## Cons:
- Expensive especially when scaling up
- Potentially unreliable

# Option 2:
Use zero-shot-classifcation to categorize text, and then based on category parse tasks through various unique means

## Pros:
- Lower costs especially when scaling
- More control and fine tuning
## Cons:
- Very complex
- - ~8 categories --> 8 unique pathways for parsing and taks creation


#Notes as reminder, figure out task class json object how to make multiple objects and then go to openai prompt playground to help
#notes what fields of the json object should i use ai to generate? can I append?
