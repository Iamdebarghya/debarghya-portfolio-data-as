import os
import unittest
from src.olist import load_dataset, prepare_orders, prepare_category_revenue

DATA_DIR = os.environ.get("OLIST_DATA_DIR", "data/raw")
REQUIRED = [
    "olist_orders_dataset.csv", "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv", "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv", "olist_products_dataset.csv",
    "product_category_name_translation.csv",
]

@unittest.skipUnless(all(os.path.exists(os.path.join(DATA_DIR, f)) for f in REQUIRED),
                     "Olist source CSVs not present; set OLIST_DATA_DIR to run integration checks")
class OlistDatasetIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frames = load_dataset(DATA_DIR)
        cls.orders = prepare_orders(cls.frames)

    def test_source_order_grain_is_preserved(self):
        self.assertEqual(len(self.orders), 99441)
        self.assertEqual(self.orders["order_id"].nunique(), 99441)

    def test_delivered_order_count(self):
        self.assertEqual(int(self.orders["is_delivered"].sum()), 96478)

    def test_item_level_category_revenue_reconciles(self):
        eligible = self.orders.loc[
            ~self.orders["order_status"].isin(["canceled", "unavailable"]), "order_id"
        ]
        categories = prepare_category_revenue(self.frames, set(eligible))
        expected = self.frames["items"].loc[
            self.frames["items"]["order_id"].isin(set(eligible)), "price"
        ].sum()
        self.assertAlmostEqual(float(categories["item_revenue"].sum()), float(expected), places=2)

if __name__ == "__main__":
    unittest.main()
