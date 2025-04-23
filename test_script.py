"""
Unit tests for podcast chapter extraction
"""

import json
import os
import unittest

from script import extract_chapters


class TestExtractChapters(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.test_json_path = os.path.join(
            os.path.dirname(__file__), "test_chapters.json"
        )
        # Verify the test file exists
        if not os.path.exists(self.test_json_path):
            raise FileNotFoundError(f"Test file not found: {self.test_json_path}")

        # Verify the JSON is valid
        with open(self.test_json_path, "r") as f:
            try:
                json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in test file: {e}")

    def test_extract_chapters(self):
        """Test that chapters are correctly extracted from the JSON file"""
        chapters = extract_chapters(self.test_json_path)

        # Verify we got the expected number of chapters
        self.assertEqual(len(chapters), 5)

        # Verify the format and content of each chapter
        expected_chapters = [
            "00:00 Earth Day & Meeting Introduction (00:00:00 - 00:02:35)",
            "02:35 Chapter Overview & Event Sources (00:02:35 - 00:10:12)",
            "10:13 Event Source Semantics & Use Cases (00:10:13 - 00:19:59)",
            "19:59 Python Implementation Demo & Architecture (00:19:59 - 00:29:09)",
            "29:11 Tooling, AI Assistance, and Next Steps (00:29:11 - 00:35:49)",
        ]

        for i, chapter in enumerate(chapters):
            self.assertEqual(chapter, expected_chapters[i])

    def test_empty_notes(self):
        """Test handling of JSON with empty Notes section"""
        # Create a temporary JSON with empty Notes
        temp_json = {"Notes": []}
        temp_path = "temp_test.json"
        with open(temp_path, "w") as f:
            json.dump(temp_json, f)

        try:
            chapters = extract_chapters(temp_path)
            self.assertEqual(chapters, [])
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_missing_notes(self):
        """Test handling of JSON without Notes section"""
        # Create a temporary JSON without Notes
        temp_json = {"title": "Test Podcast"}
        temp_path = "temp_test.json"
        with open(temp_path, "w") as f:
            json.dump(temp_json, f)

        try:
            chapters = extract_chapters(temp_path)
            self.assertEqual(chapters, [])
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
