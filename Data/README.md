---
license: cc-by-4.0
language:
- he
tags:
- hebrew
- parliament
- knesset
- twitter
viewer: false
---

<p style="text-align: center;">
    <a href="https://aclanthology.org/2024.lrec-main.819.pdf" style="display: inline-block;">
        <img src="http://img.shields.io/badge/paper-ACL--anthology-B31B1B.svg" alt="Paper">
    </a>
    <a href="https://lrec-coling-2024.org/" style="display: inline-block;">
        <img src="https://img.shields.io/badge/conference-LREC_COLING_2024-blue" alt="Conference">
    </a>
    <a href="#" style="display: inline-block;">
        <img src="https://img.shields.io/badge/license-CC_BY_4.0-orange" alt="Version">
    </a>
</p>


# IsraParlTweet: The Israeli Parliamentary and Twitter Resource

Guy Mor-Lan, Effi Levi, Tamir Sheafer, Shaul R. Shenhav. _LREC-COLING 2024_.

**Paper**: https://aclanthology.org/2024.lrec-main.819/

**Dataset**: https://huggingface.co/datasets/guymorlan/IsraParlTweet/tree/main

For access to Twitter data, please contact authors at *guy.mor -AT- mail.huji.ac.il*

## Abstract
We introduce IsraParlTweet, a new linked corpus of Hebrew-language parliamentary discussions from the Knesset (Israeli Parliament) between the years 1992-2023 and Twitter posts made by Members of the Knesset between the years 2008-2023, containing a total of 294.5 million Hebrew tokens. In addition to raw text, the corpus contains comprehensive metadata on speakers and Knesset sessions as well as several linguistic annotations. As a result, IsraParlTweet can be used to conduct a wide variety of quantitative and qualitative analyses and provide valuable insights into political discourse in Israel.

# Dataset Description

The corpus is divided into four main sections: Knesset Sessions, Twitter Posts, Office Sessions, and Linguistic Analyses.

## Knesset Sessions - knesset_speeches.csv

This section contains the utterances of the MKs on the Knesset floor, in the order in which they appeared in the consecutive plenary protocol files. The utterances vary in length and may contain anything from a few words to a complete speech. Interruptions and interjections are preserved as they appear in the protocols. In total, this section contains approximately 4.5M individual utterances. The data is organized in CSV format, where each row represents a single utterance and contains the following fields:

- **text**: The text of the utterance.
- **uuid**: A unique text identifier used for associating the text with separately provided morphological analysis.
- **knesset**: Knesset term.
- **session_number**: Session number in current Knesset term.
- **date**: Date of session.
- **person_id**: Numeric identifier for speaker. Numeric identifiers are only assigned to MKs. 3% of speakers lack an identifier in cases of non-MK politicians (e.g. president, non-MK ministers), administrative Knesset workers, or guests, or if the matching MK could not be determined. Speakers are assigned an identifier if they were MKs in the time period of the corpus, even if they are not MKs at the time the utterance is made (e.g. presidents that were previously MKs).
- **canonical_name**: The canonical name (first name and surname) of the speaker. Only present for MKs for which an identifier can be determined.
- **name**: The name of the speaker as extracted from the protocol.
- **chair**: Indicator for whether or not the speaker was the chair of the session.
- **topic**: Topic of discussion or agenda item.
- **topic_extra**: Additional information on the topic (e.g. subtitle, legislation proposal number).
- **qa**: Indicator for whether or not the utterance is part of a Questions and Answers session.
- **query**: The written query to which the utterance is an oral response.
- **only_read**: Indicator for whether or not the utterance was a Q&A response that was read and not delivered by the answerer orally.

## Twitter Posts - contact authors for access

- **text**: The text of the tweet.
- **uuid**: A unique text identifier used for associating the text with separately provided morphological analysis.
- **tweet_id**: Twitter's unique tweet identifier.
- **date**: Date of the tweet.
- **knesset**: The Knesset term corresponding to the date of the tweet.
- **person_id**: Numeric identifier for the tweet poster. All rows have an identifier since only posts by MKs were collected. However, note that the poster was not necessarily serving as an MK at the time of posting.
- **user_id**: Twitter user ID number.
- **username**: Twitter handle name.
- **name**: The canonical name (first name + surname) of the poster.
- **likes**: Number of likes received at collection time.
- **retweets**: Number of retweets at collection time.
- **replies**: Number of replies at collection time.
- **quotes**: Number of quotes at collection time.

## Office Sessions - metadata.csv

This section contains metadata describing the office sessions of the MKs. An office session is a period of time in which a person served as an MK under a given party or faction. The data is organized in CSV format, where each row, representing a single office session, contains the following fields:

- **start_date**: Start date of office session.
- **end_date**: End date of office session.
- **knesset**: Relevant Knesset term.
- **person_id**: A unique personal id used for matching with Knesset Session utterances and Twitter Posts.
- **first_name**: MK's first name.
- **surname**: MK's surname.
- **gender**: MK's gender.
- **faction**: Name of faction under which the MK served.
- **faction_id**: Unique identifier for faction.
- **party_name**: Unified party name under which the MK served.
- **dob**: MK's date of birth.
- **cob**: MK's country of birth.
- **yod**: MK's year of death.
- **yoi**: MK's year of immigration (Aliyah) to Israel.
- **city**: MK's city of residence.
- **languages**: MK's spoken languages – a comma separated string.

## Linguistic Analyses

All JSON files utilize the texts' uuid as keys.

- **knesset_sentences.json**: List of segmented sentences (processed by Stanza) for Knesset utterances.
- **knesset_lemmas.json**: List of lemmas (processed by Stanza) for Knesset utterances.
- **knesset_sentiment**: List of predicted sentiment (by HeBERT sentiment model) for Knesset utterances.

For additional linguistic analyses, please contact the authors.

## BibTeX

```
@inproceedings{mor-lan-etal-2024-israparltweet-israeli,
    title = "{I}sra{P}arl{T}weet: The Israeli Parliamentary and {T}witter Resource",
    author = "Mor-Lan, Guy  and
      Levi, Effi  and
      Sheafer, Tamir  and
      Shenhav, Shaul R.",
    editor = "Calzolari, Nicoletta  and
      Kan, Min-Yen  and
      Hoste, Veronique  and
      Lenci, Alessandro  and
      Sakti, Sakriani  and
      Xue, Nianwen",
    booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.lrec-main.819",
    pages = "9372--9381",
    abstract = "We introduce IsraParlTweet, a new linked corpus of Hebrew-language parliamentary discussions from the Knesset (Israeli Parliament) between the years 1992-2023 and Twitter posts made by Members of the Knesset between the years 2008-2023, containing a total of 294.5 million Hebrew tokens. In addition to raw text, the corpus contains comprehensive metadata on speakers and Knesset sessions as well as several linguistic annotations. As a result, IsraParlTweet can be used to conduct a wide variety of quantitative and qualitative analyses and provide valuable insights into political discourse in Israel.",
}
```