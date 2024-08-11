# %%
import pandas as pd
import numpy as np
import io
import itertools
import math
import os
import seaborn as sns
np.seterr(invalid="ignore")

# %%
def createIPCC1R():
    """Returns a dictionary having 
    keys as IPCC 1 region and values using WORLD as a reference"""
    IPCCreg = ["WORLD"
                ]
    UNreg = [["WORLD"]]
    return dict(zip(IPCCreg,UNreg))


def createIPCC5R():
    """Returns a dictionary having 
    keys as IPCC 5 regions and values as UN country names"""

    IPCCreg = ["WORLD", "R5ASIA","R5LAM", "R5MAF", 
                "R5OECD90+EU", "R5REF",
                ]
    UNreg   = [
                [
                "Burundi",
                "Comoros",
                "Djibouti",
                "Eritrea",
                "Ethiopia",
                "Kenya",
                "Madagascar",
                "Malawi",
                "Mauritius",
                "Mayotte",
                "Mozambique",
                "Réunion",
                "Rwanda",
                "Seychelles",
                "Somalia",
                "South Sudan",
                "Uganda",
                "United Republic of Tanzania",
                "Zambia",
                "Zimbabwe",
                "Angola",
                "Cameroon",
                "Central African Republic",
                "Chad",
                "Congo",
                "Democratic Republic of the Congo",
                "Equatorial Guinea",
                "Gabon",
                "Sao Tome and Principe",
                "Algeria",
                "Egypt",
                "Libya",
                "Morocco",
                "Sudan",
                "Tunisia",
                "Western Sahara",
                "Botswana",
                "Eswatini",
                "Swaziland", 
                "Lesotho",
                "Namibia",
                "South Africa",
                "Benin",
                "Burkina Faso",
                "Cabo Verde",
                "Côte d'Ivoire",
                "Gambia",
                "Ghana",
                "Guinea",
                "Guinea-Bissau",
                "Liberia",
                "Mali",
                "Mauritania",
                "Niger",
                "Nigeria",
                "Saint Helena",
                "Senegal",
                "Sierra Leone",
                "Togo",
                "Kazakhstan",
                "Kyrgyzstan",
                "Tajikistan",
                "Turkmenistan",
                "Uzbekistan",
                "China",
                "China, Hong Kong SAR",
                "China, Macao SAR",
                "China, Taiwan Province of China",
                "Dem. People's Republic of Korea",
                "Japan",
                "Mongolia",
                "Republic of Korea",
                "Afghanistan",
                "Bangladesh",
                "Bhutan",
                "India",
                "Iran (Islamic Republic of)",
                "Maldives",
                "Nepal",
                "Pakistan",
                "Sri Lanka",
                "Brunei Darussalam",
                "Cambodia",
                "Indonesia",
                "Lao People's Democratic Republic",
                "Malaysia",
                "Myanmar",
                "Philippines",
                "Singapore",
                "Thailand",
                "Timor-Leste",
                "Viet Nam",
                "Armenia",
                "Azerbaijan",
                "Bahrain",
                "Cyprus",
                "Georgia",
                "Iraq",
                "Israel",
                "Jordan",
                "Kuwait",
                "Lebanon",
                "Oman",
                "Qatar",
                "Saudi Arabia",
                "State of Palestine",
                "Syrian Arab Republic",
                "Türkiye",
                "United Arab Emirates",
                "Yemen",
                "Belarus",
                "Bulgaria",
                "Czechia",
                "Czech Republic", 
                "Hungary",
                "Poland",
                "Republic of Moldova",
                "Romania",
                "Russian Federation",
                "Slovakia",
                "Ukraine",
                "Denmark",
                "Estonia",
                "Faroe Islands",
                "Finland",
                "Guernsey",
                "Iceland",
                "Ireland",
                "Isle of Man",
                "Jersey",
                "Latvia",
                "Lithuania",
                "Norway",
                "Sweden",
                "United Kingdom",
                "Albania",
                "Andorra",
                "Bosnia and Herzegovina",
                "Croatia",
                "Gibraltar",
                "Greece",
                "Holy See",
                "Italy",
                "Kosovo (under UNSC res. 1244)",
                "Malta",
                "Montenegro",
                "North Macedonia",
                "Portugal",
                "San Marino",
                "Serbia",
                "Slovenia",
                "Spain",
                "Austria",
                "Belgium",
                "France",
                "Germany",
                "Liechtenstein",
                "Luxembourg",
                "Monaco",
                "Netherlands",
                "Switzerland",
                "Anguilla",
                "Antigua and Barbuda",
                "Aruba",
                "Bahamas",
                "Barbados",
                "Bonaire, Sint Eustatius and Saba",
                "British Virgin Islands",
                "Cayman Islands",
                "Cuba",
                "Curaçao",
                "Dominica",
                "Dominican Republic",
                "Grenada",
                "Guadeloupe",
                "Haiti",
                "Jamaica",
                "Martinique",
                "Montserrat",
                "Puerto Rico",
                "Saint Barthélemy",
                "Saint Kitts and Nevis",
                "Saint Lucia",
                "Saint Martin (French part)",
                "Saint Vincent and the Grenadines",
                "Sint Maarten (Dutch part)",
                "Trinidad and Tobago",
                "Turks and Caicos Islands",
                "United States Virgin Islands",
                "Belize",
                "Costa Rica",
                "El Salvador",
                "Guatemala",
                "Honduras",
                "Mexico",
                "Nicaragua",
                "Panama",
                "Argentina",
                "Bolivia (Plurinational State of)",
                "Brazil",
                "Chile",
                "Colombia",
                "Ecuador",
                "Falkland Islands (Malvinas)",
                "French Guiana",
                "Guyana",
                "Paraguay",
                "Peru",
                "Suriname",
                "Uruguay",
                "Venezuela (Bolivarian Republic of)",
                "Bermuda",
                "Canada",
                "Greenland",
                "Saint Pierre and Miquelon",
                "United States of America",
                "Australia",
                "New Zealand",
                "Fiji",
                "New Caledonia",
                "Papua New Guinea",
                "Solomon Islands",
                "Vanuatu",
                "Guam",
                "Kiribati",
                "Marshall Islands",
                "Micronesia (Fed. States of)",
                "Nauru",
                "Northern Mariana Islands",
                "Palau",
                "American Samoa",
                "Cook Islands",
                "French Polynesia",
                "Niue",
                "Samoa",
                "Tokelau",
                "Tonga",
                "Tuvalu",
                "Wallis and Futuna Islands",
                "Turkey",
                "Other non-specified areas",
                "Channel Islands",
                "Faeroe Islands",
                "TFYR Macedonia",
                "Caribbean Netherlands", 
                "Netherlands Antilles",
                ],
                [
                "China",
                "China, Hong Kong SAR",
                "China, Macao SAR",
                "Mongolia",
                "China, Taiwan Province of China",
                "Afghanistan",
                "Bangladesh",
                "Bhutan",
                "India",
                "Maldives",
                "Nepal",
                "Pakistan",
                "Sri Lanka",
                "Brunei Darussalam",
                "Cambodia",
                "Dem. People's Republic of Korea",
                "Timor-Leste",
                "Indonesia",
                "Lao People's Democratic Republic",
                "Malaysia",
                "Myanmar",
                "Papua New Guinea",
                "Philippines",
                "Republic of Korea",
                "Singapore",
                "Thailand",
                "Viet Nam",
                ],
                [
                "Argentina",
                "Bahamas",
                "Barbados",
                "Belize",
                "Venezuela (Bolivarian Republic of)",
                "Brazil",
                "Chile",
                "Colombia",
                "Costa Rica",
                "Cuba",
                "Dominican Republic",
                "Ecuador",
                "El Salvador",
                "Guadeloupe",
                "Guatemala",
                "Guyana",
                "Haiti",
                "Honduras",
                "Jamaica",
                "Martinique",
                "Mexico",
                "Aruba",
                "Bonaire, Sint Eustatius and Saba",
                "Curaçao",
                "Caribbean Netherlands",
                "Nicaragua",
                "Panama",
                "Paraguay",
                "Peru",
                "Puerto Rico",
                "Suriname",
                "Trinidad and Tobago",
                "Uruguay",
                "Venezuela (Bolivarian Republic of)",
                "Saint Vincent and the Grenadines",
                "United States Virgin Islands",
                "French Guiana",
                "Saint Lucia",
                "Turks and Caicos Islands",
                "Grenada",
                "Bolivia (Plurinational State of)",
                "Sao Tome and Principe",
                ],
                [
                "Bahrain",
                "Iran (Islamic Republic of)",
                "Iraq",
                "Israel",
                "Jordan",
                "Kuwait",
                "Lebanon",
                "Oman",
                "Qatar",
                "Saudi Arabia",
                "Syrian Arab Republic",
                "United Arab Emirates",
                "Yemen",
                "Algeria",
                "Angola",
                "Benin",
                "Botswana",
                "Burkina Faso",
                "Burundi",
                "Côte d'Ivoire",
                "Cameroon",
                "Cabo Verde",
                "Central African Republic",
                "Chad",
                "Comoros",
                "Congo",
                "Democratic Republic of the Congo",
                "Djibouti",
                "Egypt",
                "Equatorial Guinea",
                "Eritrea",
                "Ethiopia",
                "Gabon",
                "Gambia",
                "Ghana",
                "Guinea",
                "Guinea-Bissau",
                "Kenya",
                "Lesotho",
                "Liberia",
                "Libya",
                "Madagascar",
                "Malawi",
                "Mali",
                "Mauritania",
                "Mauritius",
                "Morocco",
                "Mozambique",
                "Namibia",
                "Niger",
                "Nigeria",
                "Réunion",
                "Rwanda",
                "Senegal",
                "Sierra Leone",
                "Somalia",
                "South Africa",
                "Sudan",
                "Swaziland",
                "Togo",
                "Tunisia",
                "Uganda",
                "United Republic of Tanzania",
                "Western Sahara",
                "Zambia",
                "Zimbabwe",
                "Mayotte",
                "Eswatini",
                "State of Palestine",
                ],
                [
                "Albania",
                "Austria",
                "Belgium",
                "Bosnia and Herzegovina",
                "Bulgaria",
                "Croatia",
                "Cyprus",
                "Czechia",
                "Czech Republic",
                "Denmark",
                "Estonia",
                "Finland",
                "France",
                "Germany",
                "Greece",
                "Hungary",
                "Iceland",
                "Ireland",
                "Italy",
                "Latvia",
                "Lithuania",
                "Luxembourg",
                "North Macedonia",
                "TFYR Macedonia",
                "Malta",
                "Montenegro",
                "Netherlands",
                "Norway",
                "Poland",
                "Portugal",
                "Spain",
                "Sweden",
                "Switzerland",
                "Turkey",
                "United Kingdom",
                "Canada",
                "United States of America",
                "Australia",
                "Fiji",
                "French Polynesia",
                "Guam",
                "Japan",
                "New Caledonia",
                "New Zealand",
                "Romania",
                "Samoa",
                "Serbia",
                "Slovakia",
                "Slovenia",
                "Solomon Islands",
                "Vanuatu",
                "Tonga",
                "Micronesia (Fed. States of)",
                ],
                [
                "Armenia",
                "Azerbaijan",
                "Belarus",
                "Georgia",
                "Kazakhstan",
                "Kyrgyzstan",
                "Republic of Moldova",
                "Russian Federation",
                "Tajikistan",
                "Turkmenistan",
                "Ukraine",
                "Uzbekistan",
                ],
                ]
    
    return dict(zip(IPCCreg,UNreg))

def createIPCC6R():
    """Returns a dictionary having 
    keys as IPCC 5 regions and values as UN country names"""

    IPCCreg = ["WORLD", "R6ASIA","R6LAM", "R6MIDDLE_EAST", "R6AFRICA", 
                "R6OECD90+EU", "R6REF",
                ]
    UNreg   = [
                [
                "Burundi",
                "Comoros",
                "Djibouti",
                "Eritrea",
                "Ethiopia",
                "Kenya",
                "Madagascar",
                "Malawi",
                "Mauritius",
                "Mayotte",
                "Mozambique",
                "Réunion",
                "Rwanda",
                "Seychelles",
                "Somalia",
                "South Sudan",
                "Uganda",
                "United Republic of Tanzania",
                "Zambia",
                "Zimbabwe",
                "Angola",
                "Cameroon",
                "Central African Republic",
                "Chad",
                "Congo",
                "Democratic Republic of the Congo",
                "Equatorial Guinea",
                "Gabon",
                "Sao Tome and Principe",
                "Algeria",
                "Egypt",
                "Libya",
                "Morocco",
                "Sudan",
                "Tunisia",
                "Western Sahara",
                "Botswana",
                "Eswatini",
                "Swaziland", 
                "Lesotho",
                "Namibia",
                "South Africa",
                "Benin",
                "Burkina Faso",
                "Cabo Verde",
                "Côte d'Ivoire",
                "Gambia",
                "Ghana",
                "Guinea",
                "Guinea-Bissau",
                "Liberia",
                "Mali",
                "Mauritania",
                "Niger",
                "Nigeria",
                "Saint Helena",
                "Senegal",
                "Sierra Leone",
                "Togo",
                "Kazakhstan",
                "Kyrgyzstan",
                "Tajikistan",
                "Turkmenistan",
                "Uzbekistan",
                "China",
                "China, Hong Kong SAR",
                "China, Macao SAR",
                "China, Taiwan Province of China",
                "Dem. People's Republic of Korea",
                "Japan",
                "Mongolia",
                "Republic of Korea",
                "Afghanistan",
                "Bangladesh",
                "Bhutan",
                "India",
                "Iran (Islamic Republic of)",
                "Maldives",
                "Nepal",
                "Pakistan",
                "Sri Lanka",
                "Brunei Darussalam",
                "Cambodia",
                "Indonesia",
                "Lao People's Democratic Republic",
                "Malaysia",
                "Myanmar",
                "Philippines",
                "Singapore",
                "Thailand",
                "Timor-Leste",
                "Viet Nam",
                "Armenia",
                "Azerbaijan",
                "Bahrain",
                "Cyprus",
                "Georgia",
                "Iraq",
                "Israel",
                "Jordan",
                "Kuwait",
                "Lebanon",
                "Oman",
                "Qatar",
                "Saudi Arabia",
                "State of Palestine",
                "Syrian Arab Republic",
                "Türkiye",
                "United Arab Emirates",
                "Yemen",
                "Belarus",
                "Bulgaria",
                "Czechia",
                "Czech Republic", 
                "Hungary",
                "Poland",
                "Republic of Moldova",
                "Romania",
                "Russian Federation",
                "Slovakia",
                "Ukraine",
                "Denmark",
                "Estonia",
                "Faroe Islands",
                "Finland",
                "Guernsey",
                "Iceland",
                "Ireland",
                "Isle of Man",
                "Jersey",
                "Latvia",
                "Lithuania",
                "Norway",
                "Sweden",
                "United Kingdom",
                "Albania",
                "Andorra",
                "Bosnia and Herzegovina",
                "Croatia",
                "Gibraltar",
                "Greece",
                "Holy See",
                "Italy",
                "Kosovo (under UNSC res. 1244)",
                "Malta",
                "Montenegro",
                "North Macedonia",
                "Portugal",
                "San Marino",
                "Serbia",
                "Slovenia",
                "Spain",
                "Austria",
                "Belgium",
                "France",
                "Germany",
                "Liechtenstein",
                "Luxembourg",
                "Monaco",
                "Netherlands",
                "Switzerland",
                "Anguilla",
                "Antigua and Barbuda",
                "Aruba",
                "Bahamas",
                "Barbados",
                "Bonaire, Sint Eustatius and Saba",
                "British Virgin Islands",
                "Cayman Islands",
                "Cuba",
                "Curaçao",
                "Dominica",
                "Dominican Republic",
                "Grenada",
                "Guadeloupe",
                "Haiti",
                "Jamaica",
                "Martinique",
                "Montserrat",
                "Puerto Rico",
                "Saint Barthélemy",
                "Saint Kitts and Nevis",
                "Saint Lucia",
                "Saint Martin (French part)",
                "Saint Vincent and the Grenadines",
                "Sint Maarten (Dutch part)",
                "Trinidad and Tobago",
                "Turks and Caicos Islands",
                "United States Virgin Islands",
                "Belize",
                "Costa Rica",
                "El Salvador",
                "Guatemala",
                "Honduras",
                "Mexico",
                "Nicaragua",
                "Panama",
                "Argentina",
                "Bolivia (Plurinational State of)",
                "Brazil",
                "Chile",
                "Colombia",
                "Ecuador",
                "Falkland Islands (Malvinas)",
                "French Guiana",
                "Guyana",
                "Paraguay",
                "Peru",
                "Suriname",
                "Uruguay",
                "Venezuela (Bolivarian Republic of)",
                "Bermuda",
                "Canada",
                "Greenland",
                "Saint Pierre and Miquelon",
                "United States of America",
                "Australia",
                "New Zealand",
                "Fiji",
                "New Caledonia",
                "Papua New Guinea",
                "Solomon Islands",
                "Vanuatu",
                "Guam",
                "Kiribati",
                "Marshall Islands",
                "Micronesia (Fed. States of)",
                "Nauru",
                "Northern Mariana Islands",
                "Palau",
                "American Samoa",
                "Cook Islands",
                "French Polynesia",
                "Niue",
                "Samoa",
                "Tokelau",
                "Tonga",
                "Tuvalu",
                "Wallis and Futuna Islands",
                "Turkey",
                "Other non-specified areas",
                "Channel Islands",
                "Faeroe Islands",
                "TFYR Macedonia",
                "Caribbean Netherlands", "Netherlands Antilles",
                ],
                [
                "China",
                "China, Hong Kong SAR",
                "China, Macao SAR",
                "Mongolia",
                "China, Taiwan Province of China",
                "Afghanistan",
                "Bangladesh",
                "Bhutan",
                "India",
                "Maldives",
                "Nepal",
                "Pakistan",
                "Sri Lanka",
                "Brunei Darussalam",
                "Cambodia",
                "Dem. People's Republic of Korea",
                "Timor-Leste",
                "Indonesia",
                "Lao People's Democratic Republic",
                "Malaysia",
                "Myanmar",
                "Papua New Guinea",
                "Philippines",
                "Republic of Korea",
                "Singapore",
                "Thailand",
                "Viet Nam",
                ],
                [
                "Argentina",
                "Bahamas",
                "Barbados",
                "Belize",
                "Venezuela (Bolivarian Republic of)",
                "Brazil",
                "Chile",
                "Colombia",
                "Costa Rica",
                "Cuba",
                "Dominican Republic",
                "Ecuador",
                "El Salvador",
                "Guadeloupe",
                "Guatemala",
                "Guyana",
                "Haiti",
                "Honduras",
                "Jamaica",
                "Martinique",
                "Mexico",
                "Aruba",
                "Bonaire, Sint Eustatius and Saba",
                "Curaçao",
                "Caribbean Netherlands",
                "Nicaragua",
                "Panama",
                "Paraguay",
                "Peru",
                "Puerto Rico",
                "Suriname",
                "Trinidad and Tobago",
                "Uruguay",
                "Venezuela (Bolivarian Republic of)",
                "Saint Vincent and the Grenadines",
                "United States Virgin Islands",
                "French Guiana",
                "Saint Lucia",
                "Turks and Caicos Islands",
                "Grenada",
                "Bolivia (Plurinational State of)",
                "Sao Tome and Principe",
                ],
                [
                "Bahrain",
                "Iran (Islamic Republic of)",
                "Iraq",
                "Israel",
                "Jordan",
                "Kuwait",
                "Lebanon",
                "Oman",
                "Qatar",
                "Saudi Arabia",
                "Syrian Arab Republic",
                "United Arab Emirates",
                "Yemen",
                ],
                [
                "Algeria",
                "Angola",
                "Benin",
                "Botswana",
                "Burkina Faso",
                "Burundi",
                "Côte d'Ivoire",
                "Cameroon",
                "Cabo Verde",
                "Central African Republic",
                "Chad",
                "Comoros",
                "Congo",
                "Democratic Republic of the Congo",
                "Djibouti",
                "Egypt",
                "Equatorial Guinea",
                "Eritrea",
                "Ethiopia",
                "Gabon",
                "Gambia",
                "Ghana",
                "Guinea",
                "Guinea-Bissau",
                "Kenya",
                "Lesotho",
                "Liberia",
                "Libya",
                "Madagascar",
                "Malawi",
                "Mali",
                "Mauritania",
                "Mauritius",
                "Morocco",
                "Mozambique",
                "Namibia",
                "Niger",
                "Nigeria",
                "Réunion",
                "Rwanda",
                "Senegal",
                "Sierra Leone",
                "Somalia",
                "South Africa",
                "Sudan",
                "Swaziland",
                "Togo",
                "Tunisia",
                "Uganda",
                "United Republic of Tanzania",
                "Western Sahara",
                "Zambia",
                "Zimbabwe",
                "Mayotte",
                "Eswatini",
                "State of Palestine",
                ],
                [
                "Albania",
                "Austria",
                "Belgium",
                "Bosnia and Herzegovina",
                "Bulgaria",
                "Croatia",
                "Cyprus",
                "Czech Republic",
                'Czechia',
                "Denmark",
                "Estonia",
                "Finland",
                "France",
                "Germany",
                "Greece",
                "Hungary",
                "Iceland",
                "Ireland",
                "Italy",
                "Latvia",
                "Lithuania",
                "Luxembourg",
                "North Macedonia",
                "TFYR Macedonia",
                "Malta",
                "Montenegro",
                "Netherlands",
                "Norway",
                "Poland",
                "Portugal",
                "Spain",
                "Sweden",
                "Switzerland",
                "Turkey",
                "United Kingdom",
                "Canada",
                "United States of America",
                "Australia",
                "Fiji",
                "French Polynesia",
                "Guam",
                "Japan",
                "New Caledonia",
                "New Zealand",
                "Romania",
                "Samoa",
                "Serbia",
                "Slovakia",
                "Slovenia",
                "Solomon Islands",
                "Vanuatu",
                "Tonga",
                "Micronesia (Fed. States of)",
                ],
                [
                "Armenia",
                "Azerbaijan",
                "Belarus",
                "Georgia",
                "Kazakhstan",
                "Kyrgyzstan",
                "Republic of Moldova",
                "Russian Federation",
                "Tajikistan",
                "Turkmenistan",
                "Ukraine",
                "Uzbekistan",
                ],
                ]
    
    return dict(zip(IPCCreg,UNreg))

def createIPCC5Rproj():
    """Returns a dictionary having 
    keys as IPCC 5 regions and values as UN country regions
    This function uses proxies to represent the IPCC regions
    to be used in the projections as there is not perfect match"""

    IPCCreg = ["WORLD", "R5MAF", "R5LAM", "R5ASIA", "R5OECD90+EU", "R5REF" ] 
    UNreg =[
        ["WORLD"], 
        ["AFRICA"], 
        ["LATIN AMERICA AND THE CARIBBEAN"], 
        ["ASIA"], 
        ["More developed regions"], 
        ["Russian Federation"]]
    
    return dict(zip(IPCCreg,UNreg))


def createIPCC6Rproj():
    """Returns a dictionary having 
    keys as IPCC 6 regions and values as UN country regions
    This function uses proxies to represent the IPCC regions
    to be used in the projections as there is not perfect match"""

    IPCCreg = ["WORLD", "R6AFRICA", "R6LAM", "R6ASIA", "R6MIDDLE_EAST", "R6OECD90+EU", "R6REF" ] 
    UNreg =[
        ["WORLD"], 
        ["AFRICA"], 
        ["LATIN AMERICA AND THE CARIBBEAN"], 
        ["ASIA"], 
        ["Western Asia"],
        ["More developed regions"], 
        ["Russian Federation"]]
    
    return dict(zip(IPCCreg,UNreg))

def createIPCC10Rproj():
    """Returns a dictionary having 
    keys as IPCC 10 regions and values as UN country regions
    This function uses proxies to represent the IPCC regions
    to be used in the projections as there is not perfect match"""

    IPCCreg = ["WORLD", 
               "R10AFRICA",  	"R10CHINA+",	"R10EUROPE",	
               "R10INDIA+",	    "R10LATIN_AM",	"R10MIDDLE_EAST",
               "R10NORTH_AM",	"R10PAC_OECD",	"R10REF_ECON",	"R10REST_ASIA"
                ]
    UNreg =[
        ["WORLD"], 
        ["AFRICA"], 
        ["China"],
        ["EUROPE"],
        ["Southern Asia"],
        ["LATIN AMERICA AND THE CARIBBEAN"],  
        ["Western Asia"],
        ["NORTHERN AMERICA"], 
        ["Japan", "OCEANIA"],
        ["Russian Federation"],
        ["South-Eastern Asia"]]
    
    return dict(zip(IPCCreg,UNreg))

def createIPCC10R():
    """Returns a dictionary having 
    keys as IPCC 10 regions and values as UN country names"""

    IPCCreg = ["WORLD", 
               "R10AFRICA",  	"R10CHINA+",	"R10EUROPE",	
               "R10INDIA+",	    "R10LATIN_AM",	"R10MIDDLE_EAST",
               "R10NORTH_AM",	"R10PAC_OECD",	"R10REF_ECON",	"R10REST_ASIA"
                ]
    UNreg   = [
                [
                "Burundi",
                "Comoros",
                "Djibouti",
                "Eritrea",
                "Ethiopia",
                "Kenya",
                "Madagascar",
                "Malawi",
                "Mauritius",
                "Mayotte",
                "Mozambique",
                "Réunion",
                "Rwanda",
                "Seychelles",
                "Somalia",
                "South Sudan",
                "Uganda",
                "United Republic of Tanzania",
                "Zambia",
                "Zimbabwe",
                "Angola",
                "Cameroon",
                "Central African Republic",
                "Chad",
                "Congo",
                "Democratic Republic of the Congo",
                "Equatorial Guinea",
                "Gabon",
                "Sao Tome and Principe",
                "Algeria",
                "Egypt",
                "Libya",
                "Morocco",
                "Sudan",
                "Tunisia",
                "Western Sahara",
                "Botswana",
                "Eswatini",
                "Swaziland", 
                "Lesotho",
                "Namibia",
                "South Africa",
                "Benin",
                "Burkina Faso",
                "Cabo Verde",
                "Côte d'Ivoire",
                "Gambia",
                "Ghana",
                "Guinea",
                "Guinea-Bissau",
                "Liberia",
                "Mali",
                "Mauritania",
                "Niger",
                "Nigeria",
                "Saint Helena",
                "Senegal",
                "Sierra Leone",
                "Togo",
                "Kazakhstan",
                "Kyrgyzstan",
                "Tajikistan",
                "Turkmenistan",
                "Uzbekistan",
                "China",
                "China, Hong Kong SAR",
                "China, Macao SAR",
                "China, Taiwan Province of China",
                "Dem. People's Republic of Korea",
                "Japan",
                "Mongolia",
                "Republic of Korea",
                "Afghanistan",
                "Bangladesh",
                "Bhutan",
                "India",
                "Iran (Islamic Republic of)",
                "Maldives",
                "Nepal",
                "Pakistan",
                "Sri Lanka",
                "Brunei Darussalam",
                "Cambodia",
                "Indonesia",
                "Lao People's Democratic Republic",
                "Malaysia",
                "Myanmar",
                "Philippines",
                "Singapore",
                "Thailand",
                "Timor-Leste",
                "Viet Nam",
                "Armenia",
                "Azerbaijan",
                "Bahrain",
                "Cyprus",
                "Georgia",
                "Iraq",
                "Israel",
                "Jordan",
                "Kuwait",
                "Lebanon",
                "Oman",
                "Qatar",
                "Saudi Arabia",
                "State of Palestine",
                "Syrian Arab Republic",
                "Türkiye",
                "United Arab Emirates",
                "Yemen",
                "Belarus",
                "Bulgaria",
                "Czechia",
                "Czech Republic", 
                "Hungary",
                "Poland",
                "Republic of Moldova",
                "Romania",
                "Russian Federation",
                "Slovakia",
                "Ukraine",
                "Denmark",
                "Estonia",
                "Faroe Islands",
                "Finland",
                "Guernsey",
                "Iceland",
                "Ireland",
                "Isle of Man",
                "Jersey",
                "Latvia",
                "Lithuania",
                "Norway",
                "Sweden",
                "United Kingdom",
                "Albania",
                "Andorra",
                "Bosnia and Herzegovina",
                "Croatia",
                "Gibraltar",
                "Greece",
                "Holy See",
                "Italy",
                "Kosovo (under UNSC res. 1244)",
                "Malta",
                "Montenegro",
                "North Macedonia",
                "Portugal",
                "San Marino",
                "Serbia",
                "Slovenia",
                "Spain",
                "Austria",
                "Belgium",
                "France",
                "Germany",
                "Liechtenstein",
                "Luxembourg",
                "Monaco",
                "Netherlands",
                "Switzerland",
                "Anguilla",
                "Antigua and Barbuda",
                "Aruba",
                "Bahamas",
                "Barbados",
                "Bonaire, Sint Eustatius and Saba",
                "British Virgin Islands",
                "Cayman Islands",
                "Cuba",
                "Curaçao",
                "Dominica",
                "Dominican Republic",
                "Grenada",
                "Guadeloupe",
                "Haiti",
                "Jamaica",
                "Martinique",
                "Montserrat",
                "Puerto Rico",
                "Saint Barthélemy",
                "Saint Kitts and Nevis",
                "Saint Lucia",
                "Saint Martin (French part)",
                "Saint Vincent and the Grenadines",
                "Sint Maarten (Dutch part)",
                "Trinidad and Tobago",
                "Turks and Caicos Islands",
                "United States Virgin Islands",
                "Belize",
                "Costa Rica",
                "El Salvador",
                "Guatemala",
                "Honduras",
                "Mexico",
                "Nicaragua",
                "Panama",
                "Argentina",
                "Bolivia (Plurinational State of)",
                "Brazil",
                "Chile",
                "Colombia",
                "Ecuador",
                "Falkland Islands (Malvinas)",
                "French Guiana",
                "Guyana",
                "Paraguay",
                "Peru",
                "Suriname",
                "Uruguay",
                "Venezuela (Bolivarian Republic of)",
                "Bermuda",
                "Canada",
                "Greenland",
                "Saint Pierre and Miquelon",
                "United States of America",
                "Australia",
                "New Zealand",
                "Fiji",
                "New Caledonia",
                "Papua New Guinea",
                "Solomon Islands",
                "Vanuatu",
                "Guam",
                "Kiribati",
                "Marshall Islands",
                "Micronesia (Fed. States of)",
                "Nauru",
                "Northern Mariana Islands",
                "Palau",
                "American Samoa",
                "Cook Islands",
                "French Polynesia",
                "Niue",
                "Samoa",
                "Tokelau",
                "Tonga",
                "Tuvalu",
                "Wallis and Futuna Islands",
                "Turkey",
                "Other non-specified areas",
                "Channel Islands",
                "Faeroe Islands",
                "TFYR Macedonia",
                "Caribbean Netherlands", "Netherlands Antilles",
                ],
                [
                "Algeria",
                "Angola",
                "Benin",
                "Botswana",
                "Burkina Faso",
                "Burundi",
                "Côte d'Ivoire",
                "Cameroon",
                "Cabo Verde",
                "Central African Republic",
                "Chad",
                "Comoros",
                "Congo",
                "Democratic Republic of the Congo",
                "Djibouti",
                "Egypt",
                "Equatorial Guinea",
                "Eritrea",
                "Ethiopia",
                "Gabon",
                "Gambia",
                "Ghana",
                "Guinea",
                "Guinea-Bissau",
                "Kenya",
                "Lesotho",
                "Liberia",
                "Libya",
                "Madagascar",
                "Malawi",
                "Mali",
                "Mauritania",
                "Mauritius",
                "Morocco",
                "Mozambique",
                "Namibia",
                "Niger",
                "Nigeria",
                "Réunion",
                "Rwanda",
                "Senegal",
                "Sierra Leone",
                "Somalia",
                "South Africa",
                "Sudan",
                "Swaziland",
                "Togo",
                "Tunisia",
                "Uganda",
                "United Republic of Tanzania",
                "Western Sahara",
                "Zambia",
                "Mayotte",
                "Eswatini",
                "Sao Tome and Principe",
                "Zimbabwe",
                ], 
                [
                "China",
                "China, Hong Kong SAR",
                "China, Macao SAR",
                "China, Taiwan Province of China",
                "Cambodia",
                "Dem. People's Republic of Korea",
                "Lao People's Democratic Republic",
                "Mongolia",
                "Viet Nam",
                ], 
                [
                "Austria",
                "Belgium",
                "Croatia",
                "Czechia",
                "Denmark",
                "France",
                "Finland",
                "Spain",
                "Sweden",
                "Germany",
                "Greece",
                "Iceland",
                "Ireland",
                "Italy",
                "Luxembourg",
                "Netherlands",
                "Norway",
                "Portugal",
                "Switzerland",
                "Turkey",
                "Albania",
                "Bosnia and Herzegovina",
                "Bulgaria",
                "Cyprus",
                "Estonia",
                "Hungary",
                "Latvia",
                "Lithuania",
                "Malta",
                "Montenegro",
                "North Macedonia",
                "Poland",
                "Romania",
                "Serbia",
                "Slovakia",
                "Slovenia",
                "United Kingdom",
                ],
                [
                "India",
                "Afghanistan",
                "Bangladesh",
                "Bhutan",
                "Maldives",
                "Nepal",
                "Pakistan",
                "Sri Lanka",
                ],
                [
                "Argentina",
                "Bahamas",
                "Barbados",
                "Belize",
                "Venezuela (Bolivarian Republic of)",
                "Brazil",
                "Chile",
                "Colombia",
                "Costa Rica",
                "Cuba",
                "Dominican Republic",
                "Ecuador",
                "El Salvador",
                "Guadeloupe",
                "Guatemala",
                "Guyana",
                "Haiti",
                "Honduras",
                "Jamaica",
                "Martinique",
                "Mexico",
                "Aruba",
                "Bonaire, Sint Eustatius and Saba",
                "Curaçao",
                "Caribbean Netherlands",
                "Nicaragua",
                "Panama",
                "Paraguay",
                "Peru",
                "Puerto Rico",
                "Suriname",
                "Trinidad and Tobago",
                "Uruguay",
                "Saint Vincent and the Grenadines",
                "United States Virgin Islands",
                "French Guiana",
                "Saint Lucia",
                "Turks and Caicos Islands",
                "Grenada",
                "Bolivia (Plurinational State of)",
                "Venezuela (Bolivarian Republic of)",
                ],
                [
                "Bahrain",
                "Iran (Islamic Republic of)",
                "Iraq",
                "Israel",
                "Jordan",
                "Kuwait",
                "Lebanon",
                "Oman",
                "Qatar",
                "Saudi Arabia",
                "Syrian Arab Republic",
                "United Arab Emirates",
                "State of Palestine",
                "Libya",
                "Yemen"
                ],
                [
                "Canada",
                "Guam",
                "United States of America", 
                ],
                [
                "Australia",
                "Japan",
                "New Caledonia",
                "New Zealand",
                "Samoa",
                "Solomon Islands",
                "Tonga",
                "Micronesia (Fed. States of)",
                "French Polynesia",
                "Vanuatu",
                ],
                [
                "Armenia",
                "Azerbaijan",
                "Belarus",
                "Georgia",
                "Kazakhstan",
                "Kyrgyzstan",
                "Republic of Moldova",
                "Russian Federation",
                "Tajikistan",
                "Turkmenistan",
                "Ukraine",
                "Uzbekistan",
                ],
                [
                "Brunei Darussalam",
                "Timor-Leste",
                "Indonesia",
                "Malaysia",
                "Myanmar",
                "Papua New Guinea",
                "Philippines",
                "Republic of Korea",
                "Singapore",
                "Thailand",
                "Fiji",
                ],
                ]
    return dict(zip(IPCCreg,UNreg))


# %%
def un_reading(years: list, 
               filename: str, 
               numregions: int, 
               ipccregion: bool, 
               countries: list):
    """Reads probabilistic data from UN database
    Returns a dataframe with all population data
    Regions are assigned to a probability
    Regions are assigned to IPCC allocation if ipccregion is True
    into 1, 5, 6, or 10 ipcc regions
    countries is used if ipccregion is False to combine country-level data into one "modelregion"
    A "modelregion" is a region modelled according to the modeller's interests
    Values are in million inhabitants.
    
    Receives
        years: list of years to consider (> 2020 ):
        - in UN_PPP2022: year >= 2022
        - in UN_PPP2019: year >= 2020
        - in UN_PPP2017: year >= 2015
        - in UN_PPP2015: year >= 2015

        filename: name of file among UN probabilistic projection to extract
        numregions: number of IPCC regions to extract (1, 5, 6, 10)
        ipccregion: boolean, True to group UN data into IPCC regions
        countries: list of UN ountries to read and aggregate into a "modelregion"
    Generates
        all_data: dataframe with population (million)
        each year has a column where each row has a population value by scenario and region"""
    folder = r"data/UN"
    destination = os.path.join (folder, filename)
    tabs = ["Lower 95", "Lower 80", "Median", "Upper 80", "Upper 95"]
    remove_columns = ["Notes",
                    "Location code",
                    "ISO3 Alpha-code",
                    "ISO2 Alpha-code",
                    "SDMX code**",
                    "Type",
                    "Parent code"]
    if ipccregion: #if True, aggregates data into ipcc regions
        if numregions==1:
            reg_dict = createIPCC1R()
        if numregions==5:
            reg_dict = createIPCC5R()
        if numregions==6:
            reg_dict = createIPCC6Rproj()
        if numregions==10:
            reg_dict = createIPCC10Rproj()
    else: #if false, aggregates data into a "modelregion"
        key = "modelregion"
        reg_dict = dict(zip(["modelregion"], [countries]))


    all_data = pd.DataFrame()
    for reg in reg_dict.keys():
        regions = reg_dict[reg]
        for tab in tabs:
            data = pd.read_excel(destination,tab, skiprows=16)

            if len(data) > 1:
                region_col = "Region, subregion, country or area *"
                columns = [region_col] + years
                new = data[columns]
                new = new.rename(columns={region_col: "UNRegion"})
                regdata = pd.DataFrame(new[new.UNRegion.isin(regions)])
                regdata["Scenario"] = tab
                regdata["IPCCRegion"] = reg
                columns = ["IPCCRegion", "UNRegion", "Scenario"] + years
                regdata[years] = regdata[years]/1000
                all_data = pd.concat((all_data, 
                            regdata[columns]), axis=0)
                
    return (all_data)

def un_reading2020(years: float, 
               filename: str, 
               numregions: int, 
               ipccregion: bool, 
               countries: list):
    """Estimates UN deterministic values in million inhab for one past year
    Returns a dataframe with all population data
    Regions are deterministic
    Regions are assigned to IPCC allocation if ipccregion is True
    into 1, 5, 6, or 10 ipcc regions
    countries is used if ipccregion is False to combine country-level data into one "modelregion"
    A "modelregion" is a region modelled according to the modeller's interests
    Values are in million inhabitants.
    Receives:
        years: 2020
        numregions: number of IPCC regions to extract (1, 5, 6, 10)
        ipccregion: boolean, True to group UN data into IPCC regions
        countries: list of UN ountries to read and aggregate into a "modelregion"
    Generates:
        all_data: dataframe with population value per year on a single column
        regions correspond to each single row
        scenario is the "Estimate" scenario of UN"""

    folder = r'data/UN'
    filename = "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_REV1.xlsx"
    destination = os.path.join (folder, filename)
    data = pd.read_excel(destination,"Estimates", skiprows=16)
    region_col = "Region, subregion, country or area *"
    readcol = "Total Population, as of 1 July (thousands)"
    columns = [region_col] + ["Year"] + [readcol]
    new = data[columns]

    if ipccregion: #if True, aggregates data into ipcc regions
        if numregions==1:
            reg_dict = createIPCC1R()
        if numregions==5:
            reg_dict = createIPCC5R()
        if numregions==6:
            # Note that here we use the same definition as in IPPC regions
            # rather than UN aggregation which is used in UN_reading()
            # We could have used UN aggregation based on createIPCC6Rproj()
            # but there is a deviation in 2020 too big for 2020
            reg_dict = createIPCC6R() #createIPCC6Rproj()
        if numregions==10:
            # Note that here we use the UN aggregation based on createIPCC10Rproj()
            # because this makes it consistent with UN_Reading() for next years
            reg_dict = createIPCC10Rproj()
    else: #if false, aggregates data into a "modelregion"
        key = "modelregion"
        reg_dict = dict(zip(["modelregion"], [countries]))

    all_data = pd.DataFrame()
    new = new.rename(columns={region_col: "UNRegion"})
    for region in reg_dict.keys():
        regions = reg_dict[region]
        regdata = pd.DataFrame(new[new.UNRegion.isin(regions)])
        newdata = pd.DataFrame()
        newdata[years] = pd.Series(regdata.loc[regdata.Year == years][readcol].sum()/1000)
        newdata["Scenario"] = "Estimates"
        newdata["IPCCRegion"] = region
        all_data = pd.concat((all_data, 
                    newdata), axis=0)

    return all_data

# %%
def ipcc_create1R(all_data: pd.DataFrame, years: list):
    """All_data is dataframe with all UN data
    years is list of years to select in dataframe
    Returns three dataframe: world, regional,
    and other rest of world data for 1R IPCC"""
    sortcolumns = ["IPCCRegion", "UNRegion",	"Scenario"] + years
    world = all_data[all_data.IPCCRegion=="WORLD"]
    world = world.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    world["UNRegion"] = "WORLD"
    world = world[sortcolumns]

    regdata = pd.DataFrame()

    owo = pd.DataFrame()
    return (world, regdata, owo)

def ipcc_create6R(all_data: pd.DataFrame, years: list):
    """All_data is a dataframe with UN data for the six regions
    years is list of years to select in dataframe
    Returns three dataframes: world, regional,
    and other rest of world data for 6R IPCC 
    R5ROWO is empty
    """
    sortcolumns = ["IPCCRegion", "UNRegion", "Scenario"] + years

    world = all_data[all_data.IPCCRegion=="WORLD"]
    world = world.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    world["UNRegion"] = "WORLD"
    world = world[sortcolumns]

    asia = all_data[all_data.IPCCRegion=="R6ASIA"]
    asia = asia.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    asia["UNRegion"] = "Eastern, Southern, South-Eastern Asia"
    asia = asia[world.columns] #re-order columns

    lam = all_data[all_data.IPCCRegion=="R6LAM"]
    lam = lam.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    lam["UNRegion"] = "Latin America"
    lam = lam[world.columns] #re-order columns

    maf = all_data[all_data.IPCCRegion=="R6AFRICA"]
    maf = maf.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    maf["UNRegion"] = "Africa"
    maf = maf[world.columns] #re-order columns

    med = all_data[all_data.IPCCRegion=="R6MIDDLE_EAST"]
    med = med.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    med["UNRegion"] = "Middle East"
    med = med[world.columns] #re-order columns

    oecd = all_data[all_data.IPCCRegion=="R6OECD90+EU"]
    oecd = oecd.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    oecd["UNRegion"] = "OECD"
    oecd = oecd[world.columns] #re-order columns

    ref = all_data[all_data.IPCCRegion=="R6REF"]
    ref = ref.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    ref["UNRegion"] = "Reformation Regions"
    ref = ref[world.columns] #re-order columns

    regdata = pd.concat((pd.concat((pd.concat((pd.concat((pd.concat((asia, lam)), maf)), med)),oecd)), ref))

    o = regdata.groupby("Scenario")[years].sum().reset_index()

    o["IPCCRegion"] = "Sum IPCC"
    o["UNRegion"] = "Sum UN"

    wo= pd.concat((world,o))
    wog = wo.groupby("Scenario")
    owo = pd.DataFrame()

    for group  in wog:
        sel = group[1]
        x = sel.loc[sel["UNRegion"]=="WORLD"][years]-sel.loc[sel["UNRegion"]=="Sum UN"][years]
        owo = pd.concat((owo, x))
    owo = owo.where(owo >0,0)
    owo["UNRegion"] = "OWO"
    owo["IPCCRegion"] = "R6OWO"
    owo["Scenario"] = world["Scenario"]
    owo = owo[world.columns]
    return (world, regdata, owo)

def ipcc_create5R(all_data: pd.DataFrame, years: list):
    """All_data is dataframe with all UN data
    years is list of years to select in dataframe
    Returns three dataframe: world, regional,
    and other rest of world data for 5R IPCC"""
    sortcolumns = ["IPCCRegion", "UNRegion",	"Scenario"] + years
    world = all_data[all_data.IPCCRegion=="WORLD"]
    world = world.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    world["UNRegion"] = "WORLD"
    world = world[sortcolumns]

    asia = all_data[all_data.IPCCRegion=="R5ASIA"]
    asia = asia.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    asia["UNRegion"] = "Eastern, Southern, South-Eastern Asia"
    asia = asia[world.columns] #re-order columns

    lam = all_data[all_data.IPCCRegion=="R5LAM"]
    lam = lam.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    lam["UNRegion"] = "Latin America"
    lam = lam[world.columns] #re-order columns

    maf = all_data[all_data.IPCCRegion=="R5MAF"]
    maf = maf.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    maf["UNRegion"] = "Middle East - Africa"
    maf = maf[world.columns] #re-order columns

    oecd = all_data[all_data.IPCCRegion=="R5OECD90+EU"]
    oecd = oecd.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    oecd["UNRegion"] = "OECD"
    oecd = oecd[world.columns] #re-order columns

    ref = all_data[all_data.IPCCRegion=="R5REF"]
    ref = ref.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    ref["UNRegion"] = "Reforming Economies"
    ref = ref[world.columns] #re-order columns

    regdata = pd.concat((pd.concat((pd.concat((pd.concat((asia, lam)), maf)),oecd)),ref))

    o = regdata.groupby("Scenario")[years].sum().reset_index()

    o["IPCCRegion"] = "Sum IPCC"
    o["UNRegion"] = "Sum UN"

    wo= pd.concat((world,o))
    wog = wo.groupby("Scenario")
    owo = pd.DataFrame()

    for group  in wog:
        sel = group[1]
        x = sel.loc[sel["UNRegion"]=="WORLD"][years]-sel.loc[sel["UNRegion"]=="Sum UN"][years]
        owo = pd.concat((owo, x))
    owo = owo.where(owo >0,0)
    owo["UNRegion"] = "OWO"
    owo["IPCCRegion"] = "R5OWO"
    owo["Scenario"] = world["Scenario"]
    owo = owo[world.columns]
    return (world, regdata, owo)

def ipcc_create10R(all_data: pd.DataFrame, years: list):
    """All_data is dataframe with all UN data
    years is list of years to select in dataframe
    Returns three dataframe: world, regional,
    and other rest of world data for 10R IPCC"""
    sortcolumns = ["IPCCRegion", "UNRegion",	"Scenario"] + years
    world = all_data[all_data.IPCCRegion=="WORLD"]
    world = world.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    world["UNRegion"] = "WORLD"
    world = world[sortcolumns]

    africa = all_data[all_data.IPCCRegion=="R10AFRICA"]
    africa = africa.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    africa["UNRegion"] = "Africa"
    africa = africa[world.columns] #re-order columns

    china = all_data[all_data.IPCCRegion=="R10CHINA+"]
    china = china.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    china["UNRegion"] = "China plus"
    china = china[world.columns] #re-order columns

    euro = all_data[all_data.IPCCRegion=="R10EUROPE"]
    euro = euro.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    euro["UNRegion"] = "Europe"
    euro = euro[world.columns] #re-order columns

    india = all_data[all_data.IPCCRegion=="R10INDIA+"]
    india = india.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    india["UNRegion"] = "India plus"
    india = india[world.columns] #re-order columns

    lam = all_data[all_data.IPCCRegion=="R10LATIN_AM"]
    lam = lam.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    lam["UNRegion"] = "Latin America"
    lam = lam[world.columns] #re-order columns

    meast = all_data[all_data.IPCCRegion=="R10MIDDLE_EAST"]
    meast = meast.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    meast["UNRegion"] = "Middle East"
    meast = meast[world.columns] #re-order columns

    northam = all_data[all_data.IPCCRegion=="R10NORTH_AM"]
    northam = northam.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    northam["UNRegion"] = "North America"
    northam = northam[world.columns] #re-order columns

    pac = all_data[all_data.IPCCRegion=="R10PAC_OECD"]
    pac = pac.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    pac["UNRegion"] = "OECD"
    pac = pac[world.columns] #re-order columns

    ref = all_data[all_data.IPCCRegion=="R10REF_ECON"]
    ref = ref.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    ref["UNRegion"] = "Reforming Economies"
    ref = ref[world.columns] #re-order columns

    rasia = all_data[all_data.IPCCRegion=="R10REST_ASIA"]
    rasia= rasia.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
    rasia["UNRegion"] = "Rest of Asia"
    rasia= rasia[world.columns] #re-order columns

    regdata = pd.concat((pd.concat((pd.concat((africa,china)), euro)), india))
    regdata = pd.concat((pd.concat((regdata,lam)), meast))
    regdata = pd.concat((pd.concat((regdata,northam)), pac))    
    regdata = pd.concat((pd.concat((regdata,ref)), rasia))

    o = regdata.groupby("Scenario")[years].sum().reset_index()

    o["IPCCRegion"] = "Sum IPCC"
    o["UNRegion"] = "Sum UN"

    wo= pd.concat((world,o))
    wog = wo.groupby("Scenario")
    owo = pd.DataFrame()

    for group  in wog:
        sel = group[1]
        x = sel.loc[sel["UNRegion"]=="WORLD"][years]-sel.loc[sel["UNRegion"]=="Sum UN"][years]
        owo = pd.concat((owo, x))
    owo = owo.where(owo >0,0)
    owo["UNRegion"] = "OWO"
    owo["IPCCRegion"] = "R5OWO"
    owo["Scenario"] = world["Scenario"]
    owo = owo[world.columns]
    return (world, regdata, owo)

# %%
def un_tseries2022 (years, filename, numregions, ipccregion, countries):
    """Create a full dataframe including 2020 (taken from "Estimates")
    which is historical value in UN projections
    and is then followed by probabilistic projections for population
    This is to be used when there is no interest in the
    variation of historical values across the projection revision.
    Values are in million inhabitants."""
    """
    It receives:
    years: list of years (greater or equal than 2023)
    filename: name of a file with probabilistic projections
    numregions: integer on the number of IPCC regions
    ipccregion: True for grouping UN data into IPCC regions
    countries: list of UN countries to read and group into one "modelregion"

    It generates a tuple with
    w: dataframe with global values of probabilistic projections
    r: dataframe with regional values of probabilistic projections
    o: dataframe with "other regional" values of probabilistic projections
    """
    ryears =[y for y in years if y != 2020]
    all_data = un_reading(ryears, filename, numregions, ipccregion, countries)

    if ipccregion:
        if numregions==1:
            w, r, o = ipcc_create1R(all_data, ryears)
        if numregions==5:
            w, r, o = ipcc_create5R(all_data, ryears)
        if numregions==6:
            w, r, o = ipcc_create6R(all_data, ryears)
        if numregions==10:
            w, r, o = ipcc_create10R(all_data, ryears)
    else:
        w = pd.DataFrame()
        sortcolumns = ["IPCCRegion", "UNRegion",	"Scenario"] + ryears
        w = all_data[all_data["UNRegion"].isin(countries)]
        w = w.groupby(["IPCCRegion", "Scenario"])[ryears].sum().reset_index()
        w["UNRegion"] = "modelregion"
        w = w[sortcolumns]
        r = pd.DataFrame()
        o = pd.DataFrame()        

    if 2020 in years:
        w2020 = un_reading2020(2020, filename, numregions, ipccregion, countries)
        if ipccregion:
            w[2020] = w2020.loc[w2020.IPCCRegion == "WORLD"][2020].values[0]
        else:
            w[2020] = w2020.loc[w2020.IPCCRegion == "modelregion"][2020].values[0]
        sortcolumns = ["IPCCRegion",  "Scenario", "UNRegion"] + years

        w = w[sortcolumns]

        if numregions==1:
            r = pd.DataFrame()
            o = pd.DataFrame()
        
        else:
            all_regions = pd.DataFrame()
            for reg in list(set(r.IPCCRegion)):
                new = pd.DataFrame(r.loc[r.IPCCRegion==reg])
                new[2020] = w2020.loc[w2020.IPCCRegion == reg][2020].values[0]
                new = new[sortcolumns]
                all_regions = pd.concat((all_regions, new))
            r = all_regions
            if numregions==4:
                o[2020] = w2020.loc[w2020.IPCCRegion == "WORLD"][2020].values[0] - (
                        + w2020.loc[w2020.IPCCRegion == "R5ASIA"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R5LAM"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R5MAF"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R5OECD90+EU"][2020].values[0]
                )
            if numregions==5:
                o[2020] = w2020.loc[w2020.IPCCRegion == "WORLD"][2020].values[0] - (
                        + w2020.loc[w2020.IPCCRegion == "R5ASIA"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R5LAM"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R5MAF"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R5OECD90+EU"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R5REF"][2020].values[0]
                )
            if numregions==6:
                o[2020] = w2020.loc[w2020.IPCCRegion == "WORLD"][2020].values[0] - (
                        + w2020.loc[w2020.IPCCRegion == "R6ASIA"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R6LAM"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R6AFRICA"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R6MIDDLE_EAST"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R6OECD90+EU"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R6REF"][2020].values[0]
                )

            if numregions==10:
                o[2020] = w2020.loc[w2020.IPCCRegion == "WORLD"][2020].values[0] - (
                        + w2020.loc[w2020.IPCCRegion == "R10AFRICA"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R10CHINA+"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R10EUROPE"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R10INDIA+"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R10LATIN_AM"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R10MIDDLE_EAST"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R10NORTH_AM"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R10PAC_OECD"][2020].values[0]
                        + w2020.loc[w2020.IPCCRegion == "R10REF_ECON"][2020].values[0]   
                        + w2020.loc[w2020.IPCCRegion == "R10REST_ASIA"][2020].values[0]                    
                )
            o[2020] = o[2020].where(o[2020] >0, 0)         
            o = o[sortcolumns]
    
    return (w, r, o)

# Note that to be adapted to 2015 different file:
# tabs were renamed: "Upper80" into "Upper 80" and so forth for ll the percentiles
# "Major area, region, country or area" changed into "Region, subregion, country or area *"
# In PPP2017, "Major area, region, country or area" changed into "Region, subregion, country or area *"
# In PPP2019, "Major area, region, country or area" changed into "Region, subregion, country or area *"
def un_tseries (years, filename, numregions, ipccregion, countries):
    """Create a full probabilistic dataframe
        of probabilistic projections for population
        For revisions 2015, 2017, 2019.
        Values are in million inhabitants."""
    """It receives:
    years: list of years (greater or equal than 2023)
    filename: name of a file with probabilistic projections
    numregions: integer on the number of IPCC regions
    ipccregion: True for grouping UN data into IPCC regions
    countries: list of UN countries to read and group into one "modelregion"

    It generates a tuple with
    w: dataframe with global values of probabilistic projections
    r: dataframe with regional values of probabilistic projections
    o: dataframe with "other regional" values of probabilistic projections"""

    all_data = un_reading(years, filename, numregions, ipccregion, countries)
    if ipccregion:
        if numregions==1:
            w, r, o = ipcc_create1R(all_data, years)  
        if numregions==5:
            w, r, o = ipcc_create5R(all_data, years)
        if numregions==6:
            w, r, o = ipcc_create6R(all_data, years)      
        if numregions==10:
            w, r, o = ipcc_create10R(all_data, years)
    else:
        w = pd.DataFrame()
        sortcolumns = ["IPCCRegion", "UNRegion",	"Scenario"] + years
        w = all_data[all_data["UNRegion"].isin(countries)]
        w = w.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
        w["UNRegion"] = "modelregion"
        w = w[sortcolumns]
        r = pd.DataFrame()
        o = pd.DataFrame()         
   
    return (w, r, o)

# %%
def un_extraction (rex: str, years: list):
    """Extracts future years estimates of deterministic population
    Values are in million inhabitants"""
    """Receives:
    - rex: region name (native UN region)
    - years: list of years to consider
    Returns:
    all: dataframe with all population scenarios (deterministic)
    for the selected region"""
    path = "data/UN"
    tabs = ["Medium variant", "High variant", 
            "Low variant", "Constant-fertility", 
            "Instant-replacement", "Instant-replacement zero migr", 
            "Momentum","Zero-migration", 
            "Constant-mortality", "No change",
            "No_AIDS_Projection", "AIDS_Projection"]

    files = ["WPP2010_GEN_DEMOGRAPHIC_INDICATORS.xlsx",
            "WPP2012_GEN_DEMOGRAPHIC_INDICATORS.xlsx",
            "WPP2015_GEN_DEMOGRAPHIC_INDICATORS.xlsx",
            "WPP2017_GEN_DEMOGRAPHIC_INDICATORS.xlsx",
            "WPP2019_GEN_DEMOGRAPHIC_INDICATORS.xlsx",
            "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_REV1.xlsx"]

    columns = [str(y) for y in years] + ["Region", "Scenario","Variant"]
    revision = ["2010", "2012", "2015", "2017", "2019", "2022"]
    all_data = pd.DataFrame()
    for file in files:
        destination = os.path.join(path,file)
        data_col = "Total Population, as of 1 July (thousands)"
        region_col = "Region, subregion, country or area *"
        year = "Year"
        for tab in tabs:
            data = pd.read_excel(destination, tab, skiprows=16)
            if len(data) > 1:
                regions = list(set(data[region_col]))
                if rex in regions:
                    current_year = revision[files.index(file)]
                    variant = "revision_" + current_year
                    region = rex
                    regdata = data.loc[data[region_col]== region]
                    new = pd.DataFrame()
                    for n in years:
                        datasel = pd.DataFrame(regdata.loc[regdata["Year"]==n][data_col].values)
                        new[str(n)] = datasel
                    new["Scenario"] = tab
                    new["Region"] = region
                    new["Variant"] = variant

                    all_data = pd.concat((all_data, 
                                new[columns]), axis=0)
                            
    all = all_data.copy(deep=True)
    all[all.columns[:9] ]= all[all.columns[:9]]/1000

    return (all)

# %%
def un_reading_historical(years: float, filename: str, numregions: int, ipccregion: bool, countries: list):
    """Estimates UN deterministic values in million inhab for historical years
    Receives:
        years: list of historical years (2000, 2005, 2010, 2015, 2020)
        filename: name of a file with probabilistic projections 
        numregions: number of IPCC regions to extract (1, 5, 6, 10)
        ipccregion: True for grouping UN data into IPCC regions
        countries: list of UN countries to read and group into one "modelregion"
    Generates:
        all_data: dataframe with population value per year on a single column
        regions correspond to each single row
        scenario is the "Estimate" scenario of UN"""
    folder = r'data/UN'
    destination = os.path.join (folder, filename)
    data = pd.read_excel(destination,"Estimates", skiprows=16)
    region_col = "Region, subregion, country or area *"
    readcol = "Total Population, as of 1 July (thousands)"
    columns = [region_col] + ["Year"] + [readcol]
    new = data[columns]

    if ipccregion:
        if numregions==1:
            reg_dict = createIPCC1R()
        if numregions==5:
            reg_dict = createIPCC5R()
        if numregions==6:
            reg_dict = createIPCC6R()
        if numregions==10:
            reg_dict = createIPCC10R()

    else:
        world = pd.DataFrame()
        sortcolumns = ["IPCCRegion", "UNRegion",	"Scenario"] + years
        for country in countries:
            dworld = all_data[all_data.IPCCRegion==country]
            world = pd.concat((world, dworld))
        world = world.groupby(["IPCCRegion", "Scenario"])[years].sum().reset_index()
        world["UNRegion"] = "modelregion"
        world = world[sortcolumns]
        regdata = pd.DataFrame()
        owo = pd.DataFrame()

    all_data = pd.DataFrame()
    new = new.rename(columns={region_col: "UNRegion"})
    for region in reg_dict.keys():
        regions = reg_dict[region]
        regdata = pd.DataFrame(new[new.UNRegion.isin(regions)])
        newdata = pd.DataFrame(regdata.groupby("Year")[readcol].sum()/1000.0).reset_index()
        newdata["Year"] = pd.Series(newdata["Year"], dtype=int)
        newdata = pd.DataFrame(newdata[newdata.Year.isin(years)]).transpose()
        rename = dict(zip(list(newdata.columns),list(years)))
        newdata = newdata.rename(columns=rename)
        newdata = newdata.reset_index()
        newdata = newdata.drop("index", axis=1)
        newdata["Scenario"] = "Estimates"
        newdata["IPCCRegion"] = region
        newdata["UNRegion"] = region
        columns = ["IPCCRegion", "Scenario", "UNRegion"] + list(years)
        newdata = newdata[columns]
        all_data = pd.concat((all_data, 
                    newdata[1:]), axis=0)
    return all_data




