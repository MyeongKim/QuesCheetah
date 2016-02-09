import "jquery";
import $ from "bootstrap";

import {Index} from "./src/index.js";
import {Mypage} from "./src/mypage.js";
import {Action} from "./src/action.js";
import {MultiAction} from "./src/multi_action.js";
import {New} from "./src/new.js";
import {Select} from "./src/select.js";
export function Submit() {
    Index();
    Mypage();
    Action();
    MultiAction();
    New();
    Select();
}