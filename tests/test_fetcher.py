import unittest
from unittest.mock import patch
from pubmed_fetcher import fetcher

class TestPubmedFetcher(unittest.TestCase):

    def test_is_academic_with_academic_affiliation(self):
        self.assertTrue(fetcher.is_academic("Harvard University"))
        self.assertTrue(fetcher.is_academic("Massachusetts Institute of Technology"))
        self.assertTrue(fetcher.is_academic("Stanford University"))

    def test_is_academic_with_non_academic_affiliation(self):
        self.assertFalse(fetcher.is_academic("Pfizer Inc."))
        self.assertFalse(fetcher.is_academic("Moderna Therapeutics"))
        self.assertFalse(fetcher.is_academic("Johnson & Johnson R&D"))

    @patch("pubmed_fetcher.fetcher.Entrez.esearch")
    @patch("pubmed_fetcher.fetcher.Entrez.read")
    def test_fetch_pubmed_ids(self, mock_read, mock_esearch):
        mock_read.return_value = {"IdList": ["12345678", "23456789"]}
        ids = fetcher.fetch_pubmed_ids("COVID-19", max_results=2)
        self.assertEqual(ids, ["12345678", "23456789"])
        mock_esearch.assert_called_once()

    @patch("pubmed_fetcher.fetcher.Entrez.efetch")
    @patch("Bio.Medline.parse")
    def test_fetch_pubmed_details(self, mock_parse, mock_efetch):
        # Mock Medline.parse to return fake records
        mock_parse.return_value = [
            {
                "PMID": "12345678",
                "TI": "A COVID-19 Study",
                "DP": "2023 Jan",
                "AU": ["John Doe"],
                "AD": ["Pfizer Inc."],
                "EM": "john.doe@pfizer.com"
            }
        ]
        papers = fetcher.fetch_pubmed_details(["12345678"])
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["PubmedID"], "12345678")
        self.assertIn("Pfizer", papers[0]["Company Affiliation(s)"])

if __name__ == "__main__":
    unittest.main()
