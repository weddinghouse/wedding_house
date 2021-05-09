odoo.define('wedding_house_custom.employees', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    models.load_fields('hr.employee', ['is_sales_person']);

    var posmodel_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        set_sales_person: function(sales_person) {
            const selectedOrder = this.get_order();
            if (selectedOrder) {
                selectedOrder.sales_person = sales_person;
            }
        },
        get_sales_person: function() {
            const selectedOrder = this.get_order();
            if (selectedOrder) {
                if (selectedOrder.sales_person)
                    return selectedOrder.sales_person
            }
            return false
        }
    });

    /*
        The loading of the POS session is not working correctly.
        Basically when I close the session and then resume it afterwards. The Sales person that was selected on before does not get loaded

    */
    var super_order_model = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
//            console.log('initialize attributes', attributes)
//            console.log('initialize options', options)
//            console.log('initialize this', this)
            super_order_model.initialize.apply(this, arguments);
            this.sales_person = this.pos.get_sales_person();
        },
        init_from_JSON: function (json) {
//            console.log('init_from_JSON json', json)
//            console.log('init_from_JSON this', this)
            super_order_model.init_from_JSON.apply(this, arguments);
            this.sales_person = this.pos.sales_person;
        },
        export_as_JSON: function () {

            const json = super_order_model.export_as_JSON.apply(this, arguments);
            json.sales_person = this.sales_person ? this.sales_person.id : false;
            return json;
        },
    });


    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function() {
            var receipt = _super_order.export_for_printing.apply(this,arguments);

            var sales_person = this.pos.env.pos.get_sales_person()
            if (sales_person)
                receipt.sales_person = sales_person.name
            return receipt;
        },
    });

});
