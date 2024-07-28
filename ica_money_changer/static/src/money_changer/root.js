/** @odoo-module */
import {Component, onWillStart, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {session} from "@web/session";

export class Root extends Component {
    static template = "ica_money_changer.Root";
    static props = {};

    setup() {
        this.state = useState({
            "mainScreen": "home_screen"
        });
        this.routerService = this.env.services.router;
        this.switchScreen = this.switchScreen.bind(this);
        onWillStart(async () => {
            this.getInitScreen();
        })
    }

    getInitScreen() {
        this.state.mainScreen = session.user_id ? 'home_screen' : 'auth_screen';
        if (session.user_id) {
            this.switchScreen(this.routerService.current.hash.route)
        } else {
            this.switchScreen('auth_screen');
        }
    }

    switchScreen(screenName) {
        const content = registry.category("ica_money_changer").content;
        if (content.hasOwnProperty(screenName)) {
            this.state.mainScreen = screenName;
        }
    }

    getComponent() {
        this.routerService.pushState({route: this.state.mainScreen});
        return registry.category("ica_money_changer").get(this.state.mainScreen);
    }
}