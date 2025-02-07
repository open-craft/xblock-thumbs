"""An XBlock providing thumbs-up/thumbs-down voting."""

import logging

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Boolean, Integer, String, Scope

log = logging.getLogger(__name__)


class ThumbsBlock(XBlock):
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

    def student_view(self, context=None):  # pylint: disable=W0613
        """
        Create a fragment used to display the XBlock to a student.
        `context` is a dictionary used to configure the display (unused)

        Returns a `Fragment` object specifying the HTML, CSS, and JavaScript
        to display.
        """

        # Load the HTML fragment from within the package and fill in the template
        html_str = pkg_resources.resource_string(__name__, "static/thumbs.html").decode('utf-8')
        frag = Fragment(str(html_str).format(block=self))

        # Load the CSS and JavaScript fragments from within the package
        css_str = pkg_resources.resource_string(__name__, "static/thumbs.css").decode('utf-8')
        frag.add_css(str(css_str))

        js_str = pkg_resources.resource_string(__name__, "static/thumbs.js").decode('utf-8')
        frag.add_javascript(str(js_str))

        frag.initialize_js('ThumbsBlock')
        return frag

    problem_view = student_view

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
            self.upvotes += 1
        else:
            self.downvotes += 1

        self.voted = True

        return {'up': self.upvotes, 'down': self.downvotes}

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
