import unittest
from parser_utils import parse_h17_message
import json

class TestHL7Parser(unittest.TestCase):

    def test_basic_parse(self):
        sample = (
            "MSH|^~\\&|EMR|HOSPITAL|RCM|RCMSYSTEM|202505021200||SIU^S12|12345|P|2.3\r"
            "SCH|123456^A|...|...|202505021300|...|Clinic A - Room 203|General Consultation\r"
            "PID|1||P12345^^^HOSP^MR||Doe^John||19850210|M\r"
            "PV1|1|...|D67890^Smith^Dr\r"
        )
        result = parse_h17_message(sample)
        print(json.dumps(result, indent=2))
        self.assertEqual(result['appointment_id'], '123456')
        self.assertEqual(result['patient']['first_name'], 'John')
        self.assertEqual(result['provider']['name'], 'Dr Smith')
        self.assertIn('appointment_datetime', result)

    def test_missing_field(self):
        sample = (
            "MSH|^~\\&|EMR|HOSPITAL|RCM|RCMSYSTEM|202505021200||SIU^S12|12345|P|2.3\r"
            "SCH|123456^A|...|...|202505021300|...||General Consultation\r"
            "PID|1||P12345^^^HOSP^MR||Doe^John||19850210|M\r"
            "PV1|1|...|D67890^Smith^Dr\r"
        )
        with self.assertRaises(ValueError):
            parse_h17_message(sample)

    



if __name__ == '__main__':
    unittest.main()
