import re


class Bible:
    """
    Detects and replaces abbreviated Bible references in text with HTML hyperlinks
    pointing to the USCCB Bible website. Handles potential abbreviation conflicts.
    """

    USCCB_BIBLE_URL = "https://bible.usccb.org/bible/{}/{}"

    BIBLE_BOOKS = {
        "genesis": {"chapters": 50, "abbreviations": ["Gen", "Ge", "Gn"]},
        "exodus": {"chapters": 40, "abbreviations": ["Exod", "Exo", "Ex"]},
        "leviticus": {"chapters": 27, "abbreviations": ["Lev", "Le", "Lv"]},
        "numbers": {"chapters": 36, "abbreviations": ["Num", "Nu", "Nm", "Nb"]},
        "deuteronomy": {"chapters": 34, "abbreviations": ["Deut", "De", "Dt"]},
        "joshua": {"chapters": 24, "abbreviations": ["Josh", "Jos", "Jsh"]},
        "judges": {"chapters": 21, "abbreviations": ["Judg", "Jdg", "Jg", "Jdgs"]},
        "ruth": {"chapters": 4, "abbreviations": ["Rth", "Ru"]},
        "1samuel": {
            "chapters": 31,
            "abbreviations": [
                "1 Sam",
                "1 Sa",
                "1S",
                "I Sa",
                "1 Sm",
                "1Sa",
                "1Sam",
                "1st Sam",
                "1st Samuel",
                "First Sam",
                "First Samuel",
            ],
        },
        "2samuel": {
            "chapters": 24,
            "abbreviations": [
                "2 Sam",
                "2 Sa",
                "2S",
                "II Sa",
                "2 Sm",
                "2Sa",
                "II Sam",
                "IISam",
                "2 Sam",
                "2Sam",
                "2nd Sam",
                "2nd Samuel",
                "Second Sam",
                "Second Samuel",
            ],
        },
        "1kings": {
            "chapters": 22,
            "abbreviations": [
                "1 Kgs",
                "1 Ki",
                "1K",
                "I Kgs",
                "1Kgs",
                "I Ki",
                "1Ki",
                "1Kin",
                "1st Kgs",
                "1st Kings",
                "First Kgs",
                "First Kings",
                "1 Kings",
                "1 Kg",
            ],
        },
        "2kings": {
            "chapters": 25,
            "abbreviations": [
                "2 Kgs",
                "2 Ki",
                "2K",
                "II Kgs",
                "2Kgs",
                "II Ki",
                "2Ki",
                "2Kin",
                "2nd Kgs",
                "2nd Kings",
                "Second Kgs",
                "Second Kings",
                "2 Kings",
                "2 Kg",
            ],
        },
        "1chronicles": {
            "chapters": 29,
            "abbreviations": [
                "1 Chron",
                "1 Ch",
                "I Ch",
                "1Ch",
                "1 Chr",
                "I Chr",
                "1Chr",
                "I Chron",
                "1Chron",
                "1st Chron",
                "1st Chronicles",
                "First Chron",
                "First Chronicles",
            ],
        },
        "2chronicles": {
            "chapters": 36,
            "abbreviations": [
                "2 Chron",
                "2 Ch",
                "II Ch",
                "2Ch",
                "II Chr",
                "2Chr",
                "II Chron",
                "2Chron",
                "2nd Chron",
                "2nd Chronicles",
                "Second Chron",
                "Second Chronicles",
                "2 Chr",
            ],
        },
        "ezra": {"chapters": 10, "abbreviations": ["Ezr", "Ez"]},
        "nehemiah": {"chapters": 13, "abbreviations": ["Neh", "Ne"]},
        "tobit": {"chapters": 14, "abbreviations": ["Tobit", "Tob", "Tb"]},
        "judith": {"chapters": 16, "abbreviations": ["Jdth", "Jdt", "Jth"]},
        "esther": {"chapters": 10, "abbreviations": ["Esth", "Es"]},
        "1maccabees": {
            "chapters": 16,
            "abbreviations": [
                "1 Macc",
                "1 Mac",
                "1M",
                "I Ma",
                "1Ma",
                "I Mac",
                "1Mac",
                "I Macc",
                "1Macc",
                "I Maccabees",
                "1Maccabees",
                "1st Maccabees",
                "First Maccabees",
            ],
        },
        "2maccabees": {
            "chapters": 15,
            "abbreviations": [
                "2 Macc",
                "2 Mac",
                "2M",
                "II Ma",
                "2Ma",
                "II Mac",
                "2Mac",
                "II Macc",
                "2Macc",
                "II Maccabees",
                "2Maccabees",
                "2nd Maccabees",
                "Second Maccabees",
            ],
        },
        "job": {"chapters": 42, "abbreviations": ["Job", "Jb"]},  # Added 'Job'
        "psalms": {
            "chapters": 150,
            "abbreviations": ["Psalm", "Pslm", "Ps", "Psa", "Psm", "Pss"],
        },
        "proverbs": {"chapters": 31, "abbreviations": ["Prov", "Pro", "Pr", "Prv"]},
        "ecclesiastes": {
            "chapters": 12,
            "abbreviations": ["Eccles", "Eccle", "Eccl", "Ecc", "Ec", "Qoh"],
        },
        "songofsongs": {
            "chapters": 8,
            "abbreviations": [
                "Song of Songs",
                "Song",
                "So",
                "SOS",
                "Canticle of Canticles",
                "Canticles",
                "Cant",
            ],
        },
        "wisdom": {
            "chapters": 19,
            "abbreviations": ["Wisd of Sol", "Wis", "Ws", "Wisdom"],
        },
        "sirach": {
            "chapters": 51,
            "abbreviations": ["Sirach", "Sir", "Ecclesiasticus", "Ecclus"],
        },
        "isaiah": {"chapters": 66, "abbreviations": ["Isa", "Is"]},
        "jeremiah": {"chapters": 52, "abbreviations": ["Jer", "Je", "Jr"]},
        "lamentations": {"chapters": 5, "abbreviations": ["Lam", "La"]},
        "baruch": {"chapters": 6, "abbreviations": ["Baruch", "Bar"]},
        "ezekiel": {"chapters": 48, "abbreviations": ["Ezek", "Eze", "Ezk"]},
        "daniel": {"chapters": 14, "abbreviations": ["Dan", "Da", "Dn"]},
        "hosea": {"chapters": 14, "abbreviations": ["Hos", "Ho"]},
        "joel": {"chapters": 4, "abbreviations": ["Joel", "Joe", "Jl"]},
        "amos": {"chapters": 9, "abbreviations": ["Amos", "Am"]},
        "obadiah": {"chapters": 1, "abbreviations": ["Obad", "Ob"]},
        "jonah": {"chapters": 4, "abbreviations": ["Jonah", "Jnh", "Jon"]},
        "micah": {"chapters": 7, "abbreviations": ["Micah", "Mic", "Mc"]},
        "nahum": {"chapters": 3, "abbreviations": ["Nah", "Na"]},
        "habakkuk": {"chapters": 3, "abbreviations": ["Hab", "Hb"]},
        "zephaniah": {"chapters": 3, "abbreviations": ["Zeph", "Zep", "Zp"]},
        "haggai": {"chapters": 2, "abbreviations": ["Haggai", "Hag", "Hg"]},
        "zechariah": {"chapters": 14, "abbreviations": ["Zech", "Zec", "Zc"]},
        "malachi": {"chapters": 3, "abbreviations": ["Mal", "Ml"]},
        "matthew": {"chapters": 28, "abbreviations": ["Matt", "Mt"]},
        "mark": {"chapters": 16, "abbreviations": ["Mrk", "Mar", "Mk", "Mr"]},
        "luke": {"chapters": 24, "abbreviations": ["Luk", "Lk"]},
        "john": {"chapters": 21, "abbreviations": ["John", "Joh", "Jhn", "Jn"]},
        "acts": {"chapters": 28, "abbreviations": ["Acts", "Act", "Ac"]},
        "romans": {"chapters": 16, "abbreviations": ["Rom", "Ro", "Rm"]},
        "1corinthians": {
            "chapters": 16,
            "abbreviations": [
                "1 Cor",
                "1 Co",
                "I Co",
                "1Co",
                "I Cor",
                "1Cor",
                "I Corinthians",
                "1Corinthians",
                "1st Cor",
                "1st Corinthians",
                "First Cor",
                "First Corinthians",
            ],
        },
        "2corinthians": {
            "chapters": 13,
            "abbreviations": [
                "2 Cor",
                "2 Co",
                "II Co",
                "2Co",
                "II Cor",
                "2Cor",
                "II Corinthians",
                "2Corinthians",
                "2nd Corinthians",
                "Second Corinthians",
            ],
        },
        "galatians": {"chapters": 6, "abbreviations": ["Gal", "Ga"]},
        "ephesians": {"chapters": 6, "abbreviations": ["Ephes", "Eph"]},
        "philippians": {"chapters": 4, "abbreviations": ["Phil", "Php", "Pp"]},
        "colossians": {"chapters": 4, "abbreviations": ["Col", "Co"]},
        "1thessalonians": {
            "chapters": 5,
            "abbreviations": [
                "1 Thess",
                "1 Th",
                "I Th",
                "1Th",
                "I Thes",
                "1Thes",
                "I Thess",
                "1Thess",
                "I Thessalonians",
                "1Thessalonians",
                "1st Thess",
                "1st Thessalonians",
                "First Thess",
                "First Thessalonians",
                "1 Thes",
            ],
        },
        "2thessalonians": {
            "chapters": 3,
            "abbreviations": [
                "2 Thess",
                "2 Th",
                "II Th",
                "2Th",
                "II Thes",
                "2Thes",
                "II Thess",
                "2Thess",
                "II Thessalonians",
                "2Thessalonians",
                "2nd Thess",
                "2nd Thessalonians",
                "Second Thess",
                "Second Thessalonians",
                "2 Thes",
            ],
        },
        "1timothy": {
            "chapters": 6,
            "abbreviations": [
                "1 Tim",
                "1 Ti",
                "I Ti",
                "1Ti",
                "I Tim",
                "1Tim",
                "I Timothy",
                "1Timothy",
                "1st Tim",
                "1st Timothy",
                "First Tim",
                "First Timothy",
            ],
        },
        "2timothy": {
            "chapters": 4,
            "abbreviations": [
                "2 Tim",
                "2 Ti",
                "II Ti",
                "2Ti",
                "II Tim",
                "2Tim",
                "II Timothy",
                "2Timothy",
                "2nd Tim",
                "2nd Timothy",
                "Second Tim",
                "Second Timothy",
            ],
        },
        "titus": {"chapters": 3, "abbreviations": ["Titus", "Tit", "Ti"]},
        "philemon": {"chapters": 1, "abbreviations": ["Philem", "Phm", "Pm"]},
        "hebrews": {"chapters": 13, "abbreviations": ["Hebrews", "Heb"]},
        "james": {"chapters": 5, "abbreviations": ["James", "Jas", "Jm"]},
        "1peter": {
            "chapters": 5,
            "abbreviations": [
                "1 Pet",
                "1 Pe",
                "I Pe",
                "1Pe",
                "I Pet",
                "1Pet",
                "I Pt",
                "1 Pt",
                "1Pt",
                "1 P",
                "1P",
                "I Peter",
                "1Peter",
                "1st Peter",
                "First Peter",
            ],
        },
        "2peter": {
            "chapters": 3,
            "abbreviations": [
                "2 Pet",
                "2 Pe",
                "II Pe",
                "2Pe",
                "II Pet",
                "2Pet",
                "II Pt",
                "2 Pt",
                "2Pt",
                "2 P",
                "2P",
                "II Peter",
                "2Peter",
                "2nd Peter",
                "Second Peter",
            ],
        },
        "1john": {
            "chapters": 5,
            "abbreviations": [
                "1 John",
                "1 Jn",
                "I Jn",
                "1Jn",
                "I Jo",
                "1Jo",
                "I Joh",
                "1Joh",
                "I Jhn",
                "1 Jhn",
                "1Jhn",
                "1 J",
                "1J",
                "I John",
                "1John",
                "1st John",
                "First John",
            ],
        },
        "2john": {
            "chapters": 1,
            "abbreviations": [
                "2 John",
                "2 Jn",
                "II Jn",
                "2Jn",
                "II Jo",
                "2Jo",
                "II Joh",
                "2Joh",
                "II Jhn",
                "2 Jhn",
                "2Jhn",
                "2 J",
                "2J",
                "II John",
                "2John",
                "2nd John",
                "Second John",
            ],
        },
        "3john": {
            "chapters": 1,
            "abbreviations": [
                "3 John",
                "3 Jn",
                "III Jn",
                "3Jn",
                "III Jo",
                "3Jo",
                "III Joh",
                "3Joh",
                "III Jhn",
                "3 Jhn",
                "3Jhn",
                "3 J",
                "3J",
                "III John",
                "3John",
                "3rd John",
                "Third John",
            ],
        },
        "jude": {"chapters": 1, "abbreviations": ["Jude", "Jud", "Jd"]},
        "revelation": {
            "chapters": 22,
            "abbreviations": ["Rev", "Re", "The Revelation"],
        },
    }

    def __init__(self):
        """
        Initializes the Bible by preparing the abbreviation lookup
        and compiling the regular expression.
        """
        self._abbrev_map = self._build_abbreviation_map()
        self._regex = self._compile_regex()

    def _build_abbreviation_map(self):
        """
        Builds a dictionary mapping lowercase abbreviations (and variations)
        to their canonical book name and chapter count.

        Handles potential conflicts by ensuring longer abbreviations are
        processed correctly later by the regex sorting. Adds variations
        with and without periods.
        """
        abbrev_map = {}
        for canonical_name, data in self.BIBLE_BOOKS.items():
            max_chapters = data["chapters"]
            abbreviations = set(data["abbreviations"])
            abbreviations.add(canonical_name.capitalize())

            processed_abbreviations = set()
            for abbrev in abbreviations:
                processed_abbreviations.add(abbrev.lower())
                processed_abbreviations.add(abbrev.replace(".", "").lower())
                if not abbrev.endswith("."):
                    processed_abbreviations.add(abbrev.lower() + ".")

            for processed_abbrev in processed_abbreviations:
                abbrev_map[processed_abbrev] = (canonical_name, max_chapters)

        if "jude" in abbrev_map and "judges" in self.BIBLE_BOOKS:
            abbrev_map["jude"] = ("jude", self.BIBLE_BOOKS["jude"]["chapters"])
            abbrev_map["jude."] = ("jude", self.BIBLE_BOOKS["jude"]["chapters"])
        if "ti" in abbrev_map:
            abbrev_map["ti"] = ("titus", self.BIBLE_BOOKS["titus"]["chapters"])
            abbrev_map["ti."] = ("titus", self.BIBLE_BOOKS["titus"]["chapters"])

        return abbrev_map

    def _compile_regex(self):
        """
        Compiles the regular expression for matching Bible citations.

        Sorts abbreviations by length (descending) to prioritize longer matches.
        Uses word boundaries (\b) to avoid partial matches within words.
        """
        abbreviations = list(self._abbrev_map.keys())

        abbreviations.sort(key=len, reverse=True)

        escaped_abbreviations = [re.escape(a) for a in abbreviations]
        book_pattern = "|".join(escaped_abbreviations)

        regex_pattern = rf"\b({book_pattern})(?:\s*\.\s*|\s+)(\d+)(?:[:.]\s*\d+(?:(?:[-–—]\s*)?\d+)?)*\b"

        return re.compile(regex_pattern, re.IGNORECASE)

    def _replace_match(self, match):
        """
        Replacement function called by re.sub for each match found.
        Validates the chapter number and constructs the HTML link.
        """
        original_text = match.group(0)
        matched_abbrev = match.group(1)
        chapter_str = match.group(2)

        lookup_key = matched_abbrev.lower()
        if lookup_key.endswith("."):
            lookup_key = lookup_key[:-1]
        if lookup_key not in self._abbrev_map:
            lookup_key_no_period = lookup_key.replace(".", "")
            if lookup_key_no_period in self._abbrev_map:
                lookup_key = lookup_key_no_period
            else:
                print(f"Warning: Abbreviation '{matched_abbrev}' not found in map.")
                return original_text

        canonical_book, max_chapters = self._abbrev_map.get(lookup_key, (None, None))

        if not canonical_book:
            print(f"Warning: Canonical book not found for lookup key '{lookup_key}'.")
            return original_text

        try:
            chapter_num = int(chapter_str)
            if 1 <= chapter_num <= max_chapters:
                url = self.USCCB_BIBLE_URL.format(canonical_book, chapter_num)
                return f'<a href="{url}">{original_text}</a>'
            else:
                return original_text
        except ValueError:
            return original_text

    def linkify(self, text):
        """
        Takes a string and replaces all valid Bible citations with HTML links.

        Args:
            text (str): The input text potentially containing Bible citations.

        Returns:
            str: The text with Bible citations converted to hyperlinks.
        """
        if not text:
            return ""
        return self._regex.sub(self._replace_match, text)
