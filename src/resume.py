from typing import List

class Resume():
    '''Class create to generate, update and save to google docs a new resume'''
    def __init__(self, standard_resume: str, text_generator, google_docs_manager):
        self.standard_resume = standard_resume
        self.text_generator = text_generator
        self.google_docs_manager = google_docs_manager
        self.generated_resume = ""
    
    def generate(self, job_keywords: List[str]) -> None:
        self.generated_resume = self.text_generator.generate_text(self.standard_resume, job_keywords)

    def update(self, new_keywords: List[str]) -> None:
        #TODO 1 update the resume with new keywords
        pass

    def save_to_google_docs(self) -> str:
        doc_url = self.google_docs_manager.save_doc(self.generated_resume)
        return doc_url
    

