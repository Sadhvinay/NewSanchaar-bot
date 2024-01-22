import openai
import numpy as np
import pymongo

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

        # Check if the user is providing feedback
        if user_input.lower().startswith('feedback:'):
            collect_feedback(user_input[9:])  # Remove 'feedback:' prefix
            feedback_response = generate_feedback_openai(user_input[9:])  # Remove 'feedback:' prefix
            print("Chatbot: Thank you for your feedback!", feedback_response)
        elif user_input.lower().startswith('issue:'):
            collect_issue(user_input[6:])
            print("Chatbot: Your issue has been considered. Issue will be resolved as soon as possible")
        else:
            chatbot_response = generate_response_with_ada(user_input, dataset_embedding, dataset)  # Pass dataset
            print("Chatbot:", chatbot_response)

def read_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data

def generate_feedback_openai(user_input):
    prompt = f"User: {user_input}"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.4,
        max_tokens=100
    )
    return response['choices'][0]['text']

def generate_response_with_ada(user_input, dataset_embedding, dataset):
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

def collect_feedback(feedback):
    # Establish a connection to the MongoDB server
    client = pymongo.MongoClient("mongodb+srv://user1:Sanchaar@cluster0.10l02sn.mongodb.net/")

    # Access the 'chatbot_database' database
    db = client["sanchaar_data"]

    # Access the 'Feedback' collection
    feedback_collection = db["Feedbacks"]

    # Create a document to insert into the collection
    feedback_data = {"feedback": feedback}

    # Insert the document into the 'Feedback' collection
    feedback_collection.insert_one(feedback_data)

def collect_issue(issue):
    # Establish a connection to the MongoDB server
    client = pymongo.MongoClient("mongodb+srv://user1:Sanchaar@cluster0.10l02sn.mongodb.net/")

    # Access the 'chatbot_database' database
    db = client["sanchaar_data"]

    # Access the 'Feedback' collection
    issue_collection = db["Issues"]

    # Create a document to insert into the collection
    issue_data = {"issue": issue}

    # Insert the document into the 'Feedback' collection
    issue_collection.insert_one(issue_data)

if __name__ == "__main__":
    main()
