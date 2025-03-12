import fitz  # import PyMuPDF
import textwrap
from anyascii import anyascii

def gen_pdf():
    doc = fitz.open("frame.pdf")
    print(doc.get_page_fonts(0))

    with open('gemini_output.txt','r', encoding='utf-8') as f: llm_output = f.read()
    for replace_str in llm_output.split('#endreplace')[:-1]:
        old_txt, new_txt = replace_str.split('#replace')[1].split('#with')
        old_txt, new_txt = old_txt.strip(), new_txt.strip()
        print(f'\n\n\033[104mold_txt:\x1b[0m\n{old_txt}\n\033[104mnew_txt:\x1b[0m\n{new_txt}')
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


gen_pdf()