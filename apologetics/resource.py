from import_export import resources
from apologetics.models import Record


class RecordResource(resources.ModelResource):

    class Meta:
        model = Record
        exclude = "id"
        import_id_fields = ["code"]
