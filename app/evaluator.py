class Evaluator:
 def evaluate(self,review,test_result):
  if test_result.get("status")!="SUCCEEDED":return {"decision":"REPAIR","reason":"tests failed"}
  if review.get("decision")!="PASS":return {"decision":"REPAIR","reason":"review failed"}
  return {"decision":"PASS","reason":"tests and review passed"}
