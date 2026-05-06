# Chapter Wordcount Baseline v1

This is the committed pre-expansion baseline for the active `working/Chapter-*.md` lane in the isolated NVIDIA expansion worktree.

## Summary

- Trilogy current words: `45,902`
- Trilogy `3x` target floor: `137,706`
- Trilogy delta to `3x`: `91,804`

| Book | Current Words | 3x Target Floor | Delta |
|---|---:|---:|---:|
| 1 | 13,293 | 39,879 | 26,586 |
| 2 | 10,815 | 32,445 | 21,630 |
| 3 | 21,794 | 65,382 | 43,588 |

## Chapter Baseline

| Ch | Book | Current | 3x Floor | Delta | Matrix Band | Matrix Covers 3x? |
|---|---|---:|---:|---:|---|---|
| 01 | 1 | 1,598 | 4,794 | 3,196 | 3200-4200 | no |
| 02 | 1 | 1,475 | 4,425 | 2,950 | 3000-4000 | no |
| 03 | 1 | 1,792 | 5,376 | 3,584 | 3200-4200 | no |
| 04 | 1 | 1,126 | 3,378 | 2,252 | 3000-3800 | yes |
| 05 | 1 | 1,431 | 4,293 | 2,862 | 3200-4200 | no |
| 06 | 1 | 1,309 | 3,927 | 2,618 | 3000-3800 | no |
| 07 | 1 | 2,212 | 6,636 | 4,424 | 3600-4600 | no |
| 08 | 1 | 2,350 | 7,050 | 4,700 | 3800-4800 | no |
| 09 | 2 | 1,611 | 4,833 | 3,222 | 3200-4200 | no |
| 10 | 2 | 1,492 | 4,476 | 2,984 | 3200-4200 | no |
| 11 | 2 | 1,733 | 5,199 | 3,466 | 3200-4200 | no |
| 12 | 2 | 1,046 | 3,138 | 2,092 | 2800-3600 | yes |
| 13 | 2 | 1,161 | 3,483 | 2,322 | 3000-3800 | yes |
| 14 | 2 | 1,921 | 5,763 | 3,842 | 3400-4400 | no |
| 15 | 2 | 1,851 | 5,553 | 3,702 | 3400-4400 | no |
| 16 | 3 | 2,516 | 7,548 | 5,032 | 3800-5000 | no |
| 17 | 3 | 2,366 | 7,098 | 4,732 | 3800-5000 | no |
| 18 | 3 | 1,682 | 5,046 | 3,364 | 3200-4200 | no |
| 19 | 3 | 1,717 | 5,151 | 3,434 | 3400-4400 | no |
| 20 | 3 | 1,853 | 5,559 | 3,706 | 3400-4400 | no |
| 21 | 3 | 1,695 | 5,085 | 3,390 | 3400-4400 | no |
| 22 | 3 | 1,364 | 4,092 | 2,728 | 3200-4200 | yes |
| 23 | 3 | 1,677 | 5,031 | 3,354 | 3600-4600 | no |
| 24 | 3 | 1,718 | 5,154 | 3,436 | 3600-4600 | no |
| 25 | 3 | 1,826 | 5,478 | 3,652 | 3800-5000 | no |
| 26 | 3 | 1,696 | 5,088 | 3,392 | 3600-4600 | no |
| 27 | 3 | 1,684 | 5,052 | 3,368 | 3400-4400 | no |

## Notes

- `Current` is measured from the active `working/Chapter-*.md` files, not the compiled books.
- `3x Floor` is the minimum post-expansion target requested for later chapter passes.
- `Matrix Covers 3x?` shows whether the existing v1 target band already reaches that `3x` floor.
- Use this artifact as the before-state for all future chapter expansion verification.
