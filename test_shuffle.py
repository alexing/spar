from shuffle import apply_ordered_groups

G = [['O', 'D']]

# no group track picked -> unchanged
assert apply_ordered_groups(['a', 'b', 'c'], G) == ['a', 'b', 'c']
# only the second one picked -> both, in order, size kept
assert apply_ordered_groups(['a', 'D', 'b', 'c'], G) == ['a', 'O', 'D', 'b']
# both picked, wrong order and apart -> joined at the first position
assert apply_ordered_groups(['D', 'a', 'O', 'b'], G) == ['O', 'D', 'a', 'b']
# already right
assert apply_ordered_groups(['a', 'O', 'D'], G) == ['a', 'O', 'D']
# group at the end must not be the one dropped
assert apply_ordered_groups(['a', 'b', 'O'], G) == ['a', 'O', 'D']
print('ok')
