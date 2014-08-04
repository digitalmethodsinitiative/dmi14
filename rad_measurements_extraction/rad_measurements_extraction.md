rad_measurements_extraction.py
==============================

Python script to extract radiation measurements reports from small text strings such as tweets.

By Antonin Segault <antonin.segault@edu.univ-fcomte.fr> (ELLIADD lab, Université de Franche-Comté, France). Written during Digital Methods Initiative's Summer School 2014 (see also https://wiki.digitalmethods.net/Dmi/DmiSummer2014MappingTheJDArchive).

Shared under Creative Commons CC-BY-SA 3.0 France (http://creativecommons.org/licenses/by-sa/3.0/fr/).

Use
---

Input : a text file with a tweet (only the text content) per line

Output : three files, one for each unit (Gray, Sivert, CPM) on each line, the tweet and the amount extracted, tab separated. If several measurements are found in one tweet, several lines will appear in the output files, with the same tweet and the different measurements.
