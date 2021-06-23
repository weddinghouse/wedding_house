odoo.define('wedding_house_custom.employees', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    models.load_fields('hr.employee', ['is_sales_person']);

    var orderline_super = models.Orderline.prototype;
    models.Orderline = models.OrderLine.extend({
        get_all_prices: function(){
            var self = this;

            var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
            var taxtotal = 0;

            var product =  this.get_product();
            // This is the part where I fix the taxes issue
            if (product === undefined)
                return false;
            var taxes =  this.pos.taxes;
            var taxes_ids = _.filter(product.taxes_id, t => t in this.pos.taxes_by_id);
            var taxdetail = {};
            var product_taxes = [];

            _(taxes_ids).each(function(el){
                var tax = _.detect(taxes, function(t){
                    return t.id === el;
                });
                product_taxes.push.apply(product_taxes, self._map_tax_fiscal_position(tax));
            });
            product_taxes = _.uniq(product_taxes, function(tax) { return tax.id; });

            var all_taxes = this.compute_all(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
            var all_taxes_before_discount = this.compute_all(product_taxes, this.get_unit_price(), this.get_quantity(), this.pos.currency.rounding);
            _(all_taxes.taxes).each(function(tax) {
                taxtotal += tax.amount;
                taxdetail[tax.id] = tax.amount;
            });

            return {
                "priceWithTax": all_taxes.total_included,
                "priceWithoutTax": all_taxes.total_excluded,
                "priceSumTaxVoid": all_taxes.total_void,
                "priceWithTaxBeforeDiscount": all_taxes_before_discount.total_included,
                "tax": taxtotal,
                "taxDetails": taxdetail,
            };
        },
    });

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
