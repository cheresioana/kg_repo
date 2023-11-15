primary_language_by_country = {
    "Albania": "Albanian",
    "Andorra": "Catalan",
    "Belarus": "Belarusian",
    "Belgium": "Dutch",  # Limba flamandă este cea mai vorbită în Belgia, dar există și regiuni francofone și germanofone.
    "Bosnia and Herzegovina": "Bosnian",
    "Bulgaria": "Bulgarian",
    "Croatia": "Croatian",
    "Czech Republic": "Czech",
    "Denmark": "Danish",
    "Estonia": "Estonian",
    "Finland": "Finnish",
    "France": "French",
    "Germany": "German",
    "Greece": "Greek",
    "Hungary": "Hungarian",
    "Iceland": "Icelandic",
    "Ireland": "Irish",  # Deși irlandeza este limba națională și primul limbaj oficial, engleza este predominantă.
    "Italy": "Italian",
    "Kosovo": "Albanian",
    "Latvia": "Latvian",
    "Lithuania": "Lithuanian",
    "Luxembourg": "Luxembourgish",
    "Malta": "Maltese",
    "Moldova": "Moldovian",
    "Monaco": "French",
    "Montenegro": "Montenegrin",
    "Netherlands": "Dutch",
    "North Macedonia": "Macedonian",
    "Norway": "Norwegian",
    "Poland": "Polish",
    "Portugal": "Portuguese",
    "Romania": "Romanian",
    "Russia": "Russian",
    "San Marino": "Italian",
    "Serbia": "Serbian",
    "Slovakia": "Slovak",
    "Slovenia": "Slovenian",
    "Spain": "Spanish",
    "Sweden": "Swedish",
    "Switzerland": "German",
    "Ukraine": "Ukrainian",
    "United Kingdom": "English",
    "Vatican City": "Latin",
    "Arabia": "Arabic",
    "Armenia": "Armenian",
    "Georgia": "Georgian",
    "Azerbaijan": "Azerbaijani",
    "Kazahstan": "Kazakh"
}

country_by_primary_language = {}
for country, language in primary_language_by_country.items():
    if language not in country_by_primary_language:
        country_by_primary_language[language] = []
    country_by_primary_language[language].append(country)


def appendLanguageNotFound(language):
    with open('languageNotFound.txt', 'a', encoding='utf-8') as file:
        file.write(language + '\n')


def get_first_country_by_language(language, url):
    countries = country_by_primary_language.get(language, [])
    return countries[0] if countries else appendLanguageNotFound(language + ' ' + url)
