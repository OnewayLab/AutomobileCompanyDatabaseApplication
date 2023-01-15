from flask import redirect, url_for

import website
from database import db
from database.import_data import import_test_data


if __name__ == "__main__":
    app = website.create_app(db)
    print("Importing test data...")
    import_test_data(
        app,
        300,
        "database/test_data/brand_models.json",
        "database/test_data/customers.json",
        "database/test_data/dealers.json",
        "database/test_data/plants.json",
        "database/test_data/suppliers.json",
        "database/test_data/etc.json",
    )
    print("Test data imported successfully.")
    app.run(debug=True, port=8888, host="127.0.0.1")
