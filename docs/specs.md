Specs
=====

Business Requirements Specification
-----------------------------------
- Know what has changed between two channel "states" (e.g. diff(staged,main) studio trees)
- Desirable changes to content channels propagate quickly through the content pipeline
- Unnecessary and undesirable changes are stopped and corrected at an early state of the pipeline
- Is able to process large trees like Khan Academy (think 500MB of uncompressed JSON)



Software Requirements Specification
-----------------------------------
Can be subdivided into essential functionality, optional, and stretch goals.

The essential objectives are:
- Produce a "summary diff" that contains only the counts of added/removed/moved/modified
- Given any two trees (ricecooker, studio, kolibri) produce the detailed diff
  information about the differences (added/removed/moved/modified) between the two trees

Optional (depending on frontend needs):
- Remove redundacy in diff format (e.g. show only node move instead of node add, node delete, and node move)
- Post-process the diff format to make it most convenient for presenting to users

Stretch goals:
- Post-process the diff to make a minimum description length and avoid information
  overload (e.g. instead of showing 30 content nodes added, display the diff as
  the action of adding a single topic node)
- Support kinds of trees:
  - JSON: ricecooker, studio wire format, studio trees
  - Django ORM: Studio, Kolibri
  - Basic ORM: standalone script processing of kolibri sqlite3 DB files

