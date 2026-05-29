f = open('BnB_report_fixed.html', 'r', encoding='utf-8')
content = f.read()
f.close()

# Fix 2: Remove orphan </div> after Marketing Calendar note
# The Marketing Calendar note is in a <div> with 4-space indent
# After it: </div> (4-space, closes note container) + </div> (4-space, ORPHAN) + blanks + next div
# Target: just the note container </div>, remove orphan

old_mc = ('Marketing Calendar:</strong> Detailed content schedule is maintained separately by the BnB team. Content pillars above guide the strategic direction.</p>\n\n    </div>\n\n    </div>\n\n\n\n'
          '    <div style="margin-top:32px; background:#fff;')

new_mc = ('Marketing Calendar:</strong> Detailed content schedule is maintained separately by the BnB team. Content pillars above guide the strategic direction.</p>\n\n  </div>\n\n\n'
          '<div style="margin-top:32px; background:#fff;')

count_mc = content.count(old_mc)
print(f'MC orphan fix: found {count_mc} occurrence(s)')
if count_mc > 0:
    content = content.replace(old_mc, new_mc, 1)
    print('Fixed')
else:
    print('Pattern not found - trying alternative')

f = open('BnB_report_fixed.html', 'w', encoding='utf-8')
f.write(content)
f.close()
print('File written')