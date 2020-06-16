Diff all the things
===================

Diffs are very useful when working with content, especially at scale.

Studio librarians, admins, and LE staff need diffs to keep track of content changes.
Curators need diffs to see what new materials are added when content channels are updated.
Teachers and learners operating in the "we're running out of materials" mode can
watch the diffs to see a list of only the new things added in the current update.



JSON trees
----------
Tree structures are ubiquitous in the [data model](https://docs.google.com/spreadsheets/d/181hSEwJ7yVmMh7LEwaHENqQetYSsbSDwybHTO_0zZM0/edit#gid=1640972430)
throughout the Kolibri platform, and each of these tree structures can be serialized
in the form of a JSON tree:

- T0: Ricecooker web archives format? (to know if source website has changed and we need to re-run the chef)
- T1: Ricecooker json input format (debug cheffing code, record input paths before processing)
- T2: Ricecooker->Studio wire format (archive chef runs, see detailed channel diff before uploading to studio)
- T3: Studio json tree format (compute diff(main tree,staged tree) before DEPLOY click)
- T4: Kolibri DB wire format sqlite3 files (show detailed diff info on UPDATE CHANNEL screen)
- T5: Kolibri tree format (show detailed diff info on IMPORT MORE screen)


#### JSON trees for diffs
Main focus of this project is T2 diffs in ricecooker, and T3 diffs for reviewing
changes between staging tree and main tree in Studio.


#### JSON trees for PUBLISH (a.k.a. EXPORT)
The Studio channel export task needs the information about the studio main tree
that is being published which can be "serialized" as a tree T3, with no further
need for the export code to "touch" the Studio DB (but may need interaction with GCP content bucket)

The T3 tree format has several uses:
 - A1 = representation format for doing diffs [see diff(main tree,staged tree) above]
 - A2 = archival (save studio json tree as "snaphots" or "staged versions", archive full studio tree data on PUBLISH version, could put in git)
 - A3 = share export code between ricecooker and studio (single path for all the Kolibri backward compatibility code)
 - A4 = publish staging tree (a Studio->Kolibri side-channel for importing a special "draft" channels exported from the staging tree,
   e.g. In Kolibri import from  https://drafts.studio.leq.org/content/databases/{ch_id}.sqlite3 == PUBLISH({ch_id}.staging_tree)



