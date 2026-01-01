from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum
import re
# ISO 3166-1 alpha-2 Ülke Kodları
class RegionEnum(str, Enum):
    AD = "AD"  # Andorra
    AE = "AE"  # United Arab Emirates
    AF = "AF"  # Afghanistan
    AG = "AG"  # Antigua and Barbuda
    AI = "AI"  # Anguilla
    AL = "AL"  # Albania
    AM = "AM"  # Armenia
    AO = "AO"  # Angola
    AQ = "AQ"  # Antarctica
    AR = "AR"  # Argentina
    AS = "AS"  # American Samoa
    AT = "AT"  # Austria
    AU = "AU"  # Australia
    AW = "AW"  # Aruba
    AX = "AX"  # Åland Islands
    AZ = "AZ"  # Azerbaijan
    BA = "BA"  # Bosnia and Herzegovina
    BB = "BB"  # Barbados
    BD = "BD"  # Bangladesh
    BE = "BE"  # Belgium
    BF = "BF"  # Burkina Faso
    BG = "BG"  # Bulgaria
    BH = "BH"  # Bahrain
    BI = "BI"  # Burundi
    BJ = "BJ"  # Benin
    BL = "BL"  # Saint Barthélemy
    BM = "BM"  # Bermuda
    BN = "BN"  # Brunei Darussalam
    BO = "BO"  # Bolivia
    BQ = "BQ"  # Bonaire, Sint Eustatius and Saba
    BR = "BR"  # Brazil
    BS = "BS"  # Bahamas
    BT = "BT"  # Bhutan
    BV = "BV"  # Bouvet Island
    BW = "BW"  # Botswana
    BY = "BY"  # Belarus
    BZ = "BZ"  # Belize
    CA = "CA"  # Canada
    CC = "CC"  # Cocos (Keeling) Islands
    CD = "CD"  # Congo, Democratic Republic of the
    CF = "CF"  # Central African Republic
    CG = "CG"  # Congo
    CH = "CH"  # Switzerland
    CI = "CI"  # Côte d'Ivoire
    CK = "CK"  # Cook Islands
    CL = "CL"  # Chile
    CM = "CM"  # Cameroon
    CN = "CN"  # China
    CO = "CO"  # Colombia
    CR = "CR"  # Costa Rica
    CU = "CU"  # Cuba
    CV = "CV"  # Cabo Verde
    CW = "CW"  # Curaçao
    CX = "CX"  # Christmas Island
    CY = "CY"  # Cyprus
    CZ = "CZ"  # Czechia
    DE = "DE"  # Germany
    DJ = "DJ"  # Djibouti
    DK = "DK"  # Denmark
    DM = "DM"  # Dominica
    DO = "DO"  # Dominican Republic
    DZ = "DZ"  # Algeria
    EC = "EC"  # Ecuador
    EE = "EE"  # Estonia
    EG = "EG"  # Egypt
    EH = "EH"  # Western Sahara
    ER = "ER"  # Eritrea
    ES = "ES"  # Spain
    ET = "ET"  # Ethiopia
    FI = "FI"  # Finland
    FJ = "FJ"  # Fiji
    FK = "FK"  # Falkland Islands (Malvinas)
    FM = "FM"  # Micronesia
    FO = "FO"  # Faroe Islands
    FR = "FR"  # France
    GA = "GA"  # Gabon
    GB = "GB"  # Great Britain
    GD = "GD"  # Grenada
    GE = "GE"  # Georgia
    GF = "GF"  # French Guiana
    GG = "GG"  # Guernsey
    GH = "GH"  # Ghana
    GI = "GI"  # Gibraltar
    GL = "GL"  # Greenland
    GM = "GM"  # Gambia
    GN = "GN"  # Guinea
    GP = "GP"  # Guadeloupe
    GQ = "GQ"  # Equatorial Guinea
    GR = "GR"  # Greece
    GS = "GS"  # South Georgia and the South Sandwich Islands
    GT = "GT"  # Guatemala
    GU = "GU"  # Guam
    GW = "GW"  # Guinea-Bissau
    GY = "GY"  # Guyana
    HK = "HK"  # Hong Kong
    HM = "HM"  # Heard Island and McDonald Islands
    HN = "HN"  # Honduras
    HR = "HR"  # Croatia
    HT = "HT"  # Haiti
    HU = "HU"  # Hungary
    ID = "ID"  # Indonesia
    IE = "IE"  # Ireland
    IL = "IL"  # Israel
    IM = "IM"  # Isle of Man
    IN = "IN"  # India
    IO = "IO"  # British Indian Ocean Territory
    IQ = "IQ"  # Iraq
    IR = "IR"  # Iran
    IS = "IS"  # Iceland
    IT = "IT"  # Italy
    JE = "JE"  # Jersey
    JM = "JM"  # Jamaica
    JO = "JO"  # Jordan
    JP = "JP"  # Japan
    KE = "KE"  # Kenya
    KG = "KG"  # Kyrgyzstan
    KH = "KH"  # Cambodia
    KI = "KI"  # Kiribati
    KM = "KM"  # Comoros
    KN = "KN"  # Saint Kitts and Nevis
    KP = "KP"  # North Korea
    KR = "KR"  # South Korea
    KW = "KW"  # Kuwait
    KY = "KY"  # Cayman Islands
    KZ = "KZ"  # Kazakhstan
    LA = "LA"  # Lao People's Democratic Republic
    LB = "LB"  # Lebanon
    LC = "LC"  # Saint Lucia
    LI = "LI"  # Liechtenstein
    LK = "LK"  # Sri Lanka
    LR = "LR"  # Liberia
    LS = "LS"  # Lesotho
    LT = "LT"  # Lithuania
    LU = "LU"  # Luxembourg
    LV = "LV"  # Latvia
    LY = "LY"  # Libya
    MA = "MA"  # Morocco
    MC = "MC"  # Monaco
    MD = "MD"  # Moldova
    ME = "ME"  # Montenegro
    MF = "MF"  # Saint Martin
    MG = "MG"  # Madagascar
    MH = "MH"  # Marshall Islands
    MK = "MK"  # North Macedonia
    ML = "ML"  # Mali
    MM = "MM"  # Myanmar
    MN = "MN"  # Mongolia
    MO = "MO"  # Macao
    MP = "MP"  # Northern Mariana Islands
    MQ = "MQ"  # Martinique
    MR = "MR"  # Mauritania
    MS = "MS"  # Montserrat
    MT = "MT"  # Malta
    MU = "MU"  # Mauritius
    MV = "MV"  # Maldives
    MW = "MW"  # Malawi
    MX = "MX"  # Mexico
    MY = "MY"  # Malaysia
    MZ = "MZ"  # Mozambique
    NA = "NA"  # Namibia
    NC = "NC"  # New Caledonia
    NE = "NE"  # Niger
    NF = "NF"  # Norfolk Island
    NG = "NG"  # Nigeria
    NI = "NI"  # Nicaragua
    NL = "NL"  # Netherlands
    NO = "NO"  # Norway
    NP = "NP"  # Nepal
    NR = "NR"  # Nauru
    NU = "NU"  # Niue
    NZ = "NZ"  # New Zealand
    OM = "OM"  # Oman
    PA = "PA"  # Panama
    PE = "PE"  # Peru
    PF = "PF"  # French Polynesia
    PG = "PG"  # Papua New Guinea
    PH = "PH"  # Philippines
    PK = "PK"  # Pakistan
    PL = "PL"  # Poland
    PM = "PM"  # Saint Pierre and Miquelon
    PN = "PN"  # Pitcairn
    PR = "PR"  # Puerto Rico
    PS = "PS"  # Palestine, State of
    PT = "PT"  # Portugal
    PW = "PW"  # Palau
    PY = "PY"  # Paraguay
    QA = "QA"  # Qatar
    RE = "RE"  # Réunion
    RO = "RO"  # Romania
    RS = "RS"  # Serbia
    RU = "RU"  # Russian Federation
    RW = "RW"  # Rwanda
    SA = "SA"  # Saudi Arabia
    SB = "SB"  # Solomon Islands
    SC = "SC"  # Seychelles
    SD = "SD"  # Sudan
    SE = "SE"  # Sweden
    SG = "SG"  # Singapore
    SH = "SH"  # Saint Helena
    SI = "SI"  # Slovenia
    SJ = "SJ"  # Svalbard and Jan Mayen
    SK = "SK"  # Slovakia
    SL = "SL"  # Sierra Leone
    SM = "SM"  # San Marino
    SN = "SN"  # Senegal
    SO = "SO"  # Somalia
    SR = "SR"  # Suriname
    SS = "SS"  # South Sudan
    ST = "ST"  # Sao Tome and Principe
    SV = "SV"  # El Salvador
    SX = "SX"  # Sint Maarten
    SY = "SY"  # Syrian Arab Republic
    SZ = "SZ"  # Eswatini
    TC = "TC"  # Turks and Caicos Islands
    TD = "TD"  # Chad
    TF = "TF"  # French Southern Territories
    TG = "TG"  # Togo
    TH = "TH"  # Thailand
    TJ = "TJ"  # Tajikistan
    TK = "TK"  # Tokelau
    TL = "TL"  # Timor-Leste
    TM = "TM"  # Turkmenistan
    TN = "TN"  # Tunisia
    TO = "TO"  # Tonga
    TR = "TR"  # Türkiye
    TT = "TT"  # Trinidad and Tobago
    TV = "TV"  # Tuvalu
    TW = "TW"  # Taiwan
    TZ = "TZ"  # Tanzania
    UA = "UA"  # Ukraine
    UG = "UG"  # Uganda
    UM = "UM"  # United States Minor Outlying Islands
    US = "US"  # United States of America
    UK = "UK"  # United Kingdom
    UY = "UY"  # Uruguay
    UZ = "UZ"  # Uzbekistan
    VA = "VA"  # Holy See
    VC = "VC"  # Saint Vincent and the Grenadines
    VE = "VE"  # Venezuela
    VG = "VG"  # Virgin Islands (British)
    VI = "VI"  # Virgin Islands (U.S.)
    VN = "VN"  # Viet Nam
    VU = "VU"  # Vanuatu
    WF = "WF"  # Wallis and Futuna
    WS = "WS"  # Samoa
    YE = "YE"  # Yemen
    YT = "YT"  # Mayotte
    ZA = "ZA"  # South Africa
    ZM = "ZM"  # Zambia
    ZW = "ZW"  # Zimbabwe

class ClanBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=25, description="Klan adı")
    region: RegionEnum = Field(..., description="ISO 3166-1 alpha-2 Bölge Kodu")

    @field_validator('name')
    def validate_name_chars(cls, v):
        v = v.strip() # Kenar boşluklarını temizle
        
        # GÜNCELLENMİŞ REGEX: 
        # Boşluk karakteri ( ) kaldırıldı.
        # Sadece: a-z, A-Z, 0-9, tire (-) ve alt çizgi (_)
        pattern = r"^[a-zA-Z0-9_-]+$"
        
        if not re.match(pattern, v):
            # Hata mesajını da güncelledik
            raise ValueError("Klan adı boşluk içeremez. Sadece harf, rakam, tire (-) ve alt çizgi (_) kullanabilirsiniz.")
        
        if v.isdigit():
             raise ValueError("Klan adı sadece rakamlardan oluşamaz.")
             
        return v

class ClanCreate(ClanBase):
    pass

class Clan(ClanBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True