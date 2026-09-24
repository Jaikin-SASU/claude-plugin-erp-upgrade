{
    "name": "ACME Legacy",
    "version": "18.0.1.0.0",
    "author": "ACME Corp",
    "license": "LGPL-3",
    "depends": ["sale", "stock_picking_batch"],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "acme_legacy/static/src/js/legacy.js",
        ],
    },
}
