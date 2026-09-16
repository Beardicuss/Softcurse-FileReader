import os
import tempfile
import unittest

from src.main import (
    get_file_ext,
    is_binary_data,
    generate_hex_dump,
    build_file_data,
    write_file_content,
    create_new_file_data,
    SoftcurseAPI,
)


class TestMainBackend(unittest.TestCase):

    def test_get_file_ext(self):
        self.assertEqual(get_file_ext("test.py"), "py")
        self.assertEqual(get_file_ext("archive.tar.gz"), "gz")
        self.assertEqual(get_file_ext("LICENSE"), "license")
        self.assertEqual(get_file_ext("/path/to/FILE.TXT"), "txt")

    def test_is_binary_data(self):
        self.assertFalse(is_binary_data(b"Hello world\nThis is plain text."))
        self.assertTrue(is_binary_data(b"Hello\x00World"))
        self.assertTrue(is_binary_data(bytes(range(256))))

    def test_generate_hex_dump(self):
        sample = b"SOFTCURSE\x0012345"
        dump = generate_hex_dump(sample)
        self.assertIn("00000000", dump)
        self.assertIn("SOFTCURSE.12345", dump)
        self.assertIn("53 4F 46 54 43 55 52 53", dump)

    def test_create_new_file_data(self):
        nf = create_new_file_data("Custom.py")
        self.assertEqual(nf["name"], "Custom.py")
        self.assertEqual(nf["ext"], "py")
        self.assertEqual(nf["content"], "")
        self.assertFalse(nf["is_binary"])

    def test_read_file_with_encoding_api(self):
        with tempfile.NamedTemporaryFile(mode="wb+", delete=False, suffix=".ans") as tf:
            tf.write("BBS ASCII Art".encode("cp437"))
            tf_path = tf.name

        try:
            api = SoftcurseAPI(None)
            res = api.read_file_with_encoding(tf_path, "cp437")
            self.assertIsNotNone(res)
            self.assertEqual(res["encoding"], "CP437")
            self.assertIn("BBS ASCII", res["content"])
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_reload_file_api(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tf:
            tf.write("Initial line")
            tf_path = tf.name

        try:
            api = SoftcurseAPI(None)
            res = api.reload_file(tf_path)
            self.assertEqual(res["content"], "Initial line")
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_write_file_content(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tf:
            tf_path = tf.name

        try:
            ok, msg = write_file_content(tf_path, "Updated SOFTCURSE content\nLine 2")
            self.assertTrue(ok)
            with open(tf_path, "r", encoding="utf-8") as f:
                saved = f.read()
            self.assertEqual(saved, "Updated SOFTCURSE content\nLine 2")
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_save_file_api(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".md") as tf:
            tf.write("# Initial")
            tf_path = tf.name

        try:
            api = SoftcurseAPI(None)
            res = api.save_file(tf_path, "# Modified Markdown")
            self.assertEqual(res["path"], tf_path)
            self.assertEqual(res["content"], "# Modified Markdown")
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_build_file_data_text(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".py", encoding="utf-8") as tf:
            tf.write("print('Hello SOFTCURSE')")
            tf_path = tf.name

        try:
            fd = build_file_data(tf_path)
            self.assertEqual(fd["name"], os.path.basename(tf_path))
            self.assertEqual(fd["ext"], "py")
            self.assertFalse(fd["is_binary"])
            self.assertEqual(fd["encoding"], "UTF-8")
            self.assertIn("print('Hello SOFTCURSE')", fd["content"])
            self.assertTrue(len(fd["hex_dump"]) > 0)
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_build_file_data_binary(self):
        with tempfile.NamedTemporaryFile(mode="wb+", delete=False, suffix=".bin") as tf:
            tf.write(b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 32)
            tf_path = tf.name

        try:
            fd = build_file_data(tf_path)
            self.assertTrue(fd["is_binary"])
            self.assertEqual(fd["encoding"], "BINARY")
            self.assertIn("[BINARY FILE", fd["content"])
            self.assertIn("7F 45 4C 46", fd["hex_dump"])
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)


if __name__ == "__main__":
    unittest.main()
