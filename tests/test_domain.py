import json
import tempfile
import unittest
from pathlib import Path
from src.domain import load_domain

FIXTURE = Path("fixtures/domain.json")

class DomainTest(unittest.TestCase):
    def test_fixture_is_complete(self):
        value = load_domain(FIXTURE)
        self.assertEqual(value["domain"], "seed-commercialization")
        self.assertGreater(len(value["entities"]), 2)
        self.assertGreater(len(value["rules"]), 2)

    def test_lifecycle_entities_present(self):
        value = load_domain(FIXTURE)
        expected = {
            "种质材料", "育种组合", "育种目标", "企业需求", "育种项目",
            "试验世代", "试验记录", "区域试种", "选择淘汰记录",
            "品种版本", "审定登记", "配套栽培技术",
            "知识产权", "企业共研参与", "权利变更", "推广授权",
            "种子批次", "推广反馈",
        }
        self.assertTrue(expected.issubset(set(value["entities"])))

    def test_key_rules_present(self):
        value = load_domain(FIXTURE)
        rules = set(value["rules"])
        self.assertIn("企业需求必须在立项时形成可验证指标", rules)
        self.assertIn("每次选择与淘汰必须保留依据", rules)
        self.assertIn("授权转让不得超出约定区域与繁育用途", rules)
        self.assertIn("上市品种可反查亲本、试验环境、采用需求与授权链", rules)
        self.assertIn("已审定未落地的环节必须可识别", rules)

    def test_sample_traceability_example(self):
        value = load_domain(FIXTURE)
        example = value["sample"]["traceability_example"]
        for key in ("variety", "stage", "parents", "trial_environments",
                    "adopted_requirements", "license_chain"):
            self.assertIn(key, example)
        self.assertTrue(example["parents"])
        self.assertTrue(example["trial_environments"])
        self.assertTrue(example["adopted_requirements"])
        self.assertTrue(example["license_chain"])

    def test_duplicate_entries_rejected(self):
        value = load_domain(FIXTURE)
        value["entities"] = value["entities"] + [value["entities"][0]]
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        ) as fh:
            json.dump(value, fh, ensure_ascii=False)
            tmp = Path(fh.name)
        try:
            with self.assertRaises(ValueError):
                load_domain(tmp)
        finally:
            tmp.unlink()

if __name__ == "__main__":
    unittest.main()
