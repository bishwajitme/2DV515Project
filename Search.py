from flask import Flask
from flask_restful import Resource, Api
from random import randint
from Score import Score
import urllib
from readfiles import documentLists

documentlist = documentLists()
documentlist.iterateOverAllDocs()
documentlist.pageRank()


class Search(Resource):
    def __init__(self):
        self.documentlist = documentlist

    def get(self, search_term):
            print(search_term)
            decoded = urllib.unquote(search_term).split()
            results = self.search(decoded)
            print results[:5]
            return {"results": results[:5]}, 200, {'Access-Control-Allow-Origin': '*'}

    # Search function that check if the search term exists receive the word id according
    # to the query, then it calculates all the metrics, normalize the values, sort the results
    # and return the sorted results that we could gather in the frontend of the application
    def search(self, search_term):
        query = []
        for word in search_term:
            if self.documentlist.keyExists(word):
                # The lower method returns a copy of the string of the word id
                # which all case-based characters have been lowercased and then
                # passed into the word_id parameter.
                word_id = self.documentlist.getIdForWord(word.lower())
                query.append(word_id)
            else:
                print ("No Search Result")
        # print(words)
        pages = self.documentlist.getDocuments(query)
        results = []
        ts = Score()
        # ts = totalScores
        i = 0
        for page in pages:
            # Total scores for each metric
            ts.content.append(self.wordFrequency(query, page))
            ts.location.append(self.documentLocation(query, page))
            ts.pageRank.append(page.pageRank)

        # Normalize every value
        # High score is better
        ts.normalize(ts.content, False)
        # Low score is better
        ts.normalize(ts.location, True)
        # High score is better
        ts.normalize(ts.pageRank, False)

        for page in pages:
            score = (1.0 * ts.content[i]) + (0.8 * ts.location[i]) + (0.5 * ts.pageRank[i])
            results.append({"url": page.url, "score": score, "content": 1.0 * ts.content[i], "location": 0.8 * ts.location[i], "pageRank": 0.5 * ts.pageRank[i]})
            i += 1
        sorted_results = sorted(results, key=lambda k: k["score"], reverse=True)
        return sorted_results


    # This metric scores a page based on how many
    # times the words in the query appears on the page
    def wordFrequency(self, query, page):
        score = 0
        for wordId in query:
            for word in page.words:
                if word == wordId:
                    score += 1

        return score

    # Document location means the search query
    # location on the page if the query asked
    # appeared close to the top of that page then
    # the page is relevant.
    def documentLocation(self, query, page):
        total_score = 0
        for wordId in query:
            score = 0
            i = 0
            for word in page.words:
                if word == wordId:
                    score += i + 1
                    break
                i += 1

            else:
                # Giving such a high score means that the
                # query asked was not find making this page irrelevant
                # because the smaller scores are better for this metric
                score += 100000
            total_score += score

        return total_score
