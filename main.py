from flask import Flask, make_response, request, jsonify
from Crawler.CgvCrawler import CgvMovieFinder
from Kafka import KafkaService
import enum


app = Flask(__name__)

kafkaService = KafkaService.KafkaService()
cgvMovieFiner = CgvMovieFinder()

class REQUESTS(enum.Enum):
    THEATER_LIST = 'theaterList'
    MOVEI_LIST = 'movieList'
    MOVIE_DETAIL = 'movieDetail'
    TOP_10 = 'rank'
    REQUEST_INVALID = 'invalidRequest'

@app.route('/LINE', methods=['GET','POST'])
def response():
    return make_response(jsonify(buildMessage()))

def getResults():
    req = request.get_json(force=True)
    callMethod = req.get('queryResult').get('parameters').get('call')
    print('API : ' + callMethod)
    if callMethod == REQUESTS.THEATER_LIST.value:
        return cgvMovieFiner.getTheaterList()

    elif callMethod == REQUESTS.MOVEI_LIST.value:
        theaterName = req.get('queryResult').get('parameters').get('theaterName')
        return cgvMovieFiner.getTheaterMovies(theaterName)

    elif callMethod == REQUESTS.MOVIE_DETAIL.value:
        theater = req.get('queryResult').get('parameters').get('theaterName')
        movieName = req.get('queryResult').get('parameters').get('movieName')
        return cgvMovieFiner.getMovieInfo(theater, movieName)

    elif callMethod == REQUESTS.TOP_10.value:
        return kafkaService.getRank()

    else:
        return [REQUESTS.REQUEST_INVALID.value]


def buildMessage():
    responseBody = getResults()
    fulfillmentMessages = []
    for item in responseBody:
        fulfillmentMessages.append({'text': {'text': [item]}})
    return {'fulfillmentMessages': fulfillmentMessages}


if __name__ == '__main__':
    app.run(debug=True)

