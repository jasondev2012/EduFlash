from utils.firebase_config import db

class User:
    def __init__(self, uid, email, nombres, apellidos):
        self.uid = uid
        self.email = email
        self.nombres = nombres
        self.apellidos = apellidos

    @staticmethod
    def get(uid):
        doc = db.collection("usuarios").document(uid).get()
        if doc.exists:
            data = doc.to_dict()
            return User(uid=uid, email=data.get("email"))
        return None

    @staticmethod
    def create(uid, email, nombres, apellidos):
        """Crea un nuevo usuario en Firestore"""
        user_ref = db.collection("usuarios").document(uid)
        user_ref.set({
            "email": email,
            "nombres": nombres,
            "apellidos": apellidos,
            "progress": {}  # por defecto sin progreso
        })
        return User(uid=uid, email=email, nombres=nombres, apellidos=apellidos)
    
    def save_progress(self, curso_id, puntaje):
        db.collection("usuarios").document(self.uid).set({
            "progress": {
                curso_id: {"completado": True, "puntaje": puntaje}
            }
        }, merge=True)
