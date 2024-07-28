/** @odoo-module */
import {Component, onWillStart, useState} from "@odoo/owl";

import {registry} from "@web/core/registry";
import {NavbarComponent} from "../../components/navbar/navbar";
import {session} from "@web/session";

export class TransactionsScreen extends Component {
    static template = "ica_money_changer.transactions_screen";
    static  components = {NavbarComponent};

    setup() {
        this.state = useState({
            transactions: [],
        });
        this.ormService = this.env.services.orm;
        onWillStart(async () => {
            await this.getAllTransactions();
        })
    }

    async getAllTransactions() {
        let currentUser = await this.ormService.searchRead('res.users', [['id', '=', session.user_id]], ['id', 'name', 'partner_id']);
        let currentPartner = await this.ormService.searchRead('res.partner', [['id', '=', currentUser[0].partner_id[0]]], ['id', 'name']);
        this.state.transactions = await this.ormService.searchRead('ica.money.changer', [['partner_id', '=', currentPartner[0].id]], []);
        console.log(this.state.transactions);
    }
}

registry.category("ica_money_changer").add("transactions_screen", TransactionsScreen)