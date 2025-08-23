import requests
import numpy as np
import faiss
import pickle

from add_index import index_5,index_10,index_15,index_20,embeddings_5,embeddings_10,embeddings_15,embeddings_20
from get_vector_embeddings import vector_embedding
total_length=len(embeddings_10)





def get_indices_data(df_5,df_10,df_15,df_20):
    final_result_data={}

    query_vector_5=vector_embedding(df_5,5)
    distances_5, indices_5= index_5.search(np.array([query_vector_5]), total_length)
    normalized_distances_5 = (distances_5 - np.min(distances_5)) / (np.max(distances_5) - np.min(distances_5))
    normalized_distances_5=normalized_distances_5[0].tolist()
    indices_5=indices_5[0].tolist()
    for i in range(len(indices_5)):
        final_result_data[indices_5[i]]=(1-normalized_distances_5[i])*3
        

    
    query_vector_10=vector_embedding(df_10,10)
    distances_10, indices_10= index_10.search(np.array([query_vector_10]), total_length)
    normalized_distances_10 = (distances_10 - np.min(distances_10)) / (np.max(distances_10) - np.min(distances_10))
    normalized_distances_10=normalized_distances_10[0].tolist()
    indices_10=indices_10[0].tolist()
    for i in range(len(indices_10)):
        final_result_data[indices_10[i]]+=(1-normalized_distances_10[i])*3

    
    query_vector_15=vector_embedding(df_15,15)
    distances_15, indices_15= index_15.search(np.array([query_vector_15]), total_length)
    normalized_distances_15 = (distances_15 - np.min(distances_15)) / (np.max(distances_15) - np.min(distances_15))
    normalized_distances_15=normalized_distances_15[0].tolist()
    indices_15=indices_15[0].tolist()
    for i in range(len(indices_15)):
        final_result_data[indices_15[i]]+=(1-normalized_distances_15[i])*2

    
    query_vector_20=vector_embedding(df_20,20)
    distances_20, indices_20= index_20.search(np.array([query_vector_20]), total_length)
    normalized_distances_20 = (distances_20 - np.min(distances_20)) / (np.max(distances_20) - np.min(distances_20))
    normalized_distances_20=normalized_distances_20[0].tolist()
    indices_20=indices_20[0].tolist()
    for i in range(len(indices_20)):
        final_result_data[indices_20[i]]+=(1-normalized_distances_20[i])*2

    

   

    # query_vector_50=vector_embedding(df_50,50)
    # distances_50, indices_50= index_50.search(np.array([query_vector_50]), total_length)
    # normalized_distances_50 = (distances_50 - np.min(distances_50)) / (np.max(distances_50) - np.min(distances_50))
    # normalized_distances_50=normalized_distances_50[0].tolist()
    # indices_50=indices_50[0].tolist()
    # for i in range(len(indices_50)):
    #     final_result_data[indices_50[i]]+=(1-normalized_distances_50[i])*1.5


    



    

    final_indices = sorted(final_result_data, key=lambda x: final_result_data[x],reverse=True)
    final_indices=final_indices[:500]   
    sorted_dict = {key: final_result_data[key] for key in final_indices}
    final_data_2=sorted_dict


    return final_indices,final_data_2



