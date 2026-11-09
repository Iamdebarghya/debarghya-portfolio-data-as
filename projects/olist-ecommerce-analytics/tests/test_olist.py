import unittest
import pandas as pd
from src.olist import calculate_kpis, prepare_category_revenue

class OlistMetricTests(unittest.TestCase):
    def test_kpis_exclude_canceled_and_unavailable(self):
        data = pd.DataFrame({
            "order_id":["a","b","c"], "order_status":["delivered","canceled","shipped"],
            "item_revenue":[100.0,50.0,40.0], "freight_value":[10.0,5.0,4.0],
            "is_delivered":[True,False,False], "is_late":[False,False,False],
            "has_delivery_dates":[True,False,False], "review_score":[5.0,None,4.0], "review_count":[1,0,1]})
        result=calculate_kpis(data)
        self.assertEqual(result["orders"],2)
        self.assertEqual(result["gmv"],140.0)
        self.assertEqual(result["freight"],14.0)
        self.assertEqual(result["aov"],70.0)
        self.assertEqual(result["late_rate"],0.0)
        self.assertEqual(result["avg_review"],4.5)

    def test_late_rate_uses_only_orders_with_both_dates(self):
        data=pd.DataFrame({
            "order_id":["a","b","c"], "order_status":["delivered"]*3,
            "item_revenue":[1.0]*3, "freight_value":[0.0]*3,
            "is_delivered":[True]*3, "is_late":[True,False,False],
            "has_delivery_dates":[True,True,False], "review_score":[4.0]*3, "review_count":[1,1,1]})
        self.assertEqual(calculate_kpis(data)["late_rate"],0.5)

    def test_category_revenue_uses_item_grain(self):
        frames={
            "items":pd.DataFrame({"order_id":["o1","o1","o2"],"order_item_id":[1,2,1],
                "product_id":["p1","p2","p1"],"price":[10.0,20.0,5.0]}),
            "products":pd.DataFrame({"product_id":["p1","p2"],"product_category_name":["a","b"]}),
            "translation":pd.DataFrame({"product_category_name":["a","b"],
                "product_category_name_english":["A","B"]})}
        result=prepare_category_revenue(frames,{"o1","o2"}).set_index("category")
        self.assertEqual(result.loc["A","item_revenue"],15.0)
        self.assertEqual(result.loc["B","item_revenue"],20.0)

if __name__=="__main__":
    unittest.main()
