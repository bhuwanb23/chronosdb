12. Phase 7H: Utility Scoring Engine

Core optimization function.

Utility Formula

U

=
W1(SLA Saved)
+
W2(Revenue Protected)
-
W3(Cost)
-
W4(Remaining Delay)
-
W5(Operational Risk)


Recommended Default

Revenue Protected = 40%

SLA Saved = 30%

Cost = 15%

Delay = 10%

Risk = 5%

Example
Candidate	UtilityDo Nothing	0.00
Transfer	0.62
Expedite	0.73
Alternate Supplier	0.78
Hybrid	0.91
Output
{
  "candidate":"HYBRID",
  "utility_score":0.91
}

