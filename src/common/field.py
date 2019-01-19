class FieldMixin:
    ENTITY = None
    FIELDS_NON_VISIBLE = None

    def _get_visible_field_names(self):
        return {field for field in self.ENTITY.__annotations__.keys() if field not in self.FIELDS_NON_VISIBLE}

    def _get_all_field_names(self):
        return set(self.ENTITY.__annotations__.keys())
