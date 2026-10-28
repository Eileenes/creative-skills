import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from character_profile import initialize, resolve, validate
from package_kit import build


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ref = self.root / "input.png"
        Image.new("RGB", (12, 12), "white").save(self.ref)

    def profile(self, name="alpha"):
        return initialize(name, name, [self.ref], self.root / "characters" / name)

    def registry(self, names, default=None):
        entries = []
        for name in names:
            p = self.profile(name)
            entries.append(dict(id=name, profile=p.relative_to(self.root).as_posix()))
        d = self.root / ".ip-characters"
        d.mkdir(exist_ok=True)
        (d / "index.json").write_text(json.dumps(dict(schemaVersion=1, defaultId=default, characters=entries)))

    def mutate(self, path, **updates):
        data = json.loads(path.read_text())
        data.update(updates)
        path.write_text(json.dumps(data))

    def test_initialize_copies_reference_and_stays_draft(self):
        p = self.profile()
        data = validate(p)
        self.assertEqual(data["status"], "draft")
        self.assertEqual((p.parent / data["referenceImages"][0]).read_bytes(), self.ref.read_bytes())

    def test_init_never_overwrites_character(self):
        p = self.profile()
        before = p.read_bytes()
        with self.assertRaises(ValueError):
            self.profile()
        self.assertEqual(p.read_bytes(), before)

    def test_multiple_characters_require_selection(self):
        self.registry(["alpha", "beta"])
        with self.assertRaisesRegex(ValueError, "Choose"):
            resolve(self.root)
        self.assertEqual(validate(resolve(self.root, "beta"))["id"], "beta")

    def test_explicit_id_overrides_default_and_missing_never_falls_back(self):
        self.registry(["alpha", "beta"], "alpha")
        self.assertEqual(validate(resolve(self.root))["id"], "alpha")
        self.assertEqual(validate(resolve(self.root, "beta"))["id"], "beta")
        with self.assertRaises(ValueError):
            resolve(self.root, "missing")

    def test_single_character_resolves_without_default(self):
        self.registry(["alpha"])
        self.assertEqual(validate(resolve(self.root))["id"], "alpha")

    def test_working_requires_real_master(self):
        p = self.profile()
        self.mutate(p, status="working")
        with self.assertRaises(ValueError):
            validate(p)
        self.mutate(p, masterReference="reference/missing.png")
        with self.assertRaises(ValueError):
            validate(p)

    def test_absolute_and_parent_reference_rejected(self):
        p = self.profile()
        for ref in [str(self.ref), "../../input.png"]:
            with self.subTest(ref=ref):
                self.mutate(p, referenceImages=[ref])
                with self.assertRaises(ValueError):
                    validate(p)

    def test_external_reference_symlink_rejected(self):
        p = self.profile()
        (p.parent / "external.png").symlink_to(self.ref)
        self.mutate(p, referenceImages=["external.png"])
        with self.assertRaises(ValueError):
            validate(p)

    def test_registry_profile_id_mismatch_rejected(self):
        self.registry(["alpha"])
        p = self.root / "characters/alpha/character.json"
        self.mutate(p, id="someone-else")
        with self.assertRaisesRegex(ValueError, "does not match"):
            resolve(self.root)

    def package_plan(self, transparent=True):
        im = Image.new("RGBA", (12, 12), (0, 0, 0, 0) if transparent else (255, 0, 0, 255))
        im.putpixel((6, 6), (255, 0, 0, 255))
        im.save(self.root / "cutout.png")
        (self.root / "prompt.txt").write_text("Synthetic fixture, not a generation claim.")
        plan = dict(name='<test & character>', assets=[dict(id="cutout", title='A < B', path="cutout.png", alpha=True, promptFile="prompt.txt", references=["input.png"])])
        path = self.root / "plan.json"
        path.write_text(json.dumps(plan))
        return path

    def test_package_checks_alpha_links_hashes_and_archive(self):
        plan = self.package_plan()
        output = self.root / "delivery"
        result = build(self.root, plan, output)
        manifest = json.loads((output / "manifest.json").read_text())
        self.assertEqual(manifest["assets"][0]["alphaRange"], [0, 255])
        self.assertIn("cutout.png", manifest["sha256"])
        page = (output / "index.html").read_text()
        self.assertIn("&lt;test &amp; character&gt;", page)
        with zipfile.ZipFile(result["archive"]) as z:
            self.assertIsNone(z.testzip())
            self.assertIn("delivery/input.png", z.namelist())
        with self.assertRaises(ValueError):
            build(self.root, plan, output)

    def test_solid_alpha_is_not_a_transparent_asset(self):
        plan = self.package_plan(False)
        with self.assertRaisesRegex(ValueError, "transparent"):
            build(self.root, plan, self.root / "delivery")

    def test_package_cannot_collect_parent_paths(self):
        plan = self.package_plan()
        data = json.loads(plan.read_text())
        data["documents"] = ["../outside.txt"]
        plan.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            build(self.root, plan, self.root / "delivery")


if __name__ == "__main__":
    unittest.main()
