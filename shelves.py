#!/usr/bin/env python

spacing = 0.17  # m
lines = []
for c in range(0, 39):
    rs = range(3)
    for r in rs:
        lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                     (c*spacing, 0, r*spacing))
print '[\n' + ',\n'.join(lines) + '\n]'
