require 'logger'

class Item
  attr_accessor :name, :sell_in, :quality

  def initialize(name, sell_in, quality)
    @name = name
    @sell_in = sell_in
    @quality = quality
  end

  def to_s
    "#{@name}, #{@sell_in}, #{@quality}"
  end
end

class GildedRose
  # Main class for managing the Gilded Rose inventory system
  
  def initialize(items)
    @items = items
    @logger = Logger.new('komoju_assignment.log')
    @logger.level = Logger::INFO
  end

  def update_quality
    # Updates the quality and sell_in values for all items according to business rules:
    # - Normal items decrease quality by 1 before sell date, 2 after
    # - Aged Brie increases quality over time
    # - Backstage passes increase quality as concert approaches, drop to 0 after
    # - Sulfuras never changes
    # - Conjured items change twice as fast as normal items
    
    @items.each do |item|
      # Store original values for logging
      old_sell_in = item.sell_in
      old_quality = item.quality

      # Sulfuras is legendary and never changes
      if sulfuras?(item)
        # Ensure Sulfuras quality is always 80
        item.quality = 80
        @logger.info("Skipping update for #{item.name} (Sulfuras), sell_in #{old_sell_in}, quality #{old_quality}")
        next
      end

      # Decrease sell_in for all non-Sulfuras items
      update_sell_in(item)

      # Apply quality changes based on item type
      if aged_brie?(item)
        update_aged_brie(item)
      elsif backstage_pass?(item)
        update_backstage_pass(item)
      else
        # Treat as normal item
        update_normal_item(item)
      end

      # Ensure quality stays within valid bounds (0-50, except Sulfuras)
      clamp_quality(item)

      # Log the changes made to this item
      @logger.info("#{item.name}, sell_in #{old_sell_in} → #{item.sell_in}, quality #{old_quality} → #{item.quality}")
    end
  end

  private

  def conjured?(item)
    # Check if an item is conjured (has 'conjured' in its name)
    item.name.downcase.include?("conjured")
  end

  def aged_brie?(item)
    # Check if an item is Aged Brie (increases in quality over time)
    item.name.downcase.include?("aged brie")
  end

  def backstage_pass?(item)
    # Check if an item is a backstage pass (special quality increase rules)
    item.name.downcase.include?("backstage passes")
  end

  def sulfuras?(item)
    # Check if an item is Sulfuras (legendary item that never changes)
    item.name.downcase.include?("sulfuras")
  end

  def update_sell_in(item)
    # Decrease the sell_in value by 1 day
    item.sell_in -= 1
  end

  def update_aged_brie(item)
    # Update quality for Aged Brie items:
    # - Increases by 1 before sell date
    # - Increases by 2 after sell date
    # - Conjured Aged Brie changes twice as fast
    
    change = item.sell_in >= 0 ? 1 : 2
    change *= 2 if conjured?(item)  # Conjured items change twice as fast
    item.quality += change
  end

  def update_backstage_pass(item)
    # Update quality for Backstage passes:
    # - Increases by 1 when more than 10 days left
    # - Increases by 2 when 10 days or less
    # - Increases by 3 when 5 days or less
    # - Drops to 0 after the concert (sell_in < 0)
    # - Conjured backstage passes change twice as fast
    
    if item.sell_in < 0
      # Concert is over, quality drops to 0
      item.quality = 0
    else
      # Determine quality increase based on days until concert
      change = case item.sell_in
               when 0...5
                 3  # 5 days or less: increase by 3
               when 5...10
                 2  # 10 days or less: increase by 2
               else
                 1  # More than 10 days: increase by 1
               end

      change *= 2 if conjured?(item)  # Conjured items change twice as fast
      item.quality += change
    end
  end

  def update_normal_item(item)
    # Update quality for normal items:
    # - Decreases by 1 before sell date
    # - Decreases by 2 after sell date
    # - Conjured normal items change twice as fast
    
    change = item.sell_in < 0 ? 2 : 1  # Double degradation after sell date
    change *= 2 if conjured?(item)     # Conjured items change twice as fast
    item.quality -= change
  end

  def clamp_quality(item)
    # Ensure quality stays within valid bounds:
    # - Sulfuras: always 80
    # - Other items: between 0 and 50
    
    if sulfuras?(item)
      item.quality = 80  # Sulfuras quality is always 80
    else
      # Clamp between 0 and 50
      item.quality = [[item.quality, 0].max, 50].min
    end
  end
end

# Test the implementation when run directly
if __FILE__ == $0
  # Test data covering all item types and edge cases
  items = [
    # Normal items
    Item.new("Normal Item 1", 0, 0),      # At sell date with 0 quality
    Item.new("Normal Item 2", 10, 10),    # Before sell date
    Item.new("Normal Item 3", 10, 50),    # Before sell date with max quality
    Item.new("Normal Item 4", -1, 10),    # After sell date

    # Aged Brie items
    Item.new("Aged Brie", 0, 0),          # At sell date with 0 quality
    Item.new("Aged Brie", 10, 10),        # Before sell date
    Item.new("Aged Brie", 10, 50),        # Before sell date with max quality
    Item.new("Aged Brie", -1, 10),        # After sell date

    # Backstage passes
    Item.new("Backstage passes 1", 10, 10),  # 10 days left
    Item.new("Backstage passes 2", 9, 10),   # 9 days left
    Item.new("Backstage passes 3", 4, 10),   # 4 days left
    Item.new("Backstage passes 4", 0, 10),   # Concert day
    Item.new("Backstage passes 5", 20, 10),  # Long time until concert

    # Sulfuras items (legendary, never change)
    Item.new("Sulfuras", 0, 80),
    Item.new("Sulfuras, Hand", 0, 80),
    Item.new("Sulfuras, Hand of Ragnaros", 0, 80),

    # Conjured normal items (degrade twice as fast)
    Item.new("Conjured Normal Item 1", 0, 0),
    Item.new("Conjured Normal Item 2", 10, 10),
    Item.new("Conjured Normal Item 3", 10, 50),
    Item.new("Conjured Normal Item 4", -1, 10),

    # Conjured Aged Brie (improves twice as fast)
    Item.new("Conjured Aged Brie", 0, 0),
    Item.new("Conjured Aged Brie", 10, 10),
    Item.new("Conjured Aged Brie", 10, 50),
    Item.new("Conjured Aged Brie", -1, 10),

    # Conjured Backstage passes (improve twice as fast)
    Item.new("Conjured Backstage passes 1", 10, 10),
    Item.new("Conjured Backstage passes 2", 9, 10),
    Item.new("Conjured Backstage passes 3", 4, 10),
    Item.new("Conjured Backstage passes 4", 0, 10),
    Item.new("Conjured Backstage passes 5", 20, 10),
  ]

  # Create Gilded Rose instance and update all items
  gilded_rose = GildedRose.new(items)
  gilded_rose.update_quality

  # Print final state of all items
  items.each do |item|
    puts item
  end
end
