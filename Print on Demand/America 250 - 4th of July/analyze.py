#!/usr/bin/env python3
import csv
import re
from collections import defaultdict

# Read CSV
items = []
with open('etsy_data_raw.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        items.append(row)

print(f"Total items: {len(items)}")

# Filter items with >25 sales
high_sales = [i for i in items if i.get('Est. Sales', '').strip() and int(i.get('Est. Sales', 0)) > 25]
print(f"Items with >25 sales: {len(high_sales)}")

# Sort by conversion rate (highest first)
high_sales_sorted = sorted(high_sales, key=lambda x: float(x.get('Conversion Rate', 0) or 0), reverse=True)

print("\n=== TOP 15 BY CONVERSION RATE ===")
for i, item in enumerate(high_sales_sorted[:15]):
    print(f"\n{i+1}. {item['Product Name'][:60]}...")
    print(f"   Sales: {item['Est. Sales']} | Conv: {item['Conversion Rate']}% | Price: ${item['Price']}")
    print(f"   Shop: {item['Shop Name']} (Age: {item['Shop Age']})")
    print(f"   Tags: {item['Tags'][:100]}...")

# Tag analysis - count tags in high performers
print("\n\n=== TAG FREQUENCY IN TOP SELLERS (50+) ===")
tag_counts = defaultdict(int)
for item in high_sales_sorted[:50]:
    tags = item.get('Tags', '').split(',')
    for tag in tags:
        tag = tag.strip().lower()
        if tag:
            tag_counts[tag] += 1

sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
for tag, count in sorted_tags[:30]:
    print(f"  {tag}: {count}")

# Price analysis
print("\n\n=== PRICE DISTRIBUTION (High Sales Items) ===")
prices = [float(i['Price']) for i in high_sales]
avg_price = sum(prices) / len(prices)
print(f"  Average price: ${avg_price:.2f}")
print(f"  Min: ${min(prices):.2f} | Max: ${max(prices):.2f}")

# Best price range for $35 target
print("\n  Price ranges:")
print(f"  $15-20: {len([p for p in prices if 15 <= p < 20])} items")
print(f"  $20-25: {len([p for p in prices if 20 <= p < 25])} items")
print(f"  $25-30: {len([p for p in prices if 25 <= p < 30])} items")
print(f"  $30-35: {len([p for p in prices if 30 <= p < 35])} items")
print(f"  $35-40: {len([p for p in prices if 35 <= p < 40])} items")
print(f"  $40+: {len([p for p in prices if p >= 40])} items")

# Shop age vs sales
print("\n\n=== SHOP AGE vs SALES (Top 20) ===")
for item in high_sales_sorted[:20]:
    print(f"  {item['Shop Age']:>8} | {item['Est. Sales']:>5} sales | {item['Shop Name'][:25]}")

# Print TOP 10 for the output file
print("\n\n=== TOP 10 BEST SELLERS ===")
top10 = []
for i, item in enumerate(high_sales_sorted[:10]):
    top10.append({
        'rank': i+1,
        'name': item['Product Name'][:80],
        'shop': item['Shop Name'],
        'price': item['Price'],
        'sales': item['Est. Sales'],
        'conversion': item['Conversion Rate'],
        'shop_age': item['Shop Age'],
        'tags': item['Tags']
    })
    print(f"{i+1}. {item['Product Name'][:60]}")
    print(f"   ${item['Price']} | {item['Est. Sales']} sales | {item['Conversion Rate']}% conv")

# Write output file
output = """# America 250th / 4th of July - Best Sellers Analysis

## Summary
- Total items analyzed: {total}
- Items with >25 sales: {high}
- Target price: ~$35

## Top 10 Best Sellers (by Conversion Rate)

| Rank | Product | Price | Est. Sales | Conv. Rate | Shop Age |
|------|---------|-------|------------|------------|----------|
""".format(total=len(items), high=len(high_sales))

for t in top10:
    output += f"| {t['rank']} | {t['name'][:40]}... | ${t['price']} | {t['sales']} | {t['conversion']}% | {t['shop_age']} |\n"

output += """
## Key Tag Insights (from top 50 sellers)

**Most common tags:**
"""
for tag, count in sorted_tags[:20]:
    output += f"- {tag}: {count}\n"

output += """
## Recommendations for $35 price point

Based on the data:
1. Comfort Colors shirts sell well at $16-40
2. Tags like "america 250", "patriotic shirt", "4th of july shirt", "semiquincentennial" are hot
3. Lower shop age (1-6 months) with high sales = good signs
4. Conversion rates 2-10% are typical for top performers
5. Rhinestone/bling designs command higher prices ($30-46)

## Design Ideas for $35

1. **Rhinestone/bling designs** - already selling at $33-46
2. **Embroidered** - premium look, easy to price high
3. **"We The People"** - strong seller, multiple versions
4. **Family matching sets** - bundled sales
5. **Custom name** - personalization premium
"""

with open('best_sellers_analysis.md', 'w') as f:
    f.write(output)

print("\n\nAnalysis saved to best_sellers_analysis.md")