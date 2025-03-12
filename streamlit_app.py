
# pylint: disable=line-too-long,invalid-name
"""
This module demonstrates the usage of the Vertex AI Gemini 1.5 API within a Streamlit application.
"""

import os
from openai import OpenAI
import streamlit as st
import vertexai
import base64
import fitz
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

import fitz  # import PyMuPDF
import textwrap
from anyascii import anyascii

## ---------- Page's Configuration ------------

# Default config for Streamlit app
st.set_page_config(
    page_title="My App",
    page_icon=":wrench:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.image("winch4ai.png", width=500)

st.header("Application Démo / Mise en forme de Dossiers de compétences", divider="blue")

## ------------ GEMINI's configuration ----------

# Initialize the Vertex AI API with the project and location
PROJECT_ID = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("GCP_REGION")

# Instructions fournies au modèle

# Configurations pour la génération de texte
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Paramètres de sécurité
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

## ------------ Fonction de lancement ----------

def generate(texte, fichiers):
    vertexai.init(project="new-e-437313", location="europe-west9")
    model = GenerativeModel(
        "gemini-1.5-pro-002",
    )
    
    responses = model.generate_content(
        [fichiers, texte],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    
    models_answer=""
    for response in responses:
        models_answer += response.text
    return models_answer

def gen_pdf(notes_entretien, fichiers):

    notes_entretien = """
DEBUT LISTE A REMPLACER:
@prenom_experience_30c_1l
@titre_30c_1l
@disponibilite_48c_1l
@liste_competences_900c_9l
@annee_formation1_9c_1l
@titre_formation1_80c_1l
@annee_formation2_9c_1l
@titre_formation2_80c_1l
@entreprise_experience1_30c_1l
@titre_experience1_30c_1l
@duree_experience1_30c_1l
@entreprise_experience2_30c_1l
@titre_experience2_30c_1l
@duree_experience2_30c_1l
@entreprise_experience3_30c_1l
@titre_experience3_30c_1l
@duree_experience3_30c_1l
@annee_experience1_30c_1l
@detail_experience1_1300c_17l
@environnementTN_experience1_200c_2l
@annee_experience2_30c_1l
@detail_experience2_1300c_17l
@environnementTN_experience2_200c_2l
@detail_experience3_1300c_17l
@outil1_25c_1l
@niveau_outil1_25c_1l
@duree_outil1_25c_1l
@outil2_25c_1l
@niveau_outil2_25c_1l
@duree_outil2_25c_1l
@langue1_20c_1l
@nv_langue1_20c_1l
@experience_langue1_60c_1l
@langue2_20c_1l
@nv_langue2_20c_1l
@experience_langue2_60c_1l
@langue3_20c_1l
@nv_langue3_20c_1l
@experience_langue3_60c_1l
@nv_langue4_20c_1l
@experience_langue4_60c_1l
@langue4_20c_1l
FIN LISTE A REMPLACER

Tu dois remplacer toutes les apparences de texte commençant par « @ » dans la liste ci dessus par des données de l’entretien ci-dessous, dans l’absence de données d’entretien remplace par TBD. Pour remplacer un texte commençant par « @ », suit l’exemple suivant :
Exemple:
#replace @disponibilite_48c_1l #with fevrier 2024 #endreplace

DEBUT COMPTE RENDU D'ENTRETIEN :
""" + notes_entretien + """
FIN COMPTE RENDU D'ENTRETIEN
Tu dois remplacer toutes les apparences de texte commençant par « @ » dans la liste ci dessous par des données de l’entretien ci-dessus, dans l’absence de données d’entretien remplace par TBD. Pour remplacer un texte commençant par « @ », suit l’exemple suivant :
Exemple:
#replace @disponibilite_48c_1l #with fevrier 2024 #endreplace

DEBUT LISTE A REMPLACER:
@prenom_experience_30c_1l
@titre_30c_1l
@disponibilite_48c_1l
@liste_competences_900c_9l
@annee_formation1_9c_1l
@titre_formation1_80c_1l
@annee_formation2_9c_1l
@titre_formation2_80c_1l
@entreprise_experience1_30c_1l
@titre_experience1_30c_1l
@duree_experience1_30c_1l
@entreprise_experience2_30c_1l
@titre_experience2_30c_1l
@duree_experience2_30c_1l
@entreprise_experience3_30c_1l
@titre_experience3_30c_1l
@duree_experience3_30c_1l
@annee_experience1_30c_1l
@detail_experience1_1300c_17l
@environnementTN_experience1_200c_2l
@annee_experience2_30c_1l
@detail_experience2_1300c_17l
@environnementTN_experience2_200c_2l
@detail_experience3_1300c_17l
@outil1_25c_1l
@niveau_outil1_25c_1l
@duree_outil1_25c_1l
@outil2_25c_1l
@niveau_outil2_25c_1l
@duree_outil2_25c_1l
@langue1_20c_1l
@nv_langue1_20c_1l
@experience_langue1_60c_1l
@langue2_20c_1l
@nv_langue2_20c_1l
@experience_langue2_60c_1l
@langue3_20c_1l
@nv_langue3_20c_1l
@experience_langue3_60c_1l
@nv_langue4_20c_1l
@experience_langue4_60c_1l
@langue4_20c_1l
FIN LISTE A REMPLACER
"""
    models_answer = generate(notes_entretien, fichiers)
    #implémenter la fonction de gen_pdf

    doc = fitz.open("frame.pdf")
    print(doc.get_page_fonts(0))

    for replace_str in models_answer.split('#endreplace')[:-1]:
        old_txt, new_txt = replace_str.split('#replace')[1].split('#with')
        old_txt, new_txt = old_txt.strip(), new_txt.strip()
        #print(f'\n\n\033[104mold_txt:\x1b[0m\n{old_txt}\n\033[104mnew_txt:\x1b[0m\n{new_txt}') #debug
        for page in doc:
            hits = page.search_for(old_txt)  # list of rectangles where to replace
            for rect in hits:
                page.add_redact_annot(rect, text="", text_color=(0, 0, 0), fontname="helv")#, fontsize=5, align=fitz.TEXT_ALIGN_CENTER)
                page.apply_redactions()

                idx_n_caracter = old_txt.find("c") # Find the index of "c"
                n_caracter = old_txt[old_txt.rfind('_')+1:idx_n_caracter] # Extract the part before "c" and after the last underscore
                page.insert_text((rect.x0, 3+(rect.y0+rect.y1)/2), textwrap.wrap(anyascii(new_txt), int(n_caracter) if n_caracter.isdigit() else 64), fontname="F5", fontsize=12, color=(0, 0, 0))

    #page.apply_annots(images=fitz.PDF_REDACT_IMAGE_NONE)  # don't touch images
    doc.save("replaced.pdf")#, garbage=3, deflate=True)

    st.write('done pdf generation')
    return

## ------------ Recevoir plusieur fichiers ----------

uploaded_file = st.file_uploader(
    "CV en format PDF", accept_multiple_files=False, type=['pdf', 'docx']
)

document1=None

# Étape 2 : Si un fichier est uploadé
if uploaded_file is not None:
    # Lecture du contenu du fichier
    file_content = uploaded_file.read()

    # Étape 3 : Création d'une partie du document à partir des données base64
    document1 = Part.from_data(
        mime_type=uploaded_file.type,  # Récupération du type MIME du fichier
        data=file_content,  # Utilisation du contenu brut du fichier
    )

    st.write("Document uploaded successfully!")

#for uploaded_file in uploaded_files:
#    bytes_data = uploaded_file.read()
#    st.write("filename:", uploaded_file.name)
#    st.write(bytes_data)

notes_entretien = st.text_area("Notes de l'entretien", height=300)
prenom = "prenom"
fichiers = document1

# Ajout du bouton de téléchargement sous le chat avec CSS pour changer sa couleur
st.markdown(
    """
    <style>
    .stDownloadButton button {
        background-color: #FF0000 !important;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

if st.button('Générer le dossier de compétences'):
    gen_pdf(notes_entretien, fichiers)

    with open("replaced.pdf", "rb") as out_pdf_f:
        st.download_button(label="Télécharger le dossier de compétences", data=out_pdf_f, file_name=f"New-E-DC-prenom.pdf", icon="📩")
