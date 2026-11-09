import unittest
import pandas as pd
from src.olist import calculate_kpis

class OlistMetricTests(unittest.TestCase):
    def test_kpis_exclude_canceled_and_unavailable(self):
        data = pd.DataFrame({
            "order_id":["a","b","c"], "order_status":["delivered","canceled","shipped"],
            "item_revenue":[100.0,50.0,40.0], "freight_value":[10.0,5.0,4.0],
            "is_delivered":[True,False,False], "is_late":[False,False,False],
            "review_score":[5.0,None,4.0]
        })
        result = calculate_kpis(data)
        self.assertEqual(result["orders"],2)
        self.assertEqual(result["gmv"],140.0)
        self.assertEqual(result["freight"],14.0)
        self.assertEqual(result["aov"],70.0)
        self.assertEqual(result["late_rate"],0.0)
        self.assertEqual(result["avg_review"],4.5)

    def test_empty_dataset_has_zero_kpis(self):
        data = pd.DataFrame(columns=["order_id","order_status","item_revenue","freight_value","is_delivered","is_late","review_score"])
        result = calculate_kpis(data)
        self.assertEqual(result["orders"],0)
        self.assertEqual(result["gmv"],0.0)
        self.assertEqual(result["aov"],0.0)

if __name__ == "__main__":
    unittest.main()
