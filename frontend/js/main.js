/*
 * Main frontend Javascript entrypoint.
 *
 * Note than jQuery is not required by Bootstrap and just loaded for convenience for
 * developers which can't or don't want to develop in vanilla Javascript.
*/

//
// Make jQuery object usable inside modules
//
//import $ from "jquery";

//
// Make jQuery object usable from templates
//
//window.jQuery = $;
//window.$ = $;

//
// Initialize Alpine.js
//
// import Alpine from "alpinejs";

// window.Alpine = Alpine;
// Alpine.start();

//
// Initialize htmx
//
import htmx from 'htmx.org';
//import "htmx-ext-response-targets";

window.htmx = htmx;

//
// Make Bootstrap components usable from templates (like "bootstrap.Modal(..)")
//
window.bootstrap = require("bootstrap/dist/js/bootstrap.bundle.js");

//
// Make Bootstrap components usable inside modules (directly through component name)
// You may disable unused components to lighten builded JS file
//
import {
    // Alert,
    Button,
    // Carousel,
    Collapse,
    Dropdown,
    // Modal,
    // Popover,
    // ScrollSpy,
    // Tab,
    // Toast,
    // Tooltip,
} from "bootstrap/dist/js/bootstrap.bundle.js";

//
// NOTE: Sample how to instanciate a Bootstrap component object.
//
// var myModal = new Modal(document.getElementById("exampleModalDefault"));
// myModal.show();

import { BootstrapColorMode } from "./components/color-modes";

///
/// Initialize components after DOM is loaded
///
document.addEventListener("DOMContentLoaded", function () {
    BootstrapColorMode();
});
