from typing import List
from coworking import Coworking, CoworkingId
from .recommender import Recommender
import numpy as np

class EuclideanRecommender(Recommender):
    def __init__(self, data: List[Coworking]):
        # get all tags from all coworkings
        all_tags = set([ tag.id for coworking in data for tag in coworking.tags ])

        # convert coworkings to vectors
        # if a coworking has a tag, then the corresponding element in the vector is 1, otherwise 0
        def coworking_to_vec(coworking: Coworking):
            vec = []

            coworking_tags = set([ tag.id for tag in coworking.tags ])
            for tag in all_tags:
                if tag in coworking_tags:
                    vec.append(1)
                else:
                    vec.append(0)

            vec.append(coworking.review_rate)
            vec.append(coworking.review_count)
            vec.append(coworking.coordinates.lat)
            vec.append(coworking.coordinates.lon)
            vec.append(coworking.avg_price_per_workplace)
            return vec
        
        self._data = np.array(list(map(coworking_to_vec, data)))

        # map coworking id to index in self._data
        self._id_to_index = { coworking.id: i for i, coworking in enumerate(data) }
        self._index_to_id = [ coworking.id for coworking in data ]

    def fit(self):
        pass

    def recommend(self, id: CoworkingId, n=4) -> List[CoworkingId]:
        vec = self._data[self._id_to_index[id]]

        # calculate euclidean distance between vec and all other vectors
        distances = np.power(np.subtract(vec, self._data), 2)
        distances = np.sqrt(np.sum(distances, axis=1))

        # sort distances in ascending order
        sorted_indices = np.argsort(distances)

        # the first element is the coworking itself, so remove it
        sorted_indices = sorted_indices[1:n+1]

        return [ self._index_to_id[i] for i in sorted_indices ]