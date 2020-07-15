#from Crawler.CgvCrawler import CgvMovieFinder
from Kafka import KafkaService
#cgvMovieFiner = CgvMovieFinder()
kafkaService = KafkaService.KafkaService()
rank = kafkaService.consume()
for key in rank:
    print(key)
userLocation = '강남'
userMovieName = '반도'

#print(cgvMovieFiner.getTheaterList())
#print(cgvMovieFiner.getTheaterMovies(userLocation))
#print(cgvMovieFiner.getTheaterMovies('이세상엔 없는 지점'))
#print(cgvMovieFiner.getMovieInfo(userLocation, userMovieName))
#print(cgvMovieFiner.getMovieInfo('이세상엔 없는 지점', userMovieName))
#print(cgvMovieFiner.getMovieInfo(userLocation, '이 세상엔 없는 영화'))
#print(cgvMovieFiner.getMovieInfo('이세상엔 없는 지점', '이 세상엔 없는 영화'))
