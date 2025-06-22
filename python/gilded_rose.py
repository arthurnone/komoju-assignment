from dataclasses import dataclass
from typing import List
from logger import logger


class Item:
    """Represents an item in the Gilded Rose inn inventory"""

    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


@dataclass
class GildedRose:
    """Main class for managing the Gilded Rose inventory system"""
    items: List[Item]

    def update_quality(self) -> None:
        """
        Updates the quality and sell_in values for all items according to business rules:
        - Normal items decrease quality by 1 before sell date, 2 after
        - Aged Brie increases quality over time
        - Backstage passes increase quality as concert approaches, drop to 0 after
        - Sulfuras never changes
        - Conjured items change twice as fast as normal items
        """
        for item in self.items:
            # Store original values for logging
            old_sell_in = item.sell_in
            old_quality = item.quality

            # Sulfuras is legendary and never changes
            if self.is_sulfuras(item):
                # Ensure Sulfuras quality is always 80
                item.quality = 80
                logger.info(
                    f"Skipping update for {item.name} (Sulfuras), sell_in {old_sell_in}, quality {old_quality}.")
                continue

            # Decrease sell_in for all non-Sulfuras items
            self.update_sell_in(item)

            # Apply quality changes based on item type
            if self.is_aged_brie(item):
                self.update_aged_brie(item)
            elif self.is_backstage_pass(item):
                self.update_backstage_pass(item)
            else:
                # Treat as normal item
                self.update_normal_item(item)

            # Ensure quality stays within valid bounds (0-50, except Sulfuras)
            self.clamp_quality(item)

            # Log the changes made to this item
            logger.info(
                f"{item.name}, sell_in {old_sell_in} → {item.sell_in}, quality {old_quality} → {item.quality}")

    def is_conjured(self, item: Item) -> bool:
        """Check if an item is conjured (has 'conjured' in its name)"""
        return "conjured" in item.name.lower()

    def is_aged_brie(self, item: Item) -> bool:
        """Check if an item is Aged Brie (increases in quality over time)"""
        return "aged brie" in item.name.lower()

    def is_backstage_pass(self, item: Item) -> bool:
        """Check if an item is a backstage pass (special quality increase rules)"""
        return "backstage passes" in item.name.lower()

    def is_sulfuras(self, item: Item) -> bool:
        """Check if an item is Sulfuras (legendary item that never changes)"""
        return "sulfuras" in item.name.lower()

    def update_sell_in(self, item: Item) -> None:
        """Decrease the sell_in value by 1 day"""
        item.sell_in -= 1

    def update_aged_brie(self, item: Item) -> None:
        """
        Update quality for Aged Brie items:
        - Increases by 1 before sell date
        - Increases by 2 after sell date
        - Conjured Aged Brie changes twice as fast
        """
        change = 1 if item.sell_in >= 0 else 2
        if self.is_conjured(item):
            change *= 2  # Conjured items change twice as fast
        item.quality += change

    def update_backstage_pass(self, item: Item) -> None:
        """
        Update quality for Backstage passes:
        - Increases by 1 when more than 10 days left
        - Increases by 2 when 10 days or less
        - Increases by 3 when 5 days or less
        - Drops to 0 after the concert (sell_in < 0)
        - Conjured backstage passes change twice as fast
        """
        if item.sell_in < 0:
            # Concert is over, quality drops to 0
            item.quality = 0
        else:
            # Determine quality increase based on days until concert
            if item.sell_in < 5:
                change = 3  # 5 days or less: increase by 3
            elif item.sell_in < 10:
                change = 2  # 10 days or less: increase by 2
            else:
                change = 1  # More than 10 days: increase by 1

            if self.is_conjured(item):
                change *= 2  # Conjured items change twice as fast
            item.quality += change

    def update_normal_item(self, item: Item) -> None:
        """
        Update quality for normal items:
        - Decreases by 1 before sell date
        - Decreases by 2 after sell date
        - Conjured normal items change twice as fast
        """
        change = 2 if item.sell_in < 0 else 1  # Double degradation after sell date
        if self.is_conjured(item):
            change *= 2  # Conjured items change twice as fast
        item.quality -= change

    def clamp_quality(self, item: Item) -> None:
        """
        Ensure quality stays within valid bounds:
        - Sulfuras: always 80
        - Other items: between 0 and 50
        """
        if self.is_sulfuras(item):
            item.quality = 80  # Sulfuras quality is always 80
        else:
            # Clamp between 0 and 50
            item.quality = max(0, min(50, item.quality))


if __name__ == "__main__":
    # Test data covering all item types and edge cases
    items = [
        # Normal items
        Item("Normal Item 1", 0, 0),      # At sell date with 0 quality
        Item("Normal Item 2", 10, 10),    # Before sell date
        Item("Normal Item 3", 10, 50),    # Before sell date with max quality
        Item("Normal Item 4", -1, 10),    # After sell date

        # Aged Brie items
        Item("Aged Brie", 0, 0),          # At sell date with 0 quality
        Item("Aged Brie", 10, 10),        # Before sell date
        Item("Aged Brie", 10, 50),        # Before sell date with max quality
        Item("Aged Brie", -1, 10),        # After sell date

        # Backstage passes
        Item("Backstage passes 1", 10, 10),  # 10 days left
        Item("Backstage passes 2", 9, 10),   # 9 days left
        Item("Backstage passes 3", 4, 10),   # 4 days left
        Item("Backstage passes 4", 0, 10),   # Concert day
        Item("Backstage passes 5", 20, 10),  # Long time until concert

        # Sulfuras items (legendary, never change)
        Item("Sulfuras", 0, 80),
        Item("Sulfuras, Hand", 0, 80),
        Item("Sulfuras, Hand of Ragnaros", 0, 80),

        # Conjured normal items (degrade twice as fast)
        Item("Conjured Normal Item 1", 0, 0),
        Item("Conjured Normal Item 2", 10, 10),
        Item("Conjured Normal Item 3", 10, 50),
        Item("Conjured Normal Item 4", -1, 10),

        # Conjured Aged Brie (improves twice as fast)
        Item("Conjured Aged Brie", 0, 0),
        Item("Conjured Aged Brie", 10, 10),
        Item("Conjured Aged Brie", 10, 50),
        Item("Conjured Aged Brie", -1, 10),

        # Conjured Backstage passes (improve twice as fast)
        Item("Conjured Backstage passes 1", 10, 10),
        Item("Conjured Backstage passes 2", 9, 10),
        Item("Conjured Backstage passes 3", 4, 10),
        Item("Conjured Backstage passes 4", 0, 10),
        Item("Conjured Backstage passes 5", 20, 10),
    ]

    # Create Gilded Rose instance and update all items
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    # Print final state of all items
    for item in items:
        print(item)
