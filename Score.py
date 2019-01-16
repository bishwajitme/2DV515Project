# Score initialization for every metric used
# In our case frequency of words (content of the page),
# document location, pageRank algorithm (inbound links)
class Score:
    def __init__(self):
        self.content = []
        self.location = []
        self.pageRank = []

    # normalization algorithm that used to normalize the values of
    # word frequency, document location and pagerank algorithm.
    # It is worked as a universal function that converts the metric
    # value to a score between 0 and 1 regardless if high values are
    # good or bad.
    def normalize(self, scores, smallIsBetter):
        if smallIsBetter:
            vmin = min(scores)
            i = 0
            for score in scores:
                scores[i] = vmin / max(scores[i], 0.00001)
                i += 1
        else:
            vmax = max(scores)
            i = 0
            for score in scores:
                scores[i] = scores[i] / vmax
                i += 1

        return scores
