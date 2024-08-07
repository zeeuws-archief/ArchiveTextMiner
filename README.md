![Logo](https://raw.githubusercontent.com/zeeuws-archief/ArchiveTextMiner/main/ArchiveTextMiner_logo.png "Logo")

# ArchiveTextMiner: van tekstuele informatie naar gestructureerde metadata in MDTO-formaat

[English text below](#english-text)

## 🚀 Probeer nu de [ArchiveTextMiner Demo](https://es-connector.acc.zeeland.nl/atm_demo)!
## 🚀 Laat feedback over ArchiveTextMiner achter: [Feedbackformulier](https://www.survio.com/survey/d/M2M8O7E8Y5D1V6J3A)


### 📝 Wat is het? 
ArchiveTextMiner is een Python package die specifiek is ontworpen om tekstuele informatie uit PDF-bestanden te halen en metadata te creëren. De tool schoont de tekst op en verwerkt het per bestand, om vervolgens gestructureerde XML-bestanden met metadata in MDTO-formaat te genereren. Het primaire doel is om ongestructureerde gegevens om te zetten in gestructureerde metadata, waardoor doorzoekbaarheid wordt verbeterd.

### 📖 Inhoud

1. [Kenmerken](#kenmerken)
2. [Benodigdheden](#benodigdheden)
3. [Installatie](#installatie)
4. [Gebruik](#gebruik)
5. [Voorbeeld](#voorbeeld)
6. [Licentie](#licentie)
7. [Bijdragen](#bijdragen)
8. [Toekomstige stappen](#toekomst)
9. [Disclaimer](#disclaimer)
10. [Auteurs](#auteurs)
11. [Dankwoord](#dankwoord)

### 🔥 Kenmerken<a name="kenmerken"></a>

1. **Verwerking van meerdere bestanden:** ArchiveTextMiner kan meerdere PDF-bestanden binnen een  gecomprimeerde map verwerken. 

2. **Bestandsextractie en voorbereiding:** De tool begint met het extraheren van bestanden uit de invoermap en creëert een nieuwe mappenstructuur waarin de invoerbestanden en metadatabestanden kunnen worden bewaard.

3. **Metadata-opslag:** De tool creëert een map genaamd ArchiveTextMiner, voor het opslaan van metagegevensbestanden, zodat er een goed georganiseerd opslagsysteem is voor de verwerkte gegevens.

4. **Identificatie van PDF-bestanden:** De tool identificeert alle PDF-bestanden op die zich bevinden binnen de geëxtraheerde bestanden, zodat ze gereed zijn voor verdere verwerking.

5. **Tekstextractie uit PDF's:** De tool haalt tekstinhoud uit elk geïdentificeerd PDF-bestand met behulp van de `extract_text_from_pdf` functie.

6. **Tekst opschonen:** De geëxtraheerde tekst ondergaat een opschoningsproces (`clean_dutch_text`) om het voor te bereiden op verdere analyse.

7. **MDTO Metadata-genereren:** De gegenereerde metadata wordt geplaatst in een MDTO-schema (Metadata voor Duurzame Toegankelijke Overheidsinformatie), waardoor naleving van Nederlandse overheidsrichtlijnen wordt gewaarborgd. Momenteel kunnen de hieronder gespecificeerde metagegevensvelden worden gegenereerd. Als er geen geschikte informatie wordt gevonden in het document, blijft het betreffende gegevensveld leeg.

   - **Genereren van werktitel:** Genereert een werktitel uit de gereinigde tekst (`generate_working_title`).
   - **Herkenning van bestandsgrootte:** De tool berekent de grootte van het PDF-bestand in bytes (`generate_size`).
   - **Taalherkenning:** De tool identificeert de taal van de tekst (`detect_language`).
   - **Samenvatting genereren:** De tool vat de tekstinhoud samen in één zin (`generate_summary`).
   - **Extractie van topzoekwoorden:** De tool haalt topzoekwoorden uit de tekst (`extract_top_keywords`).
   - **KVK-nummerextractie:** Identificeert KVK-nummers binnen de tekst (`extract_kvk_numbers`).
   - **BSN-extractie:** Haalt geldige BSN (Burgerservicenummer) uit de tekst (`extract_valid_bsn_numbers`).
   - **Identificatie van MIME-type:** Bepaalt het MIME-type van het bestand (`get_file_mime_type`).

8. **Creëren van XML-bestanden:** Met behulp van de geëxtraheerde metadata genereert de tool XML-bestanden in MDTO-formaat voor elk PDF-bestand, waarin de afgeleide informatie is opgenomen.

9. **Geschreven in Python:** De tool is flexibel en eenvoudig integreerbaar in bestaande workflows of aanpasbaar volgens individuele vereisten.

### 🖥️ Benodigdheden<a name="benodigdheden"></a>
```python
click==8.1.7
colorama==0.4.6
joblib==1.3.2
langdetect==1.0.9
nltk==3.8.1
numpy==1.26.3
PyPDF2==3.0.1
python-magic-bin==0.4.14
regex==2023.12.25
scikit-learn==1.3.2
scipy==1.11.4
setuptools==69.0.3
six==1.16.0
threadpoolctl==3.2.0
tqdm==4.66.1
```
### 💿 Installatie<a name="installatie"></a>
1. Installeer de benodigde Python bibliotheken met pip:
    ```python
    pip install langdetect
    pip install PyPDF2
    pip install python-magic
    pip install sentencepiece
    ```
   
2. Installeer ArchiveTextMiner met pip:
    ```python
    pip install ArchiveTextMiner
    ```

3. Importeer de generator
    ```python
    from ArchiveTextMiner import generator
    ```

### 👩‍💻 Gebruik<a name="gebruik"></a>
Volg deze stappen om de tool te gebruiken:

***Voorbereidende stappen***
1. Maak een map **en noem deze `input`**. U kunt de locatie voor deze map zelf bepalen.
2. Voeg de **te verwerken bestanden** samen in een map en comprimeer deze map naar een ZIP-bestand. 
3. Verplaats de gezipte map naar de `input`-map. Hierdoor weet ArchiveTextMiner waar de te verwerken bestanden zich bevinden.

***De tool gebruiken***

4. Verander de Python directory naar de locatie van de `input`-map. 
    ```python
    import os
    os.chdir("/voorbeeldlocatie/input")
    ```

5. Run de ArchiveTextMiner

    ```python
    generator.MDTO("/voorbeeldlocatie/input/bestanden.zip")
    ```
ArchiveTextMiner pakt de gezipte map uit en maakt een nieuwe map genaamd `ArchiveTextMiner` in de uitgepakte map. Hierin bevinden zich de nieuwe metadatabestanden. 
### 👨‍🏫 Voorbeeld<a name="voorbeeld"></a> 
```
python ArchiveTextMiner


     _             _     _          _____         _   __  __ _
    / \   _ __ ___| |__ (_)_   ____|_   _|____  _| |_|  \/  (_)_ __   ___ _ __
   / _ \ | '__/ __| '_ \| \ \ / / _ \| |/ _ \ \/ / __| |\/| | | '_ \ / _ \ '__|
  / ___ \| | | (__| | | | |\ V /  __/| |  __/>  <| |_| |  | | | | | |  __/ |
 /_/   \_\_|  \___|_| |_|_| \_/ \___||_|\___/_/\_/\__|_|  |_|_|_| |_|\___|_|



Welkom bij ArchiveTextMiner. 

ArchiveTextMiner starten...

Let op: De tekst in het veld 'omschrijving' is gegenereerd door kunstmatige intelligentie (AI). De betrouwbaarheid van de inhoud kan niet worden gegarandeerd; deze is enkel bedoeld voor de verrijking van metadata.

Bezig met uitpakken van input\bestanden.zip naar input\bestanden...

Uitpakken afgerond.

PDF-bestanden uitpakken in input\bestanden...

Bestanden ['Bestand-A.pdf', 'Bestand-B.pdf', 'Bestand-C.pdf'] gevonden.
Bezig met creëren metadata bestanden...

Bestand-A.pdf.xml succesvol gecreëerd.
Bestand-B.pdf.xml succesvol gecreëerd.
Bestand-C.pdf.xml succesvol gecreëerd.

Metadatabestanden opgeslagen in inputmap.

ArchiveTextMiner afgerond.

```

### 🔑 Licentie<a name="licentie"></a>
Deze tool wordt vrijgegeven onder de [European Union Public Licence V. 1.2](LICENSE).

### 🐞Bijdragen<a name="bijdragen"></a>
ArchiveTextMiner is een actief project. Bijdragen van gebruikers zijn daarom welkom.

- **Bugmeldingen:** Als u problemen of bugs tegenkomt tijdens het gebruik van ArchiveTextMiner, open dan een probleem op onze GitHub-repository. Zorg ervoor dat u gedetailleerde informatie over het opgetreden probleem en de stappen om het te reproduceren, opneemt.

- **Functieverzoeken:** Suggesties kunnen worden ingediend via GitHub-issues als u ideeën hebt voor een nieuwe functie of verbetering.

- **Pull-requests:** Bijdragen in de vorm van pull-requests worden op prijs gesteld.
🚀🚀🚀🚀
### 🔮 Toekomstige stappen<a name="toekomst"></a>
Om de tool te optimaliseren, werken we aan nieuwe toepassingen en functionaliteiten voor ArchiveTextMiner. We zijn momenteel bezig met:

- Toevoegen van meer MDTO-velden.

In de toekomst staan de volgende stappen gepland:

- Verbetering van functionaliteit om MDTO-velden aan te vullen (niet alleen genereren, maar ook bestaande metagegevens aanvullen).
- Mogelijkheid van het instellen welke MDTO-velden vereist zijn om te genereren.
- Integratie in processen en applicaties.

### ❕ Disclaimer<a name="disclaimer"></a>
ArchiveTextMiner maakt gebruik van open-source modellen die zijn samengevoegd voor het extractie- en conversieproces. Hoewel aanzienlijke inspanningen zijn geleverd om nauwkeurigheid te waarborgen, wordt benadrukt dat de prestaties van de tool kunnen variëren op basis van de aard en kwaliteit van de invoergegevens. De nauwkeurigheid en geschiktheid van de geëxtraheerde gegevens zijn de exclusieve verantwoordelijkheid van de gebruikers. De functionaliteit van de tool berust op modellen en algoritmen die open-source zijn en onderhevig zijn aan mogelijke beperkingen, vooroordelen of onnauwkeurigheden die inherent zijn aan dergelijke modellen. Het wordt ten zeerste aanbevolen dat gebruikers de geëxtraheerde gegevens verifiëren en valideren tegen de originele bronmaterialen of door passende middelen om de nauwkeurigheid en geschiktheid voor hun beoogde doeleinden te waarborgen.

De ontwikkelaars en bijdragers van ArchiveTextMiner wijzen alle garanties of garanties met betrekking tot de nauwkeurigheid, volledigheid of betrouwbaarheid van de geëxtraheerde gegevens af. Gebruikers worden aangemoedigd om hun discretie en beoordelingsvermogen te gebruiken bij het gebruik van de tool en de output voor kritieke of gevoelige toepassingen.

### 🖋️ Auteurs<a name="auteurs"></a>
- [Muriël Valckx](https://github.com/murielvalckx)
- [Simon Pouwelse](https://github.com/simonpouwelse)

### 👍 Dankwoord<a name="dankwoord"></a>
Hierbij willen wij de ontwikkelaars van de open-source modellen en bibliotheken die in ArchiveTextMiner worden gebruikt bedanken voor het beschikbaar stellen van hun open-source content.

© Zeeuws Archief and Provincie Zeeland - Alle rechten voorbehouden.

<img src="https://raw.githubusercontent.com/zeeuws-archief/ArchiveTextMiner/main/ArchiveTextMiner_favicon.png" alt="Favicon" title="Favicon" width="40" height="40" />

###

# ArchiveTextMiner: from textual information to structured metadata in MDTO-format<a name="english-text"></a>


### 📝 What is it? 
ArchiveTextMiner is a Python package specifically designed to extract and convert textual information from PDF files contained within a compressed (zipped) folder. This tool automates the extraction of text from PDF files, cleans and processes the text, and generates structured XML files containing metadata in MDTO-format, derived from the extracted content. Its primary objective is to transform unstructured data into structured metadata, enhancing searchability.

### 📖 Table of contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Example](#example)
6. [License](#license)
7. [Contributions](#contributions)
8. [Future steps](#future)
9. [Disclaimer](#disclaimer)
10. [Authors](#authors)
11. [Acknowledgments](#acknowledgments)

### 🔥 Features<a name="features"></a>

1.  **Processing multiple files:** ArchiveTextMiner handles multiple PDF files within a single compressed folder, making it convenient for batch processing.

2. **File extraction and preparation:** The tool starts by extracting files from the provided zipped folder and creates a designated folder structure for further processing.

3. **Metadata storage:** It establishes an output folder structure for storing metadata files, ensuring a well-organized storage system for the processed data.

4. **Identification of PDF files:** The tool identifies and lists all PDF files found within the extracted files, preparing them for subsequent processing.

5. **Text extraction from PDFs:** It extracts text content from each identified PDF file using the `extract_text_from_pdf` function.

6. **Text cleaning:** The extracted Dutch text undergoes a cleaning process (`clean_dutch_text`) to prepare it for further analysis.

7. **MDTO Metadata Generation:** The metadata that is generated is placed in an MDTO-schema (Metadata for Sustainable Accessible Government Information), ensuring compliance with Dutch government guidelines. Currently, the metadata fields specified below can be generated. If no suitable information is found in the document, the respective metadata field will remain empty.
   
   - **Working title generation:** It generates a working title from the cleaned text (`generate_working_title`).
   - **File size extraction:** The tool determines the size of the PDF file (`generate_size`).
   - **Language detection:** It identifies the language of the text (`detect_language`).
   - **Summary extraction:** Summarizes the text content (`generate_summary`).
   - **Top keywords extraction:** Extracts top keywords from the text (`extract_top_keywords`).
   - **KVK-numbers extraction:** Identifies KVK numbers within the text (`extract_kvk_numbers`).
   - **BSN extraction:** Extracts valid BSN (Burgerservicenummer) from the text (`extract_valid_bsn_numbers`).
   - **MIME type identification:** Determines the MIME type of the PDF file (`get_file_mime_type`).

8. **XML file creation:** Using the extracted metadata, it generates XML files in MDTO format for each PDF, incorporating the derived information. 

9.  **Python-based:** The tool is flexible and easily integratable into existing workflows or adaptable according to individual requirements.

### 🖥️ Requirements<a name="requirements"></a>
```python
click==8.1.7
colorama==0.4.6
joblib==1.3.2
langdetect==1.0.9
nltk==3.8.1
numpy==1.26.3
PyPDF2==3.0.1
python-magic-bin==0.4.14
regex==2023.12.25
scikit-learn==1.3.2
scipy==1.11.4
setuptools==69.0.3
six==1.16.0
threadpoolctl==3.2.0
tqdm==4.66.1
```

### 💿 Installation<a name="installation"></a>
1. Install the necessary Python libraries using pip:
    ```python
    pip install langdetect
    pip install PyPDF2
    pip install python-magic
    pip install sentencepiece
    ```
   
2. Install ArchiveTextMiner using pip:
    ```python
    pip install ArchiveTextMiner
    ```

3. Import the generator
    ```python
    from ArchiveTextMiner import generator
    ```

### 👩‍💻 Usage<a name="usage"></a>
Follow these steps to use the tool:

***Preparation steps***
1. Create a folder **and name it `input`**. You can choose the location for this folder.
2. Combine the **files to be processed** into a folder and compress this folder into a ZIP file.
3. Move the zipped folder to the `input` folder. This helps ArchiveTextMiner locate the files to be processed.

***Using the tool***

4. Change the Python directory to the location of the `input` folder.
    ```python
    import os
    os.chdir("/example_location/input")
    ```

5. Run ArchiveTextMiner
    ```python
    generator.MDTO("/example_location/input/files.zip")
    ```
ArchiveTextMiner extracts the zipped folder and creates a new folder named `ArchiveTextMiner` within the extracted folder. Inside, you will find the new metadata files.

### 👨‍🏫 Example (in Dutch)<a name="example"></a>
```
python ArchiveTextMiner


     _             _     _          _____         _   __  __ _
    / \   _ __ ___| |__ (_)_   ____|_   _|____  _| |_|  \/  (_)_ __   ___ _ __
   / _ \ | '__/ __| '_ \| \ \ / / _ \| |/ _ \ \/ / __| |\/| | | '_ \ / _ \ '__|
  / ___ \| | | (__| | | | |\ V /  __/| |  __/>  <| |_| |  | | | | | |  __/ |
 /_/   \_\_|  \___|_| |_|_| \_/ \___||_|\___/_/\_/\__|_|  |_|_|_| |_|\___|_|



Welkom bij ArchiveTextMiner. 

ArchiveTextMiner starten...

Let op: De tekst in het veld 'omschrijving' is gegenereerd door kunstmatige intelligentie (AI). De betrouwbaarheid van de inhoud kan niet worden gegarandeerd; deze is enkel bedoeld voor de verrijking van metadata.

Bezig met uitpakken van input\bestanden.zip naar input\bestanden...

Uitpakken afgerond.

PDF-bestanden uitpakken in input\bestanden...

Bestanden ['Bestand-A.pdf', 'Bestand-B.pdf', 'Bestand-C.pdf'] gevonden.
Bezig met creëren metadata bestanden...

Bestand-A.pdf.xml succesvol gecreëerd.
Bestand-B.pdf.xml succesvol gecreëerd.
Bestand-C.pdf.xml succesvol gecreëerd.

Metadatabestanden opgeslagen in inputmap.

ArchiveTextMiner afgerond.

```

### 🔑 License<a name="license"></a>
This tool is released under the [European Union Public Licence V. 1.2](LICENSE).

### 🐞 Contributions<a name="contributions"></a>
ArchiveTextMiner is an actively evolving project that welcomes contributions from users. 

- **Bug reports:** If you encounter any issues or bugs while using ArchiveTextMiner, please open an issue on our GitHub repository. Be sure to include detailed information about the problem encountered and steps to reproduce it.

- **Feature requests:** Feel free to submit suggestions via GitHub issues if you have an idea for a new feature or enhancement. 

- **Pull requests:** Contributions in the form of pull requests are appreciated. 

### 🔮 Future steps<a name="future"></a>
To optimize the tool, we are working on new applications and functionalities for ArchiveTextMiner. We are currently working on:

- Adding more MDTO fields.

In the future, the following steps are planned:

- Enhancing functionality to supplement MDTO fields (not just generating but also supplementing existing metadata).
- Configuring which MDTO fields are required for completion.
- Integration into processes and applications.

### ❕  Disclaimer<a name="disclaimer"></a>
ArchiveTextMiner utilizes open-source models that are concatenated for the extraction and conversion process. While considerable effort has been made to ensure accuracy, users are advised that the tool's performance may vary based on the nature and quality of the input data. The accuracy and suitability of the extracted data are the sole responsibility of the users. The tool's functionality relies on models and algorithms that are open-source and subject to potential limitations, biases, or inaccuracies inherent in such models. It's highly recommended that users verify and validate the extracted data against the original source materials or through appropriate means to ensure its accuracy and suitability for their intended purposes.

The developers and contributors of ArchiveTextMiner disclaim any warranties or guarantees regarding the accuracy, completeness, or reliability of the extracted data. Users are encouraged to exercise their discretion and judgment when utilizing the tool and its output for any critical or sensitive applications.

### 🖋️ Authors<a name="authors"></a>
- [Muriël Valckx](https://github.com/murielvalckx)
- [Simon Pouwelse](https://github.com/simonpouwelse)


### 👍 Acknowledgments<a name="acknowledgments"></a>
We would like to thank the developers of the open-source models and libraries used in ArchiveTextMiner for making their open-source content available.

 © Zeeuws Archief and Provincie Zeeland - All rights reserved. 
 
 <img src="https://raw.githubusercontent.com/zeeuws-archief/ArchiveTextMiner/main/ArchiveTextMiner_favicon.png" alt="Favicon" title="Facivon" width="40" height="40" />

