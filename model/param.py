from pydantic import BaseModel

class ChatInput ( BaseModel ): 
    age: int
    gene_fault: str
    category: str
    patient_question: str
    
