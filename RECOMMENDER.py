from KNN_ALGO import knn, euclidean_distance
import sys
import numpy as np
import glob


homedir = './PATENT_DIR/'



def recommend_pats(query, k_recommendations):
    raw_pats_data = []
    with open('./export_patents.csv', 'r') as md:
        # Discard the first line (headings)
        next(md)
        next(md)
        # Read the data into memory
        for line in md.readlines():
            data_row = line.strip().split(',')
            raw_pats_data.append(data_row)

    # Prepare the data for use in the knn algorithm by picking
    # the relevant columns and converting the numeric columns
    # to numbers since they were read in as strings
    pats_recommendation_data = []
    for row in raw_pats_data:
#        data_row = list(map(float, row[1:]))
        data_row = [float(i) for i in row[1:]]
#        print(data_row)
        pats_recommendation_data.append(data_row)
        
    # Use the KNN algorithm to get the K patentss that are most
    # similar to target.
    recommendation_indices, _ = knn(
        pats_recommendation_data, query, k=k_recommendations,
        distance_fn=euclidean_distance, choice_fn=lambda x: None
    )

    pats_recommendations = []
    for _, index in recommendation_indices:
        pats_recommendations.append(raw_pats_data[index])
    md.close()
    return pats_recommendations

#-------------------------------------------------------
#Get target data function
tar_file = glob.glob(homedir+"target_*.csv")
target_row_data = []

with open('./export_patents.csv', 'r') as mdd:
        next(mdd)
        next(mdd)
        for line in mdd.readlines():
            target_row = line.strip().split(',')
            target_row_data.append(target_row)
            break
mdd.close()

target_patent_kw_freq = [float(i) for i in target_row_data[0][1:]]
target_patent = target_row_data[0][0]

print('')
print('RECOMMENDER.py-------------')
print('Target Patent: ',target_patent)
print('Target KW Freq: ', target_patent_kw_freq)
          
#pass to recommend_pats
recommended_pats = recommend_pats(query=target_patent_kw_freq, k_recommendations=6)

    # Print recommended movie titles
print('')
print('Recommendations:')
for recommendation in recommended_pats:
    print(recommendation[0])
