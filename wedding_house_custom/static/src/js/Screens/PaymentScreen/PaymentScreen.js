odoo.define('wedding_house_custom.PaymentScreen', function (require) {
    'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { posbus } = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');



    const CustomPaymentScreen = (PaymentScreen) =>
    class extends PaymentScreen{
        constructor() {
            super(...arguments);
        }
        async selectSalesPerson() {
            const selectionList = this.env.pos.employees
                .filter((employee) => employee.is_sales_person === true)
                .map((employee) => {
                        return {
                            id: employee.id,
                            item: employee,
                            label: employee.name,
                            isSelected: false,
                        };
                    });

            const sales_person = await Gui.showPopup("SelectionPopup", {
                title: this.env._t('Select Sales Person'),
                list: selectionList,
            });
            this.env.pos.set_sales_person(sales_person.payload)
        }
    };

    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
    return CustomPaymentScreen;
});

