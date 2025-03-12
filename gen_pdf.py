import fitz  # import PyMuPDF

def gen_pdf():
    doc = fitz.open("frame.pdf")
    #page = doc[0]  # page number 0-based
    print(doc.get_page_fonts(0))
    with open('stream.txt','w') as f_stream:
        with open('gemini_output.txt','r', encoding='utf-8') as f: llm_output = f.read()
        for replace_str in llm_output.split('#endreplace')[:-1]:
            old_txt, new_txt = replace_str.split('#replace')[1].split('#with')
            old_txt, new_txt = old_txt.strip().encode(), new_txt.strip().encode()
            print(f'\n\n\033[104mold_txt:\x1b[0m\n{old_txt}\n\033[104mnew_txt:\x1b[0m\n{new_txt}')
            for page in doc:
                for xref in page.get_contents():
                    stream = doc.xref_stream(xref).replace(old_txt, new_txt) # b'@liste_competences_900c_9l', b'gfkdlsghsfdghflfk')
                    f_stream.write(f'{stream}')
                    doc.update_stream(xref, stream)

    doc.save("replaced.pdf")#, garbage=3, deflate=True)
    

gen_pdf()