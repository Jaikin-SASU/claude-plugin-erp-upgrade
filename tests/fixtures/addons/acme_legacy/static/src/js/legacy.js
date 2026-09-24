odoo.define('acme_legacy.widget', function (require) {
    "use strict";
    const { useState } = require("@odoo/owl");
    return {
        setup() {
            this.state = useState({ count: 0 });
        },
    };
});
