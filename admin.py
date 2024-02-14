from django.conf import settings
from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget


class LossEventItemResource(resources.ModelResource):
    # Defina campos estrangeiros como textos
    lot_fk = fields.Field(
        column_name='lot',
        attribute='lot',
        widget=ForeignKeyWidget(Lot, 'code')
    )
    material_fk = fields.Field(
        column_name='matnr',
        attribute='matnr',
        widget=ForeignKeyWidget(Material, 'code')
    )
    warehouse_fk = fields.Field(
        column_name='warehouse',
        attribute='warehouse',
        widget=ForeignKeyWidget(Local, 'code')
    )
    unity_type_fk = fields.Field(
        column_name='unity_type',
        attribute='unity_type',
        widget=ForeignKeyWidget(BaseData, 'value')
    )
    informed_loss_category_fk = fields.Field(
        column_name='informed_loss_category',
        attribute='informed_loss_category',
        widget=ForeignKeyWidget(LossCategoryReasonList, 'name')
    )
    informed_loss_name_fk = fields.Field(
        column_name='informed_loss_name',
        attribute='informed_loss_name',
        widget=ForeignKeyWidget(LossReasonList, 'description')
    )
    qty = fields.Field(
        column_name='qty',
        attribute='qty',
    )
    loss_from = fields.Field(
        column_name='loss_from',
        attribute='loss_from',
    )
    operator = fields.Field(
        column_name='operator',
        attribute='operator',
    )
    shift = fields.Field(
        column_name='shift',
        attribute='shift',
    )
    sync_sap = fields.Field(
        column_name='sync_sap',
        attribute='sync_sap',
    )
    sync_sap_date = fields.Field(
        column_name='sync_sap_date',
        attribute='sync_sap_date',
    )

    class Meta:
        model = LossEventItem
        fields = ('lot_fk', 'material_fk', 'warehouse_fk', 'unity_type_fk',
                  'informed_loss_category_fk', 'informed_loss_name_fk',
                  'qty', 'loss_from', 'operator', 'shift', 'sync_sap', 'sync_sap_date')
        # Inclua outros campos que você deseja exportar

    def dehydrate_unity_type_fk(self, obj):
        base_data = BaseData.objects.filter(value=obj.unit_type, type="UOM_VALUES_PACKING")
        if base_data:
            return base_data.first().value
        return None


class LossEventItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = LossEventItemResource
    actions = ("send_loss_event_item_to_sap",)
    list_display = (
        "lot",
        "loss_from",
        "informed_loss_category",
        "sync_sap",
        "updated_by",
        "last_update",
    )
    # list_filter = ("is_active",)
    readonly_fields = (
        "sync_sap",
        "created",
        "last_update",
        "created_by",
        "updated_by",
    )

    list_per_page = settings.LIST_PER_PAGE
    list_filter = ("informed_loss_category", "loss_from",)
    search_fields = ("lot__code",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "loss_from",
                    "warehouse",
                    "lot",
                    "matnr",
                    "qty",
                    "unit_type",
                    "informed_loss_category",
                    "informed_loss_name",
                    "operator",
                    "shift",
                    "sync_sap",
                    "sync_sap_date",
                )
            },
        ),
        (
            "Logs",
            {
                "classes": ("collapse",),
                "fields": (
                    "created",
                    "created_by",
                    "last_update",
                    "updated_by",
                ),
            },
        ),
    )