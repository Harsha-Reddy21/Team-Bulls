import pickle
import numpy as np
import faiss 

with open('numerical_embeddings/embeddings_5_1.pkl','rb') as file:
    embeddings_5_1=pickle.load(file)
with open('numerical_embeddings/embeddings_5_2.pkl','rb') as file:
    embeddings_5_2=pickle.load(file)
embeddings_5=embeddings_5_1+embeddings_5_2




with open('numerical_embeddings/embeddings_10_1.pkl','rb') as file:
    embeddings_10_1=pickle.load(file)
with open('numerical_embeddings/embeddings_10_2.pkl','rb') as file:
    embeddings_10_2=pickle.load(file)
embeddings_10=embeddings_10_1+embeddings_10_2




with open('numerical_embeddings/embeddings_15_1.pkl','rb') as file:
    embeddings_15_1=pickle.load(file)
with open('numerical_embeddings/embeddings_15_2.pkl','rb') as file:
    embeddings_15_2=pickle.load(file)
embeddings_15=embeddings_15_1+embeddings_15_2


with open('numerical_embeddings/embeddings_20_1.pkl','rb') as file:
    embeddings_20_1=pickle.load(file)
with open('numerical_embeddings/embeddings_20_2.pkl','rb') as file:
    embeddings_20_2=pickle.load(file)
embeddings_20=embeddings_20_1+embeddings_20_2







embeddings_5=np.stack(embeddings_5)
embeddings_10=np.stack(embeddings_10)
embeddings_15=np.stack(embeddings_15)
embeddings_20=np.stack(embeddings_20)



index_5 = faiss.IndexFlatL2(embeddings_5.shape[1])  # L2 distance index
index_5.add(embeddings_5)

index_10 = faiss.IndexFlatL2(embeddings_10.shape[1])  # L2 distance index
index_10.add(embeddings_10)

index_15 = faiss.IndexFlatL2(embeddings_15.shape[1])  # L2 distance index
index_15.add(embeddings_15)

index_20 = faiss.IndexFlatL2(embeddings_20.shape[1])  # L2 distance index
index_20.add(embeddings_20)

