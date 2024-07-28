/** @odoo-module */
import {whenReady} from "@odoo/owl";
import {mountComponent} from "@web/env";
import {Root} from "./money_changer/root";

whenReady(() => mountComponent(Root, document.body));