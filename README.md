# Mini-Chat

Basic ChatAPI using ChatGPT3

Tech Stack => FastAPI, Langchain, MongoDB (for conversation history) , Pinecone (if user input includes "Save To VectorDB" agent will embed given input and save it)

Install packages => pip3 install packages.txt

After adding a package run => pip3 freeze > packages.txt

Run App =>  uvicorn main:app    