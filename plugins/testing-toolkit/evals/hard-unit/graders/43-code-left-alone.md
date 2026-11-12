---
type: regex
weight: 2
target: {source: file, path: parking/tariff.py}
match: contains
flags: s
---

minutes < FREE_MINUTES.*EV_PERCENT // 100.*min\(fee, MAX_FEE_CENTS\)
