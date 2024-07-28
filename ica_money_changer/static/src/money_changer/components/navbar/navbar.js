/** @odoo-module */
import {Component, onWillStart, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {session} from "@web/session";

export class NavbarComponent extends Component {
    static template = "ica_money_changer.navbar_component";

    setup() {
        this.state = useState({
            currentUser: null,
            currentPartner: null,
        });
        this.ormService = this.env.services.orm;
        this.rpcService = this.env.services.rpc;
        this.userService = this.env.services.user;
        onWillStart(async () => {
            await this.getUser();
        });
    }

    gotoHome() {
        this.props.switchScreen('home_screen');
    }

    gotoTransactionsScreen() {
        this.props.switchScreen('transactions_screen');
    }

    async logout() {
        const result = await this.rpcService('/ica/logout');
        if (result.isFullFilled) {
            this.props.switchScreen('auth_screen');
        }
    }

    async getUser() {
        let currentUser = await this.ormService.searchRead('res.users', [['id', '=', session.user_id]], ['id', 'name', 'partner_id']);
        this.state.currentUser = currentUser[0];
        let currentPartner = await this.ormService.searchRead('res.partner', [['id', '=', this.state.currentUser.partner_id[0]]], ['id', 'name']);
        this.state.currentPartner = currentPartner[0];
    }
}

registry.category("ica_money_changer").add("navbar_component", NavbarComponent)