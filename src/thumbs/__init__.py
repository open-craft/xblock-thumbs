"""An XBlock providing thumbs-up/thumbs-down voting."""

import logging

from xblock.core import XBlock, XBlock2
from xblock.fields import Boolean, Integer, String, Scope

log = logging.getLogger(__name__)


class ThumbsBlock(XBlock2):
    """
    An XBlock with thumbs-up/thumbs-down voting.

    Vote totals are stored for all students to see.  Each student is recorded
    as has-voted or not.

    This demonstrates multiple data scopes and ajax handlers.
    """
    display_name = String(default="Thumbs", scope=Scope.settings)
    upvotes = Integer(help="Number of up votes", default=0, scope=Scope.user_state_summary)
    downvotes = Integer(help="Number of down votes", default=0, scope=Scope.user_state_summary)
    voted = Boolean(help="Has this student voted?", default=False, scope=Scope.user_state)

    @XBlock.json_handler
    def vote(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Update the vote count in response to a user action.
        """
        # Here is where we would prevent a student from voting twice, but then
        # we couldn't click more than once in the demo!
        #
        #     if self.voted:
        #         log.error("cheater!")
        #         return

        if data['voteType'] not in ('up', 'down'):
            log.error('error!')
            return None

        if data['voteType'] == 'up':
            self.upvotes += 1  # Would be cool to have atomic increment in the future
        else:
            self.downvotes += 1

        self.voted = True

        # Returning the updated field values to the frontend is not necessary - the runtime handles it automagically!

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("three thumbs at once",
             """\
                <vertical_demo>
                    <thumbs/>
                    <thumbs/>
                    <thumbs/>
                </vertical_demo>
             """)
        ]
