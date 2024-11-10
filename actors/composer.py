from sqlalchemy.orm import session
from db.base import Session

from db.devotional import Devotional
from db.book import Book
from db.study import Study
from db.bible import Bible
from db.promise import Promise
from db.counsel import Counsel

from utils.consts import MATERIAL_TYPES, BIBLE_VERSES_COUNT, BIBLE_BOOKS_ACRONYMS_LUT
from utils.utils import extract_material_name, parse_bible_reference, match_bible_book

def compose(subscription_title, month, day, cron_day):
    if MATERIAL_TYPES[subscription_title] == 'Devotional':
        message, file_ids = compose_devotional_message(subscription_title, day, month)
    elif MATERIAL_TYPES[subscription_title] == 'Book':
        message, file_ids = compose_book_message(subscription_title, cron_day+1)
    elif MATERIAL_TYPES[subscription_title] == 'Study':
        message, file_ids = compose_study_message(subscription_title, cron_day+1)
    elif MATERIAL_TYPES[subscription_title] == 'Promise':
        message, file_ids = compose_promise_message(subscription_title, cron_day+1)
    elif MATERIAL_TYPES[subscription_title] == 'Counsel':
        message, file_ids = compose_counsel_message(subscription_title, cron_day+1)
    else:
        raise Exception(f'Unknown material option: title={subscription_title}, month={month}, day={day}, cron_day={cron_day+1}')

    return message, file_ids


def compose_devotional_message(subscription_title, day, month):
    session = Session()
    devotional = session.query(Devotional).filter(Devotional.name == extract_material_name(subscription_title), Devotional.month == month, Devotional.day == day).all()
    session.close()
    try:
        devotional = devotional[0]
        # text portion composition
        message = f'\U0001F4C5<b> {devotional.date}</b>\n\U0001F4C3 <b>{devotional.title}</b>\n\n <i>\U0001F4D6 {devotional.verse}</i>\n\n'
        for paragraph in devotional.paragraphs:
            message += (paragraph + '\n\n')
        # urls tailing
        for source, url in devotional.urls.items():
            message += f'{source}: {url}\n'

        return message, devotional.telegram_file_ids
    except:
        message =   'Querido hermano/a,\n\n' \
                    'Lamentablemente, esta matutina originalmente no tiene este día. ' \
                    'Mañana Usted va a recibir el devocional del día. ' \
                    'Esto ocurre porque algunos devocionales no tienen días como el 29 de Febrero.\n\n' \
                    'Pedimos nuestras disculpas,\n' \
                    'El equipo de Una Mirada de Fe y Esperanza'

        return message, {}


def compose_book_message(subscription_title, day):
    session = Session()
    chapter = session.query(Book).filter(Book.name == extract_material_name(subscription_title), Book.chapter_number == day).all()
    session.close()
    try:
        chapter = chapter[0]
        # text portion composition
        message = f'\U0001F4D6<b> Capítulo {chapter.chapter_number}</b>\n\U0001F4C3 <b>{chapter.chapter_title}</b>\n\n'
        for paragraph in chapter.paragraphs:
            message += (paragraph + '\n\n')
        # video url tailing
        for source, url in chapter.urls.items():
            message += f'{source}: {url}'
        
        return message, chapter.telegram_file_ids
    except:
        message =   'Querido hermano/a,\n\n' \
                    'Lamentablemente, esta lectura ha llegado a su fin. ' \
                    'Usted ya ha recibido todos los capítulos y no hay nada más que enviar.\n\n' \
                    'Esperamos mucho que haya sido de bendición espíritual.\n' \
                    '¡Felicidades por terminar la lectura!\n' \
                    'El equipo de Una Mirada de Fe y Esperanza'

        return message, {}

def compose_study_message(subscription_title, day):
    session = Session()
    study = session.query(Study).filter(Study.book_name == extract_material_name(subscription_title), Study.day == day).all()
    session.close()
    try:
        study = study[0]
        # text portion composition
        message =   f'\U0001F4C5 <b>Día {study.day}</b>\n\U0001F4C3 <b>{study.chapter_title}, párrafos {study.chapter_paragraphs}</b>\n\n' \
                    f'<i>\U0001F4D6 {study.verse}</i>\n\n'
        for paragraph in study.paragraphs:
            message += (paragraph + '\n\n')
        # urls tailing
        for source, url in study.urls.items():
            message += f'{source}: {url}\n'

        return message, study.telegram_file_ids
    except:
        message =   'Querido hermano/a,\n\n' \
                    'Usted ya ha recibido todos los días de este estudio y no hay nada más que enviar.\n\n' \
                    'Esperamos mucho que haya sido de bendición espíritual para Usted.\n' \
                    '¡Felicidades por terminar el estudio!\n' \
                    'El equipo de Una Mirada de Fe y Esperanza'

        return message, {}

def compose_prophetic_verse(verse_bible_number : int) -> str:
    if verse_bible_number <= BIBLE_VERSES_COUNT:
        session = Session()
        verse = session.query(Bible).filter(Bible.verse_bible_number == verse_bible_number).first()
        session.close()
        return  f'{verse.verse}\n\n' \
                f'{verse.book_name} {verse.chapter_number}:{verse.verse_chapter_number}'
    else: 
        return 'Versículo vacío.'

def compose_bible(input_bible_reference: str, header_ref: bool = True) -> str:
    parsed = parse_bible_reference(input_bible_reference)
    ret = None
    if parsed != None:
        session = Session()
        # case 1 - whole chapter
        # TODO: Fix sending long chapters 
        if len(parsed[2]) == 0:
            if header_ref:
                ret = f'📖 <b>{BIBLE_BOOKS_ACRONYMS_LUT[match_bible_book(parsed[0])]} {parsed[1]}</b>\n\n'
            else:
                ret = ''
            verses = session.query(Bible).filter(Bible.book_abbr == match_bible_book(parsed[0]), Bible.chapter_number == parsed[1]).all()
            if len(verses) > 0:
                for verse in verses:
                    ret += f'[{verse.verse_chapter_number}] <i>{verse.verse}</i>\n'
            else:
                ret += '😞El capítulo no existe.'
        # case 2 - just a verse
        elif len(parsed[2]) == 1 and len(parsed[2][0]) == 1:
            if header_ref:
                ret = f'📖 <b>{BIBLE_BOOKS_ACRONYMS_LUT[match_bible_book(parsed[0])]} {parsed[1]}:{parsed[2][0][0]}</b>\n\n'
            else:
                ret = ''
            verses = session.query(Bible).filter(Bible.book_abbr == match_bible_book(parsed[0]), Bible.chapter_number == parsed[1], Bible.verse_chapter_number == parsed[2][0][0]).first()
            if verses != None:
                ret += f'<i>{verses.verse}</i>'
            else:
                ret += '😞El versículo no existe'
        # case 3 - continuous sequence
        elif len(parsed[2]) == 1 and len(parsed[2][0]) == 2:
            if header_ref:
                ret = f'📖 <b>{BIBLE_BOOKS_ACRONYMS_LUT[match_bible_book(parsed[0])]} {parsed[1]}:{parsed[2][0][0]}-{parsed[2][0][1]}</b>\n\n'
            else:
                ret = ''
            verses = session.query(Bible).filter(Bible.book_abbr == match_bible_book(parsed[0]), Bible.chapter_number == parsed[1], Bible.verse_chapter_number >= parsed[2][0][0], Bible.verse_chapter_number <= parsed[2][0][1]).all()
            if len(verses) > 0:
                for verse in verses:
                    ret += f'[{verse.verse_chapter_number}] <i>{verse.verse}</i>\n'
            else:
                ret += '😞La secuencia no existe.'
        # case 4 - discontinuous sequence(s)
        # TODO: Fix repeating sequences
        else:
            if header_ref:
                ret = f'📖 <b>{input_bible_reference}</b>\n\n'
            else:
                ret = ''
            for seq in parsed[2]:
                if len(seq) == 1:
                    verses = session.query(Bible).filter(Bible.book_abbr == match_bible_book(parsed[0]), Bible.chapter_number == parsed[1], Bible.verse_chapter_number == seq[0]).first()
                    if verses != None:
                        ret += f'[{verses.verse_chapter_number}] <i>{verses.verse}</i>\n'
                    else:
                        ret += f'😞[{seq[0]}] El versículo no existe\n'
                elif len(seq) == 2:
                    verses = session.query(Bible).filter(Bible.book_abbr == match_bible_book(parsed[0]), Bible.chapter_number == parsed[1], Bible.verse_chapter_number >= seq[0], Bible.verse_chapter_number <= seq[1]).all()
                    if len(verses) > 0:
                        for verse in verses:
                            ret += f'[{verse.verse_chapter_number}] <i>{verse.verse}</i>\n'
                    else:
                        ret += f'😞[{seq[0]}-{seq[1]}] La secuencia no existe.\n'
        session.close()
    
    return ret
    
def compose_promise_message(subscription_title: str, day: int) -> str:
    session = Session()
    promise = session.query(Promise).filter(Promise.random_order == day).first()
    session.close()
    if promise != None:
        bible_text = compose_bible(promise.verse_bible_reference, header_ref=False)

    if promise != None and bible_text != None:
        ret = f'🌼 <b>La promesa del día {day}</b> 📆\n\n' \
              f'📖 {bible_text}\n' \
              f'{promise.verse_bible_reference} ❤️'
    else:
        ret = '😞Disculpe, hubo un error al construir el mensaje. Apreciamos que nos lo comunique para que lo resolvemos rápido.'

    return ret, {}

def compose_counsel_message(subscription_title: str, day: int) -> str:
    session = Session()
    counsel = session.query(Counsel).filter(Counsel.random_order == day).first()
    session.close()

    if counsel != None:
        ret = f'🌼 <b>El consejo del día {day}</b> 📆\n\n' \
              f'📖 {counsel.counsel}\n\n' \
              f'{counsel.reference} ❤️'
    else:
        ret = '😞Disculpe, hubo un error al construir el mensaje. Apreciamos que nos lo comunique para que lo resolvemos rápido.'

    return ret, {}