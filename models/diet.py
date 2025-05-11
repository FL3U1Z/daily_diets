class Diet:
    def __init__(self, id, name, description, time, diet=False) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.time = time
        self.diet = diet
        
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.title,
            "description":self.description,
            "time":self.time,
            "diet":self.diet
        }