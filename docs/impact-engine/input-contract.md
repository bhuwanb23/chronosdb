# Impact Input Contract

An impact request contains `scenario_id`, `as_of_time`,
`simulation_end_time`, `disruption_event_id`, `rule_set_version`,
`allocation_policy`, and `scheduling_policy`.

The horizon is half-open for event availability:
`as_of_time <= event_time <= simulation_end_time`. Both timestamps must be
timezone-aware UTC values, and the end must be after the as-of time.
