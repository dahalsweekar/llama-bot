# LLamaBot 🦙: Your very own PDF summarizer 📚

# Introduction
This repository implements the latest (as of now) Large Language Model (LLM) - Ollama3 to extract meaning behind the uploaded documents.
User uploads a document (PDF), then has a conversation with the chatbot ruminating on the topics of content in the document.
The user is provided with a friendly user interface where user uploads a document and then sits in the chatroom with the bot.
This project does not utilize any API keys, as Ollama3 is integrated into the system/server. The only limitation is if the server is not powerful, the processing takes forever.

| Upload page  | Chatroom
| ------------- | ------------- |
|![w1](https://github.com/dahalsweekar/llama-bot/assets/99968233/4fd19808-c509-4ad6-8144-b9f709b1d112)|![c1](https://github.com/dahalsweekar/llama-bot/assets/99968233/55c022c8-c9ec-4d28-a9e5-86ba88f70a60)|

# Features

## 1. Ollama3
This LLM runs independenly on personal server. If a server is powerful enough i.e if a server has a powerful GPU, then the task of generating the conversation becomes feasiable. One benefit of doing this way is that your do not require API keys (which should be purchased in most cases). The installation process is fairly straight forward and the models are being upgraded everyday as I write. The process of switching between the models is easy and hence some form of research can be done on such models such as its accuracy and execution time.

## 2. Langchain
A langchain is a production ready library which allows developer to employ LLMs with single line of code. It is a open source python library, which can be installed using pip. The langchain has many features from splitting a text into chunks, to employing a LLM for text generation. 

## 3. Front-end, APIs, and Server
This project is fully equipped with three main components that makes up a runnable application. I have created fairly beautiful UI and easy navigation process.
Though, authentication is not implemented, it can be implemented and will be implemented in future projects.
The information between the client and server is done using FastAPI and Ajax, which could provide two layers of security if needed.

| Routes  | Method | Response |
| ------------- | ------------- | ------------- |
| ```/``` | *GET* |HTML Response|
| ```/room``` | *GET* | HTML Response|
| ```/upload```  | *POST*	| JSON |                                                        
| ```/question```  | *POST* | JSON |

# Installation
 1. Go to [ollama.ai](https://ollama.com/), download and install the LLM. In linux: ```curl -fsSL https://ollama.com/install.sh | sh```
 3. After download, in the same page, click on the 'Model' on top right corner. You can see the latest models being added.
 4. Open terminal and write ```ollama pull <name of your desired model>```. In my case, I have used llama3. i.e ```ollama pull llama3```. It uses approx. 4GBs of space
 5. ```git clone https://github.com/dahalsweekar/llama-bot.git```
 6. ```pip install -r requirements.txt```
 7. Navigate to the folder and in terminal write ```uvicorn main:app --reload```
 8. In your browser locate: http://localhost:8000 (port number may change)

# Usage
 1. Press ```browse```
 2. Choose a PDF file
 3. press ```Upload```
 4. Press ```Go```
 5. Have conversation

# Pipeline
```
[PDF file] ---> [PDF parser] ---> [Texts] ---> [Chunk of Texts] ---> [Embedding] ---> [LLM] ---------> [conversation]
                                                                                        ^                       |
                                                                                        |                       |
                                                                                        |                       |
                                                                                        |                       |
                                                                                        |                       |
                                                                                                                            
                                                                                    [chatroom]<---[load pdf]<---[UI]<---[User]


```

# Explaination:

In this project, I used a database to store the pdf file when uploaded. The file is stored as 'BLOB' and when extracted from the database, it must be read using io.BytesIO. PDF file is parsed by using python library such as PyPDF2. Once the pdf is parsed the contents (bytes) are organized and converted into texts. These texts are divided into chunk of texts. This is done by inbuilt langchain library. In order to reduce and avoid 'hallucination', overlapping feature is enabled. In this project, overlapping is set to 200, which means once a chunk is created in order to create the next chunk, the pointer moves 200 character backwards and starts from there. This will reduce the risk of loss of meaning in the contents. These chunks are then embedded. Embedding is the process of converting the characters/words into stream of bits. Based upon the close-ness of the meaning between two texts, these numbers varies. For example, in one demonstration the actor extracts the bit between two variables: Apple and Orange. The common feature between these two words are that they are fruits. So, one would expect the extracted number be closer to 0. In another demonstration, when bit representation of Apple and Iphone was extracted, the bit value was even smaller than the bit representing of Apple and Orange. This clearly shows that the bit is representing the relation of Apple with a company, which is one of the most fascinating feature of Embedding. Here in this project I used Chromadb as vector store. These embedding along with the question of the user is fed to the LLM, which then extracts the conversation.
 
# Difficiencies

It takes a lot of time if you do not have a powerful system. In my case, I am using CPU to do the heavy lifting. 
Therefore, my execution time for a single question was a whooping 9 minutes.
### Back-end execution
![p1](https://github.com/dahalsweekar/llama-bot/assets/99968233/68dded83-be4b-4711-887b-8efbfff209c1)

# To dos:

- [ ] Delete the contents of the database once the conversation stops.
- [ ] Do the initial embedding only once after PDF upload, and then other embedding will be done throughout the conversation.
- [ ] Fix bugs and issues 

# References:
1. FastAPI: https://fastapi.tiangolo.com/
2. JQuery/Ajax: https://api.jquery.com/jQuery.ajax/
3. Ollama: https://ollama.com/
4. ChatGPT

