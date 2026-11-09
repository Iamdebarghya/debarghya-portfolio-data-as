import unittest
import pandas as pd
from src.hr_metrics import validate_hr_data, overall_metrics, attrition_by, compare_income

class HRMetricTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "EmployeeNumber":[1,2,3,4], "Attrition":["Yes","No","No","Yes"],
            "Department":["Sales","Sales","R&D","R&D"], "JobRole":["A","A","B","B"],
            "OverTime":["Yes","No","No","Yes"], "MonthlyIncome":[1000,2000,3000,4000],
            "YearsAtCompany":[1,4,6,2], "JobSatisfaction":[1,3,4,2], "Age":[22,35,42,28]
        })
    def test_validation(self):
        self.assertEqual(len(validate_hr_data(self.df)),4)
    def test_overall(self):
        m=overall_metrics(self.df)
        self.assertEqual(m["employees"],4)
        self.assertEqual(m["attrition_count"],2)
        self.assertEqual(m["attrition_rate"],0.5)
    def test_group_rate(self):
        r=attrition_by(self.df,"Department").set_index("Department")
        self.assertEqual(r.loc["Sales","attrition_rate"],0.5)
        self.assertEqual(r.loc["R&D","attrition_rate"],0.5)
    def test_income(self):
        r=compare_income(self.df).set_index("Attrition")
        self.assertEqual(r.loc["Yes","median_income"],2500)
    def test_duplicate_employee_id_rejected(self):
        bad=pd.concat([self.df,self.df.iloc[[0]]],ignore_index=True)
        with self.assertRaisesRegex(ValueError,"unique"): validate_hr_data(bad)

if __name__=="__main__": unittest.main()
