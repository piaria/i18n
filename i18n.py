
from functools import cache
from importlib.metadata import requires
from subprocess import Popen
from typing import Dict
import translators as ts
import polib
import click
import csv


TEMPLATE_FILE_NAME = 'django.po'


@cache
def get_language_codes():
    try:
        from .config import LANGUAGES, LANGUAGE_DEFAULT
        return [lang for lang in LANGUAGES.keys() if lang != LANGUAGE_DEFAULT]
    except:
        return ['es', 'en', 'pt']


def translate_po_file(lang, remove_fuzzy=True):
    lang_path = 'translations/' + lang + '/LC_MESSAGES/' + TEMPLATE_FILE_NAME
    input_file: polib.POFile = polib.pofile(lang_path)
    for entry in input_file:
        new_text = ts.google(
            entry.msgid, if_use_cn_host=True, to_language=lang)
        entry.msgstr = new_text
        click.echo(f"{lang}:{entry.msgid} -> {entry.msgstr}")

    input_file.save()


@click.group()
def cli():
    """ i18n helper script"""


@cli.command()
def translate():
    """ Generated the translation for the given languajes """
    for lang in get_language_codes():
        lang_path = 'translations/' + lang + '/LC_MESSAGES/'
        Popen(['mkdir', '-p', lang_path]).communicate()

        Popen(['cp', TEMPLATE_FILE_NAME, lang_path +
              TEMPLATE_FILE_NAME]).communicate()
        translate_po_file(lang, remove_fuzzy=True)


@cli.command()
@click.option('--output', type=click.File('w'), default="export.csv", required=False)
def export(output):
    """ Exports the translations to the given filename """
    messages: Dict = {}

    for lang in get_language_codes():
        lang_path = 'translations/' + lang + '/LC_MESSAGES/' + TEMPLATE_FILE_NAME
        input_file: polib.POFile = polib.pofile(lang_path)
        messages[lang] = input_file

    spamwriter = csv.writer(output, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_ALL)

    spamwriter.writerow(['Como figura en el código', *get_language_codes()])

    input_file: polib.POFile = polib.pofile(TEMPLATE_FILE_NAME)
    for es_entry in input_file:
        t = [es_entry.msgid]
        for l in get_language_codes():
            t.append(messages[l].find(es_entry.msgid).msgstr)
        spamwriter.writerow(t)
