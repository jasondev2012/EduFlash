from utils.firebase_config import db

class Course:
    def __init__(self, id, titulo, descripcion, contenido, quiz):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.contenido = contenido
        self.quiz = quiz

    @staticmethod
    def all():
        cursos_ref = db.collection("cursos")
        cursos = [Course(id=doc.id, **doc.to_dict()) for doc in cursos_ref.stream()]
        return cursos

    @staticmethod
    def get(curso_id):
        doc = db.collection("cursos").document(curso_id).get()
        if doc.exists:
            return Course(id=doc.id, **doc.to_dict())
        return None
