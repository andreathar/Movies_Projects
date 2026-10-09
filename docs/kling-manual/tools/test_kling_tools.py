#!/usr/bin/env python3
"""Testes stdlib das ferramentas do manual. Offline, sem Kling, sem custo.

  python3 -I docs/kling-manual/tools/test_kling_tools.py
"""
import json
import os
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "..", "snapshots", "who_am_i.sanitized.json")
sys.path.insert(0, HERE)
import kling_preflight as pf  # noqa: E402


def make_png(path, w, h):
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    raw = b"".join(b"\x00" + b"\x80" * w for _ in range(h))
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)


class PreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = json.load(open(SNAP, encoding="utf-8"))["body"]["availableModels"]
        cls.tmp = tempfile.mkdtemp(prefix="kling_pf_")
        cls.ok = os.path.join(cls.tmp, "ok.png")
        cls.wide = os.path.join(cls.tmp, "wide.png")
        cls.mid = os.path.join(cls.tmp, "mid.png")
        make_png(cls.ok, 640, 360)
        make_png(cls.wide, 800, 200)   # 4:1
        make_png(cls.mid, 500, 200)    # 5:2

    def codes(self, job, level="ERROR"):
        rep = pf.check_job(job, self.models, self.tmp, self.tmp, False)
        return [i["code"] for i in rep.items if i["level"] == level]

    def base_i2v(self, **kw):
        job = {"job": "t", "tool": "image_to_video", "model": "kling-video-v3_0", "auth": "X",
               "args": {"duration": "5", "resolution": "720p", "prefer_multi_shots": "false",
                        "enable_audio": "false", "imageCount": "1"},
               "images": [self.ok], "prompt": "he blinks"}
        job.update(kw)
        return job

    def test_clean_job_has_no_errors(self):
        self.assertEqual(self.codes(self.base_i2v()), [])

    def test_too_many_images_for_slots(self):
        job = {"job": "t", "tool": "image_to_image", "model": "gemini-3-pro-image", "auth": "X",
               "args": {"img_resolution": "2k", "aspect_ratio": "16:9", "image_count": "1"},
               "images": [self.ok] * 5, "prompt": "x"}
        self.assertIn("SLOT_COUNT", self.codes(job))

    def test_missing_required_slot(self):
        self.assertIn("SLOT_REQUIRED", self.codes(self.base_i2v(images=[])))

    def test_unknown_model_and_tool(self):
        self.assertIn("MODEL", self.codes(self.base_i2v(model="kling-video-v9")))
        self.assertIn("TOOL", self.codes(self.base_i2v(tool="nope")))

    def test_bad_allowed_value(self):
        job = self.base_i2v()
        job["args"]["resolution"] = "8k"
        self.assertIn("ARG_VALUE", self.codes(job))

    def test_unknown_arg(self):
        job = self.base_i2v()
        job["args"]["negative_prompt"] = "x"
        self.assertIn("ARG_UNKNOWN", self.codes(job))

    def test_name_normalisation_warns_only(self):
        job = self.base_i2v()
        job["args"]["image_count"] = job["args"].pop("imageCount")
        self.assertEqual(self.codes(job), [])
        self.assertIn("ARG_NAME", self.codes(job, "WARN"))

    def test_defaults_warned_when_unset(self):
        job = self.base_i2v()
        del job["args"]["enable_audio"], job["args"]["prefer_multi_shots"]
        self.assertEqual(self.codes(job, "WARN").count("DEFAULT"), 2)

    def test_elements_need_marker_and_support(self):
        el = '[{"id":"123","bindName":"Andre"}]'
        job = self.base_i2v()
        job["args"]["elements"] = el
        self.assertIn("ELEMENT_MARKER", self.codes(job))
        job["prompt"] = "<<<123>>> blinks"
        self.assertEqual(self.codes(job), [])
        turbo = self.base_i2v(model="kling-video-v3_0_turbo")
        turbo["args"] = {"duration": "5", "resolution": "720p", "imageCount": "1", "elements": el}
        turbo["prompt"] = "<<<123>>> blinks"
        self.assertIn("ARG_UNKNOWN", self.codes(turbo))

    def test_marker_without_elements(self):
        self.assertIn("ELEMENT_NOBIND", self.codes(self.base_i2v(prompt="<<<1>>> x")))

    def test_aspect_rules(self):
        self.assertIn("FILE_ASPECT", self.codes(self.base_i2v(images=[self.wide])))
        job = self.base_i2v(images=[self.mid])
        self.assertEqual(self.codes(job), [])
        self.assertIn("FILE_ASPECT", self.codes(job, "WARN"))

    def test_missing_file_and_placeholder(self):
        self.assertIn("FILE_MISSING", self.codes(self.base_i2v(images=["nao/existe.png"])))
        self.assertIn("PLACEHOLDER", self.codes(self.base_i2v(images=["<aceito: caminho>"])))

    def test_motion_control_needs_exactly_one_source(self):
        job = {"job": "t", "tool": "motion_control", "model": "kling-video-v3_0", "auth": "X",
               "args": {"motionDirection": "image_direction"}, "images": [self.ok], "prompt": ""}
        self.assertIn("MOTION_SOURCE", self.codes(job))
        job["args"]["motionId"] = "123"
        self.assertNotIn("MOTION_SOURCE", self.codes(job))

    def test_missing_auth_warns(self):
        job = self.base_i2v()
        del job["auth"]
        self.assertIn("AUTH", self.codes(job, "WARN"))


class SheetTest(unittest.TestCase):
    def test_sheet_generates_and_lists_every_model(self):
        out = subprocess.run([sys.executable, "-I", os.path.join(HERE, "kling_model_sheet.py"), SNAP],
                             capture_output=True, text=True, check=True).stdout
        models = json.load(open(SNAP, encoding="utf-8"))["body"]["availableModels"]
        for tool, v in models.items():
            for m in v["models"]:
                self.assertIn(f"### `{m['model']}`", out)
        self.assertNotIn("userId", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
