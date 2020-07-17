import os
import re
import enum
from Kafka import KafkaService
from bs4 import BeautifulSoup
from selenium import webdriver

class Code(enum.Enum):
    NO_SUCH_THEATER = '해당 상영관이 존재하지 않습니다'
    NO_SUCH_MOVIE = '상영중인 영화가 없습니다'

class CgvMovieFinder:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    driver = webdriver.Chrome(executable_path=DRIVER_BIN)
    host = "http://www.cgv.co.kr/"
    areaListUrl = "reserve/show-times/"
    theaterTimeTableUrl = "common/showtimes/iframeTheater.aspx?"

    def getSelector(self, html, selector):
        return BeautifulSoup(html,"html.parser").body.select(selector)

    # 영화관 정보 리스트 row Data 검색
    def getTheaters(self):
        self.driver.get(self.host + self.areaListUrl)
        html = self.driver.page_source
        selector = '#contents > div.sect-common > div > div.sect-city > ul > li > div > ul > li > a'
        return self.getSelector(html, selector)

    # 영화관 목록 검색
    def getTheaterList(self):
        areas = self.getTheaters()
        theaterList = []
        for area in areas:
            theaterList.append(area.get_text().strip())

        return theaterList

    # 특정 영화관 row Data 검색
    def getTheater(self, userLocation):
        areas = self.getTheaters()
        for area in areas:
            print(area['title'], userLocation)
            if area['title'][3:] == userLocation or area['title'] == userLocation:
                return area
        return Code.NO_SUCH_THEATER

    # 특정 영화관 타임 테이블 검색
    def getTheaterInfo(self, theater):
        theaterInfo = self.getTheater(theater)
        if(theaterInfo == Code.NO_SUCH_THEATER):
            return Code.NO_SUCH_THEATER

        paramUrl = theaterInfo['href']
        self.driver.get(self.host + self.theaterTimeTableUrl + paramUrl)
        return self.driver.page_source

    # 영화 row data 검색
    def getMoviesInfo(self, theater):
        html = self.getTheaterInfo(theater)
        if (html == Code.NO_SUCH_THEATER):
            return Code.NO_SUCH_THEATER

        selector = 'body > div > div.sect-showtimes > ul > li'
        return self.getSelector(html, selector)

    # 영화관 상영영화목록 검색
    def getTheaterMovies(self, theater):
        movies = self.getMoviesInfo(theater)
        if (movies == Code.NO_SUCH_THEATER):
            return [Code.NO_SUCH_THEATER.value]

        ret = []
        for movie in movies:
            ret.append(movie.select_one('div > div > a > strong').get_text().strip())

        return ret

    # 영화 상영 시간 검색
    def getMovieInfo(self, theater, movieName):
        movies = self.getMoviesInfo(theater)
        if (movies == Code.NO_SUCH_THEATER):
            return [Code.NO_SUCH_THEATER.value]

        for movie in movies:
            if movie.select_one('div > div > a > strong').get_text().strip() == movieName:
                timeTableList = []
                timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
                for timetable in timetables:
                    try:
                        time = timetable.select_one('a > em').get_text().strip()
                        seat = timetable.select_one('a > span').get_text().strip()
                    except AttributeError:
                        time = timetable.select_one('em').get_text().strip()
                        seat = timetable.select_one('span').get_text().strip()
                    print(seat)
                    timeTableList.append('시간은 ' + time + '이고 자리는 ' + re.findall("\d+",seat)[0] + '석 남아 있어요')

                kafkaService = KafkaService.KafkaService()
                kafkaService.publish(movieName)

                return timeTableList
        return [Code.NO_SUCH_MOVIE.value]



