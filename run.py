import website
import database

if __name__ == "__main__":
    app = website.create_app(database.db)
    database.import_test_data(
        "database/test_data/brand_models.json",
        "database/test_data/customers.json",
        "database/test_data/dealers.json",
        "database/test_data/plants.json",
        "database/test_data/suppliers.json",
        "database/test_data/etc.json",
    )
    app.run(debug=True, port=8888, host="127.0.0.1")
