import openai
import numpy as np

# Set your OpenAI API key
openai.api_key = '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'  # Replace with your actual API key

# Function to create ADA embeddings (with caching)
def create_ada_embeddings(prompts, cache={}):
    missing_embeddings = [prompt for prompt in prompts if prompt not in cache]
    if missing_embeddings:
        response = openai.Embedding.create(
            input=missing_embeddings,
            engine="text-embedding-ada-002"
        )
        new_embeddings = np.array([item['embedding'] for item in response['data']])
        cache.update(zip(missing_embeddings, new_embeddings))
    return np.array([cache[prompt] for prompt in prompts])

def main():
    # Read the dataset
    file_path = r'C:\Users\DELL\OneDrive\Desktop\ngit.txt'  # Adjust the path as needed
    dataset = read_dataset(file_path)

    # Pre-compute embeddings for the entire dataset
    dataset_embedding = create_ada_embeddings([line for line in dataset.splitlines() if line.strip()])

    print("Chatbot: Hi there! I'm your AI chatbot. Ask me anything, or type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        chatbot_response = generate_response_with_ada(user_input, dataset_embedding, dataset)  # Pass dataset
        print("Chatbot:", chatbot_response)

def read_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data

def generate_response_with_ada(user_input, dataset_embedding, dataset):  # Add dataset as argument
    # Create embedding for user input
    user_input_embedding = create_ada_embeddings([user_input])[0]

    # Calculate cosine similarity efficiently
    similarity_scores = np.dot(dataset_embedding, user_input_embedding) / (
        np.linalg.norm(dataset_embedding, axis=1) * np.linalg.norm(user_input_embedding)
    )

    # Find the most similar dataset entry
    most_similar_index = np.argmax(similarity_scores)
    most_similar_dataset_entry = dataset[most_similar_index]  # Access dataset now possible

    # Use GPT-3 to generate a response based on the most similar dataset entry
    prompt = f"User: {user_input}\nDataset: {most_similar_dataset_entry}"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.4,
        max_tokens=150
    )
    return response['choices'][0]['text']

if __name__ == "__main__":
    main()
