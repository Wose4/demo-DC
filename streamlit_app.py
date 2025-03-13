# pylint: disable=line-too-long,invalid-name
"""
This module demonstrates the usage of the Vertex AI Gemini 1.5 API within a Streamlit application.
"""

import os
from openai import OpenAI
import streamlit as st
import base64
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile

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

## ------------ AI's configuration ----------

load_dotenv()
client = OpenAI()
openai_api_key = os.getenv("OPENAI_API_KEY")
client.api_key = openai_api_key

## ------------ Fonction de lancement ----------

def generate(texte, fichier=None):
    
    # Structure d'entrée pour l'API
    input_content = [
        {
            "type": "input_text",
            "text": texte,
        }
    ]

    # Si un fichier UploadedFile est fourni
    if fichier is not None:
        # 1. Créer un fichier temporaire
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(fichier.read())     # on écrit le contenu binaire
            tmp_path = tmp.name          # récupère le chemin du fichier
        
        # 2. Appel à l’API en utilisant le chemin du fichier temporaire
        uploaded_file = client.files.create(
            file=open(tmp_path, "rb"),
            purpose="user_data"
        )

        # 3. Au besoin, insérer le bloc input_file dans input_content
        input_content.insert(0, {
            "type": "input_file",
            "file_id": uploaded_file.id,
        })
        
        # On peut supprimer le fichier temporaire après usage :
        os.remove(tmp_path)
    
    # Si un fichier est fourni, on l'upload et on l'ajoute aux entrées
    #if fichier is not None:
    #    uploaded_file = client.files.create(
    #        file=open(fichier, "rb"),
    #        purpose="user_data"
    #    )
    #    input_content.insert(0, {
    #        "type": "input_file",
    #        "file_id": uploaded_file.id,
    #    })

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": input_content
            }
        ]
    )
    print(response)
    return response.output_text

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
                page.insert_text((rect.x0, 3+(rect.y0+rect.y1)/2), textwrap.wrap(anyascii(new_txt), int(n_caracter) if n_caracter.isdigit() else 64), fontname="helv", fontsize=12, color=(0, 0, 0))

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
#if uploaded_file is not None:
    # Lecture du contenu du fichier
    #file_content = uploaded_file.read()

    # Étape 3 : Création d'une partie du document à partir des données base64
    #document1 = Part.from_data(
    #    mime_type=uploaded_file.type,  # Récupération du type MIME du fichier
    #    data=file_content,  # Utilisation du contenu brut du fichier
    #)

    #st.write("Document uploaded successfully!")

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
    gen_pdf(notes_entretien, uploaded_file)

    with open("replaced.pdf", "rb") as out_pdf_f:
        st.download_button(label="Télécharger le dossier de compétences", data=out_pdf_f, file_name=f"New-E-DC-prenom.pdf", icon="📩")
