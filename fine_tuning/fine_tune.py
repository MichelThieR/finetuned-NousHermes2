import os
from dotenv import load_dotenv
from gradientai import Gradient
from datasets import load_dataset

load_dotenv()


def fine_tune(data) -> None:
    with Gradient() as gradient:
        model = gradient.get_model_adapter(
            model_adapter_id=os.getenv("GRADIENT_ADAPTER_ID"))
        
        print(f"The model's name is {model.name} and id is {model.id}")
        EPOCHS = 3
        for i in range(EPOCHS):
            # batch_size cannot be > 100 (This was not mentioned in documentation)
            # breaking data in 2
            model.fine_tune(samples=data[:90])
            model.fine_tune(samples=data[90:])
        
        

# function to format data properly for nous hermes fine tuning
# should be in format: 
# { "inputs": "<s>### Instruction:\n{{ user_message }}\n\n### Response:\n{{ response }}</s>" }
def format_data(training_data):
    finetune_data = []
    for i in range(len(training_data['train'])):
        sample = training_data['train'][i]['text']
        sample = sample.replace("<HUMAN>: ","<s>### Instruction:\n")
        sample = sample.replace("<ASSISTANT>: ","\n### Response:\n")
        sample += "</s>"
        result = {"inputs": sample}
        finetune_data.append(result)
    
    return finetune_data
    

if __name__ == "__main__":

    training_data = load_dataset("heliosbrahma/mental_health_chatbot_dataset")
    samples = format_data(training_data)
    fine_tune(samples)