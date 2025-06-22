require File.join(File.dirname(__FILE__), 'gilded_rose')

describe GildedRose do
  describe "#update_quality" do
    
    it "normal items decrease quality by 1 before sell date" do
      items = [Item.new("Normal Item 1", 5, 10)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(4)
      expect(items[0].quality).to eq(9)
    end

    it "normal items decrease quality by 2 after sell date" do
      items = [Item.new("Normal Item 2", 0, 10)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(-1)
      expect(items[0].quality).to eq(8)
    end

    it "quality never goes negative" do
      items = [Item.new("Normal Item 3", 0, 0)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(-1)
      expect(items[0].quality).to eq(0)
    end

    it "Aged Brie increases quality over time" do
      items = [Item.new("Aged Brie 1", 2, 0)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(1)
      expect(items[0].quality).to eq(1)
    end

    it "Aged Brie increases quality by 2 after sell date" do
      items = [Item.new("Aged Brie 2", 0, 10)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(-1)
      expect(items[0].quality).to eq(12)
    end

    it "quality never exceeds 50" do
      items = [Item.new("Aged Brie 3", 2, 50)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(1)
      expect(items[0].quality).to eq(50)
    end

    it "Sulfuras never changes quality or sell_in" do
      items = [Item.new("Sulfuras 1", 0, 80)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(0)
      expect(items[0].quality).to eq(80)
    end

    it "Backstage passes increase quality by 1 when more than 10 days" do
      items = [Item.new("Backstage passes 1", 15, 20)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(14)
      expect(items[0].quality).to eq(21)
    end

    it "Backstage passes increase quality by 2 when 10 days or less" do
      items = [Item.new("Backstage passes 2", 10, 20)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(9)
      expect(items[0].quality).to eq(22)
    end

    it "Backstage passes increase quality by 3 when 5 days or less" do
      items = [Item.new("Backstage passes 3", 5, 20)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(4)
      expect(items[0].quality).to eq(23)
    end

    it "Backstage passes drop to 0 quality after concert" do
      items = [Item.new("Backstage passes 4", 0, 20)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(-1)
      expect(items[0].quality).to eq(0)
    end

    it "Conjured normal items degrade twice as fast as normal items" do
      items = [Item.new("Conjured Normal Item 1", 3, 6)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(2)
      expect(items[0].quality).to eq(4)
    end

    it "Conjured normal items decrease quality by 4 after sell date" do
      items = [Item.new("Conjured Normal Item 2", 0, 6)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(-1)
      expect(items[0].quality).to eq(2)
    end

    it "Conjured Aged Brie increases quality twice as fast as normal Aged Brie" do
      items = [Item.new("Conjured Aged Brie", 2, 0)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(1)
      expect(items[0].quality).to eq(2)
    end

    it "Conjured Backstage passes increase quality twice as fast as normal ones" do
      items = [Item.new("Conjured Backstage passes 1", 15, 20)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(14)
      expect(items[0].quality).to eq(22)
    end

    it "Conjured Backstage passes increase quality by 6 when 5 days or less" do
      items = [Item.new("Conjured Backstage passes 2", 5, 20)]
      GildedRose.new(items).update_quality
      expect(items[0].sell_in).to eq(4)
      expect(items[0].quality).to eq(26)
    end

    it "comprehensive test with all item types and scenarios" do
      items = [
        Item.new("Normal Item 1", 0, 0),
        Item.new("Normal Item 2", 10, 10),
        Item.new("Normal Item 3", 10, 50),
        Item.new("Normal Item 4", -1, 10),
        Item.new("Aged Brie", 0, 0),
        Item.new("Aged Brie", 10, 10),
        Item.new("Aged Brie", 10, 50),
        Item.new("Aged Brie", -1, 10),
        Item.new("Backstage passes 1", 10, 10),
        Item.new("Backstage passes 2", 9, 10),
        Item.new("Backstage passes 3", 4, 10),
        Item.new("Backstage passes 4", 0, 10),
        Item.new("Backstage passes 5", 20, 10),
        Item.new("Sulfuras", 0, 80),
        Item.new("Sulfuras, Hand", 0, 80),
        Item.new("Sulfuras, Hand of Ragnaros", 0, 80),
        Item.new("Conjured Normal Item 1", 0, 0),
        Item.new("Conjured Normal Item 2", 10, 10),
        Item.new("Conjured Normal Item 3", 10, 50),
        Item.new("Conjured Normal Item 4", -1, 10),
        Item.new("Conjured Aged Brie", 0, 0),
        Item.new("Conjured Aged Brie", 10, 10),
        Item.new("Conjured Aged Brie", 10, 50),
        Item.new("Conjured Aged Brie", -1, 10),
        Item.new("Conjured Backstage passes 1", 10, 10),
        Item.new("Conjured Backstage passes 2", 9, 10),
        Item.new("Conjured Backstage passes 3", 4, 10),
        Item.new("Conjured Backstage passes 4", 0, 10),
        Item.new("Conjured Backstage passes 5", 20, 10),
      ]

      GildedRose.new(items).update_quality

      # Normal Items
      expect(items[0].sell_in).to eq(-1)
      expect(items[0].quality).to eq(0)   # Quality can't go below 0

      expect(items[1].sell_in).to eq(9)
      expect(items[1].quality).to eq(9)   # Normal decrease by 1

      expect(items[2].sell_in).to eq(9)
      expect(items[2].quality).to eq(49)  # Normal decrease by 1

      expect(items[3].sell_in).to eq(-2)
      expect(items[3].quality).to eq(8)   # After sell date, decrease by 2

      # Aged Brie
      expect(items[4].sell_in).to eq(-1)
      expect(items[4].quality).to eq(2)   # After sell date, increase by 2

      expect(items[5].sell_in).to eq(9)
      expect(items[5].quality).to eq(11)  # Normal increase by 1

      expect(items[6].sell_in).to eq(9)
      expect(items[6].quality).to eq(50)  # Quality capped at 50

      expect(items[7].sell_in).to eq(-2)
      expect(items[7].quality).to eq(12)  # After sell date, increase by 2

      # Backstage Passes
      expect(items[8].sell_in).to eq(9)
      expect(items[8].quality).to eq(12)  # 10 days or less, increase by 2

      expect(items[9].sell_in).to eq(8)
      expect(items[9].quality).to eq(12)  # 10 days or less, increase by 2

      expect(items[10].sell_in).to eq(3)
      expect(items[10].quality).to eq(13) # 5 days or less, increase by 3

      expect(items[11].sell_in).to eq(-1)
      expect(items[11].quality).to eq(0)  # After concert, quality drops to 0

      expect(items[12].sell_in).to eq(19)
      expect(items[12].quality).to eq(11) # More than 10 days, increase by 1

      # Sulfuras (all should remain unchanged except quality is always 80)
      expect(items[13].sell_in).to eq(0)
      expect(items[13].quality).to eq(80) # Sulfuras quality is always 80

      expect(items[14].sell_in).to eq(0)
      expect(items[14].quality).to eq(80) # Sulfuras quality is always 80

      expect(items[15].sell_in).to eq(0)
      expect(items[15].quality).to eq(80) # Sulfuras quality is always 80

      # Conjured Normal Items (degrade twice as fast)
      expect(items[16].sell_in).to eq(-1)
      expect(items[16].quality).to eq(0)  # Quality can't go below 0

      expect(items[17].sell_in).to eq(9)
      expect(items[17].quality).to eq(8)  # Conjured decrease by 2

      expect(items[18].sell_in).to eq(9)
      expect(items[18].quality).to eq(48) # Conjured decrease by 2

      expect(items[19].sell_in).to eq(-2)
      expect(items[19].quality).to eq(6)  # After sell date, conjured decrease by 4

      # Conjured Aged Brie (increase twice as fast)
      expect(items[20].sell_in).to eq(-1)
      expect(items[20].quality).to eq(4)  # After sell date, conjured increase by 4

      expect(items[21].sell_in).to eq(9)
      expect(items[21].quality).to eq(12) # Conjured increase by 2

      expect(items[22].sell_in).to eq(9)
      expect(items[22].quality).to eq(50) # Quality capped at 50

      expect(items[23].sell_in).to eq(-2)
      expect(items[23].quality).to eq(14) # After sell date, conjured increase by 4

      # Conjured Backstage Passes (increase twice as fast)
      expect(items[24].sell_in).to eq(9)
      expect(items[24].quality).to eq(14) # 10 days or less, conjured increase by 4

      expect(items[25].sell_in).to eq(8)
      expect(items[25].quality).to eq(14) # 10 days or less, conjured increase by 4

      expect(items[26].sell_in).to eq(3)
      expect(items[26].quality).to eq(16) # 5 days or less, conjured increase by 6

      expect(items[27].sell_in).to eq(-1)
      expect(items[27].quality).to eq(0)  # After concert, quality drops to 0

      expect(items[28].sell_in).to eq(19)
      expect(items[28].quality).to eq(12) # More than 10 days, conjured increase by 2
    end

    it "edge case: quality limits" do
      items = [
        Item.new("Aged Brie", 2, 49),     # Near upper limit
        Item.new("Normal Item 1", 2, 1),  # Near lower limit
        Item.new("Backstage passes 3", 5, 49) # Near upper limit
      ]
      GildedRose.new(items).update_quality

      # Aged Brie quality cannot exceed 50
      expect(items[0].quality).to eq(50)

      # Normal Item quality cannot go below 0
      expect(items[1].quality).to eq(0)

      # Backstage passes quality cannot exceed 50
      expect(items[2].quality).to eq(50)
    end
  end
end