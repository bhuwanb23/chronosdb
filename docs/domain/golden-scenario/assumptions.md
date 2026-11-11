# Golden Scenario Assumptions

- Data is synthetic.
- All component quantities use `EA`; all money uses INR.
- `C-MCU-42` requires two units per finished product and has no scrap factor.
- Facility capacity is 100 finished units per day.
- Production uses day-bucket duration and no preemption.
- Shipping lead time is one calendar day.
- Supplier recovery lag is two calendar days.
- Post-outage supply resumes at normal capacity; backlog competition is not
  modeled.
- Chennai on-hand is intentionally corrected to 700 units, producing 400
  transferable units.
- The earlier 500-unit Chennai value is rejected because it produces only 200
  transferable units and does not support the locked hybrid ground truth.
- Partial production is not needed in the corrected golden scenario.
- Human approval is required before any intervention would be executed.
- These assumptions are not observed production facts and must be labelled
  `ASSUMED` in later data and result records.
