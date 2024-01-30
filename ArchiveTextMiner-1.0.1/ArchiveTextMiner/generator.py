from ArchiveTextMiner.modules.text_miner import (
    extract_zip, extract_text_from_pdf, clean_dutch_text, generate_working_title,
      generate_size, detect_language, generate_summary, extract_top_keywords, extract_kvk_numbers, 
      extract_valid_bsn_numbers, get_file_mime_type, create_xml_file
)

import os
import langdetect
import PyPDF2
import warnings
warnings.filterwarnings("ignore")

def MDTO(zip_file_path):
    base_name = os.path.splitext(os.path.basename(zip_file_path))[0]
    extract_folder = os.path.join(os.path.dirname(zip_file_path), base_name)
    os.makedirs(extract_folder, exist_ok=True)
    extracted_files_path = extract_zip(zip_file_path, extract_folder)
    print(f"PDF-bestanden uitpakken in {extracted_files_path}...")
    print()

    output_folder = os.path.join(os.path.dirname(zip_file_path), base_name, 'ArchiveTextMiner')
    os.makedirs(output_folder, exist_ok=True)

    pdf_files = [file for file in os.listdir(extracted_files_path) if file.endswith('.pdf')]
    print(f"Bestanden {pdf_files} gevonden.")
    print("Bezig met creëren metadata bestanden...")
    print()

    for pdf_file in pdf_files:
        pdf_path = os.path.join(extracted_files_path, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        cleaned_text = clean_dutch_text(text)
        working_title = generate_working_title(cleaned_text)
        size = generate_size(pdf_path)
        detected_language = detect_language(cleaned_text)
        summary = generate_summary(cleaned_text)
        top_keywords = extract_top_keywords(cleaned_text)
        kvk_numbers = extract_kvk_numbers(cleaned_text)
        valid_bsn_numbers = extract_valid_bsn_numbers(cleaned_text)
        mime_type = get_file_mime_type(pdf_path)

        xml_file_path = os.path.join(f"{pdf_file}")
        create_xml_file(xml_file_path, working_title, size, detected_language, summary,
                        top_keywords, kvk_numbers, valid_bsn_numbers,
                        mime_type, output_folder)
        print(f"{xml_file_path}.xml succesvol gecreëerd.") 

if __name__ == "__main__":
    print()
    zip_file_path = input("Voer de padnaam van het ZIP-bestand in: ")
    MDTO(zip_file_path)
    print()
    print("Metadatabestanden opgeslagen in inputmap.")
    print()
    print("ArchiveTextMiner afgerond.")

