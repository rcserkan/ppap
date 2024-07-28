/** @odoo-module */
import {Component, useRef} from "@odoo/owl";

import {registry} from "@web/core/registry";

export class AuthScreen extends Component {
    static template = "ica_money_changer.auth_screen";

    setup() {
        this.usernameRef = useRef('username');
        this.passwordRef = useRef('password');
        this.rpcService = this.env.services.rpc;
    }

    async login() {
        let username = this.usernameRef.el.value;
        let password = this.passwordRef.el.value;
        // console.log(username, password)
        const result = await this.rpcService('/ica/login', {username, password});
        if (result.isFullFilled) {
            this.props.switchScreen('home_screen');
        } else {
            console.log(result)
        }
    }
}

registry.category("ica_money_changer").add("auth_screen", AuthScreen)