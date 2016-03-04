// third party modules
//import $ from "jquery";

// inner modules;
//import "qc-init";
//import { Submit } from "submit";

//Submit();
import "jquery";
import $ from "bootstrap";

import {Index} from "./src/index.js";
import {Mypage} from "./src/mypage.js";
import {Action} from "./src/action.js";
import {MultiAction} from "./src/multi_action.js";
import {New} from "./src/new.js";
import {Select} from "./src/select.js";

import sample_text from "./src/sample.html!text";
import "./src/sample.css!css";
import {Sample} from "./src/sample.js";

function Submit() {
    Index();
    Mypage();
    Action();
    MultiAction();
    New();
    Select();

    $('.dropdown-toggle').dropdown();

    $('#systemjs-test').html(sample_text);
    Sample();

}

Submit();