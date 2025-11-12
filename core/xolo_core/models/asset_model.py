from typing import Self
from dataclasses import dataclass
from core.xolo_core.models.naming_model import WorkNaming

""" Asset model for data representation. """


@dataclass
class AssetModel(WorkNaming):
    def get_asset_info(self) -> str:
        """Generate a string with asset information."""
        return f"Asset Name: {self.get_versioned_name()}, Task: {self.task}"

    def to_dict(self) -> dict:
        """Convert the asset model to a dictionary."""
        return {
            "name": self.name,
            "task": self.task,
        }


# local testing
test_asset = AssetModel(name="CharacterA", task="Modeling")
print(
    test_asset.get_asset_info()
)  # Output: Asset Name: Versioned name , Task: Modeling
print(test_asset.to_dict())  # Output: {'name': 'CharacterA', '
