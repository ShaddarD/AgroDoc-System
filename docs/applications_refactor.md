# Applications module refactor (final state)

## What was done

* Moved `Application` and `InspectionRecord` from `accounts.models` → `applications.models`
* Removed backward-compat re-export from `accounts.models`
* `applications.models` is now the single source of truth

## API changes

* `status` → removed from API
* `status_code` added (source=`status_id`)
* `status_description` preserved

## Tests

* Fixed broken `accounts/tests.py` (removed UserProfile usage)
* Added:

  * import smoke tests
  * serializer contract tests
  * endpoint smoke tests (mocked, no DB)

## Known limitations

* `APITestCase` requires PostgreSQL via Docker (`hostname=postgres`)
* Local run outside Docker fails at DB setup (expected)

## Temporary деградация

`applications/document_generator.py`:

* `_receiver_name`
* `_packing_type`
* `_sampling_place`
* `_containers_str`

→ return stubs (empty values)

Full implementation requires:

* Receiver model
* containers relation

(tracked in task #XXX)
