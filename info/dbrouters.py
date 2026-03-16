# erpadmin/dbrouters.py

class AssoRouter:
    """
    Route toutes les lectures/écritures/migrations de l'app 'asso' vers la DB 'db2'
    """
    route_app_labels = {"asso"}  # ⚠️ mets ici le app_label exact de ton app

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "db2"
        return None  # Django choisit 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "db2"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Autorise les relations seulement si les 2 objets sont dans les mêmes "groupes"
        if (
            obj1._meta.app_label in self.route_app_labels
            and obj2._meta.app_label in self.route_app_labels
        ):
            return True
        if (
            obj1._meta.app_label not in self.route_app_labels
            and obj2._meta.app_label not in self.route_app_labels
        ):
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Les modèles de 'asso' vont uniquement dans db2
        if app_label in self.route_app_labels:
            return db == "db2"
        # Tout le reste va dans default
        return db == "default"
