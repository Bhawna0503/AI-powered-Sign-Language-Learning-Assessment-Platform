"""
feedback_rules.py

Stores all feedback rules.

New rules can be added here without changing
the Feedback Engine or Rule Engine.
"""


class FeedbackRules:

    def __init__(self):

        self.rules = {

            # =========================================
            # BASIC FINGER RULES
            # =========================================

            "thumb":
                "Extend your thumb properly.",

            "index":
                "Straighten your index finger.",

            "middle":
                "Keep your middle finger straight.",

            "ring":
                "Straighten your ring finger.",

            "little":
                "Extend your little finger.",

            # =========================================
            # FINGER ANGLE RULES
            # =========================================

            "index_angle":
                "Adjust the angle of your index finger.",

            "middle_angle":
                "Adjust the angle of your middle finger.",

            "ring_angle":
                "Adjust the angle of your ring finger.",

            "little_angle":
                "Adjust the angle of your little finger.",

            # =========================================
            # PALM
            # =========================================

            "palm":
                "Face your palm towards the camera."
        }

    # =============================================
    # GET MESSAGE
    # =============================================

    def get_message(self, rule_name):

        return self.rules.get(
            rule_name,
            "Adjust your hand position."
        )

    # =============================================
    # GET ALL RULES
    # =============================================

    def get_all_rules(self):

        return self.rules.copy()