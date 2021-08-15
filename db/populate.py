from db.devotional import Devotional
from db.book import Book
from db.study import Study
from db.question import Question

from db.base import Session, engine, Base
import json
from configparser import ConfigParser
import utils.consts as consts
from utils.utils import get_logger

logger = get_logger()

# Deploy database schema if not done
Base.metadata.create_all(engine)

config = ConfigParser()
config.read(consts.CONFIG_FILE_NAME)

MARANATHA_FILE = f'{config["content"]["folder"]}/json/es_MSV76.json'
CS_FILE = f'{config["content"]["folder"]}/json/es_CS.json'
CS_STUDY_FILE = f'{config["content"]["folder"]}/json/es_CS_study.json'
CS_QUIZ_FILE = f'{config["content"]["folder"]}/json/es_CS_quiz.json'

def populate_devotional_maranatha():
    session = Session()
    if session.query(Devotional).filter(Devotional.name == '¡Maranata: El Señor Viene!').count() != consts.MARANATHA_DAYS_COUNT:
        devotionals = []

        with open(MARANATHA_FILE, 'rb') as fp:
            devotionals = json.load(fp)

        for i, devotional in enumerate(devotionals):
            session.add(
                Devotional(
                    name='¡Maranata: El Señor Viene!', \
                    title_date=devotional['title_date'], \
                    title=devotional['title'], \
                    date=devotional['date'], \
                    month=devotional['month'], \
                    day=devotional['day'], \
                    verse=devotional['verse'], \
                    paragraphs_count=devotional['paragraphs_count'], \
                    paragraphs=devotional['paragraphs'], \
                    urls=devotional['urls'], \
                    telegram_file_ids=devotional['telegram_file_ids'], \
                    year_day=i+1
                )
            )
            session.commit()
    else:
        logger.info('[DEVOTIONAL] ¡Maranata: El Señor Viene! devotional is aready in the db.')
    session.close()


def populate_book_great_controversy():
    session = Session()
    if session.query(Book).filter(Book.name == 'Libro: El Conflicto de los Siglos').count() != consts.GREAT_CONTROVERSY_CHAPTERS_COUNT:
        chapters = []

        with open(CS_FILE, 'rb') as fp:
            chapters = json.load(fp)

        for chapter in chapters:
            session.add(
                Book(
                    name='El Conflicto de los Siglos', \
                    chapter_number=chapter['chapter_number'], \
                    chapter_title=chapter['chapter_title'], \
                    paragraphs_count=chapter['paragraphs_count'], \
                    paragraphs=chapter['paragraphs'], \
                    urls=chapter['urls'], \
                    telegram_file_ids=chapter['telegram_file_ids']
                )
            )
            session.commit()
    else:
        logger.info('[BOOK] El Conflicto de los Siglos book is aready in the db.')
    session.close()

def populate_study_great_controversy():
    session = Session()
    if session.query(Study).filter(Study.book_name == 'Estudio: El Conflicto de los Siglos').count() != consts.GREAT_CONTROVERSY_STUDY_DAYS_COUNT:
        studies = []

        with open(CS_STUDY_FILE, 'rb') as fp:
            studies = json.load(fp)

        for study in studies:
            session.add(
                Study(
                    book_name='El Conflicto de los Siglos', \
                    study_name='El Tiempo de Estar Preparado', \
                    chapter_number=study['chapter_number'], \
                    chapter_title=study['chapter_title'], \
                    verse=study['verse'], \
                    day=study['day'], \
                    paragraphs_count=study['paragraphs_count'], \
                    paragraphs=study['paragraphs'], \
                    chapter_paragraphs=study['chapter_paragraphs'], \
                    questions=study['questions'], \
                    urls=study['urls'], \
                    telegram_file_ids=study['telegram_file_ids']
                )
            )
            session.commit()
    else:
        logger.info('[STUDY] El Conflicto de los Siglos is aready in the db.')
    session.close()

def populate_great_controversy_study_questions():
    session = Session()
    if session.query(Question).filter(Question.book_name == 'El Conflicto de los Siglos').count() < consts.GREAT_CONTROVERSY_QUESTIONS_COUNT:
        questions = []

        with open(CS_QUIZ_FILE, 'rb') as fp:
            questions = json.load(fp)

        for question in questions:
            session.add(
                Question(
                    book_name='El Conflicto de los Siglos', \
                    study_name='El Tiempo de Estar Preparado', \
                    chapter_number=question['chapter'], \
                    number=question['question_number'], \
                    question=question['question'], \
                    options=question['options'], \
                    correct_option=question['correct_option'], \
                    reference=question['reference']
                )
            )
            session.commit()
    else:
        logger.info('[QUESTIONS] El Conflicto de los Siglos is aready in the db.')
    session.close()

populate_devotional_maranatha()
populate_book_great_controversy()
populate_study_great_controversy()
populate_great_controversy_study_questions()