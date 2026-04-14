from pathlib import Path
import yaml


def test_plugin_manifest_exists_and_valid():
    manifest = Path("plugin.yaml")
    assert manifest.exists()
    data = yaml.safe_load(manifest.read_text())
    assert data["name"] == "hermes-lark"
    assert "version" in data
