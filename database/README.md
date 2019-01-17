# database migrations

All database migrations are named with a simple timestamp and "\_up" or "\_down" suffix. 
The up and down are a pair:

"\_up" applies a given set of DDL operations
"\_down" reverses or undoes the DDL operations from the corresponding up script. 

Thus, to migrate simply run all the "\_up" scripts in order.
To revert to a specific script point, run the "\_down" scripts in reverse order until you reach the desired state.

**Things the eventual migration tool will need to know:**
- the very first migration file needs to be run using the postgres DB for the connection. Following migrations will use the configuration\_application database. 
- the very first migration uses postgres role. subsiquent migrations use configurator role.
