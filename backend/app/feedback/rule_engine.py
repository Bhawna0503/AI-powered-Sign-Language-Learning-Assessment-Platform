"""
rule_engine.py

Evaluates landmark comparison results
and generates correction messages.

The RuleEngine does not contain the actual
feedback messages. Those are stored in
FeedbackRules.
"""

from app.feedback.feedback_rules import FeedbackRules


class RuleEngine:

    def __init__(self):

        self.rules = FeedbackRules()

    # =====================================================
    # EVALUATE RULES
    # =====================================================

    def evaluate(self, comparison_result):

        """
        Parameters
        ----------
        comparison_result : dict

        Example:

        {
            "thumb": True,
            "index": False,
            "middle": True,
            "ring": False,
            "little": True,
            "palm": True
        }

        Returns
        -------
        list

        Example:

        [
            "Straighten your index finger.",
            "Straighten your ring finger."
        ]
        """

        feedback = []

        if not comparison_result:
            return feedback

        for rule_name, passed in comparison_result.items():

            if not passed:

                message = self.rules.get_message(
                    rule_name
                )

                feedback.append(message)

        return feedback