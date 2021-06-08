"""Demonstrates how to make a simple call to the Natural Language API."""
from google.cloud import language


def get_info_token(token):
    # Get the text content of this token. Usually a word or punctuation.
    text = token.text
    token_text = text.content
    token_location = text.begin_offset

    # Get the part of speech information for this token.
    # Parts of spech are as defined in:
    # http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf
    part_of_speech = token.part_of_speech
    # Get the tag, e.g. NOUN, ADJ for Adjective, et al.
    part_speech_tag = language.PartOfSpeech.Tag(part_of_speech.tag).name

    # Get the voice, e.g. ACTIVE or PASSIVE
    voice = language.PartOfSpeech.Voice(part_of_speech.voice).name

    # Get the tense, e.g. PAST, FUTURE, PRESENT, et al.
    tense = language.PartOfSpeech.Tense(part_of_speech.tense).name

    # See API reference for additional Part of Speech information available
    # Get the lemma of the token. Wikipedia lemma description
    # https://en.wikipedia.org/wiki/Lemma_(morphology)
    lemma = token.lemma

    # Get the dependency tree parse information for this token.
    # For more information on dependency labels:
    # http://www.aclweb.org/anthology/P13-2017
    dependency_edge = token.dependency_edge
    head_token_index = dependency_edge.head_token_index
    label = language.DependencyEdge.Label(dependency_edge.label).name

    return {
        "text": token_text,
        "location": token_location,
        "speech_tag": part_speech_tag,
        "voice": voice,
        "tense": tense,
        "lemma": lemma,
        "head_token_index": head_token_index,
        "label": label,
    }


def analyze_syntax_sentence(text_content, display=False, client=None):

    client = client if client is not None else language.LanguageServiceClient()

    document = language.Document(
        content=text_content, type_=language.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_syntax(request={"document": document})

    list_info_token = [get_info_token(token) for token in response.tokens]

    if display:
        print(
            f"{'TEXT':<15}{'LOCATION':<10}{'SPEECH TAG':<15}{'VOICE':<20}{'TENSE':<20}{'LEMMA':<15}{'HEAD TOKEN INDEX':<20}{'LABEL':<10}"
        )
        for token in list_info_token:
            print(
                "{text:<15}{location:<10}{speech_tag:<15}{voice:<20}{tense:<20}{lemma:<15}{head_token_index:<20}{label:<10}".format(
                    text=token["text"],
                    location=token["location"],
                    speech_tag=token["speech_tag"],
                    voice=token["voice"],
                    tense=token["tense"],
                    lemma=token["lemma"],
                    head_token_index=token["head_token_index"],
                    label=token["label"],
                )
            )

        # Get the language of the text, which will be the same as
        # the language specified in the request or, if not specified,
        # the automatically-detected language.
        print("Language of the text: {}".format(response.language))

    return list_info_token, response.language
