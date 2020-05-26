
import dictdiffer                                          

a_dict = {                                                 
  'a': 'foo',
  'b': 'bar',
  'd': 'barfoo'
}                                                          

b_dict = {                                                 
  'a': 'foo',                                              
  'b': 'BAR',
  'c': 'foobar'
}                                                          

for diff in list(dictdiffer.diff(a_dict, b_dict)):         
    print diff
A diff is a tuple with the type of change, the changed value, and the path to the entry.

('change', 'b', ('bar', 'BAR'))
('add', '', [('c', 'foobar')])
('remove', '', [('d', 'barfoo')])

