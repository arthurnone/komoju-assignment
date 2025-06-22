import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):

    def test_normal_item_before_sell_date(self):
        """Normal items decrease quality by 1 before sell date"""
        items = [Item("Normal Item 1", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(9, items[0].quality)

    def test_normal_item_after_sell_date(self):
        """Normal items decrease quality by 2 after sell date"""
        items = [Item("Normal Item 2", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(8, items[0].quality)

    def test_quality_never_negative(self):
        """Quality never goes negative"""
        items = [Item("Normal Item 3", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    def test_aged_brie_increases_quality(self):
        """Aged Brie increases quality over time"""
        items = [Item("Aged Brie 1", 2, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(1, items[0].sell_in)
        self.assertEqual(1, items[0].quality)

    def test_aged_brie_after_sell_date(self):
        """Aged Brie increases quality by 2 after sell date"""
        items = [Item("Aged Brie 2", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(12, items[0].quality)

    def test_quality_never_exceeds_50(self):
        """Quality never exceeds 50"""
        items = [Item("Aged Brie 3", 2, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(1, items[0].sell_in)
        self.assertEqual(50, items[0].quality)

    def test_sulfuras_never_changes(self):
        """Sulfuras never changes quality or sell_in"""
        items = [Item("Sulfuras 1", 0, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(80, items[0].quality)

    def test_backstage_passes_long_term(self):
        """Backstage passes increase quality by 1 when more than 10 days"""
        items = [Item("Backstage passes 1", 15, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(14, items[0].sell_in)
        self.assertEqual(21, items[0].quality)

    def test_backstage_passes_medium_term(self):
        """Backstage passes increase quality by 2 when 10 days or less"""
        items = [Item("Backstage passes 2", 10, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(22, items[0].quality)

    def test_backstage_passes_short_term(self):
        """Backstage passes increase quality by 3 when 5 days or less"""
        items = [Item("Backstage passes 3", 5, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(23, items[0].quality)

    def test_backstage_passes_after_concert(self):
        """Backstage passes drop to 0 quality after concert"""
        items = [Item("Backstage passes 4", 0, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    def test_conjured_normal_item(self):
        """Conjured normal items degrade twice as fast as normal items"""
        items = [Item("Conjured Normal Item 1", 3, 6)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(2, items[0].sell_in)
        self.assertEqual(4, items[0].quality)

    def test_conjured_normal_item_after_sell_date(self):
        """Conjured normal items decrease quality by 4 after sell date"""
        items = [Item("Conjured Normal Item 2", 0, 6)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(2, items[0].quality)

    def test_conjured_aged_brie(self):
        """Conjured Aged Brie increases quality twice as fast as normal Aged Brie"""
        items = [Item("Conjured Aged Brie", 2, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(1, items[0].sell_in)
        self.assertEqual(2, items[0].quality)

    def test_conjured_backstage_passes(self):
        """Conjured Backstage passes increase quality twice as fast as normal ones"""
        items = [Item("Conjured Backstage passes 1", 15, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(14, items[0].sell_in)
        self.assertEqual(22, items[0].quality)

    def test_conjured_backstage_passes_short_term(self):
        """Conjured Backstage passes increase quality by 6 when 5 days or less"""
        items = [Item("Conjured Backstage passes 2", 5, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(26, items[0].quality)

    def test_comprehensive_all_items(self):
        """Comprehensive test with all item types and scenarios using exact names"""
        items = [
            Item("Normal Item 1", 0, 0),
            Item("Normal Item 2", 10, 10),
            Item("Normal Item 3", 10, 50),
            Item("Normal Item 4", -1, 10),
            Item("Aged Brie", 0, 0),
            Item("Aged Brie", 10, 10),
            Item("Aged Brie", 10, 50),
            Item("Aged Brie", -1, 10),
            Item("Backstage passes 1", 10, 10),
            Item("Backstage passes 2", 9, 10),
            Item("Backstage passes 3", 4, 10),
            Item("Backstage passes 4", 0, 10),
            Item("Backstage passes 5", 20, 10),
            Item("Sulfuras", 0, 80),
            Item("Sulfuras, Hand", 0, 80),
            Item("Sulfuras, Hand of Ragnaros", 0, 80),
            Item("Conjured Normal Item 1", 0, 0),
            Item("Conjured Normal Item 2", 10, 10),
            Item("Conjured Normal Item 3", 10, 50),
            Item("Conjured Normal Item 4", -1, 10),
            Item("Conjured Aged Brie", 0, 0),
            Item("Conjured Aged Brie", 10, 10),
            Item("Conjured Aged Brie", 10, 50),
            Item("Conjured Aged Brie", -1, 10),
            Item("Conjured Backstage passes 1", 10, 10),
            Item("Conjured Backstage passes 2", 9, 10),
            Item("Conjured Backstage passes 3", 4, 10),
            Item("Conjured Backstage passes 4", 0, 10),
            Item("Conjured Backstage passes 5", 20, 10),
        ]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        # Normal Items
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)  # Quality can't go below 0

        self.assertEqual(9, items[1].sell_in)
        self.assertEqual(9, items[1].quality)  # Normal decrease by 1

        self.assertEqual(9, items[2].sell_in)
        self.assertEqual(49, items[2].quality)  # Normal decrease by 1

        self.assertEqual(-2, items[3].sell_in)
        self.assertEqual(8, items[3].quality)  # After sell date, decrease by 2

        # Aged Brie
        self.assertEqual(-1, items[4].sell_in)
        self.assertEqual(2, items[4].quality)  # After sell date, increase by 2

        self.assertEqual(9, items[5].sell_in)
        self.assertEqual(11, items[5].quality)  # Normal increase by 1

        self.assertEqual(9, items[6].sell_in)
        self.assertEqual(50, items[6].quality)  # Quality capped at 50

        self.assertEqual(-2, items[7].sell_in)
        # After sell date, increase by 2
        self.assertEqual(12, items[7].quality)

        # Backstage Passes
        self.assertEqual(9, items[8].sell_in)
        # 10 days or less, increase by 2
        self.assertEqual(12, items[8].quality)

        self.assertEqual(8, items[9].sell_in)
        # 10 days or less, increase by 2
        self.assertEqual(12, items[9].quality)

        self.assertEqual(3, items[10].sell_in)
        # 5 days or less, increase by 3
        self.assertEqual(13, items[10].quality)

        self.assertEqual(-1, items[11].sell_in)
        # After concert, quality drops to 0
        self.assertEqual(0, items[11].quality)

        self.assertEqual(19, items[12].sell_in)
        # More than 10 days, increase by 1
        self.assertEqual(11, items[12].quality)

        # Sulfuras (all should remain unchanged except quality is always 80)
        self.assertEqual(0, items[13].sell_in)
        # Sulfuras quality is always 80
        self.assertEqual(80, items[13].quality)

        self.assertEqual(0, items[14].sell_in)
        # Sulfuras quality is always 80
        self.assertEqual(80, items[14].quality)

        self.assertEqual(0, items[15].sell_in)
        # Sulfuras quality is always 80
        self.assertEqual(80, items[15].quality)

        # Conjured Normal Items (degrade twice as fast)
        self.assertEqual(-1, items[16].sell_in)
        self.assertEqual(0, items[16].quality)  # Quality can't go below 0

        self.assertEqual(9, items[17].sell_in)
        self.assertEqual(8, items[17].quality)  # Conjured decrease by 2

        self.assertEqual(9, items[18].sell_in)
        self.assertEqual(48, items[18].quality)  # Conjured decrease by 2

        self.assertEqual(-2, items[19].sell_in)
        # After sell date, conjured decrease by 4
        self.assertEqual(6, items[19].quality)

        # Conjured Aged Brie (increase twice as fast)
        self.assertEqual(-1, items[20].sell_in)
        # After sell date, conjured increase by 4
        self.assertEqual(4, items[20].quality)

        self.assertEqual(9, items[21].sell_in)
        self.assertEqual(12, items[21].quality)  # Conjured increase by 2

        self.assertEqual(9, items[22].sell_in)
        self.assertEqual(50, items[22].quality)  # Quality capped at 50

        self.assertEqual(-2, items[23].sell_in)
        # After sell date, conjured increase by 4
        self.assertEqual(14, items[23].quality)

        # Conjured Backstage Passes (increase twice as fast)
        self.assertEqual(9, items[24].sell_in)
        # 10 days or less, conjured increase
        self.assertEqual(14, items[24].quality)


if __name__ == '__main__':
    unittest.main(verbosity=2)
