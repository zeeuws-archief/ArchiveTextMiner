import zipfile
import os
import re
import PyPDF2
import nltk
import langdetect
import transformers
import magic
import mimetypes
import xml.etree.ElementTree as ET
import warnings

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import DutchStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings("ignore")

nltk.download('punkt')
nltk.download('stopwords')

def extract_zip(zip_file_path, extract_folder):
    base_name = os.path.splitext(os.path.basename(zip_file_path))[0]
    extraction_path = os.path.join(extract_folder)
    os.makedirs(extraction_path, exist_ok=True)
    print("""
     _             _     _          _____         _   __  __ _                 
    / \\   _ __ ___| |__ (_)_   ____|_   _|____  _| |_|  \\/  (_)_ __   ___ _ __ 
   / _ \\ | '__/ __| '_ \\| \\ \\ / / _ \\| |/ _ \\ \\/ / __| |\\/| | | '_ \\ / _ \\ '__|
  / ___ \\| | | (__| | | | |\\ V /  __/| |  __/>  <| |_| |  | | | | | |  __/ |   
 /_/   \\_\\_|  \\___|_| |_|_| \\_/ \\___||_|\\___/_/\\_ \\__|_|  |_|_|_| |_|\\___|_|    
          
 """)
    print()
    print("Welkom bij ArchiveTextMiner.")
    print()
    print("ArchiveTextMiner starten...")
    print()
    print("Let op: De tekst in het veld 'omschrijving' is gegenereerd door kunstmatige intelligentie (AI).",
          "De betrouwbaarheid van de inhoud kan niet worden gegarandeerd;",
          "deze is enkel bedoeld voor de verrijking van metadata.")
    print()
    print(f"Bezig met uitpakken van {zip_file_path} naar {extraction_path}...")
    print()
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

    # Move the extracted files to the correct folder and remove the base_name folder
    extracted_files_path = os.path.join(extract_folder)
    for root, dirs, files in os.walk(os.path.join(extract_folder, base_name)):
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(extracted_files_path, file)
            os.rename(src_path, dst_path)
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))

    # Remove the base_name folder
    os.rmdir(os.path.join(extract_folder, base_name))

    print("Uitpakken afgerond.")
    print()
    return extracted_files_path

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    # Extract text from PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to clean Dutch text
def clean_dutch_text(text):
    # Remove email addresses and hyperlinks
    text = re.sub(r'\S*@\S*\s?', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove content inside "<...>" and "{{...}}"
    text = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', text)
    text = re.sub(r'{{[^>]+}}', '', text)

    # Remove non-alphanumeric characters and punctuation marks
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize text and remove stopwords
    words = word_tokenize(text, language='dutch')
    stop_words = set(stopwords.words('dutch'))
    words = [word for word in words if word.isalpha() and word not in stop_words]

    cleaned_text = ' '.join(words)
    return cleaned_text

# Function to generate working title from cleaned text
def generate_working_title(cleaned_text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([cleaned_text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    word_tfidf_scores = {word: score for word, score in zip(feature_names, tfidf_scores)}
    title_keywords = sorted(word_tfidf_scores, key=word_tfidf_scores.get, reverse=True)[:3]
    title_keywords = ' '.join(word.capitalize() for word in title_keywords)
    return title_keywords

# Function to generate file size
def generate_size(pdf_path):
    size = os.path.getsize(pdf_path)
    return size

# Function to detect language of text
def detect_language(cleaned_text):
    detected_language = langdetect.detect(cleaned_text)
    return detected_language

# Function to generate summary using a pre-trained model
def generate_summary(cleaned_text):
    model = transformers.MBartForConditionalGeneration.from_pretrained("ml6team/mbart-large-cc25-cnn-dailymail-nl-finetune")
    tokenizer = transformers.MBartTokenizer.from_pretrained("facebook/mbart-large-cc25")

    pipeline_summarize = transformers.pipeline(
        task="summarization",
        model=model,
        tokenizer=tokenizer
    )

    pipeline_summarize.model.config.decoder_start_token_id = tokenizer.lang_code_to_id[
        "nl_XX"
    ]
    # Encode the cleaned text with Dutch language code
    inputs = tokenizer.encode(cleaned_text, return_tensors="pt", max_length=1024, truncation=True)

    # Generate summary
    summary_ids = model.generate(inputs, top_p=0.95, top_k=3, max_length=64,
                                 min_length=0, length_penalty=2.0,
                                 num_beams=2, early_stopping=True, do_sample=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Function to extract top keywords from cleaned text
def extract_top_keywords(cleaned_text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([cleaned_text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    word_tfidf_scores = {word: score for word, score in zip(feature_names, tfidf_scores)}
    top_keywords = sorted(word_tfidf_scores, key=word_tfidf_scores.get, reverse=True)[:10]
    return top_keywords

# Function to extract KVK numbers from cleaned text
def extract_kvk_numbers(cleaned_text):
    kvk_pattern = r'\b\d{8}\b'
    kvk_numbers = re.findall(kvk_pattern, cleaned_text)
    return kvk_numbers

# Function to extract valid BSN numbers from text
def extract_valid_bsn_numbers(text):
    bsn_pattern = r'\b(\d{9})\b'
    valid_bsn_numbers = re.findall(bsn_pattern, text)
    return valid_bsn_numbers

# Function to get the mime type of a file
def get_file_mime_type(file_path):
    mime = magic.Magic()
    mime_type = mime.from_file(file_path)
    return mime_type

# Function to create XML file
def create_xml_file(pdf_filename, working_title, size, detected_language, summary,
                    top_keywords, kvk_numbers, valid_bsn_numbers, mime_type,
                    extract_folder):
    pdf_filename = str(pdf_filename)
    working_title = str(working_title)
    size = str(size)
    detected_language = str(detected_language)
    summary = str(summary)
    top_keywords = ', '.join(str(item) for item in top_keywords)
    kvk_numbers = ', '.join(str(item) for item in kvk_numbers)
    valid_bsn_numbers = ', '.join(str(item) for item in valid_bsn_numbers)
    mime_type = str(mime_type)

    root = ET.Element("MDTO", xmlns="https://www.nationaalarchief.nl/mdto", xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance", xsi_schemaLocation="https://www.nationaalarchief.nl/mdto https://www.nationaalarchief.nl/mdto/MDTO-XML1.0.1.xsd")

    bestand = ET.SubElement(root, "bestand")

    identificatie = ET.SubElement(bestand, "identificatie")
    ET.SubElement(identificatie, "identificatieKenmerk").text = ""
    ET.SubElement(identificatie, "identificatieBron").text = ""

    ET.SubElement(bestand, "naam").text = pdf_filename

    omvang = ET.SubElement(bestand, "omvang")
    omvang.text = size

    omschrijving = ET.SubElement(bestand, "omschrijving")
    omschrijving.text = summary

    taal = ET.SubElement(bestand, "taal")
    taal.text = detected_language

    kvknummer = ET.SubElement(bestand, "kvkNummer")
    kvknummer.text = kvk_numbers

    bsn_nummer = ET.SubElement(bestand, "bsnNummer")
    bsn_nummer.text = valid_bsn_numbers

    bestandsformaat = ET.SubElement(bestand, "bestandsformaat")
    ET.SubElement(bestandsformaat, "begripLabel").text = mime_type
    ET.SubElement(bestandsformaat, "begripCode").text = ""
    begripBegrippenlijst = ET.SubElement(bestandsformaat, "begripBegrippenlijst")
    ET.SubElement(begripBegrippenlijst, "verwijzingNaam").text = top_keywords

    checksum = ET.SubElement(bestand, "checksum")
    checksumAlgoritme = ET.SubElement(checksum, "checksumAlgoritme")
    ET.SubElement(checksumAlgoritme, "begripLabel").text = ""
    checksumBegrippenlijst = ET.SubElement(checksumAlgoritme, "begripBegrippenlijst")
    ET.SubElement(checksumBegrippenlijst, "verwijzingNaam").text = working_title
    ET.SubElement(checksum, "checksumWaarde").text = ""
    ET.SubElement(checksum, "checksumDatum").text = ""

    ET.SubElement(bestand, "URLBestand").text = ""

    isRepresentatieVan = ET.SubElement(bestand, "isRepresentatieVan")
    ET.SubElement(isRepresentatieVan, "verwijzingNaam").text = ""
    verwijzingIdentificatie = ET.SubElement(isRepresentatieVan, "verwijzingIdentificatie")
    ET.SubElement(verwijzingIdentificatie, "identificatieKenmerk").text = ""
    ET.SubElement(verwijzingIdentificatie, "identificatieBron").text = ""

    xml_filename = os.path.join(extract_folder, f"{pdf_filename}.xml")

    tree = ET.ElementTree(root)
    ET.indent(tree, '  ')

    with open(xml_filename, 'wb') as xml_file:
        tree.write(xml_file, encoding='utf-8')